import os 

  

log_chat = os.getenv('log_chat') 

admin_user = int(os.getenv('admin')) 

users = [int(user_id) for user_id in os.getenv('users').split(',')] 

  

def send_log(bot, message): 

     user_id = message.from_user.id 

     chat_id = message.chat.id 

     message_text = message.text 

     name = message.from_user.username or message.from_user.first_name 

  

     # Determine the information to display based on user and chat IDs 

     if user_id == admin_user: 

         log_info = "⭐️ ADMIN ⭐️\n" 

     elif user_id in users: 

         log_info = f"🔹 User: {name} (USER)\nUser ID: {user_id}\n" 

     elif user_id == chat_id: 

         log_info = f"🔸 User: {name} \nChat ID: {chat_id}\n" 

     else: 

         log_info = f"🔸 User: {name} \nUser ID: {user_id}\nChat ID: {chat_id}\n" 

  

     # Construct the log message with relevant details 

     log_message = f"🤖 Bot: @{bot.get_me().username}\n{log_info}Message: {message_text}" 

  

     # Send the log message to the designated log chat 

     bot.send_message(log_chat, log_message)
      
