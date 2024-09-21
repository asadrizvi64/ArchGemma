import json

# Load and parse the raw data
with open("raw_data.json", "r") as file:
    try:
        raw_json = json.load(file)  # Directly load as JSON
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

# Print the type and content of the loaded JSON
print("Type of loaded JSON:", type(raw_json))
print("Length of loaded JSON:", len(raw_json))
print("First item preview:", raw_json[0] if raw_json else "No data")

# Initialize a list to store the converted data
converted_data = []

# Process each JSON string in the list
for json_string in raw_json:
    try:
        # Load the JSON string into a Python object
        json_data = json.loads(json_string)
        
        # Check if the loaded JSON is a list
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    # Append formatted data to the result list
                    converted_data.append({"Q": item.get("question", ""), "A": item.get("answer", "")})
        else:
            print("Loaded JSON is not a list. Skipping...")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON string: {e}")
        continue

# Save the cleaned and converted data into a new JSON file
with open("converted_data.json", "w") as file:
    json.dump(converted_data, file, indent=4)

print("Data successfully cleaned and saved to converted_data.json.")
