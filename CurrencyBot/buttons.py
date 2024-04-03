import discord
import combat
import json

class TestView(discord.ui.View):
    
    job: str = ""
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timedout (Took too long)")
        await self.disable_all_items()
    
    @discord.ui.button(label="None", style=discord.ButtonStyle.blurple)
    async def none(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("You now have no job")
        self.job = "none"
        self.stop()
    
    @discord.ui.button(label="Police", style=discord.ButtonStyle.blurple)
    async def police(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("you are now a police officer")
        self.job = "police"
        self.stop()
        
    @discord.ui.button(label="Doctor", style=discord.ButtonStyle.blurple)
    async def doctor(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message("you are now a doctor")
        self.job = "doctor"
        self.stop()
        
class CombatUserSelect(discord.ui.View):
    user1: str = ""
    username1: str = ""
    user2: str = ""
    username2: str = ""
    count: int = 0
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    async def on_timeout(self) -> None:
        await self.message.channel.send("Fight stopped, users took >1 min to start fight")
        await self.disable_all_items()
        
    @discord.ui.button(label="Fighter 1", style=discord.ButtonStyle.blurple)
    async def player1(self, interaction: discord.Interaction, button: discord.ui.button):
        
        if interaction.user.id == self.user2 or interaction.user.id == self.user1: #if you are already in the game
            await interaction.response.send_message("You are already in the game man. Don't be greedy", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{interaction.user.mention} you are now player 1")
        if self.user1 != "":
            self.count -= 1
        self.user1 = interaction.user.id
        self.username1 = str(interaction.user)
        button.disabled = True
        self.count += 1
        await self.message.edit(view=self)
        
        
        if self.count >= 2:
            self.stop()
        
    @discord.ui.button(label="Fighter 2", style=discord.ButtonStyle.blurple)
    async def player2(self, interaction: discord.Interaction, button: discord.ui.button):
        
        if interaction.user.id == self.user2 or interaction.user.id == self.user1: #if you are already in the game
            await interaction.response.send_message("You are already in the game man. Don't be greedy", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{interaction.user.mention} you are now player 2")
        if self.user2 != "":
            self.count -= 1
        self.user2 = interaction.user.id
        self.username2 = str(interaction.user)
        button.disabled = True
        self.count += 1
        await self.message.edit(view=self)
        
        
        if self.count >= 2:
            self.stop()

 
class CombatTurns(discord.ui.View):
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    async def on_timeout(self) -> None:
        await self.message.channel.send("Fight forfeited. Someone took >2 min to make a move. All money returned")
        await self.disable_all_items()
    
        
    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red) #print the attack selection menu
    async def attack(self, interaction: discord.Interaction, button: discord.ui.button):
        combat_info = await combat.get_combat_info()
        #currently only for player1, implement system for player 2 as well with an if statment with %turns == 0
        turn: int = combat_info["battle"]["turn"]
        if turn%2 == 1:
            if str(interaction.user.id) != combat_info["battle"]["user1"]:
                await interaction.response.send_message("It's not your turn you dumbo wumbo", ephemeral=True)
                return
            async def my_callback(interaction: discord.Interaction):
                await interaction.channel.send(f"{combat_info['battle']["username1"]} selected {select.values[0]} as their weapon")
                await combat.p1_attack(message=self.message, weapon=select.values[0])
                combat_info_inner = await combat.get_combat_info()
                combat_info_inner["battle"]["timed_out"] = False
                with open("combat.json", "w") as f:
                    json.dump(combat_info_inner, f, indent=2)
                self.stop()
                
            select = await combat.get_atk_select_p1()
            select.callback = my_callback
            view = discord.ui.View()
            view.add_item(select)
            await interaction.channel.send("Player 1 is choosing their attack...")
            await interaction.response.send_message("Please select a way of attack: ", view=view, ephemeral=True)
        else:
            if str(interaction.user.id) != combat_info["battle"]["user2"]:
                await interaction.response.send_message("It's not your turn you dumbo wumbo", ephemeral=True)
                return
            async def my_callback(interaction: discord.Interaction):
                await interaction.channel.send(f"{combat_info['battle']["username2"]} selected {select.values[0]} as their weapon")
                await combat.p2_attack(message=self.message, weapon=select.values[0])
                combat_info_inner = await combat.get_combat_info()
                combat_info_inner["battle"]["timed_out"] = False
                with open("combat.json", "w") as f:
                    json.dump(combat_info_inner, f, indent=2)
                self.stop()
                
            select = await combat.get_atk_select_p2()
            select.callback = my_callback
            view = discord.ui.View()
            view.add_item(select)
            await interaction.channel.send("Player 2 is choosing their attack...")
            await interaction.response.send_message("Please select a way of attack: ", view=view, ephemeral=True) 
        
            


        
        
        
