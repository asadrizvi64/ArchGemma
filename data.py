import json

def convert_to_json(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables
    data = []
    question = None

    # Process each line
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            if question is not None:  # Save the previous question and answer
                data.append(question)
            question = {"Q": line[2:].strip(), "A": ""}
        elif line.startswith('A:') and question is not None:
            question["A"] = line[2:].strip()
    
    # Append the last question and answer
    if question is not None:
        data.append(question)
    
    # Write to the output JSON file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
  
# Usage
input_file = 'prompts.txt'  # Input text file
output_file = 'outputs.json'  # Output JSON file
convert_to_json(input_file, output_file)
