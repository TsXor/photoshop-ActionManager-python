import photoshop.api as ps
from ._utils import *
from collections import namedtuple

__all__ = ['UnitDouble', 'Enumerated', 'TypeID', 'Identifier', 'Index', 'Offset', 'ReferenceKey']

#Python class for types in ps.DescValueType
#Some types are not implemented (because I have never seen it)

UnitDouble_proto = namedtuple('UnitDouble_proto', ['unit', 'double'])
class UnitDouble(UnitDouble_proto):
  @classmethod
  def _packer(cls, obj, index):
    unit = id2str(obj.getUnitDoubleType(index))
    double = obj.getUnitDoubleValue(index)
    return cls(unit, double)
  def _unpacker(self):
    unitid = str2id(self.unit)
    double = self.double
    return (unitid, double)

Enumerated_proto = namedtuple('Enumerated_proto', ['type', 'value'])
class Enumerated(Enumerated_proto):
  @classmethod
  def _packer(cls, obj, index):
    type = id2str(obj.getEnumerationType(index))
    value = id2str(obj.getEnumerationValue(index))
    return cls(type, value)
  def _unpacker(self):
    typeid = str2id(self.type)
    valueid = str2id(self.value)
    return (typeid, valueid)

TypeID_proto = namedtuple('TypeID_proto', ['string'])
class TypeID(TypeID_proto):
  @classmethod
  def _packer(cls, obj, index):
    typeid = id2str(obj.getClass(index))
    return cls(typeid)
  def _unpacker(self):
    nid = str2id(self.typeid)
    return (nid,)

class marker:
  def __init__(self, name, value=0):
    self.name = name
    self.value = value
  def __add__(self, other):
    return type(self)(self.name, self.value+other)
  def __repr__(self):
    return '%s+%d'%(self.name, self.value)
  def __eq__(self, other):
    try:
      return self.name == other.name and self.value == other.value
    except:
      return False

Identifier = marker('Identifier')
Index = marker('Index')
Offset = marker('Offset')

psreftype2str = {
    **{vtype.value:str(vtype)[27:-4] for vtype in ps.ReferenceFormType},
    **{vtype:str(vtype)[27:-4] for vtype in ps.ReferenceFormType},
}

ReferenceKey_proto = namedtuple('ReferenceKey', ['desiredclass', 'value'])
class ReferenceKey(ReferenceKey_proto):
  @classmethod
  def _packer(cls, obj):
    ftype = psreftype2str[obj.getForm()]
    dcls = id2str(obj.getDesiredClass())
    if ftype == 'Class':
      v = None
    elif ftype == 'Enumerated':
      v = Enumerated(id2str(obj.getEnumeratedType()), id2str(obj.getEnumeratedValue()))
    elif ftype == 'Property':
      v = TypeID(id2str(obj.getProperty()))
    elif ftype == 'Name':
      v = obj.getName()
    elif ftype in ('Identifier', 'Index', 'Offset'):
      v = globals()[ftype]+get_func()
    return cls(dcls, v)
  def _unpacker(self):
    dcls = str2id(self.desiredclass)
    value = self.value
    if value is None:
      v = value
      ftype = 'Class'
    elif type(value) == TypeID:
      v = value._unpacker()
      ftype = 'Property'
    elif type(value) == marker:
      v = (value.value,)
      ftype = value.name
    elif type(value) == Enumerated:
      v = value._unpacker()
      ftype = 'Enumerated'
    elif type(value) == str:
      v = (value,)
      ftype = 'Name'
    return (ftype, dcls, v)