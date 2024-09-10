import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('KINO_Data/kinodata.db')

# Load data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM kino", conn)

# Print the DataFrame
print(df)

cursor = conn.cursor()


# Fetch data from the table
cursor.execute("SELECT winning FROM kino")
rows = cursor.fetchall()

# Perform a two tailed Z-test for each number
num = 1
fair_nums = 0
while num < 81:
    count_containing_num = 0

    # Process each row to extract numbers
    for row in rows:
        numbers_string = row[0]  # This gets the space-separated numbers
        number_list = numbers_string.split()  # Split by space
        number_list = [int(num) for num in number_list]  # Convert to integers
        # Check if the number 1 is in the list
        if num in number_list:
            count_containing_num += 1

    # Print the result
    # print(f"The number 1 appears in {count_containing_num} lists.")

    # Sample probability
    p = count_containing_num/51000

    # Z-Test statistic
    z = (p - 0.25)/((0.25*(1 - 0.25))/51000)**0.5
    print(f"{num}: Z = {z}")
    if -1.96 < z < 1.96:
        fair_nums = fair_nums + 1
        print(f"{num} is a fair number!")
    else:
        print(f"ERROR!!!")
    num = num + 1

print(f"Fair numbers = {fair_nums}")

# Close the connection
conn.close()
