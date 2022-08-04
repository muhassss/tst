import vk_api, quecnf as cnf, quecmd as cmd, json, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk = vk_api.VkApi(token=cnf.bot_token)
longpoll = VkBotLongPoll(vk, cnf.club_id)

queue = []
que_now_is = False

for event in longpoll.listen():
    # Callback-event for button
    if event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object['payload'][0]['type'] in cnf.CALLBACK_TYPES:
                payload = event.object.payload
                special = payload[1]
                payload = payload[0]
                from_id = event.object['user_id']
                # Test type of button
                if special['type'] == 'test':
                    cmd.send(peer_id, message='Sorry, now this not active func.')
                    continue

                # Prod button
                if special['type'] == 'que':
                    if que_now_is:
                        # If user in queue
                        if from_id in queue:
                            vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                        'user_id': event.object.user_id,
                                                                        'peer_id': event.object.peer_id,                                                   
                                                                        'event_data':json.dumps(cnf.in_que)})
                            continue
                        # Append user to queue
                        queue.append(from_id)
                        keyboard = VkKeyboard(**cnf.keyb_set)
                        keyboard.add_callback_button('Присоедениться!', color=VkKeyboardColor.POSITIVE, payload=[{'type': 'show_snackbar', 'text': "Вы заняли место в очереди!"}, {'type':'que'}])
                        vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                    'user_id': event.object.user_id,
                                                                    'peer_id': event.object.peer_id,                                                   
                                                                    'event_data':json.dumps(payload)})
                        if len(queue) < MXCNT:
                            last_id = vk.method('messages.edit', {'peer_id': event.obj.peer_id,
                                                        'message': f'👥 В очереди сейчас {len(queue)} из {MXCNT}',
                                                        'conversation_message_id': event.obj.conversation_message_id,
                                                        'keyboard': keyboard.get_keyboard()})
                            continue
                        random.shuffle(queue)
                        message = cmd.gen_que(queue)
                        cmd.send(peer_id, message=message, dis_ment=1)
                        keyboard = VkKeyboard(**cnf.keyb_set)
                        keyboard.add_callback_button('Я прошёл очередь.', color=VkKeyboardColor.SECONDARY, payload=[{'type': 'show_snackbar', 'text': "Вы заняли место в очереди!"}, {'type':'fin'}])
                        cmd.send(peer_id, message=f'@id{queue[0]}, Ваша очередь подошла!', keyboard=keyboard)
                        continue
                    # If queue not started
                    vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                    'user_id': event.object.user_id,
                                                                    'peer_id': event.object.peer_id,                                                   
                                                                    'event_data':json.dumps(cnf.no_que)})
                    continue
                # Prod button
                if special['type'] == 'fin':
                    if que_now_is:
                        # If not num user
                        if from_id != queue[0]:
                            vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                        'user_id': event.object.user_id,
                                                                        'peer_id': event.object.peer_id,                                                   
                                                                        'event_data':json.dumps(cnf.not_u_que)})
                            continue
                        # Del user from queue
                        queue.pop(0)
                        vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                        'user_id': event.object.user_id,
                                                                        'peer_id': event.object.peer_id,                                                   
                                                                        'event_data':json.dumps(cnf.u_que)})
                        # If queue end
                        if len(queue) == 0:
                            que_now_is = False
                            cmd.send(peer_id, message='Очередь закончилась!')
                            continue
                        # Else
                        message = cmd.gen_que(queue)
                        cmd.send(peer_id, message=message, dis_ment=1)
                        keyboard = VkKeyboard(**cnf.keyb_set)
                        keyboard.add_callback_button('Я прошёл очередь.', color=VkKeyboardColor.SECONDARY, payload=[{'type': 'show_snackbar', 'text': "Вы заняли место в очереди!"}, {'type':'fin'}])
                        cmd.send(peer_id, message=f'@id{queue[0]}, Ваша очередь подошла!', keyboard=keyboard)
                        continue
                    # If queue not started
                    vk.method('messages.sendMessageEventAnswer', {'event_id': event.object.event_id,
                                                                    'user_id': event.object.user_id,
                                                                    'peer_id': event.object.peer_id,                                                   
                                                                    'event_data':json.dumps(cnf.no_que)})
                    continue

    # Longpoll-event for message
    if event.type == VkBotEventType.MESSAGE_NEW:
        peer_id = event.message['peer_id']
        message = message = event.message['text'].lower()
        # From user for test
        if event.from_user:
            continue
        
        # From chat for production
        if event.from_chat:
            from_id = event.message['from_id']
            if message[0] in cnf.prefixes:
                message = message[1:].split()
                if from_id in cnf.white_list:
                    if message[0] == 'очередь' and len(message) > 1:
                        max_count = message[1]
                        try:
                            MXCNT = int(max_count)
                        except:
                            # If arg of cmd is дост
                            if max_count == 'дост':
                                MXCNT = len(queue)
                                max_count = MXCNT
                                # If queue end
                                if MXCNT == 0:
                                    cmd.send(peer_id, message='Очередь пустая. Набор прекращён.')
                                    continue
                                random.shuffle(queue)
                                message = cmd.gen_que(queue)
                                cmd.send(peer_id, message=message, dis_ment=1)
                                keyboard = VkKeyboard(**cnf.keyb_set)
                                keyboard.add_callback_button('Я прошёл очередь.', color=VkKeyboardColor.SECONDARY, payload=[{'type': 'show_snackbar', 'text': "Вы заняли место в очереди!"}, {'type':'fin'}])
                                cmd.send(peer_id, message=f'@id{queue[0]}, Ваша очередь подошла!', keyboard=keyboard)
                                continue
                            # Else
                            cmd.send(peer_id, message=f'⚠ @id{from_id}, 1-ый аргумент команды должен быть целым числом.')
                            continue
                        keyboard = VkKeyboard(**cnf.keyb_set)
                        keyboard.add_callback_button('Присоединиться!', color=VkKeyboardColor.POSITIVE, payload=[{'type': 'show_snackbar', 'text': "Вы заняли место в очереди!"}, {'type':'que'}])
                        cmd.send(peer_id, keyboard, f'✅ Создана очередь на {max_count} человек.\n👥 0/{max_count}')
                        que_now_is = True
                        continue
                    cmd.send(peer_id, message=f'⚠ @id{from_id}, Вы не указали аргумент команды.\n\nПример:\n/очередь 10')
                    continue
                cmd.send(peer_id, message='доступ имеют только администраторы, обратитесь к @imoon_shinei, @319914213, @mdanila254')
                continue
        
