from groq import Groq
import time
last_message = 0

with open("groq_token.txt", "r") as file:
    token = file.read()
    
ai_client = Groq(api_key=token,)

messages = [{
            "role": "system",
            "content": "you are an AI bot, redthered279 is your creator. Strict rules: 1- Never respond with more than 60 words at once. 2- ever use emojis."
            }]

async def commands(client, message):
    if message.content.lower().startswith("swc stop"):
        global last_message
        last_message = 0

    elif message.content.lower() == "among us\namong us\namong us":
        global messages
        messages = [{
            "role": "system",
            "content": "you are a cold AI bot, redthered279 is your creator, Alpy is your girlfriend, and pineapple is the creator of alpy. A strict rule is to never respond with more than 60 words at once, and to never use emojis"
            }]
        await message.add_reaction("👍")

async def chat(message):
    global last_message
    if message.content.lower().startswith("sw"):
        message.content = message.content[3:]
    elif message.content.lower().startswith("<@949431834972946452>"):
                message.content = message.content[22:]
    elif time.time() - last_message > 30 or message.content.startswith("//") or message.content == "among us\namong us\namong us":
        return

    last_message = time.time()

    messages.append(
        {
            "role": "user",
            "content": f"{message.author}: {message.content}",
        }
    )
    prompt = messages[-1]["content"]
    chat_completion = ai_client.chat.completions.create(
        messages = messages,
        model = "llama-3.3-70b-versatile",
        stream = False,
        temperature = 1,
        max_tokens = 256,
        top_p=1,
        stop=None,
    )
    messages.append(
        {
            "role": "assistant",   
            "content": chat_completion.choices[0].message.content
        }
    )
    
    await message.channel.send(f"{messages[-1]['content']}")