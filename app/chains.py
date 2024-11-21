import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.1-70b-versatile",
        )

    def generate_sql(self, user_query, schema, table_name):
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
        response = self.llm.invoke(prompt)
        match = re.search(r'```sql\n(.*?)\n```', response.content, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Failed to extract SQL query from LLM response.")

    def natural_response(self, sql_query, result):
        if "error" in result:
            return f"Error executing query: {result['error']}"

        columns = result["columns"]
        rows = result["rows"]

        data_preview = "\n".join(
            [" | ".join(columns)] + [" | ".join(map(str, row)) for row in rows[:5]]
        )

        prompt = (
            "You are an AI assistant that explains query results. Given the following SQL query:\n"
            f"### SQL QUERY ###\n{sql_query}\n\n"
            "And its results:\n"
            f"### RESULTS ###\n{data_preview}\n\n"
            "Provide a summary of these results."
        )
        response = self.llm.invoke(prompt)
        return response.content.strip()
