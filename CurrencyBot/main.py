import os
import economy
from typing import Final
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
import responses
import items
import retail
#703024548093755483 is my id
# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Step 1: Bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Step 2: Message functionality
async def send_message(message: Message, user_message: str) -> None:
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
    
    #help commands
    if user_message == "help":
        em = discord.Embed(title = "Please type one of the following commands for more info:", 
                           description="This bot is meant for fun for me and my friends :D",
                           color= discord.Color.blue())
        em.add_field(name = "=currency help", value = "all currency commands", inline=False)
        em.add_field(name = "=item help", value = "commands relating to items", inline = False)
        em.add_field(name = "=text help", value = "all commands that the bot will respond to", inline=False)
        em.add_field(name = "=retail help", value = "commands relating to the bot's retail system", inline=False)
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
    
    #economy elements
    if user_message == "open account":
        await economy.open_account(message = message, check=False)
        return
    if user_message == "check balance":
        await economy.check_balance(message = message)
        return
    if "withdraw " in user_message:
        parts = user_message.split()
        await economy.withdraw(message=message, amt=int(parts[1]))
        return
    if "deposit " in user_message:
        parts = user_message.split()
        await economy.deposit(message=message, amt=int(parts[1]))
        return
        
    
    #item elements
    if user_message == "view items":
        await items.view_items(message=message)
        return
    if "view items " in user_message:
        parts = user_message.split()
        if not len(parts) == 3:                  
            await message.channel.send("Please input 2 values after \"add\"")
            return

        await items.view_items_others(message=message, target=parts[2])
        return
    
    #retail elements
    if "buy" in user_message:
        parts = user_message.split()
        if(parts[1] == "multi"):
            count: int = int(parts[3])
            await retail.buy(message=message, item=parts[2], count=count)
            return
        else:
            await retail.buy(message=message, item=parts[1], count=1)
            return
        
    if user_message == "shop":
        await retail.shop(message=message)
        return
    
            
    try:
        response: str = responses.get_response(message, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
# Step 3: Handling the startup for our bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

    
# Step 4: 
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    if isinstance(user_message[0], str):
        if user_message[0] == "=":#prefix
            await send_message(message, user_message)
        else:
            return
    
    
# Step 5: Main entry point
def main() -> None:
    client.run(token=TOKEN)
    
if __name__ == '__main__':
    main()
    
    
    
    
    

async def removed_commands_features(message: discord.Message, user_message: str):
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