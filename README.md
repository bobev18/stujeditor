# stujeditor
ST UJ Editor

FEATURES
1. load from XML
2. replace DDI name - both in DDI definition and all references (although that is handled fine in the GUI)
3. copy, move, delete steps
4. copy, move, delete ddis
5. save to XML

TODO:
 1. recreate the object models
 2. understand the effect of :
 	... xmlns="http://www.reflective.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.reflective.com stschema.xsd" ...

 NOTES:
 http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

DESIGN DECISIONS:
Q: Knowledge amongst UJ<>STEP<>DDI:
  UJ know both Step and DDI classes/objects;
  I want to have method that pulls steps by referenced DDI.name, thus Step needs to know of DDI objects
  I want to have method that pulls DDIs by having themreferenced in step.name, thus DDI needs to know of Step objects
A: Only the UJ should know of DDI & Step objects. The desired search methods should be in the UJ class; Steps should expose only the references as strings, and pull_obj_by_name should be in the UJ level

Q: Making Changes:
  Loading the XML, I have two sets of objects - those provided bu ElementTree and those in my lib. When making updates to the data,
  I can try to simultaneously update both sets objects, then just export via ET
  or I can update only the my objects, and transfer the data to ET objects uppon exit
A: That will depend on the tool being created:
  If it's just UJ editor, the classes should be wrapper around the ET classes
  If this is something more than editor, the ET is just one side of the ptoject, and output may be via different channel (i.e. DB)
  Finally - make it a wrapper
