import requests

api="319d91fe628a441ea07aa08dbb41c5b7"
url = ("https://newsapi.org/v2/everything?q"
       "=tesla&from=2024-04-05&sortBy=publish"
       "edAt&apiKey=319d91fe628a441ea07aa08dbb41c5b7")

# Def Request
request = requests.get(url)

# Make Request for a dictionary
content = request.json()

# The "articles" entry is a list of dictionaries, so for every item in the list we only print the title
for article in content["articles"]:
       print(article["title"])
       print(article["description"])

