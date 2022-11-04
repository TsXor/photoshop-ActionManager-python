# 已归档
已经可以用于实践了： https://github.com/TsXor/photoshop-python-api/tree/action_manager_module_integration

# photoshop-ActionManager-python
## [English](https://github.com/TsXor/photoshop-ActionManager-python/blob/main/README.md)
## 为什么要写这玩意
ActionManager常被称为"编写ps脚本的黑魔法"，而ScriptListener Plug-in是塑造这种印象的主要因素之一。  
我并不是说ScriptListener Plug-in不好用。它就是能整出正好能用的脚本，就是你把一部分数字换成变量也能正常工作。但我想说的是，ScriptListener Plug-in将它生成的脚本塞满tmd缩写代号和字符串转typeid的行为其实在妨碍我们**理解**真正该理解的——ActionManager如何运行。  
在这种“不求甚解”的影响下，https://github.com/lohriialo/photoshop-scripting-python/ 和 https://loonghao.github.io/photoshop-python-api/examples/ 中都有很多这种脚本。  
给我整无语了！ScriptListener Plug-in的tmd代码风格遮掩了一切逻辑！  
看看https://loonghao.github.io/photoshop-python-api/examples/#emboss-action 中截取的这段代码：
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
太抽象了家人们！  
但如果用这种方式看呢？  
```python
#这就是desc21的内部组成
#'grain'不是我打错了
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
这就是为什么要写这玩意。  
import `ActionManager.py`，即可像字典一样操控ActionDescriptor、像列表一样操控ActionList（受限，详情看文档）。  
这是另一个以更加友好的方式展示的ActionDescriptor：  
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
## 如何使用
请看[这里](https://github.com/TsXor/photoshop-ActionManager-python/blob/main/usage_zh.md)
