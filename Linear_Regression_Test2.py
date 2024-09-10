import matplotlib.pyplot as plt
from scipy import stats
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('KINO_Data/kinodata.db')

# Fetch data from the table
query = "SELECT winning FROM kino"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Split the space-separated numbers into individual rows
df['winning'] = df['winning'].str.split()
df = df.explode('winning').astype(int)

# Count occurrences of each number
occurrences = df['winning'].value_counts().sort_index()

# Create DataFrame for plotting
df_plot = pd.DataFrame({'Number': occurrences.index, 'Occurrences': occurrences.values})

# Sort DataFrame by occurrences
df_plot = df_plot.sort_values(by='Occurrences', ascending=True).reset_index(drop=True)

# Plot the sorted occurrences
plt.scatter(df_plot.index, df_plot['Occurrences'])
plt.xlabel("Index (sorted by occurrences)")
plt.ylabel("Number of Occurrences")
plt.title("Occurrences of KINO Numbers in Ascending Order")

# Fit a linear regression line
slope, intercept, r_value, p_value, std_err = stats.linregress(df_plot.index, df_plot['Occurrences'])


# Print results of the slope hypothesis test
print(f"Slope (gradient): {slope}")
print(f"p-value: {p_value}")
if p_value < 0.05:
    print("The slope is significantly different from zero, indicating a possible bias.")
else:
    print("The slope is not significantly different from zero, indicating bias")

# Plot the regression line
plt.plot(df_plot.index, intercept + slope * df_plot.index, 'r', label=f"Fit: y = {slope:.2f}x + {intercept:.2f}")
plt.legend()
plt.show()
