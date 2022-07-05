class Buff():
    def __init__(
            self, name, buff,
            condition=None, duration=None,
            probability=None, cooldown=None,
            skill_name=None):

        self.name = name
        self.buff = buff
        self.condition = condition
        self.duration = duration
        self.probability = probability
        self.cooldown = cooldown
        self.skill_name = skill_name

        self.countdown = 0
