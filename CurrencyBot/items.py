import os
import json
import discord
import economy
import jobs

prefix: str = "="
os.chdir('C:\\Users\\nakul\\OneDrive\\Desktop\\Code\\DiscordBots\\CurrencyBot')

item_prices = [{"name": "pencil", "price": 10}, #use to set up prices when working
              {"name": "book", "price": 50},
              {"name": "dumbell", "price": 100},
              {"name": "gold_banana", "price": 200},
              {"name": "croissant", "price": 250},
              {"name": "baguette", "price": 300},
              {"name": "sniper", "price": 500},
              {"name": "machine_gun", "price": 400},
              {"name": "pistol", "price": 100},
              {"name": "shotgun", "price": 300}]

atk_item_selection_menu = [{"label": "fist", "emoji": "👊", "description": "punch your opponent for 5 dmg"},
                           {"label":"gold_banana", "emoji": "🍌", "description": "ko your opponent"},
                           {"label":"sniper", "emoji": "🔫", "description": "snipe for 40 dmg"},
                           {"label":"machine_gun", "emoji": "🔫", "description": "shoot for 30 dmg"},
                           {"label":"pistol", "emoji": "🔫", "description": "shoot for 20 dmg"},
                           {"label":"shotgun", "emoji": "🔫", "description": "shoot for 25 dmg"}]

async def get_atk_items():
    return atk_item_selection_menu

commands: str = [{"name": f"{prefix}view items", "description": "See all of your items"},
                 {"name": f"{prefix}view items (username)", "description": "See all the items of a specific user (username = username of selected target)"}
                 ]


async def print_commands(message: discord.Message):
    em = discord.Embed(title = "Item Commands", description="Commands that work with the item system",
               color=discord.Color.purple())
    for command in commands:
        em.add_field(name=command["name"], value=command["description"], inline=False)
        
    await message.channel.send(embed=em)



async def view_items(message: discord.Message):
    a = await economy.open_account(message, True)

    em = discord.Embed(title="These are all the items you have",description="item name and count are shown. Use =item help for extra help",
                       color = discord.Color.red())
    
    users = await get_bank_data()
    list = users[str(message.author.id)]["items"] #list of ur items
    for item in list:
        em.add_field(name = item["name"], value= f"\t-> count: {item["count"]}", inline=False)
        
    await message.channel.send(embed=em)
    
    
    
async def view_items_others(message: discord.Message, target: str):#target is the username
    a = await economy.open_account(message, True)

    users = await get_bank_data() #every user
    id: str = ""
    for user in users: #user is the user id
        if users[user]["username"] == target:
            id = user
    if id == "":
        await message.channel.send("This user was not found. Either they don't have an account, or you mispelled their username")
        return
    

    em = discord.Embed(title=f"These are all the items {users[id]["username"]} has",description="item name and count are shown. Use =item help for extra help",
                       color = discord.Color.red())
            
    list = users[id]["items"] #list of target's items
    for item in list:
        em.add_field(name = item["name"], value= f"\t-> count: {item["count"]}", inline=False)
    await message.channel.send(embed=em)
    


# how items will work in an array: [{"name":}]
async def add_items_bank(message: discord.Message, item: str, count: int, print: bool):
    a = await economy.open_account(message, True)
    
    users = await get_bank_data()
    list = users[str(message.author.id)]["items"] #list of all your items

    found: bool = False
    for i, object in enumerate(list):
        if item == object["name"]: #if the object added is the same as the current looped name
            object["count"] += count
            found = True
            if object["count"] == 0:  #if there is no more of the object after subtracting
                del users[str(message.author.id)]["items"][i]
    
        
    if not found: #if, after looping, it is not found
        users[str(message.author.id)]["items"].append({"name" : item, "count" : count})
    
    if print:
        await message.channel.send(f"The item {item} of count {count} was added to your account")
        
    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=2)

async def add_items_shop(message: discord.Message, item: str, count: int, print: bool):
    a = await economy.open_account(message, True)
    
    shops = await jobs.get_shops_data()
    products = shops[str(message.author.id)]["products"] #list of all your items

    found: bool = False
    for i, product in enumerate(products):   
        if item == product["name"]: #if the object added is the same as the current looped name
            product["count"] += count
            found = True
            if product["count"] == 0:  #if there is no more of the object after subtracting
                del shops[str(message.author.id)]["items"][i]
                return
    
    price: int = 0
    for thing in item_prices:
        if thing["name"] == item:
            price = thing["price"]
    
  
    if not found: #if, after looping, it is not found
        shops[str(message.author.id)]["products"].append({"name" : item, "count" : count, "price": price})
    
    if print:
        await message.channel.send(f"The item {item} of count {count} was added to your shop")
        
    with open("playershops.json", "w") as f:
        json.dump(shops, f, indent=2)



async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users