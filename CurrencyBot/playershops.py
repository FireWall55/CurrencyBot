import discord
import json
import jobs
import economy
import items

prefix: str = "="
commands: str  = [{"name": f"{prefix}view shop (username)", "description": "See the shop of the username targeted.\nCan replace username with display name and user ID as well"},
                  {"name": f"{prefix}pbuy (username) (item) (count)", "description": "Buy a certain amount of an item from (username)'s shop"},
                  {"name": f"{prefix}ban (user)/(org) (username)/(organization)", "description": "Ban a certain user or organization from your shop (must have a shop open)"},
                  {"name": f"{prefix}unban (user)/(org) (username)/(organization)", "description": "Unban a certain user or organization from your shop (must have a shop open)"}]

async def print_commands(message: discord.Message):
    em = discord.Embed(title = "Item Commands", description="Commands that work with the item system",
               color=discord.Color.purple())
    for command in commands:
        em.add_field(name=command["name"], value=command["description"], inline=False)
        
    await message.channel.send(embed=em)



async def view_shop(message: discord.Message, target: str):#target is target's username
    target = target.lower()
    users = await economy.get_bank_data()
    shops = await jobs.get_shops_data()
    author = message.author
    
    a = await economy.open_account(message, True) #just to make sure an account has been made

    found: bool = False
    target_id: str = ""         #target's id, not username
    if len(target) > 17:        #if they put in the user's id most likely
        for shop in shops:      #shop is user id
            if shop == target:
                found = True
                target_id = target
        if not found:               #if there is no shop of the username
            await message.channel.send("The id selected does not have a shop open")
            return
    else:
        for shop in shops:          #searches for username
            if shops[shop]["username"]== target:
                found = True
                target_id = shop
        for shop in shops:
            member: discord.Member = await author.guild.fetch_member(shop)           
            if target == member.display_name.lower():       #target is display name
                found = True
                target_id = shop
        if not found:               #if there is no shop of the username
            await message.channel.send("The username selected does not have a shop open")
            return
    
    #shop was found
    
    if shops[target_id]["visible"] == False:
        await message.channel.send("This user has their shop set to not visible")
        return
    
    bannedorgs = shops[target_id]["banned_orgs"]
    bannedusers = shops[target_id]["banned_users"]
    
    for org in bannedorgs:      #checks through banned organizations
        if users[str(author.id)]["organization"] == org["name"]:
            await message.channel.send(f"This shop has been banned for people of the {users[str(author.id)]["organization"]} organization")
            return
    for user in bannedusers:    #checks through banned users
        if users[str(author.id)]["username"] == user["name"]:
            await message.channel.send(f"The owner of this shop has banned you from it")
            return
        
        
    orgs_banned = map(lambda x: x["name"], bannedorgs)
    users_banned = map(lambda x: x["name"], bannedusers)
    #all is clear to view the shop
    orgs_banned = ", ".join(orgs_banned)
    users_banned = ", ".join(users_banned)
    
    
    em = discord.Embed(title=f"{shops[target_id]["username"]}'s shop", 
                       description=f"banned organizations: {orgs_banned}\nspecific banned users: {users_banned}",
                       color=discord.Color.gold())
    
    for item in shops[target_id]["products"]:
        em.add_field(name=item["name"], value=f"count -> {item["count"]}\nprice per unit -> {item["price"]}", inline=False)
        
    await message.channel.send(embed=em)
    




async def buy(message: discord.Message, target: str, item: str, count: int):
    target = target.lower()
    #is_integer
    a = await economy.open_account(message, True) #just to make sure an account has been made
    
    users = await economy.get_bank_data()
    shops = await jobs.get_shops_data()
    author = message.author
    
    found: bool = False
    target_id: str = ""         #target's id, not username
    if len(target) > 17:        #if they put in the user's id most likely
        for shop in shops:      #shop is user id
            if shop == target:
                found = True
                target_id = target
        if not found:               #if there is no shop of the username
            await message.channel.send("The id selected does not have a shop open")
            return
    else:
        for shop in shops:          #searches for username
            if shops[shop]["username"]== target:
                found = True
                target_id = shop
        for shop in shops:
            member: discord.Member = await author.guild.fetch_member(shop)           
            if target == member.display_name.lower():       #target is display name
                found = True
                target_id = shop
        if not found:               #if there is no shop of the username
            await message.channel.send("The username selected does not have a shop open")
            return
    #the shop was found
    
    if shops[target_id]["visible"] == False:
        await message.channel.send("This user has their shop set to not visible")
        return
    
    bannedorgs = shops[target_id]["banned_orgs"]
    bannedusers = shops[target_id]["banned_users"]
    
    for org in bannedorgs:      #checks through banned organizations
        if users[str(author.id)]["organization"] == org["name"]:
            await message.channel.send(f"This shop has been banned for people of the {users[str(author.id)]["organization"]} organization")
            return
    for user in bannedusers:    #checks through banned users
        if users[str(author.id)]["username"] == user["name"]:
            await message.channel.send(f"The owner of this shop has banned you from it")
            return
        
    #You can in fact buy from the shop
    found = False
    for i, product in enumerate(shops[target_id]["products"]):
        if item == product["name"]:
            found = True
            index: int = i
            bought_item = product               #to store the item being bought
    if not found:
        await message.channel.send("The selected item was not found in the player's shop")
        return
    
    #item was found
    if not bought_item["count"] >= count:
        await message.channel.send("Shop doesn't have enough of the item")
        return
    
    
    #there is enough of the item
    spent: bool = await economy.spend_money(message=message, amt=count * bought_item["price"])
    
    if not spent:
        return

    users = await economy.get_bank_data() #because you changed the data, you have to reread it
    
    
    #you can afford it
    await items.add_items_bank(message=message, item=item, count=count, print=True)
    users = await economy.get_bank_data() #with the items added to your account 
    bought_item["count"] -= count
    if bought_item["count"] == 0:
        print(shops[target_id]["products"][i])
        del shops[target_id]["products"][i]
    
    original: int = users[target_id]["wallet"]
    users[target_id]["wallet"] += count * bought_item["price"]
    
    
    with open("playershops.json", "w") as f:
        json.dump(shops, f, indent=2)
    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=2)
        
    await message.channel.send(f"Money added to {users[target_id]["username"]}'s wallet: ${original} -> {users[target_id]["wallet"]}")
    
async def ban(message: discord.Message, type: str, target: str):
    #precondition, type has already been checked to be either "org" or "user"
    a = await economy.open_account(message, True) #just to make sure an account has been made
    users = await economy.get_bank_data()
    shops = await jobs.get_shops_data()
    author = message.author
    
    found: bool = False
    for shop in shops:
        if shop == str(author.id):
            found = True
    if not found:
        await message.channel.send("You do not have a personal shop open")
        return
    
    if type != "user" and type != "org":
        await message.channel.send("You need to input a correct value for field 2. Must be \"user\" or \"org\"")
        return
    
    if type == "user": #if they want to ban a user
        found = False
        for user in users:
            if users[user]["username"] == target:
                found = True
        if not found:
            await message.channel.send("The selected username was not found in my bank system")
            return
        
        found = False
        for banned in shops[str(author.id)]["banned_users"]:
            if banned["name"] == target:
                found = True #if they were found to already be banned
        if found:
           await message.channel.send("The targeted user is already banned")
           return
        #if code reaches here it means the user isn't already banned
        if shops[str(author.id)]["banned_users"][0]["name"] == "": #if the first thing is the default "", remove
            del shops[str(author.id)]["banned_users"][0]
        shops[str(author.id)]["banned_users"].append({"name": target})
        await message.channel.send(f"The user, {target} was successfully banned from your shop")
        
        with open("playershops.json", "w") as f:
            json.dump(shops, f, indent=2)
        return
    
    found = False
    if type == "org":
                
        for banned in shops[str(author.id)]["banned_orgs"]:
            if banned["name"] == target:
                found = True #if the org were found to already be banned
        if found:
           await message.channel.send("The targeted organization is already banned")
           return
        #if code reaches here it means the organization isn't already banned
        if shops[str(author.id)]["banned_orgs"][0]["name"] == "": #if the first thing is the default "", remove
            del shops[str(author.id)]["banned_orgs"][0]
        shops[str(author.id)]["banned_orgs"].append({"name": target})
        await message.channel.send(f"The organization, {target} was successfully banned from your shop")
        
        with open("playershops.json", "w") as f:
            json.dump(shops, f, indent=2)
        return
    
async def unban(message: discord.Message, type: str, target: str):
    a = await economy.open_account(message, True) #just to make sure an account has been made
    users = await economy.get_bank_data()
    shops = await jobs.get_shops_data()
    author = message.author
    
    found: bool = False
    for shop in shops:
        if shop == str(author.id):
            found = True
    if not found:
        await message.channel.send("You do not have a personal shop open")
        return
    
    if type != "user" and type != "org":
        await message.channel.send("You need to input a correct value for field 2. Must be \"user\" or \"org\"")
        return
    
    if type == "user": #if they want to ban a user
        found = False
        for user in users:
            if users[user]["username"] == target:
                found = True
        if not found:
            await message.channel.send("The selected username was not found in my bank system")
            return
        
        found = False
        
        index: int
        for i, banned in enumerate(shops[str(author.id)]["banned_users"]):
            if banned["name"] == target:
                found = True #if they were found to already be banned
                index = i
        if not found:
           await message.channel.send("The targeted user is not banned")
           return
       
        #if code reaches here it means the user is banned
        del shops[str(author.id)]["banned_users"][index]
        if len(shops[str(author.id)]["banned_users"]) == 0:
            shops[str(author.id)]["banned_users"].append({"name": ""})
        await message.channel.send(f"The user, {target} was successfully unbanned from your shop")
        
        with open("playershops.json", "w") as f:
            json.dump(shops, f, indent=2)
        return
    
    found = False
    index: int
    if type == "org":
        for i, banned in enumerate(shops[str(author.id)]["banned_orgs"]):
            if banned["name"] == target:
                found = True #if they were found to already be banned
                index = i
        if not found:
           await message.channel.send("The targeted organization is not banned")
           return
        #if code reaches here it means the organization isn't already banned
        del shops[str(author.id)]["banned_orgs"][index]
        if len(shops[str(author.id)]["banned_orgs"]) == 0:
            shops[str(author.id)]["banned_orgs"].append({"name": ""})
        await message.channel.send(f"The organization, {target} was successfully unbanned from your shop")
        
        with open("playershops.json", "w") as f:
            json.dump(shops, f, indent=2)
        return
    
async def deposit_items(message: discord.Message, item: str, count: int):
    a = await economy.open_account(message, True)
    users = await economy.get_bank_data()
    shops = await jobs.get_shops_data()
    author = message.author
    
    found: bool = False
    for thing in users[str(author.id)]["items"]:
        if thing["name"] == item:
            found = True
            depo_item = thing                   #thing that you are selling
    if not found:
        await message.channel.send("You do not own that item")
        return
    if not depo_item["count"] >= count or depo_item["count"] == 0:
        await message.channel.send("You don't have enough to deposit")
        return
    
    #You have enough of the item
    await items.add_items_shop(message=message, item=item, count=count, print=True)
    await items.add_items_bank(message=message, item=item, count= -1 * count, print=False)
    
    
    
    
    
    
