# Authors: Aro2152
# Copyright (C) 2022 Aro2152

import json

class Army():
    def __init__(
        self, army_info
    ):
        self.army_info = army_info
        self.troop_count = army_info["troop_count"]

        self.primary_commander = army_info["primary_commander"]
        # Check for secondary commander
        if "secondary_commander" in army_info:
            self.secondary_commander = army_info["secondary_commander"]
        else:
            self.secondary_commander = {
                "name": None,
                "level": None,
                "skills_levels": None
            }

        # Init the buffs at 0
        self.buffs = {
            "infantry": {
                "attack":  0,
                "defense": 0,
                "health":  0,
                "march_speed": 0
            },
            "cavalry": {
                "attack":  0,
                "defense": 0,
                "health":  0,
                "march_speed": 0
            },
            "archer": {
                "attack":  0,
                "defense": 0,
                "health":  0,
                "march_speed": 0
            },
            "siege": {
                "attack":  0,
                "defense": 0,
                "health":  0,
                "march_speed": 0
            },
            "attack":  0,
            "defense": 0,
            "health":  0,
            "march_speed": 0,
            "damage":  0,
            "skill_damage": 0,
            "additional_skill_damage": 0,  # e.g. Kusunoki's active skill
            "reduce_damage_taken":       0,
            "reduce_skill_damage_taken": 0,
            "normal_attack_damage":   0,
            "counter_attack_damage":  0,
            "damage_to_barbarians": 0
        }

        self.rage = 0

        self.load_troop_stats()
        self.compute_buffs()

        self.total_buffs = self.get_summed_buffs()
        self.buffed_stats =  self.get_buffed_stats()

    
    # Loads the stats for the troops based on tier and special units
    def load_troop_stats(self):
        troop_tier_stats = json.load(open("../rss/troop_tier_stats.json"))
        troop_special_stats = json.load(open("../rss/troop_special_stats.json"))

        self.troop_stats = troop_tier_stats[self.army_info['troop_tier']]

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
            self.buffs["attack"] += 3

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
                    self.buffs[buff_type] += self.army_info[cat][buff_type]
        

    # Sum general buffs (attack, def, health)
    # with the one of specific troop type
    def get_summed_buffs(self):
        all_stats = {key: {} for key in ["infantry", "cavalry", "archer", "siege"]}
        for buff_type in self.buffs:
            if buff_type in ["infantry", "cavalry", "archer", "siege"]:
                for stat in ["attack", "defense", "health", "march_speed"]:
                    all_stats[buff_type][stat] = self.buffs[buff_type][stat] + self.buffs[stat]
            else:
                all_stats[buff_type] = self.buffs[buff_type]
        return all_stats


    # Compute the stats of each troop
    # after having computed and summed the buffs
    def get_buffed_stats(self):
        buffed_stats = {}
        tt = self.army_info["troop_type"]
        for stat in ["attack", "defense", "health"]:
            buffed_stats[stat] = 1 + (self.buffs[tt][stat] + self.buffs[stat])/100
            buffed_stats[stat] = self.troop_stats[tt][stat] * buffed_stats[stat]
        return buffed_stats

   
    def add_academy_buffs(self):
        military_technologies_buffs = json.load(open("../rss/military_technologies.json"))
        for research_name in self.army_info["technologies_levels"]:
            research_level = self.army_info["technologies_levels"][research_name] - 1
            for troop in military_technologies_buffs[research_name].keys():
                if isinstance(military_technologies_buffs[research_name][troop], dict):
                    for stat in military_technologies_buffs[research_name][troop].keys():
                        self.buffs[troop][stat] += military_technologies_buffs[research_name][troop][stat][research_level]
                else:
                    self.buffs[troop] += military_technologies_buffs[research_name][troop][research_level]


    def add_talents_buffs(self):
        for talent_cat in self.primary_commander["talents_levels"]:
            talents_levels = self.primary_commander["talents_levels"][talent_cat]
            talents = json.load(open(f"../rss/talents/{talent_cat}.json"))
            for talent in talents_levels:
                level = talents_levels[talent] - 1
                if talents[talent]["category"] == "simple":
                    talent_buffs = talents[talent]["buffs"]
                    for tt in talent_buffs:
                        if isinstance(talent_buffs[tt], dict):
                            for cat in talent_buffs[tt]:
                                self.buffs[tt][cat] += talent_buffs[tt][cat][level]
                        else:
                            self.buffs[tt] += talent_buffs[tt][level]

   
    def add_commander_view_buffs(self):
        buffs = json.load(open("../rss/commander_view.json"))
        for buff_name in self.army_info["commander_view"]:
            for buff in buffs[buff_name]:
                self.buffs[buff] += buffs[buff_name][buff]

   
    def add_skills_buffs(self):
        self.active_skills = []
        for commander in ["primary_commander", "secondary_commander"]:
            if commander in self.army_info:
                name = self.army_info[commander]["name"]
                skills_levels = self.army_info[commander]["skills_levels"]
                commander_info = json.load(open(f"../rss/commanders/{name}.json"))
                for i, skill in enumerate(commander_info["skills"]):
                    if skills_levels[i] > 0:
                        if commander_info["skills"][skill]["type"] == "active":
                            self.active_skills.append(commander_info["skills"][skill])
                        elif commander_info["skills"][skill]["category"] == "simple":
                            skill_buffs = commander_info["skills"][skill]["buffs"]
                            for tt in skill_buffs:
                                if isinstance(skill_buffs[tt], dict):
                                    for cat in skill_buffs[tt]:
                                        self.buffs[tt][cat] += skill_buffs[tt][cat][skills_levels[i]-1]
                                else:
                                    self.buffs[tt] += skill_buffs[tt][skills_levels[i]-1]




    def add_civ_buffs(self):
        troop_special_stats = json.load(open("../rss/troop_special_stats.json"))
        civ = self.army_info["civilization"]
        for troop_type in troop_special_stats[civ]["buffs"]:
            if isinstance(troop_special_stats[civ]["buffs"][troop_type], dict):
                for stat in troop_special_stats[civ]["buffs"][troop_type]:
                    self.buffs[troop_type][stat] += troop_special_stats[civ]["buffs"][troop_type][stat]
            else:
                self.buffs[troop_type] += troop_special_stats[civ]["buffs"][troop_type]


    def add_military_buildings_buffs(self):
        military_buildings_buffs = json.load(open("../rss/military_buildings.json"))
        for bld in self.army_info["military_buildings_levels"]:
            bld_lvl = self.army_info["military_buildings_levels"][bld]
            if bld_lvl > 10:
                bld_lvl = str(bld_lvl)
                for buff in military_buildings_buffs[bld][bld_lvl]:
                    self.buffs[buff] += military_buildings_buffs[bld][bld_lvl][buff]


    def add_vip_buffs(self):
        vip_buffs = json.load(open("../rss/vip_buffs.json"))
        for lvl in range(self.army_info["vip_level"]+1):
            for buff_type in vip_buffs[str(lvl)]:
                self.buffs[buff_type] += vip_buffs[str(lvl)][buff_type]