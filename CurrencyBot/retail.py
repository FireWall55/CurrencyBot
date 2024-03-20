import os
import json
import discord
import economy
import items

prefix: str = "="
os.chdir('C:\\Users\\nakul\\OneDrive\\Desktop\\Code\\DiscordBots\\CurrencyBot')

shops = [{"name": "gun", "price": 100},
        {"name": "weapon", "price": 500},
        {"name": "pencil", "price": 10}]
commands: str = [{"name": f"{prefix}shop", "description": "opens a shop displaying all items with prices for sale"},
                 {"name": f"{prefix}buy (item)", "description": "buy a specific item"},
                 {"name": f"{prefix}buy multi (item) (count)", "description": "buy a specific number of an item"}]



async def print_commands(message: discord.Message):
    em = discord.Embed(title = "Retail Commands", description="Commands that work with the retail system",
               color=discord.Color.purple())
    for command in commands:
        em.add_field(name=command["name"], value=command["description"], inline=False)
        
    await message.channel.send(embed=em)


async def shop(message: discord.Message):
    em = discord.Embed(title = "BLACK MARKET", description="Everything for sale that you can buy if you have enough money. and ONLY if you dare >:)",
               color=discord.Color.green())
    for item in shops:
        em.add_field(name=item["name"], value=f"-> price:\t{item["price"]}", inline=False)
        
    await message.channel.send(embed=em)




async def buy(message: discord.Message, item: str, count: int):
    a = await economy.open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    users = await get_bank_data()
    
    #checking
    price: int = 0
    found: bool = False
    for thing in shops:
        if thing["name"] == item:
            price = thing["price"]
            found = True
    if not found:
        await message.channel.send("That item was not found in the shop")
        return
    
    #if the item is valid
    enoughMoney: bool = await economy.spend_money(message=message, amt=price*count)
    if(enoughMoney):
        await items.add_items(message=message, item=item, count=count)
    
    
     
    
    
    
    
    
    
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users