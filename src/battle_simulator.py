import json
import numpy as np

class Battle_Simulator():
    def __init__(
        self, army_1, army_2
    ):
        self.army_1 = army_1
        self.army_2 = army_2

    # Display the commander pairs
    def present_commanders(self):
        pass

    
    # Display summary of buffs for each army
    def present_buffs(self):
        print(f"\n{colors.HEADER}{colors.BOLD}Report{colors.ENDC}\n")
        print(
            f"\
            Army 1: \n\
                Primary Commander:   Lvl {self.army_1.primary_commander['level']} {self.army_1.primary_commander['name']} {self.army_1.primary_commander['skills_levels']}\n\
                Secondary Commander: Lvl {self.army_1.secondary_commander['level']} {self.army_1.secondary_commander['name']} {self.army_1.secondary_commander['skills_levels']}\n\
                \n\
                Troop Buffs:\n\
                    Infantry Attack:  {colors.YELLOW}{self.army_1.total_buffs['infantry']['attack']}%{colors.ENDC}\n\
                    Infantry Defense: {colors.YELLOW}{self.army_1.total_buffs['infantry']['defense']}%{colors.ENDC}\n\
                    Infantry Health:  {colors.YELLOW}{self.army_1.total_buffs['infantry']['health']}%{colors.ENDC}\n\
                    Cavalry Attack:   {colors.YELLOW}{self.army_1.total_buffs['cavalry']['attack']}%{colors.ENDC}\n\
                    Cavalry Defense:  {colors.YELLOW}{self.army_1.total_buffs['cavalry']['defense']}%{colors.ENDC}\n\
                    Cavalry Health:   {colors.YELLOW}{self.army_1.total_buffs['cavalry']['health']}%{colors.ENDC}\n\
                    Archer Attack:    {colors.YELLOW}{self.army_1.total_buffs['archer']['attack']}%{colors.ENDC}\n\
                    Archer Defense:   {colors.YELLOW}{self.army_1.total_buffs['archer']['defense']}%{colors.ENDC}\n\
                    Archer Health:    {colors.YELLOW}{self.army_1.total_buffs['archer']['health']}%{colors.ENDC}\n\
        ")
        print(
            f"\
            Army 2: \n\
                Primary Commander:   Lvl {self.army_2.primary_commander['level']} {self.army_2.primary_commander['name']} {self.army_2.primary_commander['skills_levels']}\n\
                Secondary Commander: Lvl {self.army_2.secondary_commander['level']} {self.army_2.secondary_commander['name']} {self.army_2.secondary_commander['skills_levels']}\n\
                \n\
                Troop Buffs:\n\
                    Infantry Attack:  {colors.YELLOW}{self.army_2.total_buffs['infantry']['attack']}%{colors.ENDC}\n\
                    Infantry Defense: {colors.YELLOW}{self.army_2.total_buffs['infantry']['defense']}%{colors.ENDC}\n\
                    Infantry Health:  {colors.YELLOW}{self.army_2.total_buffs['infantry']['health']}%{colors.ENDC}\n\
                    Cavalry Attack:   {colors.YELLOW}{self.army_2.total_buffs['cavalry']['attack']}%{colors.ENDC}\n\
                    Cavalry Defense:  {colors.YELLOW}{self.army_2.total_buffs['cavalry']['defense']}%{colors.ENDC}\n\
                    Cavalry Health:   {colors.YELLOW}{self.army_2.total_buffs['cavalry']['health']}%{colors.ENDC}\n\
                    Archer Attack:    {colors.YELLOW}{self.army_2.total_buffs['archer']['attack']}%{colors.ENDC}\n\
                    Archer Defense:   {colors.YELLOW}{self.army_2.total_buffs['archer']['defense']}%{colors.ENDC}\n\
                    Archer Health:    {colors.YELLOW}{self.army_2.total_buffs['archer']['health']}%{colors.ENDC}\n\
        ")

    # Start the combat simulation
    def fight(self):
        # Initialize the fight
        self.present_buffs()
        trigger_active_skill_1 = 0
        trigger_active_skill_2 = 0
        attack_rage_generation = 86
        counterattack_rage_generation = 16
        compensation_rage_generation = 10
        turn = 1

        print(f"{colors.HEADER}{colors.BOLD}Battle Log{colors.ENDC}\n")
        
        # Begin battle loop
        while (self.army_1.troop_count > 0 and self.army_2.troop_count > 0):
            army_1_skill_losses = 0
            army_2_skill_losses = 0

            # Normal attacks
            # Army 1
            army_1_dmg = (self.army_1.buffed_stats["attack"] * self.army_1.troop_count) / self.army_2.buffed_stats["defense"] * 2
            army_2_losses = army_1_dmg / self.army_2.buffed_stats["health"]
            army_2_losses *= np.sqrt(10000 / self.army_1.troop_count)
            army_2_losses = np.ceil(army_2_losses)
            army_2_losses = int(army_2_losses)
            self.army_1.rage += attack_rage_generation
            # Army 2
            army_2_dmg = (self.army_2.buffed_stats["attack"] * self.army_2.troop_count) / self.army_1.buffed_stats["defense"] * 2
            army_1_losses = army_2_dmg / self.army_1.buffed_stats["health"]
            army_1_losses *= np.sqrt(10000 / self.army_2.troop_count)
            army_1_losses = np.ceil(army_1_losses)
            army_1_losses = int(army_1_losses)
            self.army_2.rage += attack_rage_generation

            # Counter attacks
            # Army 1
            army_1_counter_dmg = (self.army_1.buffed_stats["attack"] * self.army_1.troop_count) / self.army_2.buffed_stats["defense"] * 2
            army_2_counter_losses = army_1_counter_dmg / self.army_2.buffed_stats["health"]
            army_2_counter_losses *= np.sqrt(10000 / self.army_1.troop_count)
            army_2_counter_losses = np.ceil(army_2_counter_losses)
            army_2_counter_losses = int(army_2_counter_losses)
            self.army_1.rage += counterattack_rage_generation
            # Army 2
            army_2_counter_dmg = (self.army_2.buffed_stats["attack"] * self.army_2.troop_count) / self.army_1.buffed_stats["defense"] * 2
            army_1_counter_losses = army_2_counter_dmg / self.army_1.buffed_stats["health"]
            army_1_counter_losses *= np.sqrt(10000 / self.army_2.troop_count)
            army_1_counter_losses = np.ceil(army_1_counter_losses)
            army_1_counter_losses = int(army_1_counter_losses)
            self.army_2.rage += counterattack_rage_generation

            # Rage compensation generation
            if army_1_losses > army_2_losses:
                self.army_1.rage += compensation_rage_generation
            elif army_2_losses > army_1_losses:
                self.army_2.rage += compensation_rage_generation
            if army_1_counter_losses > army_2_counter_losses:
                self.army_1.rage += compensation_rage_generation
            elif army_2_counter_losses > army_1_counter_losses:
                self.army_2.rage += compensation_rage_generation
            
            # Active skills
            '''
            trigger_active_skill_x == 0 --> Nothing happens
            trigger_active_skill_1 == 1 --> Notify Army 1 Primary Commander will trigger
            trigger_active_skill_1 == 2 --> Army 1 Primary Commander skill is triggered
            trigger_active_skill_1 == 3 --> Notify Army 1 Secondary Commander will trigger
            trigger_active_skill_1 == 4 --> Army 1 Secondary Commander skill is triggered
            '''
            # Update active skill trigger count
            # Army 1
            if trigger_active_skill_1 in (1, 3, 4):
                trigger_active_skill_1 += 1
            elif trigger_active_skill_1 == 2:  # Temporize until second skill trigger
                if self.army_1.secondary_commander['name']:  # Check if secondary commander available
                    trigger_active_skill_1 += 1
                else:
                    trigger_active_skill_1 = 0  # If no secondary, stop and reset count
            elif trigger_active_skill_1 == 5:  # Both active skills have triggered
                trigger_active_skill_1 = 0
            # Army 2
            if trigger_active_skill_2 in (1, 3, 4):
                trigger_active_skill_2 += 1
            elif trigger_active_skill_2 == 2:
                if self.army_2.secondary_commander['name']:
                    trigger_active_skill_2 += 1
                else:
                    trigger_active_skill_2 = 0
            elif trigger_active_skill_2 == 5:
                trigger_active_skill_2 = 0

            # Check for active skills
            if self.army_1.rage >= self.army_1.active_skills[0]["rage_requirement"]:
                trigger_active_skill_1 = 1
                self.army_1.rage = 0
            if self.army_2.rage >= self.army_2.active_skills[0]["rage_requirement"]:
                trigger_active_skill_2 = 1
                self.army_2.rage = 0

            # Compute active skill dmg
            # Army 1
            if trigger_active_skill_1 == 2:  # Trigger primary
                skill_level = self.army_1.primary_commander['skills_levels'][0] - 1
                dmg_factor = self.army_1.active_skills[0]["stats"][0][skill_level]
                army_1_skill_dmg = army_1_dmg / 2 * (dmg_factor/100)
                army_2_skill_losses = army_1_skill_dmg / self.army_2.buffed_stats["health"]
                army_2_skill_losses *= np.sqrt(10000 / self.army_1.troop_count)
                army_2_skill_losses = np.ceil(army_2_skill_losses)
                army_2_skill_losses = int(army_2_skill_losses)
                self.army_1.rage += attack_rage_generation
            elif trigger_active_skill_1 == 4:  # Trigger secondary
                skill_level = self.army_1.secondary_commander['skills_levels'][0] - 1
                dmg_factor = self.army_1.active_skills[1]["stats"][0][skill_level]
                army_1_skill_dmg = army_1_dmg / 2 * (dmg_factor/100)
                army_2_skill_losses = army_1_skill_dmg / self.army_2.buffed_stats["health"]
                army_2_skill_losses *= np.sqrt(10000 / self.army_1.troop_count)
                army_2_skill_losses = np.ceil(army_2_skill_losses)
                army_2_skill_losses = int(army_2_skill_losses)
            # Army 2
            if trigger_active_skill_2 == 2:  # Trigger primary
                skill_level = self.army_2.primary_commander['skills_levels'][0] - 1
                dmg_factor = self.army_2.active_skills[0]["stats"][0][skill_level]
                army_2_skill_dmg = army_2_dmg / 2 * (dmg_factor/100)
                army_1_skill_losses = army_2_skill_dmg / self.army_1.buffed_stats["health"]
                army_1_skill_losses *= np.sqrt(10000 / self.army_2.troop_count)
                army_1_skill_losses = np.ceil(army_1_skill_losses)
                army_1_skill_losses = int(army_1_skill_losses)
                self.army_2.rage += attack_rage_generation
            elif trigger_active_skill_2 == 4:  # Trigger secondary
                skill_level = self.army_2.secondary_commander['skills_levels'][0] - 1
                dmg_factor = self.army_2.active_skills[1]["stats"][0][skill_level]
                army_2_skill_dmg = army_2_dmg / 2 * (dmg_factor/100)
                army_1_skill_losses = army_2_skill_dmg / self.army_1.buffed_stats["health"]
                army_1_skill_losses *= np.sqrt(10000 / self.army_2.troop_count)
                army_1_skill_losses = np.ceil(army_1_skill_losses)
                army_1_skill_losses = int(army_1_skill_losses)


            # Result log
            print(f"Turn {turn}\n\
                {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} ({self.army_1.troop_count}) attacked {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC}, {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_2_losses}{colors.ENDC} units\n\
                {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} launched a counterattack, {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_1_counter_losses}{colors.ENDC} units\n\n\
                {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} ({self.army_2.troop_count}) attacked {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC}, {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_1_losses}{colors.ENDC} units\n\
                {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} launched a counterattack, {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_2_counter_losses}{colors.ENDC} units\n\n\
                ")
            # Army 1
            if trigger_active_skill_1 == 1:  # Announce primary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_1 == 2:  # Actual primary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} cast their active skill!\n\
                    {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_2_skill_losses}{colors.ENDC} units\n\
                    ")
            elif trigger_active_skill_1 == 3:  # Announce secondary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.secondary_commander['name']}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_1 == 4:  # Actual secondary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.secondary_commander['name']}]{colors.ENDC} cast their active skill!\n\
                    {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_2_skill_losses}{colors.ENDC} units\n\
                    ")
            # Army 2
            if trigger_active_skill_2 == 1:  # Announce primary trigger
                print(f"\
                    {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_2 == 2:  # Actual primary trigger
                print(f"\
                    {colors.RED}[{self.army_2.primary_commander['name']}]{colors.ENDC} cast their active skill!\n\
                    {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_1_skill_losses}{colors.ENDC} units\n\
                    ")
            elif trigger_active_skill_2 == 3:  # Announce secondary trigger
                print(f"\
                    {colors.RED}[{self.army_2.secondary_commander['name']}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_2 == 4:  # Actual secondary trigger
                print(f"\
                    {colors.RED}[{self.army_2.secondary_commander['name']}]{colors.ENDC} cast their active skill!\n\
                    {colors.GREEN}[{self.army_1.primary_commander['name']}]{colors.ENDC} lost {colors.YELLOW}{army_1_skill_losses}{colors.ENDC} units\n\
                    ")


            # Update armies troop counts
            self.army_1.troop_count -= (army_1_losses + army_1_counter_losses + army_1_skill_losses)
            self.army_1.troop_count = int(self.army_1.troop_count)
            self.army_2.troop_count -= (army_2_losses + army_2_counter_losses + army_2_skill_losses)
            self.army_2.troop_count = int(self.army_2.troop_count)

            # Head to next turn
            turn += 1
        
        # Define the winner
        winner = self.army_1 if self.army_1.troop_count > 0 else self.army_2
        
        # End of battle log
        c = colors.GREEN if self.army_1.troop_count > 0 else colors.RED
        print(f"End of Battle\n\
            {c}[{winner.primary_commander['name']}]{colors.ENDC} ({winner.troop_count}) won the battle\n\
            ")



class colors:
    RED =    '\033[31m'
    GREEN =  '\033[32m'
    YELLOW = '\033[33m'
    BLUE =   '\033[34m'
    HEADER = '\033[95m'
    BOLD =   '\033[1m'
    ENDC =   '\033[0;0m'