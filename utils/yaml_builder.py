import json
import yaml
import os

# Function to read JSON from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to transform the 'depends_on' field
def transform_depends_on(depends_on):
    return [f"ref('{node.split('.')[-1]}')" for node in depends_on['nodes']]

# Function to process data with keys under 'exposures'
def process_data(data):
    yaml_data_list = []
    exposures = data.get("exposures", {})  # Access the 'exposures' key
    for key, item in exposures.items():
        transformed_item = {
            'name': item.get('name'),
            'label': item.get('package_name'),  # Adjust as needed
            'type': item.get('type', 'dashboard').capitalize(),
            'url': item.get('url'),
            'description': item.get('description').strip(),
            'depends_on': transform_depends_on(item.get('depends_on', {'nodes': []})),
            'owner': item.get('owner', {})
        }
        yaml_data_list.append(transformed_item)
    return yaml_data_list

def create_yaml_output(json_file_path):

    # Read JSON data from file
    json_data = read_json_file(json_file_path)

    # Construct the output YAML file path
    dir_path = os.path.dirname(json_file_path)
    output_file_path = os.path.join(dir_path, 'exposure.yml')
    
    # Process data
    processed_data = process_data(json_data)

    # Check if processed_data is empty
    if not processed_data:
        print("No data found under 'exposures' key.")
    else:
        # Convert to YAML
        yaml_data = yaml.dump(processed_data, sort_keys=False)

        # Write YAML data to file
        with open(output_file_path, 'w') as file:
            file.write(yaml_data)
