'''
Defines some descriptors and references that are frequently used.
'''

from ActionManager.ActionTypes import *
from ActionManager.ValueTypes import *

# Note about references.
# References points to an object which matches the information inside itself.
# For example, the following ref_current_layer always points to the current layer.

def ref_named_layer(name, textlayer=False):
  ltype = 'textLayer' if textlayer else 'layer'
  return ActionReferencePy.load(ReferenceKey(ltype, name))

def ref_current_layer(textlayer=False):
  ltype = 'textLayer' if textlayer else 'layer'
  return ActionReferencePy.load(ReferenceKey(ltype, Enumerated('ordinal', 'targetEnum')))

def desc_executor(refd=None, descd=None, extrad=None):
  adict = {'_classID':None}
  if refd is not None:
    adict.update({'null':refd})
  if descd is not None:
    adict.update({'T':descd})
  if extrad is not None:
    adict = {**adict, **extrad}
  return ActionDescriptorPy.load(adict)