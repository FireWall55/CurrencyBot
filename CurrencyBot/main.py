import os
import economy
from typing import Final
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
import responses
import items
import retail
import noPrefix
import json
import jobs
import playershops
import buttons
import combat

last_msg: str = ""
count: int = 0

# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


async def passiveHelp(message: Message):
    em = discord.Embed(title = "Passive Commands", description="if these are in your message, the bot will respond (without \"=\" prefix)",
               color=discord.Color.orange())
    em.add_field(name="damn", value="bot responds with skull emoji", inline=False)
    em.add_field(name="idiot", value="bot responds with an image of a sad face", inline=False)
    em.add_field(name="cap", value="the bear does indeed smell cap", inline=False)
    em.add_field(name="ayo", value="sesame street hit diff", inline=False)
    em.add_field(name="sigma", value="bot responds with a ping saying you are a sigma B)", inline=False)
    em.add_field(name="erm", value="erm", inline=False)
    await message.channel.send(embed=em)
    
async def quickAddSection() -> None:
    users = await economy.get_bank_data()
    for user in users:
        users[user]["organization"] = "none"
        
    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=2)

# Step 1: Bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


# Step 2: Message functionality
async def send_message(message: Message, user_message: str) -> None:
    
    users = await economy.get_bank_data()
    user_message = user_message.lower()
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    if is_private := user_message[1] == "?": #if the user message starts with =p
        user_message = user_message[2:]
    else:
        user_message = user_message[1:]
        
    # test for ping command
    if user_message == "ping":
        await message.channel.send(f'pong {message.author.mention}')
        return  
    
    #custom eval command
    if str(message.author.id) == "703024548093755483":
        parts = user_message.split(" ")
        if user_message.startswith("eval"):
            await message.delete()
            await eval(user_message[5:])
            return
    
    #buttons
    if user_message.startswith("start fight"): #start fight (bet amt)
        parts = user_message.split(" ")
        if not len(parts) == 3:
            await message.channel.send("Please input the correct number of fields")
            return
        if not parts[2].isdigit():
            await message.channel.send("Please input a number (not a string) for the count")
            return
        await combat.start(message=message, bet=int(parts[2]))
        return

    if user_message == "button test":
        view = buttons.TestView(timeout=60)
        button_msg = await message.reply("job selection that def works", view=view)
        view.message = button_msg
        
        await view.wait()
        await view.disable_all_items()
        
        if view.job == "": #timed out, will print anyway
            return
        elif view.job == "none":
            users[str(message.author.id)]["job"] = "none"
            with open("mainbank.json", "w") as f:
                json.dump(users, f, indent=2)
            return
        elif view.job == "police":
            users[str(message.author.id)]["job"] = "police"
            with open("mainbank.json", "w") as f:
                json.dump(users, f, indent=2)
            return
        else:
            users[str(message.author.id)]["job"] = "doctor"
            with open("mainbank.json", "w") as f:
                json.dump(users, f, indent=2)
            return
    
    #help commands
    if user_message == "help":
        em = discord.Embed(title = "Please type one of the following commands for more info:", 
                           description="This bot is meant for fun for me and my friends :D",
                           color= discord.Color.blue())
        em.set_thumbnail(url="https://i1.sndcdn.com/artworks-2Tbz9zQBPzNHVttm-kBcUbw-t500x500.jpg")
        em.add_field(name = "=currency help", value = "all currency commands", inline=False)
        em.add_field(name = "=item help", value = "commands relating to items", inline = False)
        em.add_field(name = "=text help", value = "all commands that the bot will respond to", inline=False)
        em.add_field(name = "=retail help", value = "commands relating to the bot's retail system", inline=False)
        em.add_field(name = "=playershop help", value = "commands relating to the personal player shops", inline=False)
        em.add_field(name = "=passive help", value = "words that if you put it in a message it will rspond (doesn't require = as a prefix)",
                     inline=False)
        
        await message.channel.send(embed = em)
        return
    if user_message == "currency help":
        await economy.print_commands(message=message)
        return
    if user_message == "text help":
        await responses.print_commands(message=message)
        return
    if user_message == "item help":
        await items.print_commands(message=message)
        return
    if user_message == "retail help":
        await retail.print_commands(message=message)
        return
    if user_message == "playershop help":
        await playershops.print_commands(message=message)
        return
    if user_message == "passive help":
        await passiveHelp(message=message)
        return
    
    #economy elements
    if user_message == "open account":
        await economy.open_account(message = message, check=False)
        return
    if user_message == "balance":
        await economy.check_balance(message = message)
        return
    if "withdraw" in user_message:
        parts = user_message.split()
        if parts[1] == "all":
            if users[str(message.author.id)]["bank"] == 0:
                await message.channel.send("You have nothing in the bank. YOU BROKE XD")
                return
            else:
                await economy.withdraw(message=message, amt=users[str(message.author.id)]["bank"])
                return
        await economy.withdraw(message=message, amt=int(parts[1]))
        return
    if user_message.startswith("deposit"):
        parts = user_message.split()
        if parts[1] == "all":
            if users[str(message.author.id)]["wallet"] == 0:
                await message.channel.send("You have nothing in your wallet. YOU BROKE XD")
                return
            else:
                await economy.deposit(message=message, amt=users[str(message.author.id)]["wallet"])
                return
        await economy.deposit(message=message, amt=int(parts[1]))
        return
        
    #item elements
    if user_message == "view items":
        await items.view_items(message=message)
        return
    if "view items " in user_message:
        parts = user_message.split()
        if not len(parts) == 3:                  
            await message.channel.send("Please input a 1 word player username")
            return

        await items.view_items_others(message=message, target=parts[2])
        return
    
    #retail elements
    if user_message.startswith("buy"): #buy (item) (count)
        parts = user_message.split()
        if not len(parts) == 3:
            await message.channel.send("Please input the correct number of fields")
            return
        if not parts[2].isdigit():
            await message.channel.send("Please input a number (not a string) for the count")
            return
        await retail.buy(message=message, item=parts[1], count=int(parts[2]))
        return
    if user_message.startswith("sell"):
        parts = user_message.split()
        if not len(parts) == 3:
            await message.channel.send("Please input the correct number of fields")
            return
        if not parts[2].isdigit():
            await message.channel.send("Please input a number (not a string) for the count")
            return
        await retail.sell(message=message, item=parts[1], count=int(parts[2]))
        return
        
    if user_message == "shop":
        await retail.shop(message=message)
        return
        
    #player shop elements
    if user_message == "open shop":
        await jobs.open_shop(message=message)
        return
        
    if "view shop" in user_message:
        parts = user_message.split(" ")
        if len(parts) == 3:
            await playershops.view_shop(message=message, target=parts[2])
            return
        else:
            await message.channel.send("Please input the user you are targeting after \"view shop\"")
            return
    if "pbuy" in user_message: # pbuy username item count
        parts = user_message.split(" ")
        if not len(parts) == 4:
            await message.channel.send("Please input the correct number of fields")
            return
        if not parts[3].isdigit():
            await message.channel.send("Please input a number (not a string) for the count")
            return
        await playershops.buy(message=message, target=parts[1], item=parts[2], count=int(parts[3]))
        return
    if user_message.startswith("ban"): #ban user/org (username)/(org name)
        parts = user_message.split(" ")
        if not len(parts) == 3:
            await message.channel.send("Plase input the correct number of fields")
            return
        await playershops.ban(message=message, type=parts[1], target=parts[2])
        return
    if user_message.startswith("unban"): #unban user/org (username)/(org name)
        parts = user_message.split(" ")
        if not len(parts) == 3:
            await message.channel.send("Please input the correct number of fields")
            return
        await playershops.unban(message=message, type=parts[1], target=parts[2])
        return
    if user_message.startswith("shop deposit"): #shop deposit (item) (count)
        parts = user_message.split(" ")
        if not len(parts) == 4:
            await message.channel.send("Please input the correct number of fields")
            return
        if not parts[3].isdigit():
            await message.channel.send("Please input a number (not a string) for the count")
            return
        await playershops.deposit_items(message=message, item=parts[2], count=int(parts[3]))
        return
    
    
    try:
        response: str = responses.get_response(message, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

        
        
# Step 3: Handling the startup for our bot
@client.event
async def on_ready() -> None:
    await quickAddSection()
    print(f'{client.user} is now running')

    
    
# Step 4: 
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    if type(user_message) == str:
        if user_message[0] == "=":#prefix
            await send_message(message, user_message)
        else:
            global last_msg
            global count
            if last_msg == user_message:
                count += 1
            else:
                count = 0
            if count > 3: #will delete the 5th one
                await message.channel.purge(limit=5)
                count = 0
                #await message.delete()
                return
            last_msg = user_message
            
            if message.author.is_on_mobile == True:
                await message.reply("hop off of mobile bro, get on a computer :index_pointing_at_the_viewer:")
            await noPrefix.send_message(message=message, user_message=user_message)
    
    
# Step 5: Main entry point
def main() -> None:
    client.run(token=TOKEN)


 
if __name__ == '__main__':
    main()
    
    

async def removed_commands_features(message: Message, user_message: str):
    if "add " in user_message:
        parts = user_message.split()
        if not len(parts) == 3:                     #if the length is not 3
            await message.channel.send("Please input 2 values after \"add\"")
            return
        
        if parts[1] and isinstance(parts[1], (str)):
            item: str = parts[1]
        else:
            await message.channel.send("Please input a word as the 3rd value. Use =help for help")
        
        if int(parts[2]) and isinstance(int(parts[2]), (int)):   #if they put a 3rd value and it is an int
            count: int = int(parts[2])
        else:
            await message.channel.send("Please input a number as the 3rd value. Use =help for help")
            return
        await items.add_items(message=message, item=item, count=count)
        return
    
    
    #await message.add_reaction('\N{SKULL}')
