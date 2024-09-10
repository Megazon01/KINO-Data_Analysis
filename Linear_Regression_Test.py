
import matplotlib.pyplot as plt
from scipy import stats
import sqlite3
import pandas as pd


# Connect to the database
conn = sqlite3.connect('KINO_Data/kinodata.db')

cursor = conn.cursor()


# Fetch data from the table
cursor.execute("SELECT winning FROM kino")
rows = cursor.fetchall()

# Create a dataframe with the numbers and their occurrences
num = 1
df = pd.DataFrame([])
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
    New_row = pd.DataFrame({'Number': [num], 'Occurrences': [count_containing_num]})
    df = pd.concat([df, New_row], ignore_index=True)
    num = num + 1


# Sort DataFrame by occurrences
df = df.sort_values(by='Occurrences', ascending=True, ignore_index=True)


# Plot the sorted occurrences
sorted_occurrences = df['Occurrences']
plt.scatter(df.index, sorted_occurrences)
plt.xlabel("KINO Database Index (sorted by occurrences)")
plt.ylabel("Number of Occurrences")
plt.title("Occurrences of KINO Numbers in Asc Order")


# Fit a linear regression line
slope, intercept, r_value, p_value, std_err = stats.linregress(df.index, sorted_occurrences)


# Print results of the slope hypothesis test
print(f"Slope (gradient): {slope}")
print(f"p-value: {p_value}")
if p_value < 0.05:
    print("The slope is significantly different from zero, indicating a possible bias.")
else:
    print("The slope is not significantly different from zero, indicating no significant bias.")

# Plot the regression line
plt.plot(df.index, intercept + slope * df.index, 'r', label=f"Fit: y = {slope:.2f}x + {intercept:.2f}")
plt.legend()
plt.show()
