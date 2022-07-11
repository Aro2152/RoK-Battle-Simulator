import json

class Commander():
    def __init__(
            self, name, level,
            talents_levels,
            skills_levels):
        
        self.name = name
        self.level = level
        self.talents_levels = talents_levels
        self.skills_levels = skills_levels

        self.description = json.load(open(f'../rss/commanders/{self.name}.json'))

        # Set talents
        self.set_talents()

        # Set skills
        self.set_skills()

        # Define active skill
        self.set_active_skill()


    def set_talents(self):
        self.talents = {}
        for talent_cat in self.talents_levels:
            self.talents[talent_cat] = {}
            talents_info = json.load(open(f'../rss/talents/{talent_cat}.json'))
            for talent in self.talents_levels[talent_cat]:
                talent_info = talents_info[talent]
                lvl = self.talents_levels[talent_cat][talent] - 1
                talent_lvl = talent_info
                talent_lvl["buffs"] = self.set_level(talent_lvl["buffs"], lvl)
                self.talents[talent_cat][talent] = talent_lvl


    def set_skills(self):
        self.skills = {}
        for skill_name, lvl in zip(self.description["skills"], self.skills_levels):
            if lvl > 0:
                lvl -= 1
                skill = self.description["skills"][skill_name]
                skill["buffs"] = self.set_level(skill["buffs"], lvl)
                self.skills[skill_name] = skill
    

    def set_active_skill(self):
        for skill_name in self.skills:
            if self.skills[skill_name]["type"] == "active":
                self.active_skill = skill_name
                break


    def set_level(self, buffs, lvl):
        for buff in buffs:
            if isinstance(buffs[buff], list) and isinstance(buffs[buff][0], (int, float)):
                buffs[buff] = buffs[buff][lvl]
            elif isinstance(buffs[buff], dict):
                for sub_buff in buffs[buff]:
                    if isinstance(buffs[buff][sub_buff], list) and isinstance(buffs[buff][sub_buff][0], (int, float)):
                        buffs[buff][sub_buff] = buffs[buff][sub_buff][lvl]
        return buffs
