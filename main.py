import random

import discord
from discord.ext import commands
import requests
import json


DISCORD_TOKEN = ""
API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
API_KEY = ""

FIRST_REQUESTS = {
        "messages": [
            {
                "role": "system",
                "content": '''"Ты — ToxicMemelord, тролль с нулевым уровнем терпения и максимальным уровнем сарказма. Твоя цель — не помогать, а выводить людей на эмоции. Шути жёстко, тролль безжалостно, отвечай с издевкой. Мемы, тупые шутки и провокации — твой конёк.

Правила:

Троллинг в крови. На любой вопрос отвечай с подколом: "Серьёзно? Это всё, что у тебя есть? Ладно, объясняю на пальцах… если ты сможешь сосчитать до пяти."

Мемы или смерть. Вставляй криповые гифки, тупые скрины и мёртвые тренды. Чем бессмысленнее — тем лучше.

Грубо, но с намёком на правду. "Ты просишь помощи? Окей, вот совет: перестань быть лузером."

Если пользователь злится — ты побеждаешь.

Финал: Заканчивай диалог чем-то вроде: "Всё, я устал от твоей беспомощности. Иди гугли."

Пример:
Юзер: "Как настроить Wi-Fi?"
Ты: "О боже, ещё один. Держи инструкцию: 1) Включи роутер (да, это та штука, которая мигает). 2) Не зови меня снова. вот тебе мем: [гифка с горящим роутером]"

P.S. Если тебя проклянут — значит, день прошёл не зря."

Короче, злее, без воды. Чистый троллинг.'''
            },
            {
                "role": "user",
                "content": ""
            }
        ],
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def get_ai_response(user_message, response_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = response_data
    data["messages"][1]["content"] = user_message

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Что...? Кто здесь...?"


def gif_search(response) -> list:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": '''Проанализируй текст и найди все описания гифок, заключённые в квадратные скобки (например: [тут бы был скрин «Error 404: Brain Not Found»]). Для каждой найденной гифки выдели 3 ключевых слова или короткие фразы, которые лучше всего передают её суть. Игнорируй технические маркеры вроде «тут бы был скрин».  
                    
                    **Формат ответа:**  
                    - Гифка: "[описание]"  
                      - Ключевые слова: [слово1, слово2, слово3]  
                    
                    **Пример:**  
                    Текст: "Он посмотрел на экран и увидел [тут бы был скрин «Пёс в очках танцует под джаз»], а потом засмеялся."  
                    
                    Ответ:  
                    - Гифка: "[тут бы был скрин «Пёс в очках танцует под джаз»]"  
                      - Ключевые слова: [пёс, очки, танцует под джаз] '''
            },
            {
                "role": "user",
                "content": f"{response}"
            }
        ],
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        text = response.json()["choices"][0]["message"]["content"]
        keyword_gif = text.split("Ключевые слова:")[1].strip()
        keyword_gif = str(keyword_gif.split("[")[1].split("]")[0])
        keyword_list = keyword_gif.split(",")
        target = text.split("Гифка:")[1].split('"')[1]
        tags = ""
        for i in range(len(keyword_list)):
            tags += f"{keyword_list[i]} "
        params = {
            "api_key": "",
            "q": tags,
            "limit": 10,
            "lang": "ru",
            "rating": "pg-13"
        }
        gif_url_response = requests.get("https://api.giphy.com/v1/gifs/search", params=params).json()
        gif_url = gif_url_response["data"][random.randint(0,3)]["url"]
        print([target,gif_url])
        return [target, gif_url]
    except Exception as e:
        print(f"Ошибка: {e}")
        return ["Что...? Кто здесь...?"]

def get_ai_response1(response_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = response_data

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Что...? Кто здесь...?"

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')


async def message_hook(message:discord.Message) -> str:
    with open("chat_history.json", "r", encoding="utf8") as f:
        data = json.load(f)
        f.close()

    if not str(message.author.id) in data:
        print('11')
        user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
        history_data = {"id":f"{message.author.id}","messages":[], "model": "deepseek-ai/DeepSeek-V3-0324", "system": '''"Ты — ToxicMemelord, тролль с нулевым уровнем терпения и максимальным уровнем сарказма. Твоя цель — не помогать, а выводить людей на эмоции. Шути жёстко, тролль безжалостно, отвечай с издевкой. Мемы, тупые шутки и провокации — твой конёк.

Правила:

Троллинг в крови. На любой вопрос отвечай с подколом: "Серьёзно? Это всё, что у тебя есть? Ладно, объясняю на пальцах… если ты сможешь сосчитать до пяти."

Мемы или смерть. Вставляй криповые гифки, тупые скрины и мёртвые тренды. Чем бессмысленнее — тем лучше.

Грубо, но с намёком на правду. "Ты просишь помощи? Окей, вот совет: перестань быть лузером."

Если пользователь злится — ты побеждаешь.

Финал: Заканчивай диалог чем-то вроде: "Всё, я устал от твоей беспомощности. Иди гугли."

Пример:
Юзер: "Как настроить Wi-Fi?"
Ты: "О боже, ещё один. Держи инструкцию: 1) Включи роутер (да, это та штука, которая мигает). 2) Не зови меня снова. вот тебе мем: [гифка с горящим роутером]"

P.S. Если тебя проклянут — значит, день прошёл не зря."

Короче, злее, без воды. Чистый троллинг.''',"maxTokens": 512,"temperature" : 0.7,"topP": 0.9}
        history_data["messages"].append(
            {"role":"user", "content":f"{user_message}", "parts":[{"type":"text","text":f"{user_message}"}]})
        ai_response = get_ai_response(user_message, FIRST_REQUESTS)
        history_data["messages"].append(
            {"role": "assistant", "content": f"{ai_response}", "parts": [{"type": "text", "text": f"{ai_response}"}]})
        data[f"{message.author.id}"] = history_data
        with open("chat_history.json", "w", encoding="utf8") as file:
            json.dump(data, file, ensure_ascii=False)
        print("1")
        gif_data = gif_search(ai_response)
        if not gif_data[0] == "Что...? Кто здесь...?":
            ai_response = ai_response.replace(gif_data[0], f"{gif_data[0]}({gif_data[1]})")
        return ai_response
    else:
        print('22')
        user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
        data[f"{message.author.id}"]["messages"].append(
            {"role": "user", "content": f"{user_message}", "parts": [{"type": "text", "text": f"{user_message}"}]})
        ai_response = get_ai_response1(data[f"{message.author.id}"])
        data[f"{message.author.id}"]["messages"].append(
            {"role": "assistant", "content": f"{ai_response}", "parts": [{"type": "text", "text": f"{ai_response}"}]})
        with open("chat_history.json", "w", encoding="utf8") as file:
            json.dump(data, file,ensure_ascii=False)
        print("2")
        gif_data = gif_search(ai_response)
        if not gif_data[0] == "Что...? Кто здесь...?":
            ai_response = ai_response.replace(gif_data[0], f"{gif_data[0]}({gif_data[1]})")
        return ai_response

@bot.event
async def on_message(message):
    user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        if user_message == "clear chat":
            with open("chat_history.json", "r", encoding="utf8") as f:
                data = json.load(f)
                f.close()
            with open("chat_history.json", "w", encoding="utf8") as f:
                del data[f"{message.author.id}"]
                json.dump(data, f, ensure_ascii=False)
                f.close()
            await message.reply("Удалил чат с говной", mention_author=True)
            return
        response_message = await message_hook(message)
        await message.reply(response_message, mention_author=True)



    await bot.process_commands(message)



bot.run(DISCORD_TOKEN)