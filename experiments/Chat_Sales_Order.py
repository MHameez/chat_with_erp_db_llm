import pandas as pd
import re
from dotenv import load_dotenv
import os
import pyodbc

from langchain_groq import ChatGroq


load_dotenv()
# Load Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATAWAREHOUSE_SERVER = os.getenv("DATAWAREHOUSE_SERVER")

# Create LLM object to LLAMA 3.1
llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-70b-versatile",
)


def connect_to_db():
    # Connect to DSO Database in Data Warehouse
    return pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          f"Server={DATAWAREHOUSE_SERVER};"
                          "Database=TS.DSO;"
                          "Trusted_Connection=yes;")


def get_table_schema(table_name):
    # Gives back the Schema of the Table
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '""" + str(table_name) + """'
        """)
        schema = cursor.fetchall()

        # Return a dictionary
        schema_dict = {row[0]: row[1] for row in schema}
        return schema_dict
    finally:
        conn.close()


def generate_sql(user_query, schema, table_name):
    # Construct the prompt template for the LLM
    prompt = (
        'You are a MS SQL expert. Given the following table schema and column names:\n'
        '### SCHEMA (Column Name and Datatype)###\n'
        f'{schema}\n'
        f'in table: [TS.DSO].[dbo].{table_name}\n'
        'Generate a simple SQL query for this user request:\n'
        'NOTE: All the columns should be in square brackets and exact column names as in the schema.\n'
        '### USER REQUEST ###\n'
        f'{user_query}'
    )

    # Invoke the LLM with the prompt
    response = llm.invoke(prompt)

    # Extract only the SQL query using regex
    match = re.search(r'```sql\n(.*?)\n```', response.content, re.DOTALL)
    if match:
        sql_query = match.group(1).strip()
        return sql_query
    else:
        raise ValueError("Failed to extract SQL query from LLM response.")

    # Invoke the LLM with the prompt
    response = llm.invoke(prompt)
    return response.content.strip()  # Extract the generated SQL query


def execute_query(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Execute the cleaned SQL query
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]  # Column names
        rows = cursor.fetchall()  # Data rows
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


def print_table(result):
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    # Convert the result into a pandas DataFrame
    df = pd.DataFrame(result["rows"], columns=result["columns"])

    # Print the table using pandas
    print("\nQuery Results in Table Format:")
    print(df)


def natural_response(sql_query, result):
    if "error" in result:
        return f"Error executing query: {result['error']}"

    columns = result["columns"]
    rows = result["rows"]

    # Prepare a data preview (up to 5 rows for compactness)
    data_preview = "\n".join(
        [" | ".join(columns)] + [" | ".join(map(str, row)) for row in rows[:5]]
    )

    # Construct the prompt for Groq LLM
    prompt = (
        "You are an AI assistant that explains query results. Given the following SQL query:\n"
        f"### SQL QUERY ###\n{sql_query}\n\n"
        "And its results:\n"
        f"### RESULTS ###\n{data_preview}\n\n"
        "Provide a summary of these results."
    )

    # Send the prompt to Groq LLM
    response = llm.invoke(prompt)

    # Return the LLM's natural language response
    return response.content.strip()


# Fetch schema and generate SQL
table_name = "Order_Statistics_Demo"
user_query = "Who is our top customer with the highest sales in each Production Country?"

# Create Chain
# 1) Get Schema of the SQL Table
schema = get_table_schema(table_name)

# 2) Generate SQL Query using Llama for Table Schema based on User's Question
sql_query = generate_sql(user_query, schema, table_name)

# 3) Execute the Generated Query on Database
query_results = execute_query(sql_query)

# Generate and print natural language response of the Results from Database using LLama
natural_response_llm = natural_response(sql_query, query_results)

print("\nResponse:")
print(natural_response_llm)

print("\nGenerated SQL Query:")
print(sql_query)
