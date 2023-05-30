import telebot
import requests

bot = telebot.TeleBot("6208754044:AAFqT-azBEgFLbwLOpa16FaS39BVXRpgMFQ")




# Start command handler
@bot.message_handler(commands=['start'])
def start_command(message):
    # Create inline keyboard markup
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    paste_url_button = telebot.types.InlineKeyboardButton(text="🔗 Paste URL", url="https://nekobin.com/")
    more_help_button = telebot.types.InlineKeyboardButton(text="⁉️ More Help", callback_data="more_help")

    # Add buttons to markup
    keyboard_markup.add(paste_url_button, more_help_button)

    # Send message with keyboard markup
    bot.send_message(
        chat_id=message.chat.id,
        text=f"*Hi there {message.from_user.first_name}, send me a message and I'll upload it to Nakobin.com for you.*\n\n*🤗 For Help - @NOOBX7 *",
        reply_markup=keyboard_markup,parse_mode="markdown"
    )

# Help command handler
@bot.callback_query_handler(func=lambda call: call.data == "more_help")
def more_help_callback(call):
    # Create inline keyboard markup
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    start_button = telebot.types.InlineKeyboardButton(text="↩ Return to Start", callback_data="start")

    # Add button to markup
    keyboard_markup.add(start_button)

    # Update message with new text and keyboard markup
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="To use this bot, simply send a text message with the content you want to upload to Nekobin.\n\nYou can also click the 'Paste URL' button to go to the Nekobin website and paste your text there.\n\nIf you encounter any issues, please contact the bot owner.",
        reply_markup=keyboard_markup
    )

# Return to Start command handler
@bot.callback_query_handler(func=lambda call: call.data == "start")
def return_to_start_callback(call):
    # Create inline keyboard markup
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    paste_url_button = telebot.types.InlineKeyboardButton(text="🔗 Paste URL", url="https://nekobin.com/")
    more_help_button = telebot.types.InlineKeyboardButton(text="⁉️ More Help", callback_data="more_help")

    # Add buttons to markup
    keyboard_markup.add(paste_url_button, more_help_button)

    # Update message with new text and keyboard markup
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"*Hi there {call.message.from_user.first_name}, send me a message and I'll upload it to Nakobin.com for you.*\n\n*🤗 Join - @NOOBX7 *",
        reply_markup=keyboard_markup,parse_mode="markdown"
    )


# Text message handler
@bot.message_handler(func=lambda message: True)
def upload_text(message):
    if message.text:
        content = message.text.strip()
        url = "https://nekobin.com/api/documents"
        response = requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            json={"content": content},
        ).json()

        try:
            if response.get("ok"):
                document_url = (
                    f"https://nekobin.com/{response.get('result').get('key')}"
                )
                web_app_url = (f"https://nekobin.com/{response.get('result').get('key')}")
                keyboard = telebot.types.InlineKeyboardMarkup()
                nekobin_link = telebot.types.InlineKeyboardButton('🗃 Open Document', url=web_app_url)
                admin_link = telebot.types.InlineKeyboardButton(text="☎️ Contact Us", url="https://t.me/NOOBX7")
                keyboard.row(nekobin_link, admin_link)
                bot.reply_to(
                    message,
                    f"*🗂 Your Text Uploaded At Nekobin.com*\n\n*🔗 Document Url -* {document_url}\n\n*© Credit - @NOOBX7 *",
                    parse_mode="markdown",
                    disable_web_page_preview=True,reply_markup=keyboard
                )

        except Exception as e:
            print(e)
            bot.reply_to(
                message, "*Failed to upload text at Nekobin.com*", parse_mode="markdown"
            )

    else:
        bot.reply_to(message, "Nekobin.com only supports text uploads")


# Handle non-text file uploads
@bot.message_handler(content_types=["document", "photo", "audio", "video"])
def handle_non_text_files(message):
    bot.reply_to(message, "Sorry, only text uploads are supported at this time.")


# Error handler
@bot.callback_query_handler(func=lambda call: True)
def error_callback(call):
    bot.send_message(chat_id=1493164653, text=f"An error occurred: {call}")


bot.polling()
