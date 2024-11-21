import pandas as pd

def print_table(result):
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    # Convert the result into a pandas DataFrame
    df = pd.DataFrame(result["rows"], columns=result["columns"])

    # Print the table using pandas
    print("\nQuery Results in Table Format:")
    print(df)