import requests
import os
# Step 1: Get the URL from the user
url = os.getenv('url')
# Step 2: Set the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Step 3: Send a request to the website and get the HTML content
response = requests.get(url, headers=headers)

for i in range(20):  
  # Step 3: Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Step 4: Print the content of the website
      print(response.text)
  else:
      print(f"Failed to fetch website: {url}")
