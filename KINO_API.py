import requests
import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame with selected KINO draws obtained using API
x = 1
draw_num = 1117799
df = pd.DataFrame({})
while x < 5:
    api = "319d91fe628a441ea07aa08dbb41c5b7"
    url = f"https://api.opap.gr/draws/v3.0/1100/{draw_num}"

# Def Request
    request = requests.get(url)

# Make Request for a dictionary
    content = request.json()

    winners_dict = content["winningNumbers"]
    winners_num = winners_dict['list']

    df[draw_num] = winners_num
    x = x+1
    draw_num = draw_num - 1

print(df)

# Count the occurrences of each number within the selected draws
flat_series = df.stack()
value_counts = flat_series.value_counts()
print(value_counts)
print(type(value_counts))

# Sample data
x = value_counts.index
y = value_counts.values

# Create a plot of occurrences against numbers
plt.figure(figsize=(8, 6))  # Optional: Set the figure size
plt.plot(x, y, marker='o', linestyle='', color='b')  # Line plot with markers
plt.title(f'Number Occurrences in {x} draws')
plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.grid(True)  # Optional: Add a grid
plt.show()  # Display the plot
