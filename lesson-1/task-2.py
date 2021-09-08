'''
2. Изучить список открытых API. Найти среди них любое, 
требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. 
Ответ сервера записать в файл.
'''

import requests
import json

# Анализ эмоциональной окрашенности текста с помощью IBM Watson tone-analyzer

url = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/2de87a86-1590-4607-a408-e209632997da/v3/tone'
api_key = '--hidden--'

text_sample = '''
Blood like rain come down
Drawn on grave and ground
Part vampire
Part warrior
Carnivore and voyeur
Stare at the transmittal
Sing to the death rattle
La, la, la, la, la, la, la-lie
Credulous at best, your desire to believe in angels in the hearts of men.
Pull your head on out your hippy haze and give a listen.
Shouldn't have to say it all again.
The universe is hostile, so Impersonal, devour to survive.
So it is. So it's always been.
We all feed on tragedy
It's like blood to a vampire
Vicariously I, live while the whole world dies
Much better you than I

(Tool, Vicarious)  
'''

params = (('text', text_sample), ('version', '2017-09-21'))
auth = ('apikey', api_key)
response = requests.get(url, params=params, auth=auth)

with open('tone_analysis.json', 'w') as file:
    json.dump(response.json(), file)
