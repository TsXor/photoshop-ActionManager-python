from ActionManager.jscompat.node_execjs import execjs
from ActionManager.jscompat.jshack import hack
from ActionManager._utils import str2id, id2str
from copy import *
from ActionManager import *
import json

def psstr(tstr):
  if type(tstr) == str and tstr.find('CharID_') == 0:
    r = id2str(str2id(tstr[7:]))
  else:
    r = tstr
  return r

str2getpacker = {
    'UnitDouble':lambda x: UnitDouble(psstr(x['unit']), psstr(x['double'])),
    'Enumerated':lambda x: Enumerated(psstr(x['enumtype']), psstr(x['enumval'])),
    'ActionDescriptor':lambda x: parsedict(x),
    'ActionReference':lambda x: parseref(x),
    'ActionList':lambda x: parselist(x),
    }
str2refgetpacker = {
    'Enumerated':lambda x: {'DesiredClass':psstr(x['DesiredClass']),'FormType':'Enumerated','Value':Enumerated(psstr(x['Value']['enumtype']), psstr(x['Value']['enumval']))}
    }

def parsedict(tdict):
  if not '_classID' in tdict:
    tdict['_classID'] = None
  else:
    tdict['_classID'] = psstr(tdict['_classID'])
  pdict = {psstr(k):(str2getpacker[v['type']](v) if type(v) == dict else v) for k,v in tdict.items()}
  del pdict['type']
  return pdict

def parselist(tdict):
  d2l = [tdict[str(i)] for i in range(tdict['len'])]
  plist = [(str2getpacker[e['type']](e) if type(e) == dict else e) for e in d2l]
  return plist

def parseref(tdict):
  d2l = [tdict[str(i)] for i in range(tdict['len'])]
  plist = ['!ref']
  plist.extend([(str2refgetpacker[e['Value']['type']](e) if type(e['Value']) == dict else {k:psstr(v) for k,v in e.items()}) for e in d2l])
  return plist

def json2obj(jsont):
  obj_init = json.loads(jsont)
  obj_desc = parsedict(obj_init['ActionDescriptor']) if 'ActionDescriptor' in obj_init else None
  obj_operation = psstr(obj_init['Operation'])
  obj_option = obj_init['Option']
  return (obj_operation,obj_desc,obj_option)

def dump(jst):
  jst = hack + '\n' + jst
  jsont = execjs(jst)
  objs = [json2obj(j) for j in jsont.split('END OF JSON') if j != '\n']
  return objs
  