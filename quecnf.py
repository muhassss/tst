bot_token = 'vk1.a.9DZfRbF1IDPgmVOOdN51VlDzTlFT2M5q6yoNCsJ457TjhACHx1EjWCRhc5U-EGg6PpPcng1lONS6sfi1aFTo-4hbUQ1OvmaTFHwnTqkro0sS4al2a_EJQTZKy0uaORxed9iPNcLukeJ5AzKSviFd3DxwYoT4kUFdnh87ADSapQyTkNbgJLEQXrWX8Olu2CBb'
club_id = 206830280 # Тута айди группы. ЦИФРАМИ

keyb_set = dict(one_time=False, inline=True)
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
prefixes = ['/', '!', '?', '.']
popup_type = 'show_snackbar'

white_list = [81073015, 50507561, 181299293, 319914213]
in_que = {'type': 'show_snackbar', 'text': 'За Вами уже числится место в очереди'}
no_que = {'type': 'show_snackbar', 'text': 'Нет активной очереди'}
not_u_que = {'type': 'show_snackbar', 'text': 'Не Ваш черёд в очереди'}
u_que = {'type': 'show_snackbar', 'text': 'Вы прошли очередь'}
