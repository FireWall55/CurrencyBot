import discord
import json
import economy



async def work(message: discord.Message):
    users = await get_bank_data()
    author = message.author
    
async def open_shop(message: discord.Message):
    a = await economy.open_account(message, True)
    users = await get_bank_data()
    shops = await get_shops_data()
    author = message.author
    
    if (not users[str(author.id)]["job"] == "supplier"):
        await message.channel.send(f"You must be a supplier to own a shop. You are of the job: {users[str(author.id)]["job"]}")
        return
    if (str(author.id) in shops) : #if they aren't a supplier or they have a shop
        await message.channel.send("You already have a shop. Do view shop (username) to view someone's shop")
        return
    shops[str(author.id)] = {}
    shops[str(author.id)]["username"] = str(author)
    shops[str(author.id)]["visible"] = True
    shops[str(author.id)]["banned_users"] = [{"name": ""}]
    shops[str(author.id)]["banned_orgs"] =  [{"name": ""}]
    shops[str(author.id)]["products"] = [{"name": "pencil", "count": 1, "price": 10}] # primary item to sell
    
    with open("playershops.json", "w") as f:
        json.dump(shops, f, indent=2)
        
    await message.channel.send(f"{author.mention} Your personal shop has been opened :)")
    return
    
    
    
    





async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users
async def get_shops_data():
    with open("playershops.json", "r") as f:
        users = json.load(f)
        return users