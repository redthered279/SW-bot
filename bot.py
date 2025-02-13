import discord
import importlib
import general
import game
import ai

class Client(discord.Client):
    async def on_ready(self):
        print('Logged on!')

def load_modules():
    global general, game, ai
    general = importlib.reload(general)
    game = importlib.reload(game)
    ai = importlib.reload(ai)

client = Client(intents = discord.Intents.all())

"""
owner = 769697272232935434
admin = (769697272232935434, 797257966973091862, 730008654694055967)
"""

@client.event
async def on_message(message):

    print(f"{message.channel} — {message.author}: {message.content}")

    if message.author == client.user:
        return

    global token
    token = "sus"
    
    if not message.content.lower().startswith("swc "):
        await ai.chat(message)

    if message.content.lower().startswith("swc eval"):
        if message.author.id in (769697272232935434, 797257966973091862, 730008654694055967):
            try:
                statement = str(eval(message.content[9:]))
                if statement == "":
                    await message.channel.send("No output")
                    return
                await message.channel.send(statement)
            except Exception as e:
                await message.channel.send(e)
            finally:
                return
        else:
            await message.channel.send("Bot admin only")
            return
    
    if message.content.lower().startswith("swc reload"):
        if message.author.id in (769697272232935434, 797257966973091862, 730008654694055967):
            try:
                load_modules()
                await message.channel.send("Reloaded all modules")
                channel = client.get_channel(1071170416879599786)
            except Exception as error:
                await message.channel.send(error)
            finally:
                return
        else:
            await message.channel.send("Bot admin only")
            return

    if message.content.lower().startswith("swc echo"):
        if message.author.id in (769697272232935434, 797257966973091862, 730008654694055967):
            text = message.content[8:]
            if len(text) == 0:
                return
            channel = client.get_channel(935956434259177483)
            await channel.send(text)

    if message.content.lower().startswith("swc shutdown") and message.author.id == 769697272232935434:
        await message.channel.send("*dies*")
        await client.close()

    await general.commands(client, message)
    await ai.commands(client, message)
    await game.commands(client, message)
    

'''
@client.event
async def on_reaction_add(reaction,user):
    global admin
    global reactors
    args=(discord,client,admin,reaction,user)

    for func in reactors:
        await func(discord,client,admin,reaction,user)
'''

with open("token.txt","r") as file:
    token = file.read()

client.run(token)