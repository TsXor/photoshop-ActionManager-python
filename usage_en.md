## "settings"
psAM_settings is a dict, by changing it, you can control the behavior of this module.  
These "settings" will be set to default on every import.
- `'psapp'`  
  The ps.Application object which this module uses in typeid conversion and ps object creation. You must set this value.  
  default：`None`  
  how to configure：(for example)  
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
  Control the languae of warnings and errors.  
  default：`'en'`  
  available：`'zh'`、`'en'`  
- `'actionlist_alwaysforce'`  
  Disable RuntimeError raised by ActionListPy when True.  
  default：`False`  
  available：`True`、`False`  

## Functions
Most of these functions are designed for convenience.  
- `str2id(psstr)`  
	Convert a `str` or a `psChar` to ps typeid  
	- Parameters  
		`psstr`: `str` or `psChar` to be converted  
	- Returns  
		`int`  
- `id2str(typeid)`  
	Convert a ps typeid to `str`    
	- Parameters  
		`typeid`: ps typeid to be converted  
	- Returns  
		`str`  
- `pytype_cvt(dtype)`  
	Convert python type to ps type in `str`  
	- Parameters  
		`dtype`: datatype, python type  
	- Returns  
		`str`  
- `pstype_cvt(dtype)`  
	Convert the type which is obtained from `getType()` method of an `ActionDescriptor` or `ActionList` to `str`  
	- Parameters  
		`dtype`: datatype, can be an `int` or a `ps.DescValueType` object  
	- Returns  
		`str`  
- `psreftype_cvt(ftype)`  
	Convert the type which is obtained from `getForm()` method of an `ActionReference` to `str`  
	- Parameters  
		`ftype`: datatype, a `ps.ReferenceFormType` object  
	- Returns  
		`str`  

## Classes
### immutable
Objects of these classes cannot be modified once created.  
- `psChar`  
	This class is used to "mark" a string as ps_Character.  
	ps_Character-s are abstract "abbreviated nicknames" of normal strings, and they can be converted to ps typeids. Every ps_Character has a corresponding normal string.  
	ps_Character-s are 4-character long strings or shorter strings padded to 4 characters with spaces.  
	However, not all 4-character strings you see are ps_Character-s. For example, "warp" is not a ps_Character.  
	That's why you need to use this class to mark a string as a ps_Character. Otherwise, this module cannot tell ps_Character-s from normal strings.  
	
	**Example:**  
	```
	chr_Usng = psChar('Usng')
	print(chr_Usng)  #'Usng'(marked as PS_Character)
	print(chr_Usng.tostr())  #'using'
	```
	
	**Attributes:**  
	- `data`  
	
	**Methods:**  
	- `tostr()`  
		Convert this ps_Character to the corresponding normal string.
		- Returns  
			`str`  

- `psEnumerated`  
	A ps_Enumerated contains type and value.  
	I don't know what to say. It's too abstract.
	
	**Example:**  
	```
	enum = psEnumerated('ordinal', 'targetEnum')
	print(enum)  #PS_Enumerated(type:ordinal targetEnum)
	print(enum.idtup)  #(1332896878, 1416783732)
	```
	
	**Attributes:**  
	- `enumtype`  
	- `enumval`  
	
	**Methods:**  
	- `idtup()`  
		Convert this ps_Enumerated to a tuple containing typeid of type and value.
		- Returns  
			`tuple`  

- `psUnitDouble`  
	UnitDouble = Unit + Double  
	
	**Example:**  
	```
	size = psUnitDouble('pointsUnit', 25.000000)
	print(size)  #PS_UnitDouble(25.000000 pointsUnit)
	print(size.idtup)  #(592473716, 25.0)
	```
	
	**Attributes:**  
	- `unit`  
	- `double`  
	
	**Methods:**  
	- `idtup()`  
		Convert this ps_UnitDouble to a tuple containing typeid of unit and double.
		- Returns  
			`tuple`  

- `ActionReferencePy`  
	Wrapper for ActionReference.  
	It is designed to be immutable because one ActionReference represents one unique ps object.  
	It can be created from parameters or an existing ActionReference.  
	
	**Parameters:**  
	DesiredClass, FormType, Value  
	or simply a ps.ActionReference() object  
	When FormType=='Class', Value is not needed.
	
	**Example:**  
	```
	#Create an ActionReferencePy from scratch
	ref0 = ActionReferencePy('textLayer', 'Enumerated', psEnumerated('ordinal', 'targetEnum'))
	#                        ^~~~~~~~~~~  ^~~~~~~~~~~~  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#                        DesiredClass FormType      Value
	print(ref0)  #Reference{'DesiredClass': 'textLayer', 'FormType': 'Enumerated', 'Value': PS_Enumerated(type:ordinal targetEnum)}
	```
	```
	#Create an ActionReferencePy from an existing ActionReference
	ref12 = ps.ActionReference()
	idContentLayer1 = app.stringIDToTypeID("contentLayer")
	ref12.putClass(idContentLayer1)
	ref12py = ActionReferencePy(ref12)
	print(ref12py)  #Reference{'DesiredClass': 'contentLayer', 'FormType': 'Class'}
	```
	
	**Attributes:**  
	- `psobj`  
		It's core -- the ps object.
	
	**Methods:**
	- `asdict()`  
		Convert this ActionReferencePy to a dict containing its information.  
		- Returns  
			`dict`  

### mutable
Objects of these classes can be extended and modified.
- `ActionDescriptorPy`  
	Wrapper for ActionDescriptor.  
	ActionDescriptorPy is `UserDict`. Just manipulate it like a dict.  
	When you want to see what is inside, just `print()` it, no need to use those `getType` and `getWhat`, this class does it for you!  
	Note that `__or__` `__ror__` `__ior__` `__copy__` are not implemented!  
	One ActionDescriptor can only have one ActionDescriptorPy.
	```
	desc = ps.ActionDescriptor()
	descpy1 = ActionDescriptorPy(None,desc)  #An ActionDescriptorPy is created and assigned to descpy1
	descpy2 = ActionDescriptorPy(None,desc)  #No ActionDescriptorPy is created and descpy1 is assigned to descpy2
	```
	For details, see the `__new__` and `__init__` method of this class.
	
	**Parameters:**  
	A ps classname and a dict or a ps.ActionDescriptor() object.  
	You may give a `None` for ps classname, and modify the `psclass` attribute later. If you make sure that you never nest this ActionDescriptorPy into other ActionDescriptorPy, you can keep it `None`.  
	
	**Example:**  
	```
	#Create an ActionDescriptorPy from scratch
	desc24py = ActionDescriptorPy('paragraphStyle', {'styleSheetHasParent': True})
	print(desc24py)  #paragraphStyle{'styleSheetHasParent': True}
	```
	```
	#Create an ActionDescriptorPy from an existing ActionDescriptor
	desc24 = ps.ActionDescriptor()
	idstyleSheetHasParent = app.stringIDToTypeID( "styleSheetHasParent" )
	desc24.putBoolean( idstyleSheetHasParent, True )
	desc24py = ActionDescriptorPy('paragraphStyle', desc24)
	print(desc24py)  #paragraphStyle{'styleSheetHasParent': True}
	```
	
	**Attributes:**  
	- `psobj`  
		It's core -- the ps object.  
	- `psclass`  
	
	**Methods:**  
	Methods for normal dicts are available and not listed here.  
	- `asdict()`  
		Convert this ActionDescriptorPy to a real dict.  
		Note that this conversion is "shallow". If there's a ActionDescriptorPy or ActionListPy nested inside, it will not be converted!
		- Returns  
			`dict`  
	
- `ActionListPy`  
	Wrapper for ActionList.  
	ActionListPy is `UserList`. Just manipulate it like a list.  
	This class is cursed when being written. Just see these limitations of ActionList:  
	(from photoshop_scriptref_js)
	> This object provides an array-style mechanism for storing data. It can be used for low-level access into Photoshop.  
	> This object is ideal when storing data of the same type. All items in the list must be of the same type.  
	> You can use the "put" methods, such as putBoolean(), to append new elements, and can clear the entire list using clear(), but cannot otherwise modify the list.  
	
	And this fkng "feature" of ActionList: https://github.com/loonghao/photoshop-python-api/issues/169  
	It surely have lots of bugs and need lots of fixes, but it's too hard to do with my merely self.  
	`__contains__` `__add__` `__radd__` `index` `remove` `count` `copy` `reverse` `sort` `__mul__` `__rmul__` `__imul__` `__copy__` `__lt__` `__le__` `__eq__` `__gt__` `__ge__` are not implemented. (because sorting and comparing is meaningless to an ActionList, and I have no idea how to implement)
	
	**Parameters:**  
	A list or a ps.ActionList() object.  
	
	**Example:**  
	```
	#Create an ActionListPy from scratch
	list1py = ActionListPy([1,2,3,4,5,6,7,8,9])
	print(list1py)  #[1, 2, 3, 4, 5, 6, 7, 8, 9]
	```
	```
	#Create an ActionListPy from an existing ActionList
	list1 = ps.ActionList()
	list1.putBoolean( True )
	list1.putBoolean( False )
	list1py = ActionListPy(list1)
	print(list1py)  #[True, False]
	```
	
	**Attributes:**  
	- `psobj`  
		It's core -- the ps object.  
	- `forceoperations`  
		You will have to set this to True every time before you insert or delete an element.  
		This is to tell you not to do this. Order is meaningless to an ActionList.  
	
	**Methods:**  
	Methods for normal lists are available and not listed here.  
	Some list methods are not available: `index()` `remove()` `sort()`  
	- `aslist()`  
		Convert this ActionListPy to a real list.  
		Note that this conversion is "shallow". If there's a ActionDescriptorPy or ActionListPy nested inside, it will not be converted!
		- Returns  
			`list`  
