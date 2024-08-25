import requests
import pandas as pd
import matplotlib.pyplot as plt
from pandas import value_counts

x = 1
draw_num = 1117898
df = pd.DataFrame({})
while x < 100:
    api="319d91fe628a441ea07aa08dbb41c5b7"
    url = (f"https://api.opap.gr/draws/v3.0/1100/{draw_num}")

# Def Request
    request = requests.get(url)

# Make Request for a dictionary
    content = request.json()

#print(content)

    winners_dict = content["winningNumbers"]
    winners_num = winners_dict['list']
#print(winners_dict)
#print(winners_num)

    df[draw_num] = winners_num


    x=x+1
    draw_num = draw_num - 1

print(df)

flat_series = df.stack()
value_counts = flat_series.value_counts()
print(value_counts)
print(type(value_counts))


# Sample data
x = value_counts.index
y = value_counts.values

# Create a plot
plt.figure(figsize=(8, 6))  # Optional: Set the figure size
plt.plot(x, y, marker='o', linestyle='', color='b')  # Line plot with markers
plt.title('Simple Line Plot')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.grid(True)  # Optional: Add a grid
plt.show()  # Display the plot


# The "articles" entry is a list of dictionaries, so for every item in the list we only print the title
#for article in content["articles"]:
#       print(article["title"])
#       print(article["description"])

