# Chat with ERP Database LLM
## Overview
Chat with ERP Database LLM is a Python-based application that combines the power of natural language processing with SQL query generation to provide seamless access to data from an ERP system. Users can ask data-related questions in plain English, and the app intelligently generates SQL queries to retrieve the required information from a Microsoft SQL Server database. The results are then processed into human-readable natural language responses for effortless understanding.

This app leverages LangChain and LLama 3.1 LLM (via Groq API) for natural language query generation and explanation. It also provides a user-friendly interface built using Streamlit.

## Features
Natural Language to SQL Query Generation: Ask questions in plain English, and the app generates the corresponding SQL query.
Real-time Data Retrieval: Executes the generated SQL query on an in-house Microsoft SQL Server data warehouse and fetches results.
Human-Readable Summaries: Converts raw query results into insightful natural language responses.
Interactive Frontend: A sleek and simple Streamlit interface for user interaction.
Dynamic Schema Handling: Automatically adapts to the schema of the queried database tables.
## How It Works
1) **User Input:** The user inputs a question (e.g., "Who is our top customer with the highest sales in each production country?").
2) **Schema Parsing:** The app retrieves the schema of the specified table from the database.
3) **Query Generation:** The LLM generates an optimized SQL query based on the question and schema.
4) **Query Execution:** The SQL query is executed on the data warehouse, and the results are fetched.
5) **Response Generation:** The LLM processes the results and generates a concise natural language summary.
6) **Results Display:** The app displays both the raw query results (in tabular format) and the natural language response.
## Tech Stack
- Python
  - LangChain: For LLM-based query generation and natural language response.
  - LLama 3.1 (via Groq API): A state-of-the-art language model for NLP tasks.
  - pyodbc: For connecting to the MS SQL Server database.
  - Streamlit: For building the interactive user interface.
  - Pandas: For processing and displaying query results in tabular form.
  - Database: Microsoft SQL Server.
## Installation
1)  Clone the Repository:


```
git clone https://github.com/MHameez/chat_with_erp_db_llm.git
cd chat_with_erp_db_llm
```
2)  Set Up a Virtual Environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3)  Install Dependencies:
```
pip install -r requirements.txt
```

4)  Set Up Environment Variables:
Create a .env file in the resources/ directory with the following keys:
```
GROQ_API_KEY=your_groq_api_key
DATAWAREHOUSE_SERVER=your_sql_server_address
```

5)  Run the App:
```
streamlit run app/main.py
```

# User Interface:
![image](https://github.com/user-attachments/assets/42a9b13d-9188-475d-9f26-bf23e1bb178f)



## Directory Structure
```
chat_with_erp_db_llm/
│
├── app/
│   ├── assets/               # Static assets like the logo
│   │   └── logo.png
│   ├── main.py               # Main Streamlit app
│   ├── chains.py             # LLM and LangChain logic
│   ├── db_connections.py     # Database connection and query execution logic
│   └── utils.py              # Utility functions (optional)
│   ├── .env                  # Environment variables
│
├── resources/
├── experiments/              # Optional: Experiments and scripts for testing
|   | └── chat_experiment.ipynb
├── requirements.txt          # Python dependencies
├── README.md                 # Project description
└── .gitignore                # Ignored files
```

## License
This project is open source and available under the MIT License.
