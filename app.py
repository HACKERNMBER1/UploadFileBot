import telebot







from flask import Flask

from threading import Thread

link = "https://pastebinupload.herokuapp.com/"

server = Flask("WebHook!")

bot_token = "6225510807:AAFodB3Vci1icTbrA_anhMu0rr4TE8-VU4g"

api_dev_key = "67jIRrhbUPwdljzfeOZZKGQmy5635_xB"

api_paste_url = "https://pastebin.com/api/api_post.php"

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])

def start(message):

    bot.reply_to(message, "مرحبًا! يرجى إرسال الملف الذي ترغب في رفعه إلى Pastebin.")

@bot.message_handler(content_types=['document'])

def handle_document(message):

    document = message.document

    file_info = bot.get_file(document.file_id)

    file_path = file_info.file_path

    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

    response = requests.get(file_url)

    bot.reply_to(message, "يرجى إرسال عنوان  النص :")

    bot.register_next_step_handler(message, lambda name_message: process_paste_name(name_message, response.content))

def process_paste_name(message, file_content):

    paste_name = message.text

    api_paste_code = file_content.decode('utf-8')

    api_paste_name = paste_name

    api_paste_format = "python"

    data = {

        'api_dev_key': api_dev_key,

        'api_option': 'paste',

        'api_paste_code': api_paste_code,

        'api_paste_name': api_paste_name,

        'api_paste_format': api_paste_format

    }

    response = requests.post(api_paste_url, data=data)

    bot.reply_to(message, f"*تم رفع الملف إلى Pastebin.\n\nرابط الملف: *{response.text}",parse_mode="Markdown")

@server.route('/' + TOKEN, methods=['POST'])

def getMessage():

    json_string = request.get_data().decode('utf-8')

    update = telebot.types.Update.de_json(json_string)

    bot.process_new_updates([update])

    return "!", 200

@server.route("/")

def webhook():

    bot.remove_webhook()

    bot.set_webhook(url=link + TOKEN)

    return "!", 200

if __name__ == "__main__":

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

