from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

from automation import Automation
from db.db import db_table_val, get_address, update_address
from main import bot, dp

load_dotenv()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!'
                                            f'\nЗа допомогою мене ти зможеш дізнатися, чи є світло у твоїй оселі!')


@dp.message_handler(commands=['save_address'])
async def saved_address(message: Message):
    if message.text == '/save_address':
        await bot.send_message(message.chat.id, f"Щоб зберегти адресу, введіть назву вулиці за такою формою: "
                                                f"\n/save_address <назва вулиці, номер вулиці>"
                                                f"\nНаприклад: /save_address вул. Кибальчича Миколи, 3/Б | /save_address вул. Макаренка, 4")
    else:
        try:

            user_id = message.from_user.id
            address = message.text[13:].strip()
            db_table_val(user_id=user_id, address=address)

            address_button = KeyboardButton(text=f'/svitlo {get_address(user_id=user_id)}')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(address_button)
            await bot.send_message(message.chat.id, f'Чудово!', reply_markup=keyboard)
        except Exception:
            await bot.send_message(message.chat.id,
                                   f'Якщо ви хочете змінити збережену адресу, оберіть команду /update_address')


@dp.message_handler(commands=['update_address'])
async def updated_address(message: Message):
    if message.text == '/update_address':
        await bot.send_message(message.chat.id, f"Щоб змінити збережену адресу, введіть назву вулиці за такою формою: "
                                                f"\n/update_address <назва вулиці, номер вулиці>"
                                                f"\nНаприклад: /update_address вул. Кибальчича Миколи, 3/Б | /update_address вул. Макаренка, 4")
    else:
        user_id = message.from_user.id
        address_upd = message.text[15:].strip()
        update_address(user_id=user_id, updated_address=address_upd)
        if get_address(user_id=user_id) is None:
            await bot.send_message(message.chat.id, f'Щоб зберегти адресу, оберіть команду /save_address')
        else:
            address_button = KeyboardButton(text=f'/svitlo {get_address(user_id=user_id)}')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(address_button)
            await bot.send_message(message.chat.id, f'Чудово!', reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help_dev(message: Message):
    await bot.send_message(message.chat.id, f'/start - Запустити бота\n'
                                            f'\n/svitlo - перевірити наявність світла\n'
                                            f'\n/save_address - зберегти адресу(перед збереженням, переконайтесь у правильності написання адреси)\n'
                                            f'\n/update_address - оновити збережену адресу(перед оновленням, переконайтесь у правильності написання адреси)\n'
                                            f'\n{"-" * 20}'
                                            f'\nЯкщо ви не можете знайти свою вулицю, перевірте її написання у https://www.dtek-kem.com.ua/ua/shutdowns'
                                            f'\n{"-" * 20}'
                                            f'\nЗа усіма пропозиціями щодо проєкту або співробітництва писати @ebduxi'
                                            f'\n{"-" * 20}'
                                            f'\n\u2615Buy me a coffee: buymeacoffee.com/shaxeno',
                           parse_mode='html', disable_web_page_preview=True)


@dp.message_handler(commands=['svitlo'])
async def ye_svitlo(message: Message):
    global number_index
    if message.text == '/svitlo':
        await bot.send_message(message.chat.id, f"Введіть назву своєї вулиці за такою формою: "
                                                f"\n/svitlo <назва вулиці, номер вулиці>"
                                                f"\nНаприклад: /svitlo вул. Кибальчича Миколи, 3/Б | /svitlo вул. Макаренка, 4")
    else:
        uid = message.chat.id
        text = message.text[7:]
        try:
            number_index = text.index(',')
        except ValueError:
            await bot.send_message(uid, 'Будь ласка, перевірте назву вулиці і правильність написання')
        await bot.send_message(uid, f"Будь ласка, зачекайте...")
        address_name = text[:number_index].strip()
        address_number = text[number_index + 1:].strip()
        aut = Automation(address_name, address_number)
        await bot.send_message(uid, aut.text())
        await bot.send_photo(uid, aut.image())
