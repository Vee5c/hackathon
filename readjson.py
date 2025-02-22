import json

def load_schema(schema_file: str) -> dict:  # Use dict instead of Dict
    """Loads and parses the database schema from a JSON file."""
    try:
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)
        return schema_data
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_file}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{schema_file}'.")
        return {}

# Example usage:
schema_file = "new.json"  # Replace with the actual filename
schema = load_schema(schema_file)

if schema:
    print("Schema loaded successfully:")
    print(json.dumps(schema, indent=2))  # Print the loaded schema
