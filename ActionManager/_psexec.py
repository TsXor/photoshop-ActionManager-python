import photoshop.api as ps
from ActionManager.ActionTypes import ActionDescriptorPy

__all__ = ['exec', 'get']
app = None

def appcheck():
  global app
  if not app:
    app = ps.Application()
def exec(operation, desc):
  appcheck()
  desc = app.executeAction(str2id(operation), desc, ps.DialogModes.DisplayNoDialogs)
  return ActionDescriptorPy(classID=None, parent=desc.app)
def get(ref):
  appcheck()
  desc = app.executeActionGet(ref)
  return ActionDescriptorPy(classID=None, parent=desc.app)