# Authors: Aro2152
# Copyright (C) 2022 Aro2152

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
        for i, army in enumerate([self.army_1, self.army_2]):
            print(
                f"\
                Army {i+1}: \n\
                    Primary Commander:   Lvl {army.primary_commander.level} {army.primary_commander.name} {army.primary_commander.skills_levels}\
                ")
            if army.secondary_commander:
                print(
                    f"\
                    Secondary Commander: Lvl {army.secondary_commander.level} {army.secondary_commander.name} {army.secondary_commander.skills_levels}\n\
                    ")
            else:
                print(
                    f"\
                    Secondary Commander: None\n\
                    ")
            print(
                f"\
                    \n\
                    Troop Buffs:\n\
                        Infantry Attack:  {colors.YELLOW}{army.total_buffs['attack']['infantry']}%{colors.ENDC}\n\
                        Infantry Defense: {colors.YELLOW}{army.total_buffs['defense']['infantry']}%{colors.ENDC}\n\
                        Infantry Health:  {colors.YELLOW}{army.total_buffs['health']['infantry']}%{colors.ENDC}\n\
                        Cavalry Attack:   {colors.YELLOW}{army.total_buffs['attack']['cavalry']}%{colors.ENDC}\n\
                        Cavalry Defense:  {colors.YELLOW}{army.total_buffs['defense']['cavalry']}%{colors.ENDC}\n\
                        Cavalry Health:   {colors.YELLOW}{army.total_buffs['health']['cavalry']}%{colors.ENDC}\n\
                        Archer Attack:    {colors.YELLOW}{army.total_buffs['attack']['archer']}%{colors.ENDC}\n\
                        Archer Defense:   {colors.YELLOW}{army.total_buffs['defense']['archer']}%{colors.ENDC}\n\
                        Archer Health:    {colors.YELLOW}{army.total_buffs['health']['archer']}%{colors.ENDC}\n\
                        Siege Attack:     {colors.YELLOW}{army.total_buffs['attack']['siege']}%{colors.ENDC}\n\
                        Siege Defense:    {colors.YELLOW}{army.total_buffs['defense']['siege']}%{colors.ENDC}\n\
                        Siege Health:     {colors.YELLOW}{army.total_buffs['health']['siege']}%{colors.ENDC}\n\
                    Additional Buffs:\n\
                        Damage:                   {colors.YELLOW}{army.total_buffs['damage']}%{colors.ENDC}\n\
                        Skill Damage:             {colors.YELLOW}{army.total_buffs['skill_damage']}%{colors.ENDC}\n\
                        Additional Skill Damage:  {colors.YELLOW}{army.total_buffs['additional_skill_damage']}%{colors.ENDC}\n\
                        Reduce Damage Taken:      {colors.YELLOW}{army.total_buffs['reduce_damage_taken']}%{colors.ENDC}\n\
                        Reduce Skil Damage Taken: {colors.YELLOW}{army.total_buffs['reduce_skill_damage_taken']}%{colors.ENDC}\n\
                        Normal Attack Damage:     {colors.YELLOW}{army.total_buffs['normal_attack_damage']}%{colors.ENDC}\n\
                        Counter Attack Damage:    {colors.YELLOW}{army.total_buffs['counter_attack_damage']}%{colors.ENDC}\n\
                        March Speed:              {colors.YELLOW}{army.total_buffs['march_speed']}%{colors.ENDC}\n\
                ")

    # Start the combat simulation
    def fight(self):
        # Initialize the fight
        self.present_buffs()
        trigger_active_skill_1 = 0
        trigger_active_skill_2 = 0
        accumulated_rage_1 = 0
        accumulated_rage_2 = 0
        attack_rage_generation = 86
        counterattack_rage_generation = 16
        compensation_rage_generation = 10
        rage_accumulation_limit = 220
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
            accumulated_rage_1 += attack_rage_generation
            # Army 2
            army_2_dmg = (self.army_2.buffed_stats["attack"] * self.army_2.troop_count) / self.army_1.buffed_stats["defense"] * 2
            army_1_losses = army_2_dmg / self.army_1.buffed_stats["health"]
            army_1_losses *= np.sqrt(10000 / self.army_2.troop_count)
            army_1_losses = np.ceil(army_1_losses)
            army_1_losses = int(army_1_losses)
            accumulated_rage_2 += attack_rage_generation

            # Counter attacks
            # Army 1
            army_1_counter_dmg = (self.army_1.buffed_stats["attack"] * self.army_1.troop_count) / self.army_2.buffed_stats["defense"] * 2
            army_2_counter_losses = army_1_counter_dmg / self.army_2.buffed_stats["health"]
            army_2_counter_losses *= np.sqrt(10000 / self.army_1.troop_count)
            army_2_counter_losses = np.ceil(army_2_counter_losses)
            army_2_counter_losses = int(army_2_counter_losses)
            accumulated_rage_1 += counterattack_rage_generation
            # Army 2
            army_2_counter_dmg = (self.army_2.buffed_stats["attack"] * self.army_2.troop_count) / self.army_1.buffed_stats["defense"] * 2
            army_1_counter_losses = army_2_counter_dmg / self.army_1.buffed_stats["health"]
            army_1_counter_losses *= np.sqrt(10000 / self.army_2.troop_count)
            army_1_counter_losses = np.ceil(army_1_counter_losses)
            army_1_counter_losses = int(army_1_counter_losses)
            accumulated_rage_2 += counterattack_rage_generation

            # Rage compensation generation
            if army_1_losses > army_2_losses:
                accumulated_rage_1 += compensation_rage_generation
            elif army_2_losses > army_1_losses:
                accumulated_rage_2 += compensation_rage_generation
            if army_1_counter_losses > army_2_counter_losses:
                accumulated_rage_1 += compensation_rage_generation
            elif army_2_counter_losses > army_1_counter_losses:
                accumulated_rage_2 += compensation_rage_generation
            
            # Active skills
            '''
            trigger_active_skill_1 == 0 --> Nothing happens
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
                if self.army_1.secondary_commander:  # Check if secondary commander available
                    trigger_active_skill_1 += 1
                else:
                    trigger_active_skill_1 = 0  # If no secondary, stop and reset count
            elif trigger_active_skill_1 == 5:  # Both active skills have triggered
                trigger_active_skill_1 = 0
            # Army 2
            if trigger_active_skill_2 in (1, 3, 4):
                trigger_active_skill_2 += 1
            elif trigger_active_skill_2 == 2:
                if self.army_2.secondary_commander:
                    trigger_active_skill_2 += 1
                else:
                    trigger_active_skill_2 = 0
            elif trigger_active_skill_2 == 5:
                trigger_active_skill_2 = 0

            # Regulate accumulated rage
            if accumulated_rage_1 > rage_accumulation_limit:
                accumulated_rage_1 = rage_accumulation_limit
            if accumulated_rage_2 > rage_accumulation_limit:
                accumulated_rage_2 = rage_accumulation_limit
            # Add accumulated rage
            self.army_1.rage += accumulated_rage_1
            self.army_2.rage += accumulated_rage_2
            # Reset accumulated rage
            accumulated_rage_1 = 0
            accumulated_rage_2 = 0

            # Check for active skills
            if self.army_1.rage >= self.army_1.primary_commander.skills[self.army_1.primary_commander.active_skill]["rage_requirement"]:
                trigger_active_skill_1 = 1
                self.army_1.rage = 0
            if self.army_2.rage >= self.army_2.primary_commander.skills[self.army_2.primary_commander.active_skill]["rage_requirement"]:
                trigger_active_skill_2 = 1
                self.army_2.rage = 0

            # Compute active skill dmg
            # Army 1
            if trigger_active_skill_1 == 2:  # Trigger primary
                dmg_factor = self.army_1.primary_commander.skills[self.army_1.primary_commander.active_skill]["buffs"]["direct_damage_factor"]["direct_damage_factor"]
                army_1_skill_dmg = army_1_dmg / 2 * (dmg_factor/100)
                army_2_skill_losses = army_1_skill_dmg / self.army_2.buffed_stats["health"]
                army_2_skill_losses *= np.sqrt(10000 / self.army_1.troop_count)
                army_2_skill_losses = np.ceil(army_2_skill_losses)
                army_2_skill_losses = int(army_2_skill_losses)
                self.army_1.rage += attack_rage_generation
            elif trigger_active_skill_1 == 4:  # Trigger secondary
                dmg_factor = self.army_1.secondary_commander.skills[self.army_1.secondary_commander.active_skill]["buffs"]["direct_damage_factor"]["direct_damage_factor"]
                army_1_skill_dmg = army_1_dmg / 2 * (dmg_factor/100)
                army_2_skill_losses = army_1_skill_dmg / self.army_2.buffed_stats["health"]
                army_2_skill_losses *= np.sqrt(10000 / self.army_1.troop_count)
                army_2_skill_losses = np.ceil(army_2_skill_losses)
                army_2_skill_losses = int(army_2_skill_losses)
            # Army 2
            if trigger_active_skill_2 == 2:  # Trigger primary
                dmg_factor = self.army_2.primary_commander.skills[self.army_2.primary_commander.active_skill]["buffs"]["direct_damage_factor"]["direct_damage_factor"]
                army_2_skill_dmg = army_2_dmg / 2 * (dmg_factor/100)
                army_1_skill_losses = army_2_skill_dmg / self.army_1.buffed_stats["health"]
                army_1_skill_losses *= np.sqrt(10000 / self.army_2.troop_count)
                army_1_skill_losses = np.ceil(army_1_skill_losses)
                army_1_skill_losses = int(army_1_skill_losses)
                self.army_2.rage += attack_rage_generation
            elif trigger_active_skill_2 == 4:  # Trigger secondary
                dmg_factor = self.army_2.secondary_commander.skills[self.army_2.secondary_commander.active_skill]["buffs"]["direct_damage_factor"]["direct_damage_factor"]
                army_2_skill_dmg = army_2_dmg / 2 * (dmg_factor/100)
                army_1_skill_losses = army_2_skill_dmg / self.army_1.buffed_stats["health"]
                army_1_skill_losses *= np.sqrt(10000 / self.army_2.troop_count)
                army_1_skill_losses = np.ceil(army_1_skill_losses)
                army_1_skill_losses = int(army_1_skill_losses)


            # Result log
            print(f"Turn {turn}\n\
                {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} ({self.army_1.troop_count}) attacked {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC}, {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_2_losses}{colors.ENDC} units\n\
                {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} launched a counterattack, {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_1_counter_losses}{colors.ENDC} units\n\n\
                {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} ({self.army_2.troop_count}) attacked {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC}, {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_1_losses}{colors.ENDC} units\n\
                {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} launched a counterattack, {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_2_counter_losses}{colors.ENDC} units\n\n\
                ")
            # Army 1
            if trigger_active_skill_1 == 1:  # Announce primary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_1 == 2:  # Actual primary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} cast their active skill!\n\
                    {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_2_skill_losses}{colors.ENDC} units\n\
                    ")
            elif trigger_active_skill_1 == 3:  # Announce secondary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.secondary_commander.name}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_1 == 4:  # Actual secondary trigger
                print(f"\
                    {colors.GREEN}[{self.army_1.secondary_commander.name}]{colors.ENDC} cast their active skill!\n\
                    {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_2_skill_losses}{colors.ENDC} units\n\
                    ")
            # Army 2
            if trigger_active_skill_2 == 1:  # Announce primary trigger
                print(f"\
                    {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_2 == 2:  # Actual primary trigger
                print(f"\
                    {colors.RED}[{self.army_2.primary_commander.name}]{colors.ENDC} cast their active skill!\n\
                    {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_1_skill_losses}{colors.ENDC} units\n\
                    ")
            elif trigger_active_skill_2 == 3:  # Announce secondary trigger
                print(f"\
                    {colors.RED}[{self.army_2.secondary_commander.name}]{colors.ENDC} is going to activate an active skill!\n\
                    ")
            elif trigger_active_skill_2 == 4:  # Actual secondary trigger
                print(f"\
                    {colors.RED}[{self.army_2.secondary_commander.name}]{colors.ENDC} cast their active skill!\n\
                    {colors.GREEN}[{self.army_1.primary_commander.name}]{colors.ENDC} lost {colors.YELLOW}{army_1_skill_losses}{colors.ENDC} units\n\
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
            {c}[{winner.primary_commander.name}]{colors.ENDC} ({winner.troop_count}) won the battle\n\
            ")



class colors:
    RED =    '\033[31m'
    GREEN =  '\033[32m'
    YELLOW = '\033[33m'
    BLUE =   '\033[34m'
    HEADER = '\033[95m'
    BOLD =   '\033[1m'
    ENDC =   '\033[0;0m'