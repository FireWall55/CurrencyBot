import os
import json
import discord
import economy

prefix: str = "="
os.chdir('C:\\Users\\nakul\\OneDrive\\Desktop\\Code\\DiscordBots\\CurrencyBot')

vali_items: str = {"gun", "weapon", "extra", "powder", "pencil"}
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
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')

    em = discord.Embed(title="These are all the items you have",description="item name and count are shown. Use =item help for extra help",
                       color = discord.Color.red())
    
    users = await get_bank_data()
    list = users[str(message.author.id)]["items"] #list of ur items
    for item in list:
        em.add_field(name = item["name"], value= f"\t-> count: {item["count"]}", inline=False)
        
    await message.channel.send(embed=em)
    
    
    
async def view_items_others(message: discord.Message, target: str):#target is the username
    a = await economy.open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')

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
async def add_items(message: discord.Message, item: str, count: int):
    a = await economy.open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    
    users = await get_bank_data()
    if item in vali_items: #if it is a valid item
        list = users[str(message.author.id)]["items"] #list of all your items

        found: bool = False
        for object in list:
            if item == object["name"]: #if the object added is the same as the current looped name
                object["count"] += count
                found = True
            
        if not found: #if, after looping, it is not foundD
            users[str(message.author.id)]["items"].append({"name" : item, "count" : count})
        
        await message.channel.send(f"The item {item} of count {count} was added to your account")
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
            
    else:
        await message.channel.send("That was not a valid item")




async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users