#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None

class PageContentItem:
  """
  Attributes:
   - raw
   - fullText
   - articleText
   - dom
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'raw', None, None, ), # 1
    (2, TType.STRING, 'fullText', None, None, ), # 2
    (3, TType.STRING, 'articleText', None, None, ), # 3
    (4, TType.STRING, 'dom', None, None, ), # 4
  )

  def __init__(self, raw=None, fullText=None, articleText=None, dom=None,):
    self.raw = raw
    self.fullText = fullText
    self.articleText = articleText
    self.dom = dom

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.raw = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.fullText = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.articleText = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.dom = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('PageContentItem')
    if self.raw is not None:
      oprot.writeFieldBegin('raw', TType.STRING, 1)
      oprot.writeString(self.raw)
      oprot.writeFieldEnd()
    if self.fullText is not None:
      oprot.writeFieldBegin('fullText', TType.STRING, 2)
      oprot.writeString(self.fullText)
      oprot.writeFieldEnd()
    if self.articleText is not None:
      oprot.writeFieldBegin('articleText', TType.STRING, 3)
      oprot.writeString(self.articleText)
      oprot.writeFieldEnd()
    if self.dom is not None:
      oprot.writeFieldBegin('dom', TType.STRING, 4)
      oprot.writeString(self.dom)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Context:
  """
  Attributes:
   - left
   - right
   - middle
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'left', None, None, ), # 1
    (2, TType.STRING, 'right', None, None, ), # 2
    (3, TType.STRING, 'middle', None, None, ), # 3
  )

  def __init__(self, left=None, right=None, middle=None,):
    self.left = left
    self.right = right
    self.middle = middle

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.left = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.right = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.middle = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Context')
    if self.left is not None:
      oprot.writeFieldBegin('left', TType.STRING, 1)
      oprot.writeString(self.left)
      oprot.writeFieldEnd()
    if self.right is not None:
      oprot.writeFieldBegin('right', TType.STRING, 2)
      oprot.writeString(self.right)
      oprot.writeFieldEnd()
    if self.middle is not None:
      oprot.writeFieldBegin('middle', TType.STRING, 3)
      oprot.writeString(self.middle)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Mention:
  """
  Attributes:
   - wiki_url
   - anchor_text
   - raw_text_offset
   - context
   - freebase_id
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'wiki_url', None, None, ), # 1
    (2, TType.STRING, 'anchor_text', None, None, ), # 2
    (3, TType.I32, 'raw_text_offset', None, None, ), # 3
    (4, TType.STRUCT, 'context', (Context, Context.thrift_spec), None, ), # 4
    (5, TType.STRING, 'freebase_id', None, None, ), # 5
  )

  def __init__(self, wiki_url=None, anchor_text=None, raw_text_offset=None, context=None, freebase_id=None,):
    self.wiki_url = wiki_url
    self.anchor_text = anchor_text
    self.raw_text_offset = raw_text_offset
    self.context = context
    self.freebase_id = freebase_id

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.wiki_url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.anchor_text = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.raw_text_offset = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRUCT:
          self.context = Context()
          self.context.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.freebase_id = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Mention')
    if self.wiki_url is not None:
      oprot.writeFieldBegin('wiki_url', TType.STRING, 1)
      oprot.writeString(self.wiki_url)
      oprot.writeFieldEnd()
    if self.anchor_text is not None:
      oprot.writeFieldBegin('anchor_text', TType.STRING, 2)
      oprot.writeString(self.anchor_text)
      oprot.writeFieldEnd()
    if self.raw_text_offset is not None:
      oprot.writeFieldBegin('raw_text_offset', TType.I32, 3)
      oprot.writeI32(self.raw_text_offset)
      oprot.writeFieldEnd()
    if self.context is not None:
      oprot.writeFieldBegin('context', TType.STRUCT, 4)
      self.context.write(oprot)
      oprot.writeFieldEnd()
    if self.freebase_id is not None:
      oprot.writeFieldBegin('freebase_id', TType.STRING, 5)
      oprot.writeString(self.freebase_id)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class RareWord:
  """
  Attributes:
   - word
   - offset
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'word', None, None, ), # 1
    (2, TType.I32, 'offset', None, None, ), # 2
  )

  def __init__(self, word=None, offset=None,):
    self.word = word
    self.offset = offset

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.word = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.offset = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('RareWord')
    if self.word is not None:
      oprot.writeFieldBegin('word', TType.STRING, 1)
      oprot.writeString(self.word)
      oprot.writeFieldEnd()
    if self.offset is not None:
      oprot.writeFieldBegin('offset', TType.I32, 2)
      oprot.writeI32(self.offset)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class WikiLinkItem:
  """
  Attributes:
   - doc_id
   - url
   - content
   - rare_words
   - mentions
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'doc_id', None, None, ), # 1
    (2, TType.STRING, 'url', None, None, ), # 2
    (3, TType.STRUCT, 'content', (PageContentItem, PageContentItem.thrift_spec), None, ), # 3
    (4, TType.LIST, 'rare_words', (TType.STRUCT,(RareWord, RareWord.thrift_spec)), None, ), # 4
    (5, TType.LIST, 'mentions', (TType.STRUCT,(Mention, Mention.thrift_spec)), None, ), # 5
  )

  def __init__(self, doc_id=None, url=None, content=None, rare_words=None, mentions=None,):
    self.doc_id = doc_id
    self.url = url
    self.content = content
    self.rare_words = rare_words
    self.mentions = mentions

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.doc_id = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.content = PageContentItem()
          self.content.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.LIST:
          self.rare_words = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = RareWord()
            _elem5.read(iprot)
            self.rare_words.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.LIST:
          self.mentions = []
          (_etype9, _size6) = iprot.readListBegin()
          for _i10 in xrange(_size6):
            _elem11 = Mention()
            _elem11.read(iprot)
            self.mentions.append(_elem11)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('WikiLinkItem')
    if self.doc_id is not None:
      oprot.writeFieldBegin('doc_id', TType.I32, 1)
      oprot.writeI32(self.doc_id)
      oprot.writeFieldEnd()
    if self.url is not None:
      oprot.writeFieldBegin('url', TType.STRING, 2)
      oprot.writeString(self.url)
      oprot.writeFieldEnd()
    if self.content is not None:
      oprot.writeFieldBegin('content', TType.STRUCT, 3)
      self.content.write(oprot)
      oprot.writeFieldEnd()
    if self.rare_words is not None:
      oprot.writeFieldBegin('rare_words', TType.LIST, 4)
      oprot.writeListBegin(TType.STRUCT, len(self.rare_words))
      for iter12 in self.rare_words:
        iter12.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.mentions is not None:
      oprot.writeFieldBegin('mentions', TType.LIST, 5)
      oprot.writeListBegin(TType.STRUCT, len(self.mentions))
      for iter13 in self.mentions:
        iter13.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)