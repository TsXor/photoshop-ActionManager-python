## `erupt.py`实用工具
`erupt.py`可以将ScriptListener Plug-In录制的js脚本转换为python对象。  
需要安装node.js到PATH才能使用。  
用法：（命令行）`erupt.py <js文件名>`  
可以输出每次executeAction调用的ActionDescriptor及其他参数  
输出格式：  
```
Operation: （操作）
ActionDescriptor:（直观表达）
evalable_string:（可执行表达）
```

## “设置”
psAM_settings是一个字典，通过修改它的项，您可控制此模块的行为。  
此“设置”每次import都会被设为默认值。
- `'psapp'`  
  此模块用于typeid转换和创建ps对象的ps.Application对象，这个值必须设置。  
  默认值：`None`  
  如何设置：（举例）  
    ```
    import photoshop.api as ps
    from ActionManager import *
    app = ps.Application()
    psAM_settings['psapp'] = app
    ```
    ```
    import photoshop.api as ps
    import ActionManager as psAM
    app = ps.Application()
    psAM.psAM_settings['psapp'] = app
    ```
- `'locale'`  
  控制警告和报错的语言  
  默认值：`'en'`  
  可选值：`'zh'`、`'en'`  
- `'actionlist_alwaysforce'`  
  值为True时，一次性关掉ActionListPy操作时的RuntimeError  
  默认值：`False`  
  可选值：`True`、`False`  
- `'prepr_indent'`  
  `prettyrepr()`缩进的空格数  
  默认值：4  
  可选值：任何整数  
- `'evalable_repr'`  
  是否使用“可eval表达”  
  对于大部分python对象，都有：`x == eval(repr(x))`，即此对象使用了“可eval表达”  
  为了直观，本模块中的类默认都不使用“可eval表达”，但你可以通过此选项改变此行为，以获得可执行代码。  
  默认值：`False`  
  可选值：`True`、`False`  

## 函数
这些函数中大部分都是为方便而设计的。  
- `str2id(psstr)`  
	将一个`str`或`psChar`转换为ps typeid  
	- 参数  
		`psstr`: 将被转换的`str`或`psChar`  
	- 返回结果  
		`int`  
- `id2str(typeid)`  
	将一个ps typeid转换为`str`    
	- 参数  
		`typeid`: 将被转换的ps typeid  
	- 返回结果  
		`str`  
- `pytype_cvt(dtype)`  
	将python数据类型转换成以`str`形式表示的ps数据类型  
	- 参数  
		`dtype`: python数据类型  
	- 返回结果  
		`str`  
- `pstype_cvt(dtype)`  
	将用`ActionDescriptor`或`ActionList`的`getType()`方法获取的数据类型转换为`str`  
	- 参数  
		`dtype`: ps数据类型，可能是`int`或`ps.DescValueType`对象  
	- 返回结果  
		`str`  
- `psreftype_cvt(ftype)`  
	将用`ActionReference`的`getForm()`方法获取的数据类型转换为`str`  
	- 参数  
		`ftype`: ps数据类型，`ps.ReferenceFormType`对象  
	- 返回结果  
		`str`  
- `prettyrepr(pyobj)`  
	用较为易读的方式显示一个`ActionDescriptorPy`，`ActionListPy`或`ActionReferencePy`。  
	这个方法只是字面意义上的对这个对象的`repr`做一些处理
	- 参数  
		`pyobj`: 要处理的对象，`ActionDescriptorPy`，`ActionListPy`或`ActionReferencePy`  
	- 返回结果  
		`str` 

## 类
### 不可变
这些类的对象创建后就无法更改。  
- `psChar`  
	这个类用于将一个字符串“标记”为ps_Character。  
	ps_Character是正常字符串的抽象的“缩写代号”，可被转换成ps typeid。每个PS_Character都有一个对应的正常字符串。  
	ps_Character-s都是4字符长，不足者用空格对齐到4个字符。  
	然而，不是所有4字符长的字符串都是ps_Character，"warp"就不是。  
	这就是必须用这个类将一个字符串标记为ps_Character的原因。否则这个模块也没法区分ps_Character和正常字符串。
	
	**使用例：**  
	```
	chr_Usng = psChar('Usng')
	print(chr_Usng)  #'Usng'(marked as PS_Character)
	print(chr_Usng.tostr())  #'using'
	```
	
	**属性：**  
	- `data`  
	
	**方法：**  
	- `tostr()`  
		将此ps_Character转化成对应的正常字符串
		- 返回结果  
			`str`  

- `psEnumerated`  
	一个ps_Enumerated对象包含“类型”和“值”。  
	我不知道说啥好，欧内的手太哈比下了。  
	
	**使用例：**  
	```
	enum = psEnumerated('ordinal', 'targetEnum')
	print(enum)  #PS_Enumerated(type:ordinal targetEnum)
	print(enum.idtup)  #(1332896878, 1416783732)
	```
	
	**属性：**  
	- `enumtype`  
	- `enumval`  
	
	**方法：**  
	- `idtup()`  
		将此ps_Enumerated转化成一个包含自身“类型”和“值”对应typeid的元组。  
		- 返回结果  
			`tuple`  

- `psUnitDouble`  
	UnitDouble = Unit(单位) + Double(双精度浮点)  
	
	**使用例：**  
	```
	size = psUnitDouble('pointsUnit', 25.000000)
	print(size)  #PS_UnitDouble(25.000000 pointsUnit)
	print(size.idtup)  #(592473716, 25.0)
	```
	
	**属性：**  
	- `unit`  
	- `double`  
	
	**方法：**  
	- `idtup()`  
		将此ps_UnitDouble转化成一个包含自身“单位”对应typeid和“数值”的元组。  
		- 返回结果  
			`tuple`  

- `ActionReferencePy`  
	ActionReference的包装。  
	我将它设计为不可变，因为一个ActionReference对应一个ps对象。  
	可以从一个现存的ActionReference创建。  
	
	**参数：**  
	DesiredClass, FormType, Value  
	或者一个ps.ActionReference()对象  
	当FormType=='Class'，无需提供Value。
	
	**使用例：**  
	```
	#从头创建一个ActionReferencePy
	ref0 = ActionReferencePy('textLayer', 'Enumerated', psEnumerated('ordinal', 'targetEnum'))
	#                        ^~~~~~~~~~~  ^~~~~~~~~~~~  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#                        DesiredClass FormType      Value
	print(ref0)  #Reference{'DesiredClass': 'textLayer', 'FormType': 'Enumerated', 'Value': PS_Enumerated(type:ordinal targetEnum)}
	```
	```
	#从一个现存的ActionReference创建一个ActionReferencePy
	ref12 = ps.ActionReference()
	idContentLayer1 = app.stringIDToTypeID("contentLayer")
	ref12.putClass(idContentLayer1)
	ref12py = ActionReferencePy(ref12)
	print(ref12py)  #Reference{'DesiredClass': 'contentLayer', 'FormType': 'Class'}
	```
	
	**属性：**  
	- `psobj`  
		它的核心 -- ps对象。
	
	**Methods:**
	- `asdict()`  
		将这个ActionReferencePy转换为包含自身信息的字典。  
		- 返回结果  
			`dict`  

### 可变
这些类的对象创建后可被更改或扩展。
- `ActionDescriptorPy`  
	ActionDescriptor的包装。  
	ActionDescriptorPy是`UserDict`。像字典一样操作即可。  
	如果你想看看一个对象里面有什么，`print()`它即可，无需使用那些`getType`和`getWhat`这个类会自动帮你完成这些。  
	注意：`__or__` `__ror__` `__ior__` `__copy__`未实现！  
	一个ActionDescriptor只对应一个ActionDescriptorPy。  
	```
	desc = ps.ActionDescriptor()
	descpy1 = ActionDescriptorPy(None,desc)  #创建一个ActionDescriptorPy，并分配给descpy1
	descpy2 = ActionDescriptorPy(None,desc)  #不创建ActionDescriptorPy，descpy1被分配给descpy2
	```
	细节请看这个类的`__new__`和`__init__`方法。
	
	**参数：**  
	一个ps类名和一个字典或者ps.ActionDescriptor()对象。  
	你可以用`None`做ps类名，过后再更改`psclass`属性。如果你很确定这个ActionDescriptorPy不会被嵌套到其他ActionDescriptorPy中，保持`psclass`为`None`也行。  
	
	**使用例：**  
	```
	#从头创建一个ActionDescriptorPy
	desc24py = ActionDescriptorPy('paragraphStyle', {'styleSheetHasParent': True})
	print(desc24py)  #paragraphStyle{'styleSheetHasParent': True}
	```
	```
	#从一个现存的ActionDescriptor创建一个ActionDescriptorPy
	desc24 = ps.ActionDescriptor()
	idstyleSheetHasParent = app.stringIDToTypeID( "styleSheetHasParent" )
	desc24.putBoolean( idstyleSheetHasParent, True )
	desc24py = ActionDescriptorPy('paragraphStyle', desc24)
	print(desc24py)  #paragraphStyle{'styleSheetHasParent': True}
	```
	
	**属性：**  
	- `psobj`  
		它的核心 -- ps对象。  
	- `psclass`  
	
	**方法：**  
	普通字典的方法可用，此处不列出。  
	- `asdict()`  
		将这个ActionDescriptorPy转化为真正的字典。  
		注意，这是“浅转换”。如果里面嵌套着ActionDescriptorPy或ActionListPy，他们不会被转换！
		- 返回结果  
			`dict`  
	
- `ActionListPy`  
	ActionList的包装。  
	ActionListPy is `UserList`. Just manipulate it like a list.  
	这个类从被写出来开始就可以说是“被诅咒”的。还是看看ActionList的这些限制吧家人们：  
	(引自photoshop_scriptref_js，自行翻译)
	> This object provides an array-style mechanism for storing data. It can be used for low-level access into Photoshop.  
	> This object is ideal when storing data of the same type. All items in the list must be of the same type.  
	> You can use the "put" methods, such as putBoolean(), to append new elements, and can clear the entire list using clear(), but cannot otherwise modify the list.  
	
	而且ActionList还有这个TMD“特性”: https://github.com/loonghao/photoshop-python-api/issues/169  
	这个类必然充满着bug，需要大量的修补，但是单靠我恐怕很难做到。  
	`__contains__` `__add__` `__radd__` `index` `remove` `count` `copy` `reverse` `sort` `__mul__` `__rmul__` `__imul__` `__copy__` `__lt__` `__le__` `__eq__` `__gt__` `__ge__`未被实现。(因为对于一个ActionList来说排序和比较是无意义的，外加我不会。)
	
	**参数：**  
	A list or a ps.ActionList() object.  
	
	**使用例：**  
	```
	#从头创建一个ActionListPy
	list1py = ActionListPy([1,2,3,4,5,6,7,8,9])
	print(list1py)  #[1, 2, 3, 4, 5, 6, 7, 8, 9]
	```
	```
	#从一个现存的ActionList创建一个ActionListPy
	list1 = ps.ActionList()
	list1.putBoolean( True )
	list1.putBoolean( False )
	list1py = ActionListPy(list1)
	print(list1py)  #[True, False]
	```
	
	**属性：**  
	- `psobj`  
		它的核心 -- ps对象。  
	- `forceoperations`  
		你每次插入或删除元素前都需将此属性设为True。  
		这是为了告诉你别这么做。顺序对ActionList来说没有意义。  
	
	**方法：**  
	普通列表的方法可用，此处不列出。  
	某些列表方法不可用：`index()` `remove()` `sort()`  
	- `aslist()`  
		将这个ActionListPy转化为真正的列表。  
		注意，这是“浅转换”。如果里面嵌套着ActionDescriptorPy或ActionListPy，他们不会被转换！
		- 返回结果  
			`list`  
