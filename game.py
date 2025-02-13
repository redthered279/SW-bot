# Currently unused


async def commands(client, message):
    pass

"""
import discord
from random import randint, uniform
import asyncio
from math import floor, ceil
from re import match
from time import time


#GOD = ("", 99999999, 9999, 9999, 9999, 1)
#NORMAL = ("", 100, 8, 0, 10, 0)

def run():

    def num_simple(num):
        num = str(num)
        size = len(num)
        if size <= 4:
            return num
        power = size - 4
        return f"{int(num[:4]):,}×10^{power}"

    def get_items(id):
        try:
            with open(f"/home/container/SW/items/{id}", "r") as file:
               items = file.read().split(",")

            for i in range(3):
                items[i] = int(items[i])
            return items

        except FileNotFoundError:
            with open(f"/home/container/SW/items/{id}", "w") as file:
                file.write("0,0,0")
            return [0, 0, 0]

    def set_items(id, items):
        out = ""
        for x in items:
            out += f"{x},"
        out = out[:-1]
        with open(f"/home/container/SW/items/{id}", "w") as file:
            file.write(out)

    def get_cd(id):
        try:
            with open(f"/home/container/SW/cooldown/{id}", "r") as file:
                t = int(float(file.read()))
            return t
        except FileNotFoundError:
            with open(f"/home/container/SW/cooldown/{id}", "w") as file:
                t = time()
                file.write(str(t))
            return None

    def set_cd(id):
        with open(f"/home/container/SW/cooldown/{id}", "w") as file:
            file.write(str(time()))

    def get_wk(id):
        if id == 949431834972946452:
            return
        try:
            with open(f"/home/container/SW/userfiles/{id}", "r") as file:
                wk = int(file.read())
            return wk
        except FileNotFoundError:
            with open(f"/home/container/SW/userfiles/{id}", "w") as file:
                file.write("200")
            return 200

    def set_wk(id, wk):
        with open(f"/home/container/SW/userfiles/{id}", "w") as file:
            file.write(str(wk))

    def wk_add(id, amount):
        wk = get_wk(id)
        if wk == None:
            return
        set_wk(id, wk + amount)

    def embeded(players, report):
        embed = discord.Embed(title="**__TIME TO FIGHT!__**",color=0x923CB9)
        for player in players:
            stats = player.stats()
            embed.add_field(name=f"**{player.name}**:", value=stats,inline=True)
        embed.add_field(name=report[0], value=report[1])
        return embed

    def evolved(level):
        hp = floor(160 * 1.2 ** level)
        power = floor(8 * 1.25 ** level)
        energy = floor(11 * 1.22 ** level)
        return ("SW/annihilator", hp, power, 4, energy, 2)

    def mention_eval(guild, input):
        if type(input) == tuple:
            found = {}
            for user in input:
                sample = "<@" + ("\d" * (len(user) -3)) + ">"
                if match(sample, user):
                    id = int(user[2:-1])
                    user = guild.get_member(id)
                    if user == None:
                        return 2
                    found[id] = user.name
                else:
                    return 1

            return found
        else:
            sample = "<@" + ("\d" * (len(input) -3)) + ">"
            if match(sample, input):
                id = int(input[2:-1])
                user = guild.get_member(id)
                if user == None:
                    return 2
                else:
                    return user
            else:
                return 1
            #1 for invalid, 2 for not found


    class Fighter():
        def __init__(self, card, control):
            self.name = card[0]
            self.hp = card[1]
            self.max_hp = card[1]
            self.power = card[2]
            self.energy = card[3]
            self.max_energy = card[4]
            self.control = control
            self.pron = "itself" if control == 949431834972946452 else "themself"
            self.dead = False
            self.type = card[5]
            #0 for normal, 1 for God

        def attack(self,other):
            if randint(1,10) == 1:
                mul = uniform(1,2.5)
                hit = "kicked"
            else:
                mul = uniform(0.5,1.5)
                hit = "punched"
            damage = floor(self.power*mul)
            other.hp -= damage
            other.hp = 0 if other.hp < 0 else other.hp
            self.energy += 1 if self.energy < 10 else 0
            death = ""
            if other.hp == 0:
                death="\n\n"+f"**{other.name}** died"
                other.dead=True
            return f"**{self.name}** {hit} **{other.name}** (-{damage})"+death

        def heal(self):
            heal = floor((self.power * (1.25 ** self.energy)) * uniform(0.8, 1.2))
            if self.type != 1:
                self.energy = 0
            self.hp += heal
            self.hp = self.hp if self.hp < self.max_hp else self.max_hp
            return f"**{self.name}** healed {self.pron} (+{heal})"

        def stats(self):
            return f"**HP**: {self.hp:,}/{self.max_hp:,}\n**Power**: {self.power:,}\n**Energy**: {self.energy:,}/{self.max_energy:,}"

        def ai(self,other):
            hp = (self.hp/self.max_hp)*100
            if hp < 30 and self.energy > 0:
                return self.heal()
            else:
                return self.attack(other)

        async def human(self,other,game,client):
            def check(reaction,user):
                return user.id == self.control and reaction.message.id == game.id
            while True:
                try:
                    reaction,user = await client.wait_for("reaction_add", timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    self.dead = True
                    return f"**{self.name}** took too long to respond"
                emoji=str(reaction.emoji)
                output=None
                if emoji == "👊":
                    output=self.attack(other)
                elif emoji == "❤️":
                    output=self.heal()
                elif emoji == "🏃":
                    self.dead=True
                    output=f"**{self.name}** ran away"
                if output != None:
                    try:
                        await reaction.remove(user)
                    finally:
                        return output

        async def play(self,other,game,client):
                if self.control != None:
                    return await self.human(other,game,client)
                else:
                    await asyncio.sleep(1)
                    return self.ai(other)

    async def c_fight(client, message, trigger, admin):
        if trigger.startswith("fight"):
            list = trigger.split(" ")
            if len(list) == 1:
                control = None
                name = "/SW/bot"
                pron = 0
                id = 0
            elif len(list) >= 3:
                await message.channel.send("You can only fight one person at a time")
                return
            else:
                user = mention_eval(message.guild, list[1])
                if user == 2:
                   await message.channel.send("Could not find that user")
                   return
                elif user == 1:
                    await message.channel.send(f"The correct syntax is `sw fight <@user>`")
                    return

                id = user.id
                name = user.name
                if id == message.author.id:
                    name = name[::-1]
                control = id
                pron = 1

            with open("/home/container/SW/userfiles/god", "r") as file:
                GOD_ID = int(file.read())

            if message.author.id == GOD_ID:
                card1 = (message.author.name + " (GOD)", 9999999, 99999, 9999, 9999, 1)
            else:
                card1 = (message.author.name, 100, 8, 0, 10, 0)

            if id == GOD_ID:
                card2 = (name + " (GOD)", 9999999, 99999, 9999, 9999, 1)
            else:
                card2 = (name, 100, 8, 0, 10, 0)


            player1 = Fighter(card1, message.author.id)
            player2 = Fighter(card2, control)

            turn = player1
            target = player2
            a = ""
            b = ""
            c = ""
            winner= None

            game = await message.channel.send(embed = embeded(discord, (player1, player2), ["**INSTRUCTIONS**","👊: attack\n❤️: heal\n🏃: run"]))
            await game.add_reaction("👊")
            await game.add_reaction("❤️")
            await game.add_reaction("🏃")

            while True:
                action = await turn.play(target,game,client)
                a, b, c = b, c, action

                if turn.dead == True or target.dead == True:
                    winner = turn if target.dead == True else target
                    if winner.control != None:
                        wk = randint(1, 200)
                        c += f"\n{winner.name} got {wk} William's kidneys"
                        wk_add(winner.control, wk)

                tup = (a,b,c)
                output = ""
                for x in tup:
                    if len(x) > 0:
                        output+=x+"\n\n"
                await game.edit(embed=embeded(discord, (player1, player2), ("**ACTIONS**", output)))
                if turn.dead == True or target.dead == True:
                    await game.clear_reactions()
                    break
                turn, target = target , turn


    async def c_boss(client, message, trigger, admin):
        if trigger.startswith("boss"):
            list = trigger[5:]
            if list == "":
                await message.channel.send("You need at least one more partner to run this command.")
                return
            list = list.split(" ")
            list = mention_eval(message.guild, tuple(list))
            if list == 1:
                await message.channel.send("The correct usage is `sw boss @user1 @user2...`")
                return
            elif list == 2:
                await message.channel.send("Could not find one or more of the users")
                return
            list[message.author.id] = message.author

            boss = Fighter(evolved(len(list)), None)

            for id in list:
                list[id] = Fighter((list[id], 100, 8, 0, 10, 0), id)

    async def c_wk(client, message, trigger, admin):
        if trigger.startswith("wk"):
            if trigger == "wk":
                id = message.author.id
                name = message.author.name
            else:
                id = trigger[3:].split(" ")[0]
                user = mention_eval(message.guild, id)
                if user == client.user:
                    await message.channel.send("Sorry I don't have anything")
                    return
                if user == 1:
                    await message.channel.send("Correct usage: `sw wk (optional: @mention)`")
                    return
                if user == 2:
                    await message.channel.send("Could not find that usee")
                    return
                id = user.id
                name = user.name
            wk = get_wk(id)
            if wk == None:
                return
            embed = discord.Embed(title = f"**{name}'s WK:**", description = f"Got {num_simple(wk)} William's kidneys", color = 0x923CB9)
            await message.channel.send(embed = embed)

    async def c_cf(client, message, trigger, admin):
        if trigger.startswith("cf"):
            try:
                list = trigger[3:].split(" ")
                if not(list[0] == "h" or list[0] == "t"):
                    await message.channel.send("Correct usage: `sw cf (h/t) (amount)`")
                    return
                choice = list[0]
                wk = get_wk(message.author.id)
                amount = wk if list[1] == "all" else floor(wk/2) if list[1] == "half" else int(list[1])
                if amount < 10:
                    await message.channel.send("You need to gamble at least 10 William's kidneys")
                    return

            except ValueError:
                await message.channel.send("Correct usage: `sw cf (h/t) (amount)`")
                return

            if amount > wk:
                await message.channel.send(f"You only have {wk} William's kidneys")
                return


            rand = randint(0, 3)
            rand = choice if rand == 0 else "t" if choice == "h" else "h"
            win = rand == 0
            if win:
                set_wk(message.author.id, wk + amount)
            else:
                set_wk(message.author.id, wk - amount)
            win = "won" if win else "lost"
            rand = "**heads**" if rand == "h" else "**tails**"
            color = 0x00ff1e if win == "won" else 0xff0000
            await message.channel.send(embed = discord.Embed(title = f"**{message.author.name}'s coinflip**", color = color, description = f"You got {rand} and {win} {num_simple(amount)} William's kidneys"))

    async def c_add(client, message, trigger, admin):
        if trigger.startswith("add") and message.author.id in admin:
            list = trigger[4:].split(" ")
            id = list[0][2:-1]
            if id == 949431834972946452:
                return

            user = message.guild.get_member(int(id))
            wk_add(id, int(list[1]))
            amount = int(list[1])
            await message.channel.send(f"Added {num_simple(amount)} William's kidneys to {user.name}'s inventory")

    async def c_dice(client, message, trigger, admin):
        if trigger.startswith("dice"):
            try:
                wk = get_wk(message.author.id)
                input = trigger[5:]
                amount = wk if input == "all" else floor(wk/2) if input == "half" else int(input)
            except ValueError:
                await message.channel.send("Correct usage: `sw dice (amount)`")
                return
            if amount < 10:
                await message.channel.send("You need to gamble at least 10 William's kidneys")
                return
            if amount > wk:
                await message.channel.send(f"You only have {wk} William's kidneys")
                return
            wk -= amount
            rand = randint(1, 6)
            result = floor(amount * ((0.4 * rand) - 0.4))
            wk += result
            set_wk(message.author.id, wk)
            delta = result - amount
            win = "won" if delta >= 0 else "lost"
            delta = - delta if delta < 0 else delta
            delta = f"{num_simple(delta)} William's kidneys" if delta != 0 else "nothing"
            color = 0x00ff1e if win == "won" else 0xff0000
            await message.channel.send(embed = discord.Embed(title = f"**{message.author.name}'s dice roll**", color = color, description = f"You rolled {rand} and {win} {delta}"))

    async def c_god(client, message, trigger, admin):
        if trigger.startswith("god"):
            id = trigger[4:]
            if id == "":
                return

            with open("userfiles/god", "w") as file:
                file.write(id)

            await message.add_reaction("✅")

    async def c_cups(client, message, trigger, admin):
        if trigger.startswith("cups"):
            try:
                wk = get_wk(message.author.id)
                input = trigger[5:]
                amount = wk if input == "all" else floor(wk/2) if input == "half" else int(input)
            except ValueError:
                await message.channel.send("Correct usage: `sw dice (amount)`")
                return
            if amount < 10:
                await message.channel.send("You need to gamble at least 10 William's kidneys")
                return
            if amount > wk:
                await message.channel.send(f"You only have {wk} William's kidneys")
                return
            rand = 3.5 if randint(1, 4) == 1 else 0
            amount = floor((amount * rand) - amount)
            wk += amount
            amount = - amount if amount < 0 else amount
            win = "You picked the right cup and won" if rand != 0 else "You picked the wrong cup and lost"
            color = 0x00ff1e if rand != 0 else 0xff0000
            await message.channel.send(embed = discord.Embed(title = f"**{message.author.name}'s dice roll**", color = color, description = f"{win} {amount} William's kidneys"))


    async def c_give(client, message, trigger, admin):
        if trigger.startswith("give"):
            list = trigger[5:].split(" ")
            user = mention_eval(message.guild, list[0])

            try:
                amount = int(list[1])
                assert user != 1
            except ValueError or AssertionError:
                await message.channel.send("Correct usage: `sw give @mention (amount)`")
                return
            if user == 2:
                await message.channel.send("Could not find that user")
                return

            if user == client.user:
                await message.channel.send("Oh... Thank you ☺️ \nbut I don't really need this for anything")
                return

            if user == message.author:
                await message.channel.send("...What?")
                return

            wk_self = get_wk(message.author.id)
            if amount > wk_self:
                await message.channel.send(f"You only have {wk_self} William's kidneys")
                return

            wk_add(user.id, amount)
            wk_add(message.author.id, -amount)
            await message.channel.send(f"{message.author.name} gave {amount} William's kidney to {user.name}")

    async def c_mine(client, message, trigger, admin):
        if trigger == "mine":
            t = get_cd(message.author.id)
            delta_t = time() - get_cd(message.author.id) if t != None else 61
            if delta_t >= 60:
                wk = get_wk(message.author.id)
                amount = floor(randint(10, 35) + (wk * uniform(0.005, 0.01)))
                set_wk(message.author.id, wk + amount)
                set_cd(message.author.id)
                await message.channel.send(f"{message.author.name} mined out {num_simple(amount)} William's kidneys")
            else:
                await message.channel.send(f"You have already mined! Wait at least {60 - ceil(delta_t)}s")

    h_fight = ("`fight`", "A simple fight minigame\nUsage: `sw fight {optional: @user}`")
    h_boss = ("`boss`", "Fight with your partners against an evolved version of /SW/bot [NOT FINISHED YET]\nUsage: `sw boss @mention1 @mention2...`")
    h_wk = ("`wk`","Show your or other players' current amout of William's kidneys\nUsage: `sw wk (optional: @mention)`")
    h_cf = ("`cf`", "Gamble your William's kidneys with a coinflip\nUsage: `sw cf (h/t) (amount)`")
    h_dice = ("`dice`", "Gamble your William's kidneys with a dice roll\nUsage: `sw dice (amount)`")
    h_cups = ("`cups`", "Gamble your William's kidneys by choosing a cup out of 3\nUsage: `sw cups (amount)`")
    h_give = ("`give`", "Give other players your William's kidneys\nUsage: `sw give @mention (amount)`")
    h_mine = ("`mine`", "Mine for William's kidneys (please don't ask how is that possible)")

    return (c_fight, c_boss, c_wk, c_cf, c_dice, c_cups, c_add, c_give, c_mine, c_god),(h_fight, h_boss, h_wk, h_cf, h_dice, h_cups, h_mine, h_give),(),()
"""