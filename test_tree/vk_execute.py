# -*- coding: utf8 -*-

import requests
from random import getrandbits

my_id = 252833211
another_id = 7108139
api_url = "https://api.vk.com/method"
token = "30638db4b8b941601f6517c2b8a96f978ea79d38d1a06cc9cf5fd74a652ba52a94ffad2f9282ded13dffe"
api_version = 5.103

def mass_send(messages, user_ids, **kwargs):
    request_code = ""
    for i in range(min(user_ids.__len__(), 25)):
        try:
            message = messages[i]
        except KeyError:
            message = ""
        except IndexError:
            message = ""
        request_code += "API.messages.send({\"message\": \"" + message + "\", \"user_ids\": \"" + str(
            user_ids[i]).replace('[', ' ').replace(']', ' ').replace(' ', '') + "\", \"random_id\": \"" + str(
            int(getrandbits(64))) + "\""
        for key, value in kwargs.items():
            try:
                request_code += ", \"" + str(key) + "\": \"" + str(value[i]) + "\""
            except KeyError:
                pass
            except IndexError:
                pass
        request_code += "});\n"
    request_code += "return;\n"
    print(request_code)
    response = requests.post(url=f"{api_url}/execute",
                             data={
                                 "code": request_code,
                                 "access_token": token,
                                 "v": api_version,
                             }).json()
    if 'error' in response.keys():
        print(response)
    else:
        print(response['response'])
    return


messages = ["Хочу картинки"]
user_ids = [[my_id, 7108139, ],]
mass_send(messages, user_ids, attachment=['photo7108139_456240833,photo7108139_456240832'])
