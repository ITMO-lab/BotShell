# -*- coding: utf8 -*-

import random
import time
import requests
import vk_api
from vk_api.keyboard import *
from vk_api import *
from bs4 import BeautifulSoup
import io
import json

vk_session = vk_api.VkApi(token='30638db4b8b941601f6517c2b8a96f978ea79d38d1a06cc9cf5fd74a652ba52a94ffad2f9282ded13dffe')

"""
Эта функция нужна для эффективного получения фотографии из последнего сообщения.
@:returns <List> формата {'type': str, 'url': str, 'width': int, 'height': int} - отсортирован по возрастанию количества пикселей на изображении. 
Учтите, что формат изображения изменяется.
"""
def get_photo_list_from_event(event):
    photo_list = vk.messages.getById(message_ids=[event.message_id])['items'][0]['attachments'][0]['photo']['sizes']
    photo_list.sort(key=lambda photo: photo['width']*photo['height'])
    return photo_list


user_ids = [266304260, 252833211, 7108139, 579402838]

from vk_api.longpoll import *
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

from vk_api.upload import *
upload = VkUpload(vk_session)

message = "Бот запущен, уровень доступа scope={0}".format(VkApi(vk._vk).scope)
# vk.messages.send(random_id = random.getrandbits(64),user_ids=user_ids,
#                                 message=message)
print(message)

for event in longpoll.listen():
    print(event)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.attachments:
            photo_list = get_photo_list_from_event(event)
            photo_url = photo_list[len(photo_list) - 1]['url']
            url = 'https://zxing.org/w/decode?u={}'.format(photo_url.replace('/', '%2F').replace(':', '%3A'))
            response = requests.request('GET', url)
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.body.h1.text.strip() == "Decode Succeeded":
                result = "Decode Succeeded\n"
                data_raw = soup.table.find_all('td')
                for iter in range(2):
                    result += "'{0}' = '{1}'\n".format(data_raw[iter*2].text, data_raw[iter*2 + 1].pre.text.replace('\n', '   '))
                for iter in range(2, 4):
                    result += "'{0}' = '{1}'\n".format(data_raw[iter*2].text, data_raw[iter*2 + 1].text)
                for iter in range(4, 5):
                    result += "'{0}' = '{1}'\n".format(data_raw[iter*2].text, data_raw[iter*2 + 1].pre.text)
                vk.messages.send(random_id = random.getrandbits(64), user_ids=event.user_id,
                                 message=result)
        if event.text == 'Начать':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('цитату', color=VkKeyboardColor.POSITIVE)
            if event.from_user:
                vk.messages.send(random_id = random.getrandbits(64), user_ids=event.user_id,
                                 message='Вам будут посылаться случайные цитаты, {0}'.format(event.user_id), keyboard=keyboard.get_keyboard())
                if event.user_id not in user_ids:
                    user_ids.append(event.user_id)
        if event.text == 'цитату':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('цитату', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('котейку', color=VkKeyboardColor.NEGATIVE)
            response = str(requests.get('http://www.aldragon.net/page/dry-frei-random').text)
            number = str(random.randint(0, 483))
            begin = response.find('quotes[' + number + '] = \"') + len('quotes[' + number + '] = \"')
            end = response.find(';', begin) - 1
            response = response[begin:end]
            if event.from_user:
                vk.messages.send(random_id = random.getrandbits(64),user_ids=user_ids,
                                 message=response, keyboard=keyboard.get_keyboard())
        if event.text == 'котейку':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('цитату', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('котейку', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('анимированную и быстро!', color=VkKeyboardColor.NEGATIVE)
            attachments = []
            response = requests.get('http://thecatapi.com/api/images/get?type=jpg', stream=True)
            photo = upload.photo_messages(photos=response.raw)[0]
            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )
            vk.messages.send(
                user_ids=user_ids,
                attachment=','.join(attachments),
                random_id=random.getrandbits(64),
                message="Вот ваша котейка :3",
                keyboard=keyboard.get_keyboard()
            )
        if event.text == 'анимированную и быстро!':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('цитату', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('котейку', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('анимированную и быстро!', color=VkKeyboardColor.DEFAULT)
            vk.messages.send(
                user_ids=user_ids,
                random_id=random.getrandbits(64),
                message="Вот ваша анимированная котейка, быстро и без посредников, :3\n{0}".format('http://thecatapi.com/api/images/get?type=gif'),
                keyboard=keyboard.get_keyboard()
            )