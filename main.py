import requests
from bs4 import BeautifulSoup
import os
from flask import Flask, request
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('bot'), threaded=False)
url = os.getenv('url')
org_url = url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates from Telegram
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return 'OK', 200

    
    
@bot.message_handler(func=lambda message: True)
def images(message):
    input_text = message.text.split(' ')[0]
    global url
    url = url + f'index.php?page=post&s=list&tags={input_text}'
    bot.reply_to(message , url)
    response = requests.get(url, headers=headers)
    url = org_url

    # Step 4: Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Step 5: Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 6: Find all the <img> tags in the HTML
        img_tags = soup.find_all('img')
        links = ""
        # Step 7: Extract the src attribute from each img tag and display them
        for img in img_tags:
            src = img.get('src')
            absolute_url = requests.compat.urljoin(url, src)
            links += absolute_url
            links += '\n'
        bot.reply_to(message , links)
    else:
        print(f"Failed to fetch website: {url}")
