import PIL.ImageEnhance
from PIL import Image
import telebot
from telebot import types
import os.path
import effects


TOKEN = "TOKEN" # сюда ваш токен


# проверка папок
if (os.path.exists("images/") == False):
    os.makedirs('images')
if (os.path.exists("cooldb/") == False):
    os.makedirs('cooldb')

bot = telebot.TeleBot(TOKEN)
print("Бот был запущен!")

def show_keyboard(): # клавиатура
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Яркость", "Резкость", "Констраст", "Насыщенность", "Повернуть на X", "Выйти", "День", "Ночь")
    return markup


@bot.message_handler(commands=['start']) # сообщение при старте
def send_welcome(message):
    bot.send_message(message.chat.id, "👋Привет! Это бот для изменения изображений. \n\n 🖼Для начала работы отправьте изображение! \n Для начала работы с другой фотографией, отправьте ее.")


def set_mode(message): # ожидание значения (после нажатия на клавиатуру)
    if str(message.text) in ["Яркость", "Резкость", "Констраст", "Насыщенность", "Повернуть на X"]: # основные эффекты
        if (os.path.exists(f"cooldb/{message.from_user.id}.txt")):
            os.remove(f"cooldb/{message.from_user.id}.txt")
        f = open(f"cooldb/{message.from_user.id}.txt", "w+") # сохраняем какой эффект будет использоватся
        f.write(message.text)
        f.close()
        msg = bot.send_message(message.chat.id, "Для выхода напишите любую букву\nНапишите значение:")
    elif str(message.text) in ["День", "Ночь"]: # пресеты
        imagef = Image.open(f"images/{message.from_user.id}.jpg")

        if (message.text == "День"):
            imagef1 = effects.brightness(imagef, 1.2)
            imagef1 = effects.contrast(imagef1, 1.2)
        elif (message.text == "Ночь"):
            imagef1 = effects.brightness(imagef, 0.4)
            imagef1 = effects.contrast(imagef1, 1.7)
            imagef1 = effects.color(imagef1, 1.2)

        imagef1.save(f"images/{message.from_user.id}.jpg")
        markup = show_keyboard()
        msg = bot.send_photo(message.chat.id, photo=open(f"images/{message.from_user.id}.jpg", 'rb'), reply_markup=markup)
        bot.register_next_step_handler(msg, set_mode)

    elif (str(message.text) == "Выйти"): # выход
        if (os.path.exists(f"images/{message.from_user.id}.jpg")):
            os.remove(f"images/{message.from_user.id}.jpg")
        if (os.path.exists(f"cooldb/{message.from_user.id}.txt")):
            os.remove(f"cooldb/{message.from_user.id}.txt")
        bot.send_message(message.chat.id, "Изображение удалено. Для редактирования изображения отправьте его!")
    else:
        markup = show_keyboard()
        msg = bot.send_message(message.chat.id, "Команда не найдена. Для выхода из режима редактирования нажмите кнопку выйти", reply_markup=markup)
        bot.register_next_step_handler(msg, set_mode)


@bot.message_handler(content_types=["text"])
def photo(message):  # применение изменений к фотографии
    if (os.path.exists(f"images/{message.from_user.id}.jpg") and os.path.exists(f"cooldb/{message.from_user.id}.txt")):
        f = open(f"cooldb/{message.from_user.id}.txt")
        imagef = Image.open(f"images/{message.from_user.id}.jpg")
        fd = f.readlines()
        try:
            if (fd[0] == "Яркость"):
                imagef1 = effects.brightness(imagef, float(message.text)/10)
            elif (fd[0] == "Резкость"):
                imagef1 = effects.sharpness(imagef, float(message.text)/10)
            elif (fd[0] == "Констраст"):
                imagef1 = effects.contrast(imagef, float(message.text)/10)
            elif (fd[0] =="Повернуть на X"):
                imagef1 = effects.rotate(imagef, float(message.text))
            elif (fd[0] == "Насыщенность"):
                imagef1 = effects.color(imagef, float(message.text)/10)

            imagef1.save(f"images/{message.from_user.id}.jpg")
            markup = show_keyboard()
            msg = bot.send_photo(message.chat.id, photo=open(f"images/{message.from_user.id}.jpg", 'rb'), reply_markup=markup)
            bot.register_next_step_handler(msg, set_mode)
            f.close()
            os.remove(f"cooldb/{message.from_user.id}.txt")
        except: # если введенный аргумент не число или какая-то билиберда
            if (os.path.exists(f"images/{message.from_user.id}.jpg")):
                markup = show_keyboard()
                msg = bot.send_message(message.chat.id, "Не удалось обработать аргумент! \nНапишите новый аргумент или отправьте новую фотографию.", reply_markup=markup)
                bot.register_next_step_handler(msg, set_mode)
            else:
                bot.send_message(message.chat.id, "Не удалось обработать аргумент! \n Для начала работы отправьте фотографию.")
    elif (os.path.exists(f"images/{message.from_user.id}.jpg") == False):
        bot.send_message(message.chat.id, "🖼Для начала работы отправьте изображение!")


@bot.message_handler(content_types=["photo"])  # сохранение фотки
def photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f"images/{message.from_user.id}.jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    markup = show_keyboard()
    msg = bot.send_message(message.chat.id, "Изображение сохранено! Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(msg, set_mode)


bot.polling()