from aiogram.fsm.state import State, StatesGroup

class ConnectionStates(StatesGroup):
    waiting_for_source_id = State()           # ожидание ID источника Telegram
    waiting_for_vk_api_key = State()          # ожидание API-ключа ВКонтакте
    waiting_for_vk_group_id = State()         # ожидание ID группы ВКонтакте
    waiting_for_ok_access_token = State()     # ожидание ACCESS TOKEN Одноклассников
    waiting_for_ok_group_id = State()         # ожидание GROUP ID Одноклассников
    waiting_for_ok_app_key = State()          # ожидание APPLICATION KEY Одноклассников
    waiting_for_ok_session_key = State()      # ожидание SESSION SECRET KEY Одноклассников
    waiting_for_delay = State()               # ожидание задержки перед публикацией
    waiting_for_delete_id = State()           # ожидание ID записи для удаления

class ConnectionStates(StatesGroup):
    waiting_for_source_id = State()
    waiting_for_vk_api_key = State()
    waiting_for_vk_group_id = State()
    waiting_for_ok_access_token = State()
    waiting_for_ok_group_id = State()
    waiting_for_ok_app_key = State()
    waiting_for_ok_session_key = State()
    waiting_for_delay = State()
    waiting_for_delete_id = State()