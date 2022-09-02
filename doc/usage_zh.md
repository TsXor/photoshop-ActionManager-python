## 使用指导
过程和之前您用js或py写AM代码时差不多。  
0. 安装node.js到PATH
1. 用ScriptListener插件录制js  
2. 在终端中执行：`python -m ActionManager.jscompat < 录制的js的路径`  
得到的输出类似：  
```
==========
Executed an object:
Operation:
set
Descriptor:
{
    'null':[
        '!ref',
        ReferenceKey('channel', 'fsel')
    ],
    'T':[
        '!ref',
        ReferenceKey('path', Enumerated(type='path',value='vectorMask')),
        ReferenceKey('Lyr', 'aaaaaaaaaa')
    ],
    'version':1,
    'vectorMaskParams':True,
    '_classID':None
}
```
3. 将Descriptor中的一部分东西改成变量，然后封装成函数  
写出来类似：  
```python
import ActionManager as am
def do_it(name):
    descpy = {
        'null':[
            '!ref',
            am.ReferenceKey('channel', 'fsel')
        ],
        'T':[
            '!ref',
            am.ReferenceKey('path', Enumerated(type='path',value='vectorMask')),
            am.ReferenceKey('Lyr', name)
        ],
        'version':1,
        'vectorMaskParams':True,
        '_classID':None
    }
    desc = am.ActionDescriptorPy.load(descpy)
    am.exec('set', desc)
```
优点显而易见：更易理清AM对象的结构  

如果您愿意再多挖掘AM，这个模块也能起到很大的帮助：  
`uput`和`uget`方法可以方便地在AM对象中添加和获取项，您无需用getType查看类型再使用对应类型的get和put方法（python又不是强类型，这样做多少有点折磨）。同时这个模块可以最大程度的避免你亲自做typeID到stringID的转换。  

## 从原有的js或py项目扒代码
本节讲述一些*技巧*
### js
如果你试图直接对一个js项目的代码执行`python -m ActionManager.jscompat < js的路径`，那么大多不会有任何输出。  
这是因为大多数js项目都把AM代码封装成函数，因此，当你用上面的方法执行项目中含AM代码的文件时，AM代码事实上没有被执行，而jscompat子模块解释js代码的关键就在于AM代码需要**被通过executeAction执行**。  
事实上，jscompat子模块**不解释js代码**，它只是在要执行的js前面加了一段类和函数定义，诱导这段js代码在最终执行executeAction时以json形式输出执行的ActionDescriptor的全部信息，然后在python这边将json中的信息转换成可load的python对象。
以这一段js为例:  
```javascript
function selectVisibleIn(layer){
	var idsetd = charIDToTypeID( "setd" );
	var desc2 = new ActionDescriptor();
	var idnull = charIDToTypeID( "null" );
	var ref1 = new ActionReference();
	var idChnl = charIDToTypeID( "Chnl" );
	var idfsel = charIDToTypeID( "fsel" );
	ref1.putProperty( idChnl, idfsel );
	desc2.putReference( idnull, ref1 );
	var idT = charIDToTypeID( "T   " );
	var ref2 = new ActionReference();
	var idChnl = charIDToTypeID( "Chnl" );
	var idChnl = charIDToTypeID( "Chnl" );
	var idTrsp = charIDToTypeID( "Trsp" );
	ref2.putEnumerated( idChnl, idChnl, idTrsp );
	var idLyr = charIDToTypeID( "Lyr " );
	ref2.putName( idLyr, layer );
	desc2.putReference( idT, ref2 );
	executeAction( idsetd, desc2, DialogModes.NO );
}
function selectVisibleInVector(layer){
	var idsetd = charIDToTypeID( "setd" );
	var desc29 = new ActionDescriptor();
	var idnull = charIDToTypeID( "null" );
	var ref30 = new ActionReference();
	var idChnl = charIDToTypeID( "Chnl" );
	var idfsel = charIDToTypeID( "fsel" );
	ref30.putProperty( idChnl, idfsel );
	desc29.putReference( idnull, ref30 );
	var idT = charIDToTypeID( "T   " );
	var ref31 = new ActionReference();
	var idPath = charIDToTypeID( "Path" );
	var idPath = charIDToTypeID( "Path" );
	var idvectorMask = stringIDToTypeID( "vectorMask" );
	ref31.putEnumerated( idPath, idPath, idvectorMask );
	var idLyr = charIDToTypeID( "Lyr " );
	ref31.putName( idLyr, layer );
	desc29.putReference( idT, ref31 );
	var idVrsn = charIDToTypeID( "Vrsn" );
	desc29.putInteger( idVrsn, 1 );
	var idvectorMaskParams = stringIDToTypeID( "vectorMaskParams" );
	desc29.putBoolean( idvectorMaskParams, true );
	executeAction( idsetd, desc29, DialogModes.NO );
}
```
我们要给这段代码加一个“执行”部分，以您一眼就能认出来的变量名执行这个函数。如果原函数接受一个数字，您就把这个数字写成容易辨认的梗数字，比如`114514`或者`65472`；如果原函数接受一个字符串，您就加一个`'var_'`之类的头部来标识。
```javascript
selectVisibleIn('var_layername')
selectVisibleInVector('var_layername')
```
然后即可用jscompat子模块转换。
### py
本模块的`Action*`类兼容原`Action*`类的`put*`方法，因此您原来用ScriptListener录制并转化的python代码在简单的查找替换后即可继续使用。
在不久的将来，本模块将并入photoshop-api-python。

## 为什么取消原来模拟python类型的做法
本项目原来为ActionDescriptor和ActionList实现了各种魔法方法，以使它们接近python原生的dict和list，但是AM的一个机制差点把我逼疯：如果一个ActionDescriptor或ActionList中嵌套了一个ActionDescriptor或ActionList，那么子对象更改的时候，父对象不会跟着更改！  
我想了很多方法来克服这个机制，但是都有些太难实现。最终，我觉得，AM对我不仁，那我何必对它有义。直接将他们转化成原生python类型，编辑完再转化回去不就行了吗？

## 函数
- `exec(operation_string, descriptor)`  
	执行ActionDescriptor  
	相当于`app.executeAction(app.stringIDToTypeID(operation_string), descriptor, ps.DialogModes.DisplayNoDialogs)`  
- `get(reference)`  
	根据ActionReference获取ActionDescriptor  
	相当于`app.executeActionGet(reference)`  
- `jformat(repr, indent=4) -> formatted_repr`  
	用类似json的方式格式化一个表达式字符串。  
	这个方法只是字面意义上的做一些处理  
- `jprint(obj, indent=4)`  
	把对象表达式jformat的结果print出来  


## 类
- `Enumerated(type, value)`  
	一个ps_Enumerated对象包含“类型”和“值”。  
	我不知道说啥好，欧内的手太哈比下了。  
	由`namedtuple`创建。  
	
	**属性：**  
	- `type`  
	- `val`  

- `UnitDouble(unit, double)`  
	UnitDouble = Unit(单位) + Double(双精度浮点)  
	由`namedtuple`创建。  
	
	**属性：**  
	- `unit`  
	- `double`  


- `ActionReferencePy()`  
	可迭代  
	
	**方法:**  
	- `uget(index)`  
		从对象中获取一个引用。
		- 参数: index - 整数
	
	- `uput(refkey)`  
		向对象中放置一个引用。
		- 参数: refkey - 字典
	
	- `load(pyobject)` *类方法*  
		从一个符合格式的python对象生成一个ActionReferencePy。
		格式见下方“python dump格式”  
		- 参数: pyobject - 符合格式的python对象
		- 返回结果: ActionReferencePy  
	
	- `dump()`  
		将这个ActionReferencePy转换为符合格式的python对象。  
		格式见下方“python dump格式”  
		- 返回结果: python对象  
	
	**python dump格式:**  
	```
	[
	    '!ref',  #表明它是ActionReference的固定头
	    ReferenKey 对象,
	    ReferenKey 对象,
	    ...
	]
	```


- `ActionDescriptorPy(classID=None)`  
	可迭代  
	
	**属性：**  
	- `classID`  
	
	**方法：**  
	- `uget(key)`  
		从对象中获取一个...东西。
		- 参数: key - 字符串
	
	- `uput(thing)`  
		向对象中放置一个...东西。
		- 参数: thing - 支持的都可以放
	
	- `load(pyobject)` *类方法*  
		从一个符合格式的python对象生成一个ActionDescriptorPy。
		格式见下方“python dump格式”  
		- 参数: pyobject - 符合格式的python对象
		- 返回结果: ActionDescriptorPy  
	
	- `dump()`  
		将这个ActionDescriptorPy转换为符合格式的python对象。  
		格式见下方“python dump格式”  
		- 返回结果: python对象  
	
	**python dump格式:**  
	与正常字典一致，但是`'_classID'`键是保留的，用于存放它的classID


- `ActionListPy()`  
	可迭代  
	
	**方法：**  
	- `uget(index)`  
		从对象中获取一个...东西。
		- 参数: index - 整数
	
	- `uput(thing)`  
		向对象中放置一个...东西。
		- 参数: thing - 支持的都可以放
	
	- `load(pyobject)` *类方法*  
		从一个符合格式的python对象生成一个ActionDescriptorPy。
		格式见下方“python dump格式”  
		- 参数: pyobject - 符合格式的python对象
		- 返回结果: ActionDescriptorPy  
	
	- `dump()`  
		将这个ActionDescriptorPy转换为符合格式的python对象。  
		格式见下方“python dump格式”  
		- 返回结果: python对象  
	
	**python dump格式:**  
	与正常列表一致
