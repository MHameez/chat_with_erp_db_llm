import streamlit as st
from db_conections import DataWarehouse
from chains import Chain
import pandas as pd

# Initialize objects
dw = DataWarehouse()
chain = Chain()

# Display the company logo:
# st.logo(image="https://139682175.fs1.hubspotusercontent-eu1.net/hubfs/139682175/Documents%20and%20files/Logos%20247TS/Logo_blauw_RGB.png")
st.title("ChatDWH")

# Streamlit UI
user_query = st.text_input("Ask me a data question?:")
table_name = st.text_input("Table name from DSO:")

if st.button("Send"):
    try:
        # Step 1: Get schema
        schema = dw.get_table_schema(table_name)

        # Step 2: Generate SQL query
        sql_query = chain.generate_sql(user_query, schema, table_name)
        st.code(sql_query, language="sql")

        # Step 3: Execute SQL query
        query_results = dw.execute_query(sql_query)

        if "error" in query_results:
            st.error(query_results["error"])
        else:
            # Validate query results
            rows = query_results["rows"]
            columns = query_results["columns"]

            if not rows or not columns:
                st.warning("The query returned no results.")
            else:

                # Step 4: Generate natural language response
                natural_response = chain.natural_response(sql_query, query_results)
                # st.write("Natural Response:")
                st.write(natural_response)

                # Convert rows and columns to DataFrame
                df = pd.DataFrame(rows, columns=columns)
                st.write("Query Results:")
                st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
