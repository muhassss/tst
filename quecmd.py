import quecnf as cnf, vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


vk = vk_api.VkApi(token=cnf.bot_token)

def send(peer_id: int, keyboard: VkKeyboard=None, message: str='', dis_ment: int=None):
    if keyboard == None:
        vk.method('messages.send', {'peer_id': peer_id,
                                'random_id': 0,
                                'message': message,
                                'disable_mentions': dis_ment})
    else:
        vk.method('messages.send', {'peer_id': peer_id,
                                    'random_id': 0,
                                    'message': message,
                                    'keyboard': keyboard.get_keyboard()})

def gen_que(queue: list):
    ans = 'Очередь:\n'
    for i in range(len(queue)):
        if queue[i] == 0:
            pass
        ans += f'{i+1}. @id{queue[i]}\n'
    return ans
    

