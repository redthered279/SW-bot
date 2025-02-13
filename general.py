from random import randint

async def commands(client, message):
    if message.content.lower()[4:] == "hello":
        if randint(0, 99) == 0:
            await message.channel.send("Allahu Akbar")
        else:
            await message.channel.send("Hi!")
            
    if message.content.lower()[4:] == "gn":
        await message.channel.send("Good night!")

    if "sus" in message.content.lower() or "amogus" in message.content.lower():
        await message.add_reaction(":amogus:926419014643773470")