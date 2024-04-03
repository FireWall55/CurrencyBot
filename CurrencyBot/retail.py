import os
import json
import discord
import economy
import items

prefix: str = "="
os.chdir('C:\\Users\\nakul\\OneDrive\\Desktop\\Code\\DiscordBots\\CurrencyBot')

shops =[{"name": "pencil", "price": 10},
        {"name": "book", "price": 50},
        {"name": "dumbell", "price": 100},
        {"name": "croissant", "price": 250},
        {"name": "baguette", "price": 300}]


commands: str = [{"name": f"{prefix}shop", "description": "opens a shop displaying all items with prices for sale"},
                 {"name": f"{prefix}buy (item) (count)", "description": "buy a specific item of a specific count"},
                 {"name": f"{prefix}sell (item) (count)", "description": "sell a specific number of an item"}]



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
        await items.add_items_bank(message=message, item=item, count=count, print=True)
    
async def sell(message: discord.Message, item: str, count: int):
    a = await economy.open_account(message, True)
    users = await get_bank_data()
    author = message.author
    
    found: bool = False
    for thing in users[str(author.id)]["items"]:
        if thing["name"] == item:
            found = True
            sell_item = thing
    if not found:
        await message.channel.send("You do not own that item")
        return
    if not sell_item["count"] >= count or sell_item["count"] == 0:
        await message.channel.send("You don't have enough to sell")
        return
    #add money to wallet
    #remove items from inventory
    original = users[str(author.id)]["wallet"]
    item_price: int = 0
    for index in items.item_prices:
        if index["name"] == item:
            item_price = index["price"]
    
    users[str(author.id)]["wallet"] += int(count * item_price * 0.8) #you get 80% back
    await message.channel.send(f"You sold {item} of count {count} for 80% of what it would be bought for. \nTransaction: ${original} -> ${users[str(author.id)]["wallet"]}")
    #sell_item["count"] -= count
    await items.add_items_bank(message=message, item=item, count= -1 * count,print=False)

     
    
    
    
    
    
    
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users