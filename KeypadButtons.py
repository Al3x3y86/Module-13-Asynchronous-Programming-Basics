from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создаем класс состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calculate = KeyboardButton('Рассчитать')
btn_info = KeyboardButton('Информация')
keyboard.add(btn_calculate, btn_info)

@dp.message_handler(text=['/start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью. Нажмите на кнопку ниже, чтобы начать.',
                         reply_markup=keyboard)

@dp.message_handler(text=['Рассчитать'])
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()  # Переход к состоянию age

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Сохранение возраста
    await message.answer('Введите свой рост:')
    await UserState.growth.set()  # Переход к состоянию growth

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Сохранение роста
    await message.answer('Введите свой вес:')
    await UserState.weight.set()  # Переход к состоянию weight

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)  # Сохранение веса
    data = await state.get_data()  # Получение всех введенных данных

    # Рассчет калорий по упрощенной формуле
    age = int(data.get('age', 0))
    growth = int(data.get('growth', 0))
    weight = int(data.get('weight', 0))
    caloric_norm = 10 * weight + 6.25 * growth - (5 * age) + 5  # Формула для мужчин

    await message.answer(f'Ваша норма калорий: {caloric_norm}')

    # Завершение машины состояний
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
