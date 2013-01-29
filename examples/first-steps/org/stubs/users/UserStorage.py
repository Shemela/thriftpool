#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:dynamic,slots,utf8strings,new_style
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.protocol.TBase import TBase, TExceptionBase


class Iface(object):
  def retrieve(self, uid):
    """
    Parameters:
     - uid
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def retrieve(self, uid):
    """
    Parameters:
     - uid
    """
    self.send_retrieve(uid)
    return self.recv_retrieve()

  def send_retrieve(self, uid):
    self._oprot.writeMessageBegin('retrieve', TMessageType.CALL, self._seqid)
    args = retrieve_args()
    args.uid = uid
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_retrieve(self, ):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = retrieve_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "retrieve failed: unknown result");


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["retrieve"] = Processor.process_retrieve

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_retrieve(self, seqid, iprot, oprot):
    args = retrieve_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = retrieve_result()
    result.success = self._handler.retrieve(args.uid)
    oprot.writeMessageBegin("retrieve", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class retrieve_args(TBase):
  """
  Attributes:
   - uid
  """

  __slots__ = [ 
    'uid',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'uid', None, None, ), # 1
  )

  def __init__(self, uid=None,):
    self.uid = uid


class retrieve_result(TBase):
  """
  Attributes:
   - success
  """

  __slots__ = [ 
    'success',
   ]

  thrift_spec = (
    (0, TType.STRUCT, 'success', (UserProfile, UserProfile.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success
