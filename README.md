# ST UJ Editor

### FEATURES:
- load from XML
- replace DDI name - both in DDI definition and all references (although that is handled fine in the GUI)
- *reset steps' order values (why?)*
- elevate stepgroups
- copy, move, delete steps
- create, copy, delete DDIs
- save to XML

### TODO:
 1. recreate the object models
 2. understand the effect of :
 	... xmlns="http://www.reflective.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.reflective.com stschema.xsd" ...
 3. add classes for post & flow_control
 4. make UI enforce data types and mandatory fields
 5. implement step details
 5. implement Save on switching element
 6. implement Undo
 7. implement Copy/Paste/Move/Drag
 8. implement Search/Replace
 9. implement additional features like list of Steps referencing selected DDI

 99. add option to populate table from CSV file for the List DDI

### NOTES:
- http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

- The execution order is determined by the order of the steps in the XML, thus:
  - renamed attribute 'order' to 'id' for my objects
  - utilize stepgroup referencing limitation:
    - stepgroup reference cannot be to id, that hasn't been encountered as a step id
    - stepgroup starts with self referencing step - the lead step
    - stepgroup closes upon encountering step that has reference other than the previous one

- to write without the namespace prefix:
  - register namespace prior to parse:  `ET.register_namespace('', 'http://www.reflective.com')`
  - use ET.parse instead of ET.ElementTree(file):  `self.tree = ET.parse(filename) # self.tree = ET.ElementTree(file=filename)`
  - use file write with `ET.tostring(self.root)` instead of the ET export `tree.write('output.xml')`;
  * one issue is that this process strips the 1st line, so add it manually:
```python
with open(file_name, 'w') as xml_file:
	xml_file.write(self.raw.split('\n')[0] + '\n' + ET.tostring(self.root).decode("utf-8"))
```

- deletion of step ignores the dependence of DDIs upon the step as a source

- deletion of DDI ignores the dependence on related DDIs and references of that DDI in steps

- seems like good code structure: https://github.com/baoboa/pyqt5/blob/master/examples/widgets/groupbox.py

- I should find, learn and utilize PyQt's unit testing

### BUGS:
1. trying to use `bool(element.get('NAMEUSERDEFINED'))` fails because the strings in source are not capitalized; use instead `element.get('NAMEUSERDEFINED') == 'true'`
2. showing DDI that has invalid step reference, silently uses the last value of the 'source step' field
3. Field Name dropdown for Correlated DDI mixes the possible selections for Repeated and Known fields.
4. exporting siphon strings adds extra encoding on some characters i.e. double quotes:
  - original

```
<STARTTEXT>&lt;td    nowrap="nowrap"  id="mx\d{2,8}(\[R:\d+?\])_0"  align="left"   valign="top".+?id="(mx\d{2,8})\1_holder" class="bc"&gt;&lt;span ctype="label"  id="\2\1".+?title="([^"]+?)"&gt;[^"]+?&lt;/span&gt;&lt;/div&gt;&lt;/td&gt;[^~]+?&lt;td    nowrap="nowrap"  id="mx\d{2,8}\1_0"[^~]+?id="mx\d{2,8}\1_holder" class="bc"&gt;&lt;span ctype="label"  id="mx\d{2,8}\1"[^~]+?title="([^"]+?)"&gt;\4&lt;/span&gt;&lt;/div&gt;&lt;/td&gt;[^~]+?title="([^"]+?)"[^~]+?title="WAPPR"&gt;WAPPR&lt;/label&gt;&lt;/div&gt;&lt;/td&gt;</STARTTEXT>
```
  - processed
```
<STARTTEXT>&lt;td    nowrap=&quot;nowrap&quot;  id=&quot;mx\d{2,8}(\[R:\d+?\])_0&quot;  align=&quot;left&quot;   valign=&quot;top&quot;.+?id=&quot;(mx\d{2,8})\1_holder&quot; class=&quot;bc&quot;&gt;&lt;span ctype=&quot;label&quot;  id=&quot;\2\1&quot;.+?title=&quot;([^&quot;]+?)&quot;&gt;[^&quot;]+?&lt;/span&gt;&lt;/div&gt;&lt;/td&gt;[^~]+?&lt;td    nowrap=&quot;nowrap&quot;  id=&quot;mx\d{2,8}\1_0&quot;[^~]+?id=&quot;mx\d{2,8}\1_holder&quot; class=&quot;bc&quot;&gt;&lt;span ctype=&quot;label&quot;  id=&quot;mx\d{2,8}\1&quot;[^~]+?title=&quot;([^&quot;]+?)&quot;&gt;\4&lt;/span&gt;&lt;/div&gt;&lt;/td&gt;[^~]+?title=&quot;([^&quot;]+?)&quot;[^~]+?title=&quot;WAPPR&quot;&gt;WAPPR&lt;/label&gt;&lt;/div&gt;&lt;/td&gt;</STARTTEXT>
```
5. Export forces STEPGROUP tag on steps that didn't have one
6. switching the DDI type of a selected DDI, should change the type specific items in the UI

### BUG NOTES:
- on bug 1 - this is now fixed in some places to properly interpret the values, and on other places to retain the string value
- on bug 2 - this occurs only when the input UJ is technically incomplete; should be handled along with setting the DDI attribute 'valid' to False
- on bug 3 - fixing this would need to circumvent/extend the algorithm that maps DDI type to UI fields; extra UI field change triggered by selection of the ddi_auto_correlate_type field
- on bug 4 - this is crazy, but this does not seem to affect import:
  - in ST value for the ID 10 of the processed XML:
```
<input  aria-required="true"  role="textbox"  id="([^'"\[]*?)" class="fld text    ibfld fld_req"     ctype="textbox"   li="mx[\d]{1,8}"     maxlength="[\d]{1,8}" style=";width:[\d]{1,8}\.[\d]{1,8}px;"         type="text" title="Description:? ?.*?" value=".*?" ov=".*?" work="[\d]{1,8}" fldInfo='\{&quot;length&quot;:&quot;[\d]{1,8}&quot;,&quot;inttype&quot;:&quot;[\d]{1,8}&quot;,&quot;required&quot;:true\}'/>
```
  - in ST value for the ID 10 of the original XML:
```
<input  aria-required="true"  role="textbox"  id="([^'"\[]*?)" class="fld text    ibfld fld_req"     ctype="textbox"   li="mx[\d]{1,8}"     maxlength="[\d]{1,8}" style=";width:[\d]{1,8}\.[\d]{1,8}px;"         type="text" title="Description:? ?.*?" value=".*?" ov=".*?" work="[\d]{1,8}" fldInfo='\{&quot;length&quot;:&quot;[\d]{1,8}&quot;,&quot;inttype&quot;:&quot;[\d]{1,8}&quot;,&quot;required&quot;:true\}'/>
```
- on bug 5 - ST import should not complain about that, and the UJ functionality does not change as a result [WONTFIX]
- on bug 6 -

#### DESIGN DECISIONS:
 - Q: Knowledge among UJ<>STEP<>DDI:
    - UJ know both Step and DDI classes/objects;
    - I want to have method that pulls steps by referenced DDI.name, thus Step needs to know of DDI objects
    - I want to have method that pulls DDIs by having them referenced in step.name, thus DDI needs to know of Step objects
 - A: Only the UJ should know of DDI & Step objects. The desired search methods should be in the UJ class; Steps should expose only the references as strings, and pull_obj_by_name should be in the UJ level
***
 - Q: Making Changes:
  - Loading the XML, I have two sets of objects - those provided bu ElementTree and those in my lib. When making updates to the data,
  - I can try to simultaneously update both sets objects, then just export via ET
  - or I can update only the my objects, and transfer the data to ET objects upon exit
 - A: That will depend on the tool being created:
  If it's just UJ editor, the classes should be wrapper around the ET classes
  If this is something more than editor, the ET is just one side of the project, and output may be via different channel (i.e. DB)
  Finally - make it a wrapper
***
 - Q: Handle StepGroups.
  - The UJs deal with stepgroups as step property
  - I want to have stepgroups as an object that contains the steps
   - I can have the stepgroup class, to be able to lookup belonging steps, and still have a step property.
The question is, if I have class, stepgroup, should I have step references in the UJ class, or should the UJ class only see stepgroups.
 - A: Have the UJ see only stepgroups. Add stepgroup objects for orphan steps, but keep the step's stepgroup attribute as is. During export we can respect the step attribute to properly export orphan steps;
   Or we can export forcing orphaned steps into their own stepgroups - that should not affect experience in the ST GUI
  - PR: I cant create stepgroup objects before creating step objects
  - PR: when I need to insert step at specific position, I need to use the full list of steps. I cannot use the lists attached to stepgroups, because they are not represented as ET objects, thus do not export.
  - PR: I cant leverage having a StepGroup class, without bottom up creation of the ET object upon export
 - A: the 'steps' attribute of StepGroup objects is valid ET object since it contains sub-element objects. Manage the XML edits withing that list, and then concatenate all lists before write/output
***
 - Q: How should I implement the interface for copy/delete/move steps?
   - the tree structure is best for representing the stepgroups in steps
   - I can have UJ class display all elements of the tree or
   - I can have the UJ class show stepgroup elements, and stepgroup to return it's own subtree representation
 - A: try having them separate, because otherwise UJ will need visibility of step objects
***
 - Q: What should be the grouping of UI elements for objects that have "sub" types
   - all added to single group, and disabled/hidden dependent on the "sub" type (reuse layout)
   - have separate groups with "sub" type specific layout, and load only the relevant group (more granularity -- may allow for DDI subclasses)
 - A: Have the common fields in one group, and the fields that differ in "sub" type specific layouts/groups
***
 - Q: How to implement Undo if triggered on after element change (i.e. Save)
   - undo all changes made since prior Save
   - undo just last field change
 - A: If you apply undo just to the last field, you can keep using Undo to revert all changes for that element i.e. covers both use cases; Alternatively provide two separate undo flavours - 'undo' & 'undo element';
 - Q: Should there be multi-select edit, where each field change is applied to all selected fields, while fields that are not altered remain different for the different elements.
 - A: Sure, why not. Especially if Undo works.

#### OTHER CONSIDERATIONS
There are too many design issues that creep from the XML structure into the object structure. I should create an alternative, using my structures, and adjust the XML feed as needed once I get to that point.

Which components would I not overwrite? Because these would be the ones to structure around:

- XML
- GUI
- DB
- Injector
- MA
- SAF
- MaxPack
- Recorder
- Post Recording processing
- LDAP/NTLM/etc integration

To consider key features:

* injector handles threads as browser
* injector handles cookies as browser
* MA has incorporated various communication templates/handshakes to access variety of sources
* recorder (mostly) integrates

---
The XML structure is horrible -- take the 'constant' DDI:
 - some values are listed as element arguments (name, valid), others are listed as sub-elements (source, lifecycle). A third kind are listed as repeating sub-element with unique different attributes (encode, fieldname, inurl), and forth kind are siphons, which have complex structure of list of elements, with element that has attributes sequence & type, then each has three consistent sub-elements - starttext, endtext, rfindex; where values for these are in the form of in-element text, rather than attributes
 - the 'selector' field is not available in the GUI for this DDI type. The default value is "First", but is never omitted in XML, although it cannot be anything different
 - the 'refresh' (named lifecycle in XML) and 'shared' (scope), are shown in UI, but fully disabled; the defaults cannot be changed, yet are not omitted in XML, nor hidden in UI
 - seems like every DDI object has an boolean 'encode' attribute, but in XML, that's not in the the DDI element attributes, not even as a child like 'selection' or 'scope', but is under sub-element 'item' identified with specific attribute-value pair i.e `CODE="ENCODE    "` , and the actual boolean value is as in element text: `<ITEM CODE="ENCODE    ">true</ITEM>`
 - indication whether the success validation string should be RegEx or strig is in NVP towards the step, while it fits better as attribute to the SUCCESS tag


---
I have set of UJ sub objects and another set of UI elements, and I need certain UJ elements to affect the state of the UI elements; I should add map towards each UJ element indicating the needed state of the UI elements. Example:
- for Constant DDI - `map = { 'value_field': {set: true, show: true, default: ''}, 'selector_field': {set: false, show: false, default: ''}, ...}`
- for List DDI - `map = { 'value_field': {set: false, show: false, default: ''}, 'selector_field': {set: true, show: true, default: 'First'}, ...}`
- ...
when the signal for update is called, each UI element will look at the map of the UJ object to determine what state to apply to it's self


---
I have 4 structures:
0. ST's native objects
1. XML objects
2. My UJ objects
3. UI objects
So far I have altered the MY UJ & XML objects in paralel to avoid the need of composing XML. Now that I'm using UI, I'll need save primitive that does not involve the XML objects.
I have to loose the XML objects, and generate the XML for the export from scratch.