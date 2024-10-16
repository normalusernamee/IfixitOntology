import os
import json

#ful_json_file = "/Users/dheya19/Documents/Uni/Y3S1/Knowledge representation/Project/c1.json"

ful_json_file = "c1.json"

# Ensure TestData directory exists
test_data_dir = "TestData"
os.makedirs(test_data_dir, exist_ok=True)

def get_guide_id(guide_data):
    return guide_data.get("GuideId")

with open (ful_json_file, 'r') as full_file:
    for id, line in enumerate(full_file):
        new_file_path = os.path.join(test_data_dir, f"line{id}.json")
        
        with open(new_file_path, 'w') as new_file:
            new_file.write(line)

print("JSON files created successfully.")

def format_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

vehicles_dir = "TestData"
for filename in os.listdir(vehicles_dir):
    if filename.endswith(".json"):
        format_json(os.path.join(vehicles_dir, filename))

print("JSON files formatted successfully.")