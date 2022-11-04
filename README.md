# Archived
It's ready to use at https://github.com/TsXor/photoshop-python-api/tree/action_manager_module_integration.

# photoshop-ActionManager-python
## [简体中文](https://github.com/TsXor/photoshop-ActionManager-python/blob/main/README_zh.md)
## Why this thing is written
ActionManager is often referred to as "the black magic of photoshop scripting", and ScriptListener Plug-in contributes a lot in making such a reputation.  
I am not saying that ScriptListener Plug-in is not useful. It can just create scripts that can just work --- even after you replace some of the numbers in the script with variables. What I want to say is that the ScriptListener Plug-in actually blocks us from **understanding** the real thing --- how ActionManager works by making the generated scripts filled with fkng abbreviated nicknames and conversion between strings and typeids.  
At the same time, there are so much scripts like this in https://github.com/lohriialo/photoshop-scripting-python/ and https://loonghao.github.io/photoshop-python-api/examples/.  
I really don't know what to say! The fkng codestyle of the ScriptListener Plug-in actually covers up all logics!  
See this piece of code from https://loonghao.github.io/photoshop-python-api/examples/#emboss-action:
```python
index = 0
idMk = app.charIDToTypeID("Mk  ")
desc21 = ps.ActionDescriptor()
idNull = app.charIDToTypeID("null")
ref12 = ps.ActionReference()
idContentLayer1 = app.stringIDToTypeID("contentLayer")
ref12.putClass(idContentLayer1)
desc21.putReference(idNull, ref12)
idUsng = app.charIDToTypeID("Usng")
desc22 = ps.ActionDescriptor()
idType = app.charIDToTypeID("Type")
desc23 = ps.ActionDescriptor()
idClr = app.charIDToTypeID("Clr ")
desc24 = ps.ActionDescriptor()
idRd = app.charIDToTypeID("Rd  ")
desc24.putDouble(idRd, index)
idGrn = app.charIDToTypeID("Grn ")
desc24.putDouble(idGrn, index)
idBl = app.charIDToTypeID("Bl  ")
desc24.putDouble(idBl, index)
idRGBC = app.charIDToTypeID("RGBC")
desc23.putObject(idClr, idRGBC, desc24)
idSolidColorLayer = app.StringIDToTypeID("solidColorLayer")
desc22.putObject(idType, idSolidColorLayer, desc23)
idContentLayer2 = app.StringIDToTypeID("contentLayer")
desc21.putObject(idUsng, idContentLayer2, desc22)
```
This is way too abstract.  
And... What if I can see them this way:  
```python
#This is what the inner things of desc21 looks like
#That 'grain' is NOT MY TYPO
{
  'null': Reference{
    'DesiredClass': 'contentLayer',
    'FormType': 'Class'
  },
  'using': contentLayer{
    'type': solidColorLayer{
      'color': RGBColor{
        'red': 0.0,
        'grain': 0.0,
        'blue': 0.0
      }
    }
  }
}
```
After importing the `ActionManager.py`, you can manage ActionDescriptor like dicts, ActionList like lists.
Here is another example of an ActionDescriptor shown in a more friendly way:
```python
{
  'textKey': 'somewhat text',
  'textStyleRange': [
    textStyleRange{
      'from': 0,
      'to': 48,
      'textStyle': textStyle{
        'styleSheetHasParent': True,
        'fontPostScriptName': 'STKaiti',
        'fontName': 'STKaiti',
        'fontStyleName': 'Regular',
        'fontScript': 25,
        'fontTechnology': 1,
        'size': PS_UnitDouble(25.000000 pointsUnit),
        'syntheticBold': True,
        'autoLeading': False,
        'leading': PS_UnitDouble(32.000000 pointsUnit)
      }
    }
  ],
  'paragraphStyleRange': [
    paragraphStyleRange{
      'from': 0,
      'to': 48,
      'paragraphStyle': paragraphStyle{
        'styleSheetHasParent': True
      }
    }
  ]
}
```
## How to use
See [this](https://github.com/TsXor/photoshop-ActionManager-python/blob/main/usage_en.md).
