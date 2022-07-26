import photoshop.api as ps
from collections import UserString,UserDict,UserList
import warnings
from textwrap import dedent

psAM_settings = { \
  'psapp':None, \
  'locale':'en', \
  'actionlist_alwaysforce':False, \
  'prepr_indent':4, \
  'evalable_repr':False, \
}
psAM_texts = { \
  'en':{ \
    'psChar_len_error':'You can only mark a string with length <= 4 as a PS_Character', \
    'appcheck_fail_error':'Please set a ps.Application()', \
    'str2id_type_error':'Only string or PS_Character can be converted to ps typeid.', \
    'id2str_invalid_error':'Result is None, please check if the typeid is vaild!', \
    'pytypecvt_unknowntype_error':'Unknown or unimplemented type of value: %s', \
    'refpy_wrongvalue1_warn':'Now that Formtype==\'Enumerated\', you shouldn\'t provide a value, and that is ignored.', \
    'refpy_wrongvalue2_err':'Please give an object of psEnumerated class when Formtype==\'Enumerated\'.', \
    'refpy_wrongvalue3_err':'Please give a string when Formtype==\'Name\'.', \
    'listpy_suck_err':dedent('''
                             ActionList itself cannot be modified (yes that sucks but photoshop developers define this).
                             Although this operation is implemented, it is not recommended because it clears the list and reappend elements.
                             If you just want to do this anyway, set the "forceoperations" attribute of this object to True.
                             "forceoperations" will be automatically reverted to False after you forced such an operation.
                             '''), \
    'listpy_appendtype_err':'An ActionList can only hold elements of the same type!', \
  }, \
  'zh':{ \
    'psChar_len_error':'只有4个字及以内的字符串能被标记为PS_Character', \
    'appcheck_fail_error':'请设置一个ps.Application()', \
    'str2id_type_error':'只有字符串或者PS_Character可被转换为ps typeid。', \
    'id2str_invalid_error':'查询结果为None请检查输入的typeid是否有效！', \
    'pytypecvt_unknowntype_error':'未知的或者没实现的数据类型：%s', \
    'refpy_wrongvalue1_warn':'当Formtype被指定为\'Enumerated\'时，不应提供Value，提供的Value已被忽略。', \
    'refpy_wrongvalue2_err':'当Formtype被指定为\'Enumerated\'时，请提供一个psEnumerated类的对象。', \
    'refpy_wrongvalue3_err':'当Formtype被指定为\'Name\'时，请提供一个字符串。', \
    'listpy_suck_err':dedent('''
                             ActionList本身是不能修改的（这简直是太艹了但是是photoshop开发者们这样规定的）
                             尽管这里实现了这个功能，但是并不推荐使用，因为实现方式是清空列表再重建。
                             如果您说啥也要这么做，那么请将此对象的“forceoperations”属性设为True。
                             在您强制完成此操作后，“forceoperations”会自动恢复为False。
                             '''), \
    'listpy_appendtype_err':'ActionList只能存放同种类的元素', \
  }, \
}
global_desc_dict = {}

class psChar(UserString):
  def __init__(self,seq):
    super().__init__(seq)
    if len(self.data) > 4:
      raise RuntimeError(psAM_texts[psAM_settings['locale']]['psChar_len_error'])
    self.data = self.data.ljust(4)
  def tostr(self):
    return id2str(str2id(self))
  def __repr__(self):
    if psAM_settings['evalable_repr']:
      return self.tostr()
    else:
      return '\'%s\'(marked as PS_Character)'%self.data

#Python class for types in ps.DescValueType
#Python类，对应ps.DescValueType中的类
#Some types are not implemented (because I have never seen it), see below.
#有些类没实现（因为我没见过），详情往下看
class psUnitDouble:
  def __init__(self,unit,double):
    self.unit = unit
    self.double = double
  def idtup(self):
    return (str2id(self.unit), self.double)
  def __repr__(self):
    if psAM_settings['evalable_repr']:
      return 'psUnitDouble(\'%s\', %f)'%(self.unit,self.double)
    else:
      return 'PS_UnitDouble(%f %s)'%(self.double,self.unit)
class psEnumerated:
  def __init__(self,enumtype,enumval):
    self.enumtype = enumtype
    self.enumval = enumval
  def idtup(self):
    return (str2id(self.enumtype), str2id(self.enumval))
  def __repr__(self):
    if psAM_settings['evalable_repr']:
      return 'psEnumerated(\'%s\', \'%s\')'%(self.enumtype,self.enumval)
    else:
      return 'PS_Enumerated(type:%s %s)'%(self.enumtype,self.enumval)
class psClass(UserString):
  def __init__(self,seq):
    super().__init__(seq)
  def __repr__(self):
    if psAM_settings['evalable_repr']:
      return 'psClass(\'%s\')'%self.data
    else:
      return 'PS_Class(%s)'%self.data

#ps.DescValueType.AliasType             state: not implemented
#ps.DescValueType.BooleanType           state: okay(->standard python bool)
#ps.DescValueType.ClassType             state: not implemented
#ps.DescValueType.DoubleType            state: okay(->standard python float)
#ps.DescValueType.EnumeratedType        state: okay(psEnumerated)
#ps.DescValueType.IntegerType           state: okay(->standard python int)
#ps.DescValueType.LargeIntegerType      state: not implemented
#ps.DescValueType.ListType              state: okay(ActionListPy)
#ps.DescValueType.ObjectType            state: okay(ActionDescriptorPy)
#ps.DescValueType.RawType               state: not implemented
#ps.DescValueType.ReferenceType         state: okay(ActionReferencePy)
#ps.DescValueType.StringType            state: okay(->standard python str)
#ps.DescValueType.UnitDoubleType        state: okay(psUnitDouble)

def appcheck():
  if not psAM_settings['psapp']:
    raise RuntimeError(psAM_texts[psAM_settings['locale']]['appcheck_fail_error'])
def str2id(psstr):
  appcheck()
  app = psAM_settings['psapp']
  if type(psstr) == str:
    typeid = app.stringIDToTypeID(psstr)
  elif type(psstr) == psChar:
    typeid = app.charIDToTypeID(psstr.data)
  elif type(psstr) == psClass:
    typeid = app.stringIDToTypeID(psstr.data)
  else:
    raise TypeError(psAM_texts[psAM_settings['locale']]['str2id_type_error'])
  return typeid
def id2str(typeid):
  appcheck()
  app = psAM_settings['psapp']
  psstr = app.typeIDToStringID(typeid)
  if not psstr:
    raise RuntimeError(psAM_texts[psAM_settings['locale']]['id2str_invalid_error'])
  return psstr
def pytype_cvt(dtype):
  typedict = { \
              int:'Integer', \
              float:'Double', \
              psUnitDouble:'UnitDouble', \
              str:'String', \
              bool:'Boolean', \
              psEnumerated:'Enumerated', \
              ActionDescriptorPy:'Object', \
              ActionReferencePy:'Reference', \
              ActionListPy:'List', \
              psChar:'Class', \
              psClass:'Class', \
              }
  if not type(dtype) in typedict:
    raise TypeError(psAM_texts[psAM_settings['locale']]['pytypecvt_unknowntype_error']%type(dtype))
  return typedict[type(dtype)]
def pstype_cvt(dtype):
  if type(dtype) == int:
    for vtype in ps.DescValueType:
      if vtype.value == dtype:
        cvt = str(vtype)[14:-4]
        break
  if type(dtype) == ps.DescValueType:
    cvt = str(dtype)[14:-4]
  return cvt
def psreftype_cvt(ftype):
  if type(ftype) == int:
    for vtype in ps.ReferenceFormType:
      if vtype.value == ftype:
        cvt = str(vtype)[27:-4]
        break
  if type(ftype) == ps.ReferenceFormType:
    cvt = str(ftype)[27:-4]
  return cvt

def nmin(*args):
  lst = []
  for n in args:
    if n != -1:
      lst.append(n)
  if len(lst):
    if len(lst) == 1:
      return lst[0]
    else:
      return min(*lst)
  else:
    return -1
def prettyrepr(pyobj):
  assert type(pyobj) == ActionDescriptorPy \
      or type(pyobj) == ActionListPy \
      or type(pyobj) == ActionReferencePy
  reprstr = repr(pyobj)
  idt = psAM_settings['prepr_indent']
  indentn = 0
  index = 0
  op_offset = 0
  reprstr = reprstr.replace(', ', ',')
  reprstr = reprstr.replace('[]', '[(empty)]')
  reprstr = reprstr.replace('{}', '{(empty)}')
  pstr = list(reprstr)
  while True:
    first_comma = reprstr.find(',',index)
    #first_left = nmin(reprstr.find('{',index), reprstr.find('[',index), reprstr.find('(',index))
    first_left = nmin(reprstr.find('{',index), reprstr.find('[',index))
    #first_right = nmin(reprstr.find('}',index), reprstr.find(']',index), reprstr.find(')',index))
    first_right = nmin(reprstr.find('}',index), reprstr.find(']',index))
    first_mark = nmin(first_comma, first_left, first_right)
    index = first_mark
    if first_mark == -1:
      break
    if first_mark == first_left:
      indentn += 1
      istidx = index
    if first_mark == first_right:
      indentn += -1
      istidx = index-1
    if first_mark == first_comma:
      istidx = index
    index += 1
    pstr.insert(istidx+op_offset+1, '\n'+indentn*idt*' '); op_offset += 1
  return ''.join(pstr)

class ActionDescriptorPy(UserDict):
  def __new__(cls, psclass, dictorpsobj={}):
    if type(dictorpsobj) != dict:
      global global_desc_dict
      for key in global_desc_dict:
        if dictorpsobj.isEqual(key):
          return global_desc_dict[key]
    return super().__new__(cls)
  def __init__(self, psclass, dictorpsobj={}):
    appcheck()
    self.psclass = psclass
    self.sublists = {}
    if type(dictorpsobj) == dict:
      self.psobj = ps.ActionDescriptor()
      for key in dictorpsobj:
        val = dictorpsobj[key]
        self.__setitem__(key,val)
    else:
      self.psobj = dictorpsobj
      #self.__repr__()
    global global_desc_dict
    global_desc_dict.update({self.psobj:self})
  def __getitem__(self,key):
    keyid = str2id(key)
    valtype = self.psobj.getType(keyid)
    typestr = pstype_cvt(valtype)
    if typestr == 'Enumerated':
      val_enumtype = id2str(self.psobj.getEnumerationType(keyid))
      val_enumval = id2str(self.psobj.getEnumerationValue(keyid))
      val = psEnumerated(val_enumtype,val_enumval)
    elif typestr == 'UnitDouble':
      val_unit = id2str(self.psobj.getUnitDoubleType(keyid))
      val_double = self.psobj.getUnitDoubleValue(keyid)
      val = psUnitDouble(val_unit,val_double)
    elif typestr == 'Object':
      val_psobj = self.psobj.getObjectValue(keyid)
      val_psclass = id2str(self.psobj.getObjectType(keyid))
      val = ActionDescriptorPy(val_psclass,val_psobj)
    elif typestr == 'Reference':
      get_func = getattr(self.psobj, 'get'+typestr)
      val_psobj = get_func(keyid)
      val = ActionReferencePy(val_psobj)
    elif typestr == 'List':
      get_func = getattr(self.psobj, 'get'+typestr)
      if key in self.sublists:
        val = self.sublists[key]
      else:
        val_psobj = get_func(keyid)
        val = ActionListPy(val_psobj)
        self.sublists.update({key:val})
        val.bindfather(self,'Descriptor',key)
    elif typestr == 'Class':
      get_func = getattr(self.psobj, 'get'+typestr)
      val_id = get_func(keyid)
      val = psClass(id2str(val_id))
    else:
      get_func = getattr(self.psobj, 'get'+typestr)
      val = get_func(keyid)
    return val
  def __setitem__(self,key,val):
    keyid = str2id(key)
    typestr = pytype_cvt(val)
    put_func = getattr(self.psobj, 'put'+typestr)
    if type(val) == psEnumerated or type(val) == psUnitDouble:
      put_func(keyid,*val.idtup())
    elif type(val) == psChar or type(val) == psClass:
      put_func(keyid,str2id(val))
    elif type(val) == ActionDescriptorPy:
      put_func(keyid,str2id(val.psclass),val.psobj)
    elif type(val) == ActionReferencePy:
      put_func(keyid,val.psobj)
    elif type(val) == ActionListPy:
      put_func(keyid,val.psobj)
      self.sublists.update({key:val})
      val.bindfather(self,'Descriptor',key)
    else:
      put_func(keyid,val)
  def __delitem__(self,key):
    keyid = str2id(key)
    if key in self.sublists:
      self.sublists[key].unbind()
      del self.sublists[key]
    self.psobj.erase(keyid)
  def clear(self):
    self.psobj.clear()
    for key in self.sublists:
      self.sublists[key].unbind()
    self.sublists = {}
  def __len__(self):
    return self.psobj.count
  def __iter__(self):
    self.iternum = 0
    return self
  def __next__(self):
    if self.iternum >= self.__len__():
      raise StopIteration()
    keyid = self.psobj.getKey(self.iternum)
    keystr = id2str(keyid)
    self.iternum += 1
    return keystr
  def listkey(self):
    keylist = []
    for i in range(self.__len__()):
      keyid = self.psobj.getKey(i)
      keystr = id2str(keyid)
      keylist.append(keystr)
    return keylist
  def asdict(self):
    rtdict = {}
    for key in self:
      val = self[key]
      plusdict = {key:val}
      rtdict.update(plusdict)
    return rtdict
  def __repr__(self):
    #Tweak: You can use __repr__() method to 'pythonize' all nested ps objects in an ps object.
    #小技巧：调用__repr__()方法可以“python化”所有嵌套的ps对象。
    if psAM_settings['evalable_repr']:
      return 'ActionDescriptorPy(\'%s\', %s)'%(self.psclass,self.asdict())
    else:
      return '%s%s'%(self.psclass,self.asdict())
  def __contains__(self, key):
    for ikey in self:
      if str2id(ikey) == str2id(key):
        return True
    return False
  def __copy__(self):
    return ActionDescriptorPy(self.psclass,self.asdict())
  def __deepcopy__(self):
    cpy = ActionDescriptorPy(self.psclass)
    cdic = self.asdict()
    for k in cdic:
      v = cdic[k]
      if type(v) == ActionDescriptorPy or type(v) == ActionListPy:
        v = v.__deepcopy__()
      if type(v) == ActionReferencePy:
        v = v.__copy__()
      cpy.update({k:v})
    return cpy
  #Just blame me. I really cannot implement these.
  #怪我，我不会写这些。
  def __or__(self, other):
    raise NotImplementedError
  def __ror__(self, other):
    raise NotImplementedError
  def __ior__(self, other):
    raise NotImplementedError
  def copy(self):
    raise NotImplementedError

class ActionReferencePy:
  def __init__(self, classorpsobj, *value):
    appcheck()
    if type(classorpsobj) == str or type(classorpsobj) == psChar:
      self.psobj = ps.ActionReference()
      classn = str2id(classorpsobj)
      vtype = value[0]
      put_func = getattr(self.psobj, 'put'+vtype)
      if vtype == 'Class':
        if len(value) > 1:
          warnings.warn(psAM_texts[psAM_settings['locale']]['refpy_wrongvalue1_warn'])
        put_func(classn)
      elif vtype == 'Enumerated':
        val = value[1]
        assert type(val) == psEnumerated, psAM_texts[psAM_settings['locale']]['refpy_wrongvalue2_err']
        put_func(classn,*val.idtup())
      elif vtype == 'name':
        val = value[1]
        assert type(val) == str, psAM_texts[psAM_settings['locale']]['refpy_wrongvalue3_err']
        put_func(classn,val)
      else:
        val = value[1]
        try:
          val = str2id(val)
        except TypeError:
          pass
        put_func(classn,val)
    else:
      self.psobj = classorpsobj
  def asdict(self): #Note that although ActionReferencePy can be converted to a dict, its structure is different!
    try:
      classstr = id2str(self.psobj.getDesiredClass())
    except:
      return None
    vtype = psreftype_cvt(self.psobj.getForm())
    if vtype == 'Enumerated':
      val_enumtype = id2str(self.psobj.getEnumeratedType())
      val_enumval = id2str(self.psobj.getEnumeratedValue())
      val = psEnumerated(val_enumtype,val_enumval)
      return {'DesiredClass':classstr, 'FormType':'Enumerated', 'Value':val}
    elif vtype == 'Class':
      return {'DesiredClass':classstr, 'FormType':'Class'}
    else:
      get_func = get_func = getattr(self.psobj, 'get'+vtype)
      val = get_func()
      if type(val) == int and len(str(val)) > 4:
        val = id2str(val)
      return {'DesiredClass':classstr, 'FormType':vtype, 'Value':val}
  def __copy__(self):
    sdict = self.asdict()
    if sdict['FormType'] == 'Class':
      nobj = ActionReferencePy(sdict['DesiredClass'],sdict['FormType'])
    else:
      nobj = ActionReferencePy(sdict['DesiredClass'],sdict['FormType'],sdict['Value'])
    return nobj
  def __repr__(self):
    sdict = self.asdict()
    if psAM_settings['evalable_repr']:
      if self.asdict() == None:
        return 'ActionReferencePy()'
      else:
        if sdict['FormType'] == 'Class':
          return 'ActionReferencePy(\'%s\', \'%s\')'%(sdict['DesiredClass'],sdict['FormType'])
        elif sdict['FormType'] == 'Index':
          return 'ActionReferencePy(\'%s\', \'%s\', %d)'%(sdict['DesiredClass'],sdict['FormType'],sdict['Value'])
        elif sdict['FormType'] == 'Enumerated':
          return 'ActionReferencePy(\'%s\', \'%s\', %s)'%(sdict['DesiredClass'],sdict['FormType'],repr(sdict['Value']))
        else:
          if type(sdict['Value']) == int:
            return 'ActionReferencePy(\'%s\', \'%s\', %d)'%(sdict['DesiredClass'],sdict['FormType'],sdict['Value'])
          else:
            return 'ActionReferencePy(\'%s\', \'%s\', \'%s\')'%(sdict['DesiredClass'],sdict['FormType'],sdict['Value'])
    else:
      if self.asdict() == None:
        return 'Reference(empty)'
      else:
        return 'Reference%s'%sdict

class ActionListPy(UserList):
  def __init__(self, listorpsobj=[]):
    appcheck()
    self.sublists = {}
    self.father = None
    self.fathertype = None
    self.findex = None
    self.forceoperations = False
    if type(listorpsobj) == list:
      self.psobj = ps.ActionList()
      for val in listorpsobj:
        self.append(val)
    else:
      self.psobj = listorpsobj
      #self.__repr__()
  def syncops(self):
    if self.fathertype == 'List':
      self.father.forceoperations = True
    self.father[self.findex] = self
  def __getitem__(self,index):
    valtype = self.psobj.getType(index)
    typestr = pstype_cvt(valtype)
    if typestr == 'Enumerated':
      val_enumtype = id2str(self.psobj.getEnumerationType(index))
      val_enumval = id2str(self.psobj.getEnumerationValue(index))
      val = psEnumerated(val_enumtype,val_enumval)
    elif typestr == 'UnitDouble':
      val_unit = id2str(self.psobj.getUnitDoubleType(index))
      val_double = self.psobj.getUnitDoubleValue(index)
      val = psUnitDouble(val_unit,val_double)
    elif typestr == 'Object':
      val_psobj = self.psobj.getObjectValue(index)
      val_psclass = id2str(self.psobj.getObjectType(index))
      val = ActionDescriptorPy(val_psclass,val_psobj)
    elif typestr == 'Reference':
      get_func = getattr(self.psobj, 'get'+typestr)
      val_psobj = get_func(index)
      val = ActionReferencePy(val_psobj)
    elif typestr == 'List':
      get_func = getattr(self.psobj, 'get'+typestr)
      if index in self.sublists:
        val = self.sublists[index]
      else:
        val_psobj = get_func(index)
        val = ActionListPy(val_psobj)
        val.bindfather(self,'List',index)
        self.sublists.update({index:val})
    elif typestr == 'Class':
      get_func = getattr(self.psobj, 'get'+typestr)
      val_id = get_func(index)
      val = psClass(id2str(val_id))
    else:
      get_func = getattr(self.psobj, 'get'+typestr)
      val = get_func(index)
    return val
  def __len__(self):
    return self.psobj.count
  def __iter__(self):
    self.iternum = 0
    return self
  def __next__(self):
    if self.iternum >= self.__len__():
      raise StopIteration()
    elem = self[self.iternum]
    self.iternum += 1
    return elem
  def bindfather(self,father,ftype,findex):
    self.father = father
    self.fathertype = ftype
    self.findex = findex
  def unbind(self):
    self.father = None
    self.fathertype = None
    self.findex = None
  def getelemtype(self):
    if self.__len__() == 0:
      return None
    valtype = self.psobj.getType(0)
    typestr = pstype_cvt(valtype)
    return typestr
  def append(self,val):
    #Note: All methods that modifies an ActionList uses and relies on this append method!
    #注意：所有可以更改一个ActionList的方法都使用并且依赖这个append方法！
    typestr = pytype_cvt(val)
    if typestr != self.getelemtype() and self.getelemtype():
      raise TypeError(psAM_texts[psAM_settings['locale']]['listpy_appendtype_err'])
    put_func = getattr(self.psobj, 'put'+typestr)
    if type(val) == psEnumerated or type(val) == psUnitDouble:
      put_func(*val.idtup())
    elif type(val) == psChar or type(val) == psClass:
      put_func(str2id(val))
    elif type(val) == ActionDescriptorPy:
      put_func(str2id(val.psclass),val.psobj)
    elif type(val) == ActionReferencePy:
      put_func(val.psobj)
    elif type(val) == ActionListPy:
      put_func(val.psobj)
      ni = self.__len__()-1
      self.sublists.update({ni:val})
      val.bindfather(self,'List',ni)
    else:
      put_func(val)
    if self.father:
      self.syncops()
  def extend(self, other):
    for pluselem in other:
      self.append(pluselem)
  def __iadd__(self, other):
    self.extend(other)
    return self
  def clear(self):
    self.psobj.clear()
    for i in self.sublists:
      self.sublists[i].unbind()
    self.sublists = {}
  def aslist(self):
    rtlist = []
    for elem in self:
      rtlist.append(elem)
    return rtlist
  def auditop(self):
    if not (self.forceoperations or psAM_settings['actionlist_alwaysforce']):
      raise RuntimeError(psAM_texts[psAM_settings['locale']]['listpy_suck_err'])
  def __setitem__(self, index, item):
    self.auditop()
    self.append(item)
    lastindex = self.__len__()-1
    tmplist = self.asdict()
    ritem = tmplist[lastindex]
    tmplist.pop()
    tmplist[index] = ritem
    self.clear()
    self.extend(tmplist)
    self.forceoperations = False
  def __delitem__(self, index):
    self.auditop()
    tmplist = self.asdict()
    del tmplist[index]
    self.clear()
    self.extend(tmplist)
    self.forceoperations = False
  def insert(self, index, item):
    self.auditop()
    self.append(item)
    lastindex = self.__len__()-1
    tmplist = self.asdict()
    ritem = tmplist[lastindex]
    tmplist.pop()
    tmplist.insert(index,ritem)
    self.clear()
    self.extend(tmplist)
    self.forceoperations = False
  def pop(self, index=-1):
    self.__delitem__(self,index)
  def __repr__(self):
    #Tweak: You can use __repr__() method to 'pythonize' all nested ps objects in an ps object.
    #小技巧：调用__repr__()方法可以“python化”所有嵌套的ps对象。
    if psAM_settings['evalable_repr']:
      return 'ActionListPy(%s)'%self.aslist()
    else:
      return '%s'%self.aslist()
  def __copy__(self):
    return ActionListPy(self.aslist())
  def __deepcopy__(self):
    cpy = ActionListPy()
    clst = self.aslist()
    for v in clst:
      if type(v) == ActionDescriptorPy or type(v) == ActionListPy:
        v = v.__deepcopy__()
      if type(v) == ActionReferencePy:
        v = v.__copy__()
      cpy.append(v)
    return cpy
  #I am the worst thing. I really cannot implement these.
  #我太烂了，我不会写这些。
  def __contains__(self, item):
    #ActionDescriptor have __contains__ because it only looks up keys, which can be easily judged as equal or not.
    #For ActionList, instead, __contains__ looks up elements, and there is not a method to judge if two ActionList-s are equal.
    raise NotImplementedError
  def __add__(self, other):
    raise NotImplementedError('Please use +=')
  def __radd__(self, other):
    raise NotImplementedError('Please use +=')
  def index(self, item, *args):
    raise NotImplementedError
  def remove(self, item):
    raise NotImplementedError
  def count(self, item):
    raise NotImplementedError
  def copy(self):
    raise NotImplementedError
  def reverse(self):
    raise NotImplementedError
  def sort(self, /, *args, **kwds):
    raise NotImplementedError
  def __mul__(self, n):
    raise NotImplementedError
  __rmul__ = __mul__
  def __imul__(self, n):
    raise NotImplementedError
  def __lt__(self, other):
    raise NotImplementedError
  def __le__(self, other):
    raise NotImplementedError
  def __eq__(self, other):
    raise NotImplementedError
  def __gt__(self, other):
    raise NotImplementedError
  def __ge__(self, other):
    raise NotImplementedError

class ActionObjectPy:
  def __init__(self, refpy):
    self.refpy = refpy
    self.pyobjw = ActionDescriptorPy(None)
  def pyobjr(self):
    app = psAM_settings['psapp']
    psobjr = app.executeActionGet(self.refpy.psobj)
    pyobjr = ActionDescriptorPy(self.refpy.asdict()['DesiredClass'],psobjr)
    return pyobjr
  def __getitem__(self,path):
    pathlist = path.split('/')
    pyobjr = self.pyobjr()
    for ki in pathlist:
      if ki:
        if ki.isdigit():
          ki = int(ki)
        curobj = curobj.__getitem__(ki)
      else:
        curobj = pyobjr
    return curobj
  def __setitem__(self, path, item):
    if type(item) in (ActionDescriptorPy,ActionListPy):
      raise RuntimeError('Please use merge()')
    app = psAM_settings['psapp']
    pathlist = path.split('/')
    fpth = '/'.join(pathlist[:-1])
    r = self[fpth]
    if type(r) == ActionDescriptorPy:
      w = ActionDescriptorPy(r.psclass)
      w.update({pathlist[-1]:item})
    if type(r) == ActionListPy:
      w = ActionListPy()
      w.append(item)
    self.pyobjw.update({'null':self.refpy})
    self.pyobjw.update({'to':w})
    app.executeAction(str2id('set'), self.pyobjw.psobj, ps.DialogModes.DisplayNoDialogs)
    self.pyobjw.clear()
  def merge(self,item):
    app = psAM_settings['psapp']
    self.pyobjw.update({'null':self.refpy})
    self.pyobjw.update({'to':item})
    app.executeAction(str2id('set'), self.pyobjw.psobj, ps.DialogModes.DisplayNoDialogs)
    self.pyobjw.clear()
