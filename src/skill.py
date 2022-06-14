class Skill():
    def __init__(self, name, type,
                 buffs, rage_requirement=None,
                 duration=None, probability=None,
                 condition=None):

        self.name = name
        self.type = type
        self.buffs = buffs
        self.rage_requirement = rage_requirement
        self.duration = duration
        self.probability = probability
        self.condition = condition

        self.remaining_turns = 0

        
        