import os
from telegraph import Telegraph
from datetime import datetime

bot_name = '@TheRule34_bot'
telegraph = Telegraph(os.getenv('telegraph_token'))
path = os.getenv('telegraph_path')

def logg(new_content):
    page = telegraph.get_page(path=path,return_content=True,return_html=True)
    title, content = page['title'], page['content']
    content = new_content + content
    telegraph.edit_page(path=path,title=title,html_content=content,author_name='bots')
    return


def log(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_text = message.text
    name = message.from_user.username or message.from_user.first_name

    # Determine the information to display based on user and chat IDs
    if user_id == chat_id:
        log_info = f"🔸 User: {name}   Chat ID: {chat_id}  "
    else:
        log_info = f"🔸 User: {name}   User ID: {user_id}, Chat ID: {chat_id}  "
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construct the log message with relevant details
    log_message = f"{bot_name} {current_time} {log_info}Text: {message_text}"
    log_message = f"<p>{log_message}</p>"
    logg(log_message)