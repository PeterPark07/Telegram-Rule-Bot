import requests

# Step 1: Get the URL from the user
url = os.getenv('url')

# Step 2: Send a request to the website and get the HTML content
response = requests.get(url)

for i in range 20:  
  # Step 3: Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Step 4: Print the content of the website
      print(response.text)
  else:
      print(f"Failed to fetch website: {url}")
