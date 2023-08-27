#!/usr/bin/env python
# pylint: disable=invalid-name,missing-docstring,unused-import,unused-variable,unused-argument,line-too-long
# pylint: disable=too-many-locals,unnecessary-pass,pointless-string-statement,using-constant-test
# pylint: disable=multiple-statements,logging-fstring-interpolation,multiple-imports,wrong-import-position
# pylint: disable=import-outside-toplevel

import inspect
import sys
from abc import ABC, abstractmethod
from random import randint, random
from typing import Any, Callable, Dict, Generic, List, TypeVar

from eventlet.event import Event
import eventlet as hub

from eventlet_promise.thread_utils import LockList
# from .log import CRITICAL, DEBUG, ERROR, INFO, LOG, WARNING, pf

def async_(func : Callable[..., Any]):
    def wrapper(*args, **kwargs):
        return Promise.resolve(func(*args, **kwargs))
    return wrapper

def await_(promise_ : 'Promise'):
    while promise_.isPending():
        hub.sleep(0)
    return promise_.getValue()

class Thenable(ABC):
    _counter = 0
    _clsThreads = LockList()

    def __init__(self):
        self.name = __class__._counter
        __class__._counter += 1
        self._state = 'pending'
        self._fate = 'unresolved'
        self._value = None
        self._event = Event()
        self._callbacks = LockList()
        self._threads = LockList[Event]()
        self._observables = LockList()

    def execute(self, executor):
        return executor(self._resolve, self._reject)

    def waitExecute(self, func : Callable[[Any], None], *args):
        def waiter():
            self._event.wait()
            func(*args)
            self._threads.remove(hub.getcurrent())
        thread = hub.spawn(waiter)
        self._threads.append(thread)
        return thread

    def _resolve(self, result, _overrideResolved=False):
        if not self.isPending():
            return
        if not _overrideResolved and self.isResolved():
            self._resolveAttached()
            return
        if result is self:
            self._reject(TypeError('Promise resolved with itself'))
            return
        if isinstance(result, Promise):
            self.referenceTo(result)
            return
        self._settle('fulfilled', result)

    def _reject(self, reason, _overrideResolved=False):
        if not self.isPending():
            return
        if not _overrideResolved and self.isResolved():
            self._resolveAttached()
            return
        self._settle('rejected', reason)

    def _settle(self, state, value):
        self._state = state
        self._fate = 'resolved'
        self._value = value
        self._event.send()
        self._executeCallbacks()

    def _executeCallbacks(self):
        idx = 0
        while idx < len(self._callbacks):
            if self._callbacks[idx]():
                self._callbacks.pop(idx)
                idx -= 1
            idx += 1

    def _resolveAttached(self):
        if self.isPending() and self.isResolved():
            self._value : Promise
            if self._value.isPending():
                return
            # wait for the saved promise (the one that self is so attached to) to settle (for someone else?;)
            Promise.allSettled([self._value])\
                .finally_(lambda x: x[0]['value'] if x[0]['status'] == 'fulfilled' else x[0]['reason'])\
                .then(lambda x: self._resolve(x, True), lambda x: self._reject(x, True))
            hub.sleep(0)

    def addCallback(self, callback : Callable[[], bool]):
        self._callbacks.append(callback)

    def addThread(self, thread : hub.greenthread.GreenThread):
        self._threads.append(thread)

    def removeThread(self, thread : hub.greenthread.GreenThread):
        self._threads.remove(thread)

    def addObservable(self, observable : 'Promise'):
        self._observables.append(observable)

    def referenceTo(self, thenable : 'Promise', *args):
        if not self.isResolved():
            try:
                thenable.addCallback(lambda: thenable.then(
                    lambda x: self._resolve(x, True),
                    lambda x: self._reject(x, True)
                ))
                thenable.addCallback(lambda: thenable.then(*args))
            except Exception as error:      # pylint: disable=broad-except
                self._reject(Exception(f'Promise rejected from thenable {thenable} : {error}.', True))
                return
            self._fate = 'resolved'
            self._value = thenable

    def isResolved(self):
        return self._fate == 'resolved'

    def isFulfilled(self):
        return self._state == 'fulfilled'

    def isRejected(self):
        return self._state == 'rejected'

    def isPending(self):
        return self._state == 'pending'

    def isSettled(self):
        return self._state != 'pending'

    def getValue(self):
        return self._value

    def getState(self):
        return self._state

    @staticmethod
    @abstractmethod
    def resolve(value : Any):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def reject(reason : Any):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def all(promises : List):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def allSettled(promises : List):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def any(promises : List):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def race(promises : List):
        raise NotImplementedError()

    @abstractmethod
    def then(self, onFulfilled : Callable[[Any], Any] = None, onRejected : Callable[[Any], Any] = None):
        raise NotImplementedError()

    @abstractmethod
    def catch(self, onRejected : Callable[[Any], Any] = None):
        raise NotImplementedError()

    @abstractmethod
    def finally_(self, onFinally : Callable[[Any], Any] = None):
        raise NotImplementedError()

    # def __str__(self):
    #     return f"<{__class__.__name__}{self.name, self._state, self._value},\n\t{pf(self._callbacks)}>"

    def __repr__(self):
        value = self._value
        fmt = f'<{self.__class__.__name__}' + '({}, {}, {})>'
        def fmt_(value):
            if isinstance(value, Thenable):
                return fmt.format(value.name, value.getState(), fmt_(value.getValue()))
            return value
        return f'<{self.__class__.__name__} {self.name, self._state, self._fate, fmt_(value), len(self._callbacks), len(self._threads)}>'

class Promise(Thenable):
    """
    A Promise represents the eventual result of an asynchronous operation.
    The primary way of interacting with a promise is through its then method,
    which registers callbacks to receive either a promise's eventual value or
    the reason why the promise cannot be fulfilled.

    A promise has an state, which can be either 'pending', 'fulfilled', or 'rejected'.

    A promise has three internal properties:
    - _fate is either 'resolved' (attached, fulfilled or rejected) or 'unresolved'.
    - _value is the result of the operation. Initially undefined.
    - _callbacks is a list of functions to call when the promise is resolved or rejected.

    A promise is in one of three different states:
    - pending: initial state, neither fulfilled nor rejected.
    - resolved: meaning that the operation completed successfully.
    - rejected: meaning that the operation failed.
    - attached: meaning that the promise has been attached to another promise.

    A pending promise can either be fulfilled with a value, or rejected with a
    reason (error). When either of these options happens, the associated
    handlers queued up by a promise's then method are called.

    The promise is said to be settled if it is either fulfilled or rejected,
    but not pending. Once settled, a promise can not be resettled.
    
    Arguments:
    - executor is a function with the signature executor(resolve, reject).
        - resolve is a function with the signature resolve(result).
        - reject is a function with the signature reject(reason).
        An `executor` call is expected to do one of the following:
        - Call resolveFunc(result) side-effect if it successfully completes.
        - Call rejectFunc(reason) side-effect if it fails to complete.
        - Register callbacks to be called when the promise is resolved or rejected.
    """
    def __init__(self, executor : Callable[[Callable[[Any], None], Callable[[Any], None]], None]):
        super().__init__()
        executor = executor or (lambda _, __: None)
        self.execute(executor)

    def __del__(self):
        for thread in self._threads:
            thread.kill()

    @staticmethod
    def resolve(value : Any) -> 'Promise':
        if isinstance(value, Promise):
            return value
        return Promise(lambda resolveFunc, _: resolveFunc(value))

    @staticmethod
    def reject(reason : Any):
        return Promise(lambda _, rejectFunc: rejectFunc(reason))

    @staticmethod
    def all(promises : List['Promise']):
        def executor(resolveFunc, rejectFunc):
            def chainExecute(promises : List['Promise'], results, resolveFunc, rejectFunc):
                assert promises, 'No promises to chain'
                promises = list(promises)
                promise_ : Promise = promises.pop(0)
                nextPromise : Promise = promises[0] if promises else None
                promise_.then(lambda x, nextPromise=nextPromise:
                    nextPromise.waitExecute(chainExecute,
                            promises, results + [x],
                            resolveFunc, rejectFunc
                    ) if nextPromise
                    else resolveFunc(results + [x])
                , rejectFunc)
            return hub.spawn(chainExecute, promises, [], resolveFunc, rejectFunc)
        return Promise(executor)

    @staticmethod
    def allSettled(promises : List['Promise']) -> 'Promise':
        if not promises:
            return Promise.resolve([])
        def executor(resolveFunc, rejectFunc):
            def chainExecute(promises : List['Promise'], results, resolveFunc, rejectFunc):
                assert promises, 'No promises to chain'
                promises = list(promises)
                promise_ : Promise = promises.pop(0)
                nextPromise : Promise = promises[0] if promises else None
                promise_.finally_(lambda x, nextPromise=nextPromise:
                    nextPromise.waitExecute(chainExecute,
                        promises, results + [{
                            'status': promise_.getState(),
                            'value' if promise_.isFulfilled() else 'reason': x
                        }],
                        resolveFunc, rejectFunc
                    ) if nextPromise
                    else resolveFunc(results + [{
                        'status': promise_.getState(),
                        'value' if promise_.isFulfilled() else 'reason': x
                    }])
                )
            return hub.spawn(chainExecute, promises, [], resolveFunc, resolveFunc)
        return Promise(executor)

    @staticmethod
    def any(promises : List['Promise']):
        promises = list(promises)
        def executor(resolveFunc, rejectFunc):
            for promise_ in promises:
                promise_ : Promise
                promise_.waitExecute(promise_.then, lambda x: resolveFunc(x, True))
            resolveFunc(Promise.allSettled(promises)
                    .then(lambda _: rejectFunc(Exception('No promises resolved'))))
        return Promise(executor)

    @staticmethod
    def race(promises : List):
        promises = list(promises)
        def executor(resolveFunc, rejectFunc):
            for promise_ in promises:
                promise_ : Promise
                promise_.waitExecute(promise_.finally_, lambda x: resolveFunc(x, True))
        return Promise(executor)

    def then(self, onFulfilled : Callable[[Any], Any] = None, onRejected : Callable[[Any], Any] = None):
        """
        Before accessing result, at least once, `eventlet.sleep` must be called.
        """
        def raise_(reason):
            if isinstance(reason, Exception):
                raise reason
            raise Exception(reason)     # pylint: disable=broad-exception-raised
        onFulfilled = onFulfilled if callable(onFulfilled) else (lambda value: value)
        onRejected = onRejected if callable(onRejected) else raise_
        try:
            if self.isFulfilled():
                value = onFulfilled(self._value)
                promise_ = Promise(lambda resolveFunc, _: self.waitExecute(resolveFunc, value))
                # hub.sleep(0)
                return promise_
            if self.isRejected():
                value = onRejected(self._value)     # pylint: disable=assignment-from-no-return
                promise_ = Promise(lambda _, rejectFunc: self.waitExecute(rejectFunc, value))
                # hub.sleep(0)
                return promise_
            promise_ = Promise(lambda resolveFunc, _: resolveFunc(self))
            promise_.referenceTo(self, onFulfilled, onRejected)
            return promise_
        except Exception as error:          # pylint: disable=broad-except
            return Promise.reject(error)

    def catch(self, onRejected : Callable[[Any], Any] = None):
        return self.then(None, onRejected)

    def finally_(self, onFinally : Callable[[Any], Any] = None):
        return self.then(onFinally, onFinally)

if __name__ == '__main__':
    def executor_(resolveFunc : Callable[[Any], None], rejectFunc : Callable[[Any], None]):      # match, timeout
        t1, t2 = 5, 6
        # print(t := 1.5 * random())
        hub.spawn_after(t1, lambda: print('\tResolving') or resolveFunc(t1))
        hub.spawn_after(t2, lambda: print('\tRejecting') or rejectFunc(TimeoutError("Timed out")))

    # promise = Promise(None)
    promise = Promise(executor_)
    new_promise = promise.then()
    attached = Promise(lambda resolveFunc, _: resolveFunc(new_promise))
    attached.referenceTo(new_promise)
    p1 = Promise.resolve(1).then(2).then()
    p2 = Promise.reject(1).then(2, 2).then().then()
    p3 = p1.then()

    print(promise)
    print(new_promise)
    print(attached)
    print(p1)
    print(p2)
    print(p3)

    p_all = Promise.all([p1, p3, new_promise, promise])
    print('all', p_all)
    p_settled = Promise.allSettled([p1, p2, p3, new_promise, promise])
    print('allSettled', p_settled)
    p_any = Promise.any([p2, promise.then(), new_promise, promise])
    print('any', p_any)
    p_race = Promise.race([new_promise.then(), new_promise.then()])
    print('race', p_race)

    print('\nFinished\n')
    hub.sleep(1)

    while True:
        hub.sleep(0)
        try:
            print()
            print(promise)
            print(new_promise)
            print(attached)
            print(p1)
            print(p2)
            print(p3)
            print('all', p_all)
            print('allSettled', p_settled)
            print('any', p_any)
            print('race', p_race)
            hub.sleep(3)
        except KeyboardInterrupt:
            sys.exit(0)
