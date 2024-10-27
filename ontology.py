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
    class Item(Thing):  
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

    # Procedure has required tools (this will represent a procedure's toolbox)
    class requires_tool(Procedure >> Tool, ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    # Inverse of the above: Tool is used in procedures
    class used_in(Tool >> Procedure, ObjectProperty):
        domain = [Tool]
        range = [Procedure]
        inverse_property = requires_tool  # Inverse function

    
    # Tools used in a step of the procedure appear in the toolbox of the procedure
    
    class requiresTool(Step >> Tool, ObjectProperty):
        domain = [Step]
        range = [Tool]

    # inverse of the above
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
        transitive = True 
        symetric = False 


    class sub_procedure_for(ObjectProperty):
        domain = [Procedure]
        range = [Item]
        inverse_property = has_sub_procedure


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
        
    
            # Link 'Item' to 'RepairGuide'
    class hasProcedure(Item >> Procedure, ObjectProperty):
        domain = [Item]
        range = [Procedure]

            # inverse of the above
    class ProcedureForThis( Procedure >> Item, ObjectProperty):
        domain = [Procedure]
        range = [Item]
        inverse_property = hasProcedure
        
            # Create the has_Item Object Property
    class has_Item(ObjectProperty):
        domain = [Procedure]  
        range = [Item]     
        

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


    # Axioms

    # 1. A `Procedure` must have at least one `Step`
    Procedure.equivalent_to.append(Procedure & has_step.some(Step))

    # 2. Any Procedure that has at least one Step that requires a Tool must itself require that Tool
    Procedure.equivalent_to.append(Procedure & has_step.some(Step & requiresTool.some(Tool)) & requires_tool.some(Tool))


    # 3. A `Step` requiring a `Tool` must have that tool in the `Toolbox`
    Step.equivalent_to.append(Step & requiresTool.some(Tool) & isRequiredFor.some(requires_tool.some(Tool)))

    # 4. A sub-procedure of a Procedure must involve a part or the same item as the parent Procedure 
    Procedure.equivalent_to.append(Procedure & has_sub_procedure.some(Procedure & sub_procedure_for.some(Item & has_part.some(Item))))

    # 5. A Tool Must Be Used in At Least One Procedure
    Tool.equivalent_to.append(Tool & used_in.some(Procedure))

    #SWRl rules


    # Rule 1: If a Step Requires a Tool, That Tool Must Be in the Procedure's Toolbox
    rule1 = Imp()
    rule1.set_as_rule("""
    Step(?s), Procedure(?p), Tool(?t), has_step(?p, ?s), requiresTool(?s, ?t) -> requires_tool(?p, ?t)
    """)

    # Rule 2: If a Procedure Has a Sub-Procedure, Both Must Be for the Same Item or a Part of the Same Item
    rule3 = Imp()
    rule3.set_as_rule("""
    Procedure(?p1), Procedure(?p2), has_sub_procedure(?p1, ?p2), 
    sub_procedure_for(?p1, ?item1), sub_procedure_for(?p2, ?item2), part_of(?item2, ?item1) -> sub_procedure_for(?p2, ?item2)
    """)

    # Rule 3: If a Procedure Requires a Tool, That Tool Must Be Used in One of Its Steps
    rule4 = Imp()
    rule4.set_as_rule("""
    Procedure(?p), Tool(?t), requires_tool(?p, ?t) -> has_step(?p, ?s), requiresTool(?s, ?t)
    """)

    # Rule 4: If a Step Is Part of a Procedure, It Must Have a Step Order
    rule5 = Imp()
    rule5.set_as_rule("""
    Step(?s), Procedure(?p), has_step(?p, ?s) -> stepOrder(?s, ?o)
    """)

    sync_reasoner_pellet()


    # Save the ontology to an OWL file
onto.save(file="cars_trucks_ontology.owl", format="rdfxml")
print("ontology created successfuly")


