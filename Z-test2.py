import sqlite3
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('KINO_Data/kinodata.db')

# Load data into a pandas DataFrame
df = pd.read_sql_query("SELECT winning FROM kino", conn)

# Close the connection
conn.close()

# Process the DataFrame
# Split the 'winning' column into separate numbers and explode into individual rows
df['winning'] = df['winning'].str.split()  # Split space-separated numbers into lists
df_exploded = df.explode('winning')  # Explode lists into separate rows
df_exploded['winning'] = df_exploded['winning'].astype(int)  # Convert to integers

# Count occurrences of each number
occurrences = df_exploded['winning'].value_counts().sort_index()

# Perform a two-tailed Z-test for each number
expected_prob = 0.25  # Probability for a fair game
n_draws = len(df)  # Number of draws

# Calculate the expected occurrences for each number
expected_occurrences = expected_prob * n_draws

# List to store outliers
outliers = []

# Store z-scores in a dictionary
z_scores = {}

for num in range(1, 81):
    observed_count = occurrences.get(num, 0)
    observed_prob = observed_count / n_draws

    # Calculate the standard error
    standard_error = np.sqrt(expected_prob * (1 - expected_prob) / n_draws)

    # Calculate the Z-score
    z = (observed_prob - expected_prob) / standard_error
    z_scores[num] = z

    # Use scipy.stats for p-value calculation
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed test

    if p_value < 0.05:
        outliers.append(num)
        print(f'{num}: Outlier!!! Z = {z:.2f}, p-value = {p_value:.4f}')
    else:
        print(f'{num}: Fair number! Z = {z:.2f}, p-value = {p_value:.4f}')

# Output results
fair_nums = len(set(range(1, 81)) - set(outliers))
print(f'Fair numbers = {fair_nums}')
print(f'Outliers: {outliers}')

outliers_db = pd.DataFrame({'Number': occurrences.index, 'Winnings': occurrences.values})
outliers_db['Highlight'] = outliers_db['Number'].isin(outliers)

# Plotting
plt.figure(figsize=(10, 6))

# Plot points that should be highlighted
plt.scatter(outliers_db[outliers_db['Highlight']]['Number'],
            outliers_db[outliers_db['Highlight']]['Winnings'],
            color='red',
            label='Significant result suggesting bias')

# Plot points that should not be highlighted
plt.scatter(outliers_db[~outliers_db['Highlight']]['Number'],
            outliers_db[~outliers_db['Highlight']]['Winnings'],
            color='blue',
            label='Expected result')

plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.title('Occurrences of KINO Numbers over 51000 draws')
plt.legend()
plt.grid(False)
plt.show()
