import buttons
import json
import discord
import economy
import items

async def start(message: discord.Message, bet: int):
    
    combat_info = await get_combat_info()
    users = await economy.get_bank_data()
    if len(combat_info) > 0:
        await message.channel.send("A battle is already in process")
        return

    combat_info["battle"] = {}
    combat_info["battle"]["user1"] = ""
    combat_info["battle"]["username1"] = ""
    combat_info["battle"]["user1health"] = ""
    combat_info["battle"]["user2"] = ""
    combat_info["battle"]["username2"] = ""
    combat_info["battle"]["user2health"] = ""
    combat_info["battle"]["turn"] = 0
    combat_info["battle"]["timed_out"] = True
    with open("combat.json", "w") as f:
        json.dump(combat_info, f, indent=2)
    combat_info = await get_combat_info()
    
    view = buttons.CombatUserSelect(timeout=60)
    
    
    button_msg = await message.reply("Player selection for a non started fight; you have 60 seconds", view=view)
    view.message = button_msg
    
    await view.wait()
    await view.disable_all_items()

    if view.user1 == "" or view.user2 == "":
        del combat_info["battle"]
        with open("combat.json", "w") as f:
            json.dump(combat_info, f, indent=2)
        return
    
    combat_info["battle"]["user1"] = str(view.user1)
    combat_info["battle"]["username1"] = view.username1
    combat_info["battle"]["user1health"] = users[str(view.user1)]["health"]
    combat_info["battle"]["user2"] = str(view.user2)
    combat_info["battle"]["username2"] = view.username2
    combat_info["battle"]["user2health"] = users[str(view.user2)]["health"]
    combat_info["battle"]["turn"] = 1
    
    #checks if both players have enough for the bet
    if users[combat_info["battle"]["user1"]]["wallet"] < bet:
        await message.channel.send(f"{view.username1} does not have enough money in their walletfor the bet :(")
        return
    if users[combat_info["battle"]["user2"]]["wallet"] < bet:
        await message.channel.send(f"{view.username2} does not have enough money  in their wallet for the bet :(")
        return
    
    
    with open("combat.json", "w") as f:
        json.dump(combat_info, f, indent=2)
    
    await turns(message=message, bet=bet)
    return
    
    
    
async def turns(message: discord.Message, bet: int):
    users = await economy.get_bank_data()
    combat_info = await get_combat_info()
    user1: str = combat_info["battle"]["user1"]
    user2: str = combat_info["battle"]["user2"]
    
    while combat_info["battle"]["user1health"] > 0 and combat_info["battle"]["user2health"] > 0:
        view = buttons.CombatTurns(timeout=60)
        turn = combat_info["battle"]["turn"]
        if turn%2 == 1:
            button_msg = await message.channel.send(f"It is {combat_info["battle"]["username1"]}'s turn. Please choose an option", view=view)
            view.message = button_msg
            await view.wait()
            combat_info = await get_combat_info()
            if combat_info["battle"]["timed_out"]:
                break
            await view.disable_all_items()
            combat_info["battle"]["timed_out"] = True
        else:
            button_msg = await message.channel.send(f"It is {combat_info["battle"]["username2"]}'s turn. Please choose an option", view=view)
            view.message = button_msg
            await view.wait()
            combat_info = await get_combat_info()
            if combat_info["battle"]["timed_out"]:
                break
            print(f"p2: {combat_info["battle"]["timed_out"]}")
            await view.disable_all_items()
            combat_info["battle"]["timed_out"] = True
        
        combat_info["battle"]["turn"] += 1
        with open("combat.json", "w") as f:
            json.dump(combat_info, f, indent=2)
    
    print("while loop exited")
    users = await economy.get_bank_data()
    if combat_info["battle"]["user1health"] <= 0:
        await message.channel.send(f"{combat_info["battle"]["username2"]} won the battle and won ${bet}")
        users[user2]["wallet"] += bet
        users[user1]["wallet"] -= bet
        del combat_info["battle"]
        with open("combat.json", "w") as f:
            json.dump(combat_info, f, indent=2)
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)    
        return
    elif combat_info["battle"]["user2health"] <= 0:
        await message.channel.send(f"{combat_info["battle"]["username1"]} won the battle and won ${bet}")
        users[user1]["wallet"] += bet
        users[user2]["wallet"] -= bet
        del combat_info["battle"]
        with open("combat.json", "w") as f:
            json.dump(combat_info, f, indent=2)
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
        return
    else:
        print("timed out")
        del combat_info["battle"]
        with open("combat.json", "w") as f:
            json.dump(combat_info, f, indent=2)
        return
    
    
async def get_player1_attacks():
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    weapon_options = await items.get_atk_items()
    user1_weapons = []# weapon names that you have
    for item in users[combat["battle"]["user1"]]["items"]:
        for weapon_option in weapon_options:
            if item["name"] == weapon_option["label"]: #checks if your item is a valid atk item
                user1_weapons.append(item["name"])
    return user1_weapons
    
    
async def get_atk_select_p1():
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    weapon_options = await items.get_atk_items()
    user1_weapons = await get_player1_attacks()
    options = [discord.SelectOption(label=weapon_options[0]["label"], emoji=weapon_options[0]["emoji"], description=weapon_options[0]["description"])]
    
    for weapon in weapon_options: #adds all your weapons to the selection list
        if weapon["label"] in user1_weapons:
            options.append(discord.SelectOption(label=weapon["label"], emoji=weapon["emoji"], description=weapon["description"]))    
            
    select = discord.ui.Select(placeholder="choose an attack", options=options)
    return select
    
    
async def p1_attack(message: discord.Message, weapon: str):
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    dmg: int = 0
    if weapon == "fist":
        dmg = 5
    if weapon == "gold_banana":
        dmg = combat["battle"]["user2health"]
    if weapon == "sniper":
        dmg = 40
    if weapon == "machine_gun":
        dmg = 30
    if weapon == "pistol":
        dmg = 20
    if weapon == "shotgun":
        dmg = 25
    
    combat["battle"]["user2health"] -= dmg
    with open("combat.json", "w") as f:
        json.dump(combat, f, indent=2)
        
    await message.channel.send(f"{combat["battle"]["username1"]} did {dmg} dmg to {combat["battle"]["username2"]} with a {weapon}")
    
    
    
async def get_player2_attacks():
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    weapon_options = await items.get_atk_items()
    user2_weapons = []# weapon names that you have
    for item in users[combat["battle"]["user2"]]["items"]:
        for weapon_option in weapon_options:
            if item["name"] == weapon_option["label"]: #checks if your item is a valid atk item
                user2_weapons.append(item["name"])
    return user2_weapons

async def get_atk_select_p2():
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    weapon_options = await items.get_atk_items()
    user2_weapons = await get_player2_attacks()
    options = [discord.SelectOption(label=weapon_options[0]["label"], emoji=weapon_options[0]["emoji"], description=weapon_options[0]["description"])]
    
    for weapon in weapon_options: #adds all your weapons to the selection list
        if weapon["label"] in user2_weapons:
            options.append(discord.SelectOption(label=weapon["label"], emoji=weapon["emoji"], description=weapon["description"]))    
            
    select = discord.ui.Select(placeholder="choose an attack", options=options)
    return select

async def p2_attack(message: discord.Message, weapon: str):
    users = await economy.get_bank_data()
    combat = await get_combat_info()
    dmg: int = 0
    if weapon == "fist":
        dmg = 5
    if weapon == "gold_banana":
        dmg = combat["battle"]["user1health"]
    if weapon == "sniper":
        dmg = 40
    if weapon == "machine_gun":
        dmg = 30
    if weapon == "pistol":
        dmg = 20
    if weapon == "shotgun":
        dmg = 25
    
    combat["battle"]["user1health"] -= dmg
    with open("combat.json", "w") as f:
        json.dump(combat, f, indent=2)
        
    await message.channel.send(f"{combat["battle"]["username2"]} did {dmg} dmg to {combat["battle"]["username1"]} with a {weapon}")
    
    
async def get_combat_info():
    with open("combat.json", "r") as f:
        combat = json.load(f)
        return combat