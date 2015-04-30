# stujeditor
ST UJ Editor

FEATURES
- load from XML
- replace DDI name - both in DDI definition and all references (although that is handled fine in the GUI)
[- reset steps' order values (why?)]
- elevate stepgroups
- copy, move, delete steps
- create, copy, delete ddis
- save to XML

TODO:
 1. recreate the object models
 2. understand the effect of :
 	... xmlns="http://www.reflective.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.reflective.com stschema.xsd" ...
 3. add classes for post & flow_control

NOTES:
 - http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
 - The execution order is determined by the order of the steps in the XML, thus:
   = rename attribute 'order' to 'id' for my objects
   = utilize stepgroup referencing limitation:
     ~ stepgroup reference cannot be to id, that hasn't been encountered as a step id
     ~ stepgroup starts with selfreferencing step - the lead step
     ~ stepgroup closes upon encountering step that has reference other than the previous one

BUGS:


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

Q: Handle StepGroups
  The UJs deal with stepgroups as step property
  I want to have stepgroups as an object that contains the steps
  I can have the stepgroup class, to be able to lookup belonging steps, and still have a step property.
The question is, if I have class, stepgroup, should I have step references in the UJ class, or should the UJ class only see stepgroups.
A: Have the UJ see only stepgroups. Add stepgroup objects for orphan steps, but keep the step's stepgroup attribute as is. During export we can respect the step attribute to properly export orphan steps;
   Or we can export forcing orphaned steps into their own stepgroups - that should not affect experience in the ST GUI
PR: I cant create stepgroup objects before creating step objects

Q: How should I implement the interface for copy/delete/move steps?
   the tree structure is best for representing the stepgroups in steps
   I can have UJ class display all elements of the tree or
   I can have the UJ class show stepgroup elements, and stepgroup to return it's own subtree representation
A: try haing them separate, because otherwise UJ will need visibility of step objects

!: There are too many design issues that creep from the XML structure into the object structure. I should create an alternative, using my structures, and adjust the XML feed as needed once I get to that point.
?: Which components would I not overwite? Because these would be the ones to structure around:
  - XML
  - GUI
  - DB
  - Inj
  - MA
  - SAF
  - MaxPack
  - Recorder
  - Post Recording processing
  - LDAP/NTLM/etc integration
  To consider key features:
  = inj handles threads as browser
  = inj handles cookies as browser
  = MA has incorporated various communication templates/handshakes to access variety of sources
  = recorder (mostly) integrates


