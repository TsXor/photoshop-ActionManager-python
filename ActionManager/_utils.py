import photoshop.api as ps

__all__ = ['str2id', 'id2str']
app = ps.Application()

def str2hash(x: str) -> int:
  '''Convert charID to typeID.'''
  assert len(x) == 4
  x = x.replace(' ', '\x20')
  return int.from_bytes(bytes(x, encoding='utf-8'), byteorder='big')

def hash2str(x: int) -> str:
  '''Convert typeID to charID.'''
  assert len(hex(x)) == 10
  return x.to_bytes(length=4, byteorder='big').decode()

def str2id(psstr: str) -> str:
  '''Convert charID or stringID to typeID'''
  assert type(psstr) == str
  if len(psstr) == 4:
    typeid = str2hash(psstr)
    try:
      restr = app.typeIDToStringID(psstr)
    except:
      restr = ''
    if not restr:
      typeid = app.stringIDToTypeID(psstr)
  else:
    typeid = app.stringIDToTypeID(psstr)
  return typeid

def id2str(typeid: int) -> str:
  '''Convert typeID to stringID'''
  psstr = app.typeIDToStringID(typeid)
  return psstr