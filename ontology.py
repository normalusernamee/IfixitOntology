from owlready2 import *

# Create the ontology
onto = get_ontology("http://example.org/ifixit.owl")

with onto:
    # Define Classes
    class Procedure(Thing): 
        pass
    class Step(Thing): 
        pass
    class Tool(Thing): 
        pass
    class Item(Thing):  #physical object involved in the procedure
        pass
    class Part(Thing): 
        pass
    class Image(Thing): 
        pass
    
    class ToolImage(Image):
        pass
    
    class StepImage(Image):
        pass
    
    
    class Model(Thing): 
        pass
    
    class Make(Thing):
        pass
    
    
    
    
    

    # Define Properties
    
    
        # Tools used in a step of the procedure appear in the toolbox of the procedure
    
    class requiresTool(Step >> Tool, ObjectProperty):
        domain = [Step]
        range = [Tool]

    class isRequiredFor(Tool >> Step, ObjectProperty):        
        domain = [Tool]
        range = [Step]
        inverse_property = requiresTool
    
    
        # An item, with a subclass relation that is transitive, 
        # and a part-of relation that identifies when one item is a part of another item 
        
    class has_part(ObjectProperty):
        domain = [Item]
        range = [Item]
        transitive = True
    
    class part_of(ObjectProperty):
        domain = [Item]
        range = [Item]
        inverse_property = has_part
        
        # A sub-procedure of a procedure must be a procedure 
        # for the same item or a part of that item.
    
    class has_sub_procedure(Procedure >> Procedure, ObjectProperty):
        domain = [Procedure]
        range = [Procedure]

    class procedure_for(ObjectProperty):
        domain = [Procedure]
        range = [Item]


    #       Define Make-Model Relationshas_make: Links a Procedure to a Make.
    # has_model: Links a Procedure to a Model.
    # is_for_make: Inverse of has_make, linking a Make back to its associated Procedure.
    # is_for_model: Inverse of has_model, linking a Model back to its associated Procedure.
    # has_model_for_make: Links a Make to its associated Model.
    # is_model_of: Inverse of has_model_for_make, linking a Model back to its associated Make.
    

    class has_make(Procedure >> Make, ObjectProperty):
        domain = [Procedure]
        range = [Make]

    class has_model(Procedure >> Model, ObjectProperty):
        domain = [Procedure]
        range = [Model]

    class is_for_make(Make >> Procedure, ObjectProperty):
        domain = [Make]
        range = [Procedure]
        inverse_property = has_make

    class is_for_model(Model >> Procedure, ObjectProperty):
        domain = [Model]
        range = [Procedure]
        inverse_property = has_model


    class has_model_for_make(Make >> Model, ObjectProperty):
        domain = [Make]
        range = [Model]

    class is_model_of(Model >> Make, ObjectProperty):
        domain = [Model]
        range = [Make]
        inverse_property = has_model_for_make
        
        
        ##  Things have images
        
            # Link 'Item' to 'RepairGuide'
    class hasProcedure(Item >> Procedure, ObjectProperty):
        domain = [Item]
        range = [Procedure]
        
    class ProcedureForThis( Procedure >> Item, ObjectProperty):
        domain = [Procedure]
        range = [Item]
        inverse_property = hasProcedure
        
            # Create the has_Item Object Property
    class has_Item(ObjectProperty):
        domain = [Procedure]  # The domain is Procedure
        range = [Item]     # The range is Item
        
         # Link 'RepairGuide' to Item 
    class isRepairGuideFor(Procedure >> Item, ObjectProperty):
        domain = [Procedure]
        range = [Item]
        inverse_property = hasProcedure

    # Links a Step to Images that may illustrate it
    class has_image_for_step(Step >> StepImage, ObjectProperty):
        domain = [Step]
        range = [Image]
        
    # Links a Tool to its Images (e.g., thumbnails, detailed views)
    class has_image(Tool >> ToolImage, ObjectProperty):
        domain = [Tool]
        range = [Image]



    # Links a Procedure to its unique guide identifier
    class has_guideID(Procedure >> str, DataProperty):
        domain = [Procedure]
        range = [str]
        
    # Links a Procedure to its title
    class guideTitle(Procedure >> str, DataProperty):
        domain = [Procedure]
        range = [str]

    # Indicates the order of a Step within a Procedure
    class stepOrder(Step >> int, DataProperty):
        domain = [Step]
        range = [int]
        
    # Data property for tool URL
    class toolURL(Tool >> str, DataProperty):
        domain = [Tool]
        range = [str]

    # Data property for tool image URL
    class toolImageURL(ToolImage >> str, DataProperty):
        domain = [ToolImage]
        range = [str]

    # Add a new data property for step text
    class stepText(onto.Step >> str, DataProperty):
        pass


        # Define the new object property 'has_step'
    class has_step(Procedure >> Step, ObjectProperty):
        domain = [Procedure]
        range = [Step]

# Save the ontology to an OWL file
onto.save(file="cars_trucks_ontology.owl", format="rdfxml")


