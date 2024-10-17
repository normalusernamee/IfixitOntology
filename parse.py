import json
from owlready2 import *
import glob


# Load the modified ontology
onto = get_ontology("file:///Users/wissam/Dheya/KnowledgeRep/cars_trucks_ontology.owl").load()






# Function to parse Ancestors and extract make and model
def extract_make_model(ancestors):
    if len(ancestors) >= 4:
        # Example: ["Dodge Caravan", "Dodge", "Car and Truck", "Root"]
        model = ancestors[0]
        make = ancestors[1]
    elif len(ancestors) == 3:
        # Example: ["Chevrolet", "Car and Truck", "Root"]
        model = "NA"
        make = ancestors[0]
    elif len(ancestors) == 2:
        # Example: ["Car and Truck", "Root"]
        model = "NA"
        make = "NA"
    else:
        # Handle unexpected cases
        print("Error: Ancestors list has unexpected format.")
        model, make = "NA", "NA"
    
    return make, model

c1 = 0
c2 = 0
c3 = 0

# Function to parse a single entry in the JSON file
def parse_json_entry(guide):
    global c1, c2, c3
    # Check if the procedure is for an auto part
    if "Auto Part" in guide['Ancestors'] or guide['Category'] == "Auto Part":
        c2+=1
        #print("Parsing Auto Part procedure")
        parse_auto_part_procedure(guide)
    elif "Auto Accessory" in guide['Ancestors'] or "Car Audio" in guide['Ancestors']:
        c3+=1
        #print("Parsing Auto Accessory procedure")
        parse_auto_accessory_procedure(guide)
    else:
        c1+=1
        #print("Parsing Car and Truck procedure")
        parse_car_truck_procedure(guide)

# Parsing for car and truck procedure
def parse_car_truck_procedure(guide_data):
    with onto:
        # Create Procedure instance
        procedure_instance = onto.Procedure(f"Procedure_{guide_data['Guidid']}")
        procedure_instance.has_guideID.append(str(guide_data['Guidid']))  # Use append() method
        procedure_instance.guideTitle.append(guide_data['Title'])  # Use append() method

        # Extract make and model from Ancestors
        make, model = extract_make_model(guide_data['Ancestors'])

        # Create Procedure instance
        procedure_instance = onto.Procedure(f"Procedure_{guide_data['Guidid']}")
        procedure_instance.has_guideID.append(str(guide_data['Guidid']))  # Use append() method
        procedure_instance.guideTitle.append(guide_data['Title'])  # Use append() method

                # Create Make and Model instances or skip them if "NA"
        if make != "NA":
            make_instance = onto.Make(make.replace(" ", "_"))
            procedure_instance.has_make.append(make_instance)  # Use append() method
        
        if model != "NA":
            model_instance = onto.Model(model.replace(" ", "_"))
            procedure_instance.has_model.append(model_instance)  # Use append() method
            
            
            
            # Create Item instance from Category
        category_instance = onto.Item(guide_data['Category'].replace(" ", "_"))
        procedure_instance.has_Item.append(category_instance)  # Link Item to Procedure
        
         # Link Item to Procedure using hasProcedure
        procedure_instance.ProcedureForThis.append(category_instance)  # Use append() method


        # Add tools to the ontology
        for tool_data in guide_data.get('Toolbox', []):
            tool_name = tool_data['Name'].replace(" ", "_")
            

    
            tool_instance = onto.Tool(tool_name)  # Use existing instance if it already exists

            procedure_instance.requires_tool.append(tool_instance) # add tool to procedure's toolbox


                # Only append the URL if it's not None
            url = tool_data.get('Url')
            if url is not None:
                tool_instance.toolURL.append(url)

            # If there's a thumbnail image, create ToolImage instance
            if tool_data.get('Thumbnail'):
                tool_image_instance = onto.ToolImage(f"ToolImage_{tool_name}")
                tool_image_instance.toolImageURL.append(tool_data['Thumbnail'])  # Use append() method
                tool_instance.has_image.append(tool_image_instance)  # Use append() method

        # Create Step instances and link them to the procedure
        for step_data in guide_data.get('Steps', []):
            step_instance = onto.Step(f"Step_{step_data['StepId']}")
            step_instance.stepOrder.append(step_data['Order'])  # Use append() method

            # Directly use the Text_raw field for the step description
            step_text = step_data.get('Text_raw', "No description provided.")
            step_instance.stepText.append(step_text)  # Use append() method

            # Add images to the steps
            for image_url in step_data.get('Images', []):
                step_image_instance = onto.StepImage(f"StepImage_{step_data['StepId']}")
                step_image_instance.toolImageURL.append(image_url)  # Use append() method
                step_instance.has_image_for_step.append(step_image_instance)  # Use append() method

            # Link required tools for the step
            for tool_name in step_data.get('Tools_extracted', []):
                # Skip tools that are labeled "NA"
                if tool_name == "NA":
                    continue
                tool_instance = onto.Tool(tool_name.replace(" ", "_"))  # Create or reference existing
                step_instance.requiresTool.append(tool_instance)  # Use append() method

            # Link each Step instance to the Procedure
            procedure_instance.has_step.append(step_instance)  # Use append() method

# Parsing for auto part procedure
def parse_auto_part_procedure(guide_data):
    with onto:
        # Create Procedure instance for auto part
        procedure_instance = onto.Procedure(f"Procedure_{guide_data['Guidid']}")
        procedure_instance.has_guideID.append(str(guide_data['Guidid']))  # Use append() method
        procedure_instance.guideTitle.append(guide_data['Title'])  # Use append() method
        
                    # Create Item instance from Category
        category_instance = onto.Item(guide_data['Category'].replace(" ", "_"))
        procedure_instance.has_Item.append(category_instance)  # Link Item to Procedure
        
                 # Link Item to Procedure using hasProcedure
        procedure_instance.ProcedureForThis.append(category_instance)  # Use append() method


        # Add tools to the ontology
        for tool_data in guide_data.get('Toolbox', []):
            tool_name = tool_data['Name'].replace(" ", "_")

    
            tool_instance = onto.Tool(tool_name)  # Use existing instance if it already exists

            procedure_instance.requires_tool.append(tool_instance) # add tool to procedure's toolbox

                            # Only append the URL if it's not None
            url = tool_data.get('Url')
            if url is not None:
                tool_instance.toolURL.append(url)

            # If there's a thumbnail image, create ToolImage instance
            if tool_data.get('Thumbnail'):
                tool_image_instance = onto.ToolImage(f"ToolImage_{tool_name}")
                tool_image_instance.toolImageURL.append(tool_data['Thumbnail'])  # Use append() method
                tool_instance.has_image.append(tool_image_instance)  # Use append() method

        # Create Step instances and link them to the procedure
        for step_data in guide_data.get('Steps', []):
            step_instance = onto.Step(f"Step_{step_data['StepId']}")
            step_instance.stepOrder.append(step_data['Order'])  # Use append() method

            # Directly use the Text_raw field for the step description
            step_text = step_data.get('Text_raw', "No description provided.")
            step_instance.stepText.append(step_text)  # Use append() method

            # Add images to the steps
            for image_url in step_data.get('Images', []):
                step_image_instance = onto.StepImage(f"StepImage_{step_data['StepId']}")
                step_image_instance.toolImageURL.append(image_url)  # Use append() method
                step_instance.has_image_for_step.append(step_image_instance)  # Use append() method

            # Link required tools for the step
            for tool_name in step_data.get('Tools_extracted', []):
                tool_instance = onto.Tool(tool_name.replace(" ", "_"))  # Create or reference existing
                                # Skip tools that are labeled "NA"
                if tool_name == "NA":
                    continue
                step_instance.requiresTool.append(tool_instance)  # Use append() method

            # Link each Step instance to the Procedure
            procedure_instance.has_step.append(step_instance)  # Use append() method
            
            
            # Parsing for auto accessory procedure
def parse_auto_accessory_procedure(guide_data):
    with onto:
        # Create Procedure instance
        procedure_instance = onto.Procedure(f"Procedure_{guide_data['Guidid']}")
        procedure_instance.has_guideID.append(str(guide_data['Guidid']))
        procedure_instance.guideTitle.append(guide_data['Title'])

        # Create Item instance from Category
        category_instance = onto.Item(guide_data['Category'].replace(" ", "_"))
        procedure_instance.has_Item.append(category_instance)
        
                 # Link Item to Procedure using hasProcedure
        procedure_instance.ProcedureForThis.append(category_instance)  # Use append() method


        # Add tools to the ontology
        for tool_data in guide_data.get('Toolbox', []):
            tool_name = tool_data['Name'].replace(" ", "_")
                # Skip tools that are labeled "NA"

    
            tool_instance = onto.Tool(tool_name)

            procedure_instance.requires_tool.append(tool_instance) # add tool to procedure's toolbox
            
                # Only append the URL if it's not None
            url = tool_data.get('Url')
            if url is not None:
                tool_instance.toolURL.append(url)

            if tool_data.get('Thumbnail'):
                tool_image_instance = onto.ToolImage(f"ToolImage_{tool_name}")
                tool_image_instance.toolImageURL.append(tool_data['Thumbnail'])
                tool_instance.has_image.append(tool_image_instance)

        # Create Step instances and link them to the procedure
        for step_data in guide_data.get('Steps', []):
            step_instance = onto.Step(f"Step_{step_data['StepId']}")
            step_instance.stepOrder.append(step_data['Order'])

            # Directly use the Text_raw field for the step
            step_instance.stepText.append(step_data['Text_raw'])

            # Link images to the step
            for image_url in step_data.get('Images', []):
                image_instance = onto.StepImage(f"StepImage_{step_data['StepId']}_{image_url.split('/')[-1]}")
                image_instance.toolImageURL.append(image_url)
                step_instance.has_image.append(image_instance)


# Link required tools for the step
            for tool_name in step_data.get('Tools_extracted', []):
                tool_instance = onto.Tool(tool_name.replace(" ", "_"))  # Create or reference existing
                                # Skip tools that are labeled "NA"
                if tool_name == "NA":
                    continue
                step_instance.requiresTool.append(tool_instance)  # Use append() method

            # Link each Step instance to the Procedure
            procedure_instance.has_step.append(step_instance)  # Use append() method
            
                    

        
      
# Load the JSON files and process each one
json_files = glob.glob("TestData/*.json")

for json_file in json_files:
    try:
        with open(json_file, 'r') as file:
            #print(f"Processing file: {json_file}")
            guide_data = json.load(file)
            parse_json_entry(guide_data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error processing {json_file}: {e}")

# Save the updated ontology
onto.save(file="updated_cars_trucks_ontology.owl", format="rdfxml")  
        
        
print(c1, c2, c3)
print(len(json_files))