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
    input_text = message.text.split()[0]

    local_url = url + f'index.php?page=post&s=list&tags={input_text}'
    response = requests.get(local_url, headers=headers)

    # Step 4: Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Step 5: Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        links = ""
        counter = 0  # Counter variable for limiting the number of links

        # Step 5: Find all the <a> tags in the HTML
        a_tags = soup.find_all('a')

        # Step 6: Extract the href attribute from each <a> tag and display it
        for a in a_tags:
            href = a.get('href')
            if 's=view' in href:
                absolute_url = requests.compat.urljoin(url, href)
                links += absolute_url
                links += '\n'
                counter += 1  # Increment the counter
            if counter == 10:  # Break the loop when counter reaches 10
                break
        if links != "":
            bot.reply_to(message, links)
            images = []
            for i in links.splitlines():
                # Send a request to the absolute URL
                img_response = requests.get(i, headers=headers)
                if img_response.status_code == 200:
                    img_soup = BeautifulSoup(img_response.text, 'html.parser')

                    # Find all <img> tags with id="image"
                    img_tags = img_soup.find_all('img', id='image')
                    for img in img_tags:
                        # Remove the query string from the image URL
                        img_src = img['src'].split('?', 1)[0]

                        images.append(img_src)
            if len(images) != 0:
                for img_url in images:
                    sent_message = bot.send_photo(message.chat.id, img_url)
                    message_ids.append(sent_message.message_id)  # Store the message ID
            else:
                bot.reply_to(message, "No results")
        else:
            bot.reply_to(message, "No results")
    else:
        bot.reply_to(message, "Failed to fetch website")

    # Schedule the deletion of sent messages after 10 seconds
    time.sleep(10)
    for message_id in message_ids:
        bot.delete_message(message.chat.id, message_id)
    message_ids.clear()  # Clear the list of message IDs

