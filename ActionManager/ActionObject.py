class ActionObjectPy:
  def __init__(self, refpy):
    self.refpy = refpy
    self.pyobjw = ActionDescriptorPy(None)
  def pyobjr(self):
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
    pathlist = path.split('/')
    fpth = '/'.join(pathlist[:-1])
    r = self[fpth]
    if type(r) == ActionDescriptorPy:
      w = ActionDescriptorPy(r.ClassID)
      w.update({pathlist[-1]:item})
    if type(r) == ActionListPy:
      w = ActionListPy()
      w.append(item)
    self.pyobjw.update({'null':self.refpy})
    self.pyobjw.update({'to':w})
    app.executeAction(str2id('set'), self.pyobjw.psobj, ps.DialogModes.DisplayNoDialogs)
    self.pyobjw.clear()
  def merge(self,item):
    self.pyobjw.update({'null':self.refpy})
    self.pyobjw.update({'to':item})
    app.executeAction(str2id('set'), self.pyobjw.psobj, ps.DialogModes.DisplayNoDialogs)
    self.pyobjw.clear()