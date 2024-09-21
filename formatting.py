import json

# Define file paths
input_file = 'raw_data.json'
output_file = 'converted_data1.json'

# Load data from the input JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

# Transform the data
transformed_data = [
    {
        "Q": item["question"],
        "A": item["answer"]
    }
    for item in data
]

# Save the transformed data to the output JSON file
with open(output_file, 'w') as file:
    json.dump(transformed_data, file, indent=4)

print(f"Data has been transformed and saved to {output_file}")
