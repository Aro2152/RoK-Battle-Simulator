# Authors: Aro2152
# Copyright (C) 2022 Aro2152

import json
from commander import Commander

class Army():
    def __init__(
        self, army_info
    ):
        self.army_info = army_info
        self.troop_count = army_info["troop_count"]

        # Load commanders
        primary_commander_info = army_info["primary_commander"]
        self.primary_commander = Commander(
            primary_commander_info["name"],
            primary_commander_info["level"],
            primary_commander_info["talents_levels"],
            primary_commander_info["skills_levels"]
        )

        # Check for secondary commander
        if "secondary_commander" in army_info:
            secondary_commander_info = army_info["secondary_commander"]
            self.secondary_commander = Commander(
                secondary_commander_info["name"],
                secondary_commander_info["level"],
                secondary_commander_info["talents_levels"],
                secondary_commander_info["sklls_levels"]
            )
        else:
            self.secondary_commander = None

        # Init the buffs at 0
        self.buffs = {
            "attack": {
                "all":      0,
                "infantry": 0,
                "cavalry":  0,
                "archer":   0,
                "siege":    0
            },
            "defense": {
                "all":      0,
                "infantry": 0,
                "cavalry":  0,
                "archer":   0,
                "siege":    0
            },
            "health": {
                "all":      0,
                "infantry": 0,
                "cavalry":  0,
                "archer":   0,
                "siege":    0
            },
            "march_speed": {
                "all":      0,
                "infantry": 0,
                "cavalry":  0,
                "archer":   0,
                "siege":    0
            },
            "damage":                             0,
            "skill_damage":                       0,
            "additional_skill_damage":            0,  # e.g. Kusunoki's active skill
            "reduce_damage_taken":                0,
            "reduce_skill_damage_taken":          0,
            "reduce_counter_attack_damage_taken": 0,
            "normal_attack_damage":               0,
            "counter_attack_damage":              0,
            "damage_to_barbarians":               0
        }

        self.rage = 0

        self.categories = json.load(open("../rss/categories.json"))

        self.load_troop_stats()
        self.compute_buffs()

        self.total_buffs = self.get_summed_buffs()
        self.buffed_stats =  self.get_buffed_stats()

    
    # Loads the stats for the troops based on tier and special units
    def load_troop_stats(self):
        troop_tier_stats = json.load(open("../rss/troop_tier_stats.json"))
        troop_special_stats = json.load(open("../rss/troop_special_stats.json"))

        # Load basic unit stats
        self.troop_stats = troop_tier_stats[self.army_info['troop_tier']]

        # Load special unit stats
        civ = self.army_info["civilization"]
        tier = self.army_info["troop_tier"]
        tt = self.army_info["troop_type"]
        if tier in troop_special_stats[civ]["troops"]:
            if tt in troop_special_stats[civ]["troops"][tier]:
                self.troop_stats[tt] = troop_special_stats[civ]["troops"][tier][tt]


    def compute_buffs(self):
        # Add talents buffs
        self.add_talents_buffs()

        # Add skills buffs
        self.add_skills_buffs()

        # Add war frenzy buffs
        if self.army_info["war_frenzy"]:
            self.buffs["attack"]["all"] += 3

        # Add vip buffs
        self.add_vip_buffs()

        # Add military buildings buffs
        self.add_military_buildings_buffs()

        # Add civilization buffs
        self.add_civ_buffs()

        # Add commander view buffs
        self.add_commander_view_buffs()

        # Add academy buffs
        self.add_academy_buffs()

        # Add other buffs
        for cat in [
            "items_buffs", "city_skin",
            "alliance_buffs", "kingdom_buffs"
        ]:
            for buff_type in self.army_info[cat]:
                if isinstance(self.army_info[cat][buff_type], dict):
                    for troop_buff in self.army_info[cat][buff_type]:
                        self.buffs[buff_type][troop_buff] += self.army_info[cat][buff_type][troop_buff]
                else:
                    self.buffs[buff_type]["all"] += self.army_info[cat][buff_type]
        

    # Sum general buffs (attack, def, health)
    # with the one of specific troop type (only used for visualization)
    def get_summed_buffs(self):
        all_stats = {key: {} for key in self.categories["stat_types"]}
        for stat in self.buffs:
            if stat in self.categories["stat_types"]:
                if isinstance(self.buffs[stat], dict):
                    for tt in self.categories["troop_types"]:
                        all_stats[stat][tt] = self.buffs[stat][tt] + self.buffs[stat]["all"]
            else:
                all_stats[stat] = self.buffs[stat]
        return all_stats


    # Compute the stats of each troop
    # after having computed and summed the buffs
    def get_buffed_stats(self):
        buffed_stats = {}
        tt = self.army_info["troop_type"]
        for stat in self.categories["stat_types"]:
            buffed_stats[stat] = 1 + (self.buffs[stat][tt] + self.buffs[stat]["all"])/100
            buffed_stats[stat] = self.troop_stats[tt][stat] * buffed_stats[stat]
        return buffed_stats

   
    def add_academy_buffs(self):
        military_technologies_buffs = json.load(open("../rss/military_technologies.json"))
        for research_name in self.army_info["technologies_levels"]:
            research_level = self.army_info["technologies_levels"][research_name] - 1
            for stat in military_technologies_buffs[research_name].keys():
                if isinstance(military_technologies_buffs[research_name][stat], dict):
                    for tt in military_technologies_buffs[research_name][stat].keys():
                        self.buffs[stat][tt] += military_technologies_buffs[research_name][stat][tt][research_level]
                else:
                    self.buffs[stat]["all"] += military_technologies_buffs[research_name][stat][research_level]


    def add_talents_buffs(self):
        for talent_cat in self.primary_commander.talents:
            for talent_name in self.primary_commander.talents[talent_cat]: 
                talent = self.primary_commander.talents[talent_cat][talent_name]
                if talent["category"] == "simple":
                    talent_buffs = talent["buffs"]
                    for stat in talent_buffs:
                        if isinstance(talent_buffs[stat], dict):
                            for tt in talent_buffs[stat]:
                                self.buffs[stat][tt] += talent_buffs[stat][tt]
                        else:
                            self.buffs[stat] += talent_buffs[stat]
   

    def add_commander_view_buffs(self):
        buffs = json.load(open("../rss/commander_view.json"))
        for buff_name in self.army_info["commander_view"]:
            for stat in buffs[buff_name]:
                self.buffs[stat]["all"] += buffs[buff_name][stat]

   
    def add_skills_buffs(self):
        stat_buffs = self.categories["stat_buffs"] + self.categories["stat_types"]
        for commander in [self.primary_commander, self.secondary_commander]:
            if commander:
                for skill in commander.skills:
                    for buff in commander.skills[skill]["buffs"]:
                        skill_buffs = commander.skills[skill]["buffs"][buff]
                        if ("probability" not in skill_buffs and
                            "condition" not in skill_buffs and
                            "duration" not in skill_buffs and
                            buff in stat_buffs):
                            for stat in skill_buffs:
                                # if isinstance(skill_buffs[stat], dict):
                                #     for tt in skill_buffs[stat]:
                                #         self.buffs[stat][tt] += skill_buffs[stat][tt]
                                # else:
                                self.buffs[buff][stat] += skill_buffs[stat]


    def add_civ_buffs(self):
        troop_special_stats = json.load(open("../rss/troop_special_stats.json"))
        civ = self.army_info["civilization"]
        for stat in troop_special_stats[civ]["buffs"]:
            if isinstance(troop_special_stats[civ]["buffs"][stat], dict):
                for tt in troop_special_stats[civ]["buffs"][stat]:
                    self.buffs[stat][tt] += troop_special_stats[civ]["buffs"][stat][tt]
            else:
                self.buffs[stat]["all"] += troop_special_stats[civ]["buffs"][stat]


    def add_military_buildings_buffs(self):
        military_buildings_buffs = json.load(open("../rss/military_buildings.json"))
        for bld in self.army_info["military_buildings_levels"]:
            bld_lvl = self.army_info["military_buildings_levels"][bld]
            if bld_lvl >= 10:
                bld_lvl = str(bld_lvl)
                for stat in military_buildings_buffs[bld][bld_lvl]:
                    self.buffs[stat]["all"] += military_buildings_buffs[bld][bld_lvl][stat]


    def add_vip_buffs(self):
        vip_buffs = json.load(open("../rss/vip_buffs.json"))
        for lvl in range(self.army_info["vip_level"]+1):
            for stat in vip_buffs[str(lvl)]:
                self.buffs[stat]["all"] += vip_buffs[str(lvl)][stat]