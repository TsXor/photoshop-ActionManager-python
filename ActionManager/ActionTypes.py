import photoshop.api as ps
from ActionManager.ValueTypes import *
from ActionManager.type_mapper import *
from ActionManager._utils import *

__all__ = ['ActionDescriptorPy', 'ActionListPy', 'ActionReferencePy']

AD = ps.ActionDescriptor
AL = ps.ActionList
AR = ps.ActionReference

def _initialize(class_name, *args, **kwargs):
  return globals()[class_name](*args, **kwargs)

class ActionDescriptorPy(AD):
  typename = 'ActionDescriptor'
  @classmethod
  def inherit(cls, obj):
    try:
      return cls(parent=obj.app, classID=obj.classID)
    except:
      return cls(parent=obj.app)
  @classmethod
  def load(cls, adict):
    clsid = adict['_classID'] if '_classID' in adict else None
    new = cls(classID=clsid)
    for k,v in adict.items():
      if k == '_classID':
        continue
      if type(v) == dict:
        v = ActionDescriptorPy.load(v)
      elif type(v) == list:
        first = v[0] if v else None
        if first == '!ref':
          v = ActionReferencePy.load(v)
        else:
          v = ActionListPy.load(v)
      new.uput(k,v)
    return new
  def __init__(self, classID=None, parent=None):
    self.classID = classID
    super().__init__(parent=parent)
  def uget(self, key):
    keyid = str2id(key)
    val = pack(self, keyid)
    if hasattr(val, 'typename'):
      val = globals()[val.typename+'Py'].inherit(val)  #delete 'Py' on integration
    return val
  def uput(self,key,val):
    keyid = str2id(key)
    typestr, args = unpack(val)
    put_func = getattr(self, 'put'+typestr)
    put_func(keyid,*args)
  def __len__(self):
    return self.count
  def __iter__(self):
    return ActionDescriptorPy_Iterator(self)
  def __contains__(self, key):
    keys = [key for key in self]
    return key in keys
  def __copy__(self):
    return ActionDescriptorPy(self.classID,self.asdict())
  def dump(self):
    #This is a dict comprehension.
    ddict = {'_classID':self.classID}
    ddict.update({key:(value.dump() if hasattr(value := self.uget(key), 'dump') else value) for key in self})
    return ddict
  def _unpacker(self):
    value = self
    clsid = str2id(self.classID)
    return (clsid, value)

class ActionDescriptorPy_Iterator:
  def __init__(self,psobj):
    self.curobj = psobj
    self.n = -1
  def __next__(self):
    self.n += 1
    try:
      keyid = self.curobj.getKey(self.n)
    except:
      raise StopIteration
    keystr = id2str(keyid)
    return keystr

class ActionReferencePy(AR):
  typename = 'ActionReference'
  @classmethod
  def inherit(cls, obj):
    return cls(parent=obj.app)
  @classmethod
  def load(cls, alist):
    new = cls()
    alist = [alist] if type(alist) == ReferenceKey else alist
    for e in alist:
      if e == '!ref':
        continue
      new.uput(e)
    return new
  def __init__(self, parent=None):
    super().__init__(parent=parent)
  def uget(self,index):
    target = self
    for i in range(index+1):
      try:
        target = target.getContainer()
      except:
        raise IndexError('list index out of range')
    return ReferenceKey._packer(target)
  def uput(self,e):
    assert type(e) == ReferenceKey
    ftype, dcls, v = e._unpacker()
    put_func = getattr(self, 'put'+ftype)
    args = (dcls,) if v is None else (dcls, *v)
    put_func(*args)
  def dump(self):
    target = self
    tlist = ['!ref']
    tlist.extend([key for key in self])
    return tlist
  def __len__(self):
    len = 1; target = self
    while True:
      try:
        target = target.getContainer(); len += 1
      except:
        len -= 1; break
    return len
  def __iter__(self):
    return ActionReferencePy_Iterator(self)

class ActionReferencePy_Iterator:
  def __init__(self,psobj):
    self.curobj = psobj
    self.init = True
  def __next__(self):
    if self.init:
      self.init = False
      return ReferenceKey._packer(self.curobj)
    self.curobj = self.curobj.getContainer()
    try:
      self.curobj.getContainer()
    except:
      raise StopIteration
    return ReferenceKey._packer(self.curobj)

class ActionListPy(AL):
  typename = 'ActionList'
  @classmethod
  def inherit(cls, obj):
    return cls(parent=obj.app)
  @classmethod
  def load(cls, alist):
    new = cls()
    for v in alist:
      if type(v) == dict:
        v = ActionDescriptorPy.load(v)
      elif type(v) == list:
        first = v[0] if v else None
        if first == '!ref':
          v = ActionReferencePy.load(v)
        else:
          v = ActionListPy.load(v)
      new.uput(v)
    return new
  def __init__(self, parent=None):
    super().__init__(parent=parent)
  @property
  def dtype(self):
    if len(self) == 0:
      return None
    valtype = self.getType(0)
    typestr = str(valtype)[14:-4]
    return typestr
  def uget(self,index):
    val = pack(self, index)
    print(val)
    if hasattr(val, 'typename'):
      val = globals()[val.typename+'Py'].inherit(val)  #delete 'Py' on integration
    return val
  def uput(self,val):
    typestr, args = unpack(val)
    #ActionList type checking
    assert True if self.dtype == None else self.dtype == typestr, \
      'ActionList can only hold things of the same type'
    put_func = getattr(self, 'put'+typestr)
    put_func(*args)
  def __len__(self):
    return self.count
  def __iter__(self):
    return ActionListPy_Iterator(self)
  def dump(self):
    #This is a list comprehension.
    dlist = [(elem.dump() if hasattr(elem, 'dump') else elem) for elem in self]
    return dlist

class ActionListPy_Iterator:
  def __init__(self,psobj):
    self.curobj = psobj
    self.n = -1
  def __next__(self):
    self.n += 1
    try:
      elem = self.curobj.uget(self.n)
    except:
      raise StopIteration()
    return elem