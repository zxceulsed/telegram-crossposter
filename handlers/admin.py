# src/handlers/admin.py
from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from src.config import config
from src.states import ConnectionStates
from src.services.db import Database

router = Router()
db = Database()

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    if message.from_user.id in config.ADMINS:
        await message.answer("Привет, админ! Я бот, и я готов помочь!")
    else:
        await message.answer("Извините, команда доступна только администраторам.")

@router.message(Command(commands=['add_connection']))
async def add_connection(message: types.Message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        await message.answer("Введите ID группы Telegram для репостов:")
        await state.set_state(ConnectionStates.waiting_for_source_id)
    else:
        await message.answer("Извините, команда доступна только администраторам.")

@router.message(ConnectionStates.waiting_for_source_id)
async def process_source_id(message: types.Message, state: FSMContext):
    await state.update_data(source_id=message.text)
    await message.answer("Введите API ключ ВКонтакте целевой группы:")
    await state.set_state(ConnectionStates.waiting_for_vk_api_key)

@router.message(ConnectionStates.waiting_for_vk_api_key)
async def process_vk_api_key(message: types.Message, state: FSMContext):
    await state.update_data(vk_api_key=message.text)
    await message.answer("Введите ID группы ВКонтакте (с '-' перед номером):")
    await state.set_state(ConnectionStates.waiting_for_vk_group_id)

@router.message(ConnectionStates.waiting_for_vk_group_id)
async def process_vk_group_id(message: types.Message, state: FSMContext):
    await state.update_data(vk_group_id=message.text)
    await message.answer("Введите ACCESS TOKEN Одноклассников:")
    await state.set_state(ConnectionStates.waiting_for_ok_access_token)

@router.message(ConnectionStates.waiting_for_ok_access_token)
async def process_ok_access_token(message: types.Message, state: FSMContext):
    await state.update_data(ok_access_token=message.text)
    await message.answer("Введите GROUP ID Одноклассников:")
    await state.set_state(ConnectionStates.waiting_for_ok_group_id)

@router.message(ConnectionStates.waiting_for_ok_group_id)
async def process_ok_group_id(message: types.Message, state: FSMContext):
    await state.update_data(ok_group_id=message.text)
    await message.answer("Введите APPLICATION KEY Одноклассников:")
    await state.set_state(ConnectionStates.waiting_for_ok_app_key)

@router.message(ConnectionStates.waiting_for_ok_app_key)
async def process_ok_app_key(message: types.Message, state: FSMContext):
    await state.update_data(ok_app_key=message.text)
    await message.answer("Введите SESSION SECRET KEY Одноклассников:")
    await state.set_state(ConnectionStates.waiting_for_ok_session_key)

@router.message(ConnectionStates.waiting_for_ok_session_key)
async def process_ok_session_key(message: types.Message, state: FSMContext):
    await state.update_data(ok_session_key=message.text)
    await message.answer("Укажите задержку перед публикацией в часах (1–24):")
    await state.set_state(ConnectionStates.waiting_for_delay)

@router.message(ConnectionStates.waiting_for_delay)
async def process_delay(message: types.Message, state: FSMContext):
    try:
        delay = int(message.text)
        if not 1 <= delay <= 24:
            raise ValueError
        data = await state.get_data()
        data['delay'] = delay
        conn_id = db.add_connection(data)
        await message.answer(f"Связка #{conn_id} успешно создана.")
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 24.")
    finally:
        await state.clear()

@router.message(Command(commands=['show_connections']))
async def show_connections(message: types.Message):
    if message.from_user.id in config.ADMINS:
        connections = db.get_all()
        if connections:
            text = "Список связок:\n"
            for c in connections:
                text += f"ID: {c[0]}, Источник: {c[1]}, VK: {c[3]}, OK: {c[5]}, Задержка: {c[8]} ч.\n"
        else:
            text = "Связки не найдены."
        await message.answer(text)
    else:
        await message.answer("Извините, команда доступна только администраторам.")

@router.message(Command(commands=['delete_connection']))
async def delete_connection(message: types.Message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        await message.answer("Введите ID связки для удаления:")
        await state.set_state(ConnectionStates.waiting_for_delete_id)
    else:
        await message.answer("Извините, команда доступна только администраторам.")

@router.message(ConnectionStates.waiting_for_delete_id)
async def process_delete_connection(message: types.Message, state: FSMContext):
    try:
        conn_id = int(message.text)
        deleted = db.delete(conn_id)
        if deleted:
            await message.answer(f"Связка #{conn_id} удалена.")
        else:
            await message.answer(f"Связка #{conn_id} не найдена.")
    except ValueError:
        await message.answer("Введите корректный ID.")
    finally:
        await state.clear()
