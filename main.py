import requests
from bs4 import BeautifulSoup
import os
from flask import Flask, request
import telebot
import time

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('bot'), threaded=False)
url = os.getenv('url')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

message_ids = []  # List to store message IDs

@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates from Telegram
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return 'OK', 200

@bot.message_handler(func=lambda message: True)
def images(message):
    input_text = message.text.replace(' ', '_')

    local_url = url + f'index.php?page=post&s=list&tags={input_text}'
    response = requests.get(local_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = ""
        counter = 10

        a_tags = soup.find_all('a')

        for a in a_tags:
            href = a.get('href')
            if 's=view' in href:
                absolute_url = requests.compat.urljoin(url, href)
                links += absolute_url
                links += '\n'
                counter -= 1
            if counter == 0:
                break

        if links != "":
            images = get_image_urls(links)
            if len(images) != 0:
                send_images(message.chat.id, images)
            else:
                bot.reply_to(message, "No results")
        else:
            bot.reply_to(message, "No results")
    else:
        bot.reply_to(message, "Failed to fetch website")

    schedule_message_deletion()

    
def get_image_urls(links):
    images = []
    for i in links.splitlines():
        img_response = requests.get(i, headers=headers)
        if img_response.status_code == 200:
            img_soup = BeautifulSoup(img_response.text, 'html.parser')
            img_tags = img_soup.find_all('img', id='image')
            for img in img_tags:
                img_src = img['src'].split('?', 1)[0]
                images.append(img_src)
    return images


def send_images(chat_id, images):
    for img_url in images:
        sent_message = bot.send_photo(chat_id, img_url)
        message_ids.append(sent_message.message_id)

        
def schedule_message_deletion():
    time.sleep(10)
    for message_id in message_ids:
        bot.delete_message(message.chat.id, message_id)
    message_ids.clear()
