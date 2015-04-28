# stujeditor
ST UJ Editor

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
