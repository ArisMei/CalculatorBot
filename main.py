import os
import telebot
from dotenv import load_dotenv
from telebot import types
import requests
import random


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token de acceso del bot desde las variables de entorno
TOKEN = os.environ.get("TOKEN")
YOUR_USER_ID = int(os.environ.get("YOUR_USER_ID"))

sticker_ids = ["CAACAgIAAxkBAAEJR1lkhbhylT-AoicmnnPUOAv4fKVoVgACGwkAAhhC7gjcuaXV80quyC8E", 
               "CAACAgIAAxkBAAEJR1tkhbhzsh0oc61Qi1LA1bQTxYzuWQACGQkAAhhC7gjnA3EwBUHY7y8E",
                 "CAACAgIAAxkBAAEJR1xkhbhz0fQNP09mh4Tw3eLbnC5-EAACHgkAAhhC7gj5WNnuHSGcIS8E", 
                 "CAACAgIAAxkBAAEJR1ZkhbhwqibOGosIJ2NjKWYepp-7HgACGAkAAhhC7ggHge2pz_Yyay8E",
                 "CAACAgIAAxkBAAEJR1VkhbhwdqZApn7DjYPXL12Zdob4MQACMgkAAhhC7ggR-4x175jn2i8E",
                 "CAACAgIAAxkBAAEJR2FkhbkLEYb89Iz4nXEjw4RbeePLPAACIgkAAhhC7giwkQ5lZwxHoC8E",
                 "CAACAgIAAxkBAAEJR2NkhbkhkMdJGiYaGoxBXkwjJKQvLgACAQEAAladvQoivp8OuMLmNC8E",
                 "CAACAgIAAxkBAAEJR2VkhbkyeC5_9HlKBDTkNE_0qoDm7wAC9wADVp29CgtyJB1I9A0wLwQ",
                 "CAACAgIAAxkBAAEJR2dkhbmpyLeGlb4beSoUH-JaAcV2RQACSgIAAladvQrJasZoYBh68C8E",
                 "CAACAgIAAxkBAAEJR2lkhbnY8ZHHzEkcOagzziJzuLC4OwACryUAApuicEu4OcV9u14IZi8E",
                 "CAACAgIAAxkBAAEJR2tkhbnqkBXdUjjoQ1TzsOZeRyWGmwAC9gADVp29CvfbTiFAPqWKLwQ",
                 "CAACAgIAAxkBAAEJR25khbn-D1JFMg4Mntyoe-SmMp5nvwACTwIAAladvQrPysaJZ3VllS8E"]  # Add the sticker IDs you want to use


# Crear una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Diccionario para almacenar los parámetros de la conversación
conversation_params = {}

# Handler para el comando /start o al iniciar el bot
@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.from_user.id != YOUR_USER_ID:
        print("Unauthorized user. Exiting program.")
        exit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    calculate_button = types.KeyboardButton("CALCULATE")
    markup.add(calculate_button)

    random_sticker_id = random.choice(sticker_ids)
    bot.send_sticker(message.chat.id, random_sticker_id, reply_markup=markup)
    bot.reply_to(message, "¡Hola! Puedes iniciar la conversación con el bot utilizando el botón CALCULATE.", reply_markup=markup)

# Handler para manejar el botón CALCULATE
@bot.message_handler(func=lambda message: message.text == "CALCULATE", content_types=['text'])
def calculate_button_handler(message):
    if message.from_user.id != YOUR_USER_ID:
        print("Unauthorized user. Exiting program.")
        exit()
    calculate_handler(message)

# Handler para el comando /calculate
@bot.message_handler(commands=['calculate'])
def calculate_handler(message):
    bot.reply_to(message, "Por favor, ingresa el primer número:")

    # Establecer el estado de la conversación
    bot.register_next_step_handler(message, process_first_number)

# Handler para procesar el primer número
def process_first_number(message):
    try:
        first_num = float(message.text)
        conversation_params['first_num'] = first_num
        bot.reply_to(message, "Por favor, ingresa el segundo número:")
        bot.register_next_step_handler(message, process_second_number)
    except ValueError:
        bot.reply_to(message, "El valor ingresado no es válido. Por favor, ingresa un número.")

# Handler para procesar el segundo número
def process_second_number(message):
    try:
        second_num = float(message.text)
        conversation_params['second_num'] = second_num
        bot.reply_to(message, "Por favor, selecciona el operador:")

        # Crear el teclado en línea con las opciones de operador
        markup = types.InlineKeyboardMarkup(row_width=2)
        add_button = types.InlineKeyboardButton("Add", callback_data='add')
        subtract_button = types.InlineKeyboardButton("Subtract", callback_data='subtract')
        multiply_button = types.InlineKeyboardButton("Multiply", callback_data='multiply')
        divide_button = types.InlineKeyboardButton("Divide", callback_data='divide')
        markup.add(add_button, subtract_button, multiply_button, divide_button)
        # Seleccionar solo una opción y mandar el mensaje al bot 


        bot.send_message(message.chat.id, "Selecciona una opción:", reply_markup=markup)
    except ValueError:
        bot.reply_to(message, "El valor ingresado no es válido. Por favor, ingresa un número.")

# Handler para procesar la selección del operador
# Handler para procesar el operador
@bot.callback_query_handler(func=lambda call: call.data in ['add', 'subtract', 'multiply', 'divide'])
def process_operator(call):
    operator = call.data
    message = call.message

    if operator in ['add', 'subtract', 'multiply', 'divide']:
        conversation_params['operator'] = operator

        # Realizar la llamada a la función lambda
        URL = os.environ.get("URL")
        url = URL + f"?first_num={int(conversation_params['first_num'])}&second_num={int(conversation_params['second_num'])}&operator={conversation_params['operator']}"
        try:
            response = requests.get(url)
            result = response.json()
            if response.status_code == 200:
                bot.send_message(message.chat.id, f"El resultado es: {result}")
                bot.send_message(message.chat.id, "Trabajo terminado, firmado:")
                bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJR3Zkhbo_zVOjLQ34S47pZSB0FaxrvAACfgEAAgeGFQeoscUZz8zsNS8E")
                bot.send_message(message.chat.id, "Aris_Mentta")
            else:
                bot.reply_to(message, "Ha ocurrido un error al ejecutar la función.")
        except ValueError:
            bot.reply_to(message, "Ha ocurrido un error al llamar a la API Gateway.")

        # Eliminar el teclado en línea después de seleccionar el operador
        bot.edit_message_reply_markup(message.chat.id, message.message_id)
    else:
        bot.reply_to(message, "Operador no válido. Por favor, ingresa uno de los siguientes: add, subtract, multiply, divide.")

# Ejecutar el bot
bot.polling()
