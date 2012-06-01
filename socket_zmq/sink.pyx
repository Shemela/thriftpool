# cython: profile=True
cimport cython
from cpython cimport bool
from gevent.hub import get_hub
import zmq
from zmq.core.socket cimport Socket as ZMQSocket


cdef enum States:
    WAIT_MESSAGE = 1
    SEND_REQUEST = 2
    READ_REPLY = 3


cdef class ZMQSink(object):

    cdef ZMQSocket socket
    cdef object callback
    cdef object message
    cdef States status

    cdef object __read_watcher
    cdef object __write_watcher

    def __init__(self, socket, callback):
        assert socket.getsockopt(zmq.TYPE) == zmq.REQ
        self.socket = socket
        self.callback = callback
        self.message = None
        self.status = WAIT_MESSAGE
        self.__setup_events()

    cdef __setup_events(self):
        loop = get_hub().loop
        MAXPRI = loop.MAXPRI
        io = loop.io
        fileno = self.socket.getsockopt(zmq.FD)

        self.__read_watcher = io(fileno, 1)
        self.__read_watcher.priority = MAXPRI
        self.__write_watcher = io(fileno, 2)
        self.__write_watcher.priority = MAXPRI

    @cython.profile(False)
    cdef inline void start_listen_read(self):
        """Start listen read events."""
        self.__read_watcher.start(self.on_readable)

    @cython.profile(False)
    cdef inline void stop_listen_read(self):
        """Stop listen read events."""
        self.__read_watcher.stop()

    @cython.profile(False)
    cdef inline void start_listen_write(self):
        """Start listen write events."""
        self.__write_watcher.start(self.on_writable)

    @cython.profile(False)
    cdef inline void stop_listen_write(self):
        """Stop listen write events."""
        self.__write_watcher.stop()

    @cython.profile(False)
    cdef inline bool is_writeable(self):
        return self.status == SEND_REQUEST

    @cython.profile(False)
    cdef inline bool is_readable(self):
        return self.status == READ_REPLY

    @cython.profile(False)
    cdef inline bool is_ready(self):
        return self.status == WAIT_MESSAGE

    cpdef read(self):
        assert self.is_readable()
        self.message = self.socket.recv(zmq.NOBLOCK)
        self.callback(self.message)
        self.status = WAIT_MESSAGE
        self.message = None

    cpdef write(self):
        assert self.is_writeable()
        self.socket.send(self.message, zmq.NOBLOCK)
        self.status = READ_REPLY
        self.message = None

    cpdef ready(self, message):
        assert self.is_ready()
        self.status = SEND_REQUEST
        self.message = message
        self.start_listen_write()

    cpdef on_readable(self):
        try:
            while self.is_readable():
                self.read()
        except zmq.ZMQError, e:
            if e.errno != zmq.EAGAIN:
                raise
        else:
            self.stop_listen_read()

    cpdef on_writable(self):
        try:
            while self.is_writeable():
                self.write()
        except zmq.ZMQError, e:
            if e.errno != zmq.EAGAIN:
                raise
        else:
            self.stop_listen_write()
            self.on_readable()
            self.start_listen_read()