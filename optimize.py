import json
import yaml
import spacy
import os

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# 🔍 Schema file path (Change this if needed)
SCHEMA_FILE_PATH = "/Users/vee/Documents/notebook-main/notebook/hackathon/new.json"

def load_schema(file_path):
    """Loads the database schema from a JSON or YAML file."""
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        return None
    
    print(f"🔍 Loading schema from: {file_path}")
    
    with open(file_path, "r") as file:
        try:
            if file_path.endswith(".json"):
                schema = json.load(file)
            elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                schema = yaml.safe_load(file)
            else:
                print("❌ Unsupported file format. Use JSON or YAML.")
                return None
        except Exception as e:
            print(f"❌ Error loading schema: {e}")
            return None

    print("✅ Schema Loaded Successfully!")
    return schema

def analyze_nl_query(query, schema):
    """Extracts relevant tables and columns from an NL query based on schema."""
    
    if not schema:
        print("❌ Error: Schema not loaded.")
        return None

    print(f"\n🔎 Analyzing Query: {query}")
    doc = nlp(query.lower())

    relevant_tables = set()
    relevant_columns = set()

    # Define keyword rules
    order_keywords = {"order", "purchase", "transaction"}
    customer_keywords = {"customer", "client", "buyer", "user"}
    date_keywords = {"date", "time", "last", "month"}

    # Explicit table mapping
    table_map = {
        "Orders": order_keywords | date_keywords,
        "Customers": customer_keywords
    }

    # Scan query words
    for word in doc:
        word_text = word.text.lower()

        # Check if word matches a table
        for table, keywords in table_map.items():
            if word_text in keywords:
                relevant_tables.add(table)

        # Check for column relevance
        for table in relevant_tables:
            for column in schema[table]["columns"]:
                column_name = column["name"].lower()
                if word_text in column_name or word_text in date_keywords:
                    relevant_columns.add(column["name"])

    # Ensure required columns are present
    if "Orders" in relevant_tables:
        relevant_columns.update(["OrderDate", "CustomerID", "OrderID"])

    extracted_info = {"tables": list(relevant_tables), "columns": list(relevant_columns)}
    print(f"✅ Extracted Info: {extracted_info}")

    return extracted_info

def filter_schema(schema, extracted_info):
    """Filters schema to keep only relevant tables and columns."""
    
    relevant_tables = extracted_info["tables"]
    relevant_columns = extracted_info["columns"]

    if not relevant_tables:
        print("❌ No relevant tables found.")
        return None

    print(f"\n🗂️ Filtering Schema: Keeping Tables {relevant_tables}")

    filtered_schema = {"tables": {}}
    for table in relevant_tables:
        if table in schema:
            filtered_schema["tables"][table] = {
                "columns": [col for col in schema[table]["columns"] if col["name"] in relevant_columns]
            }

    print("✅ Final Filtered Schema:")
    print(json.dumps(filtered_schema, indent=2))
    return filtered_schema

if __name__ == "__main__":
    # ✅ Load schema automatically from the specified path
    schema = load_schema(SCHEMA_FILE_PATH)

    if schema:
        # ✅ Example NL Query
        query = "Find all orders placed by customers last month."

        extracted_info = analyze_nl_query(query, schema)

        if extracted_info:
            filter_schema(schema, extracted_info)
