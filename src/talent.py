# Authors: Aro2152
# Copyright (C) 2022 Aro2152

class Talent():
    def __init__(
        self, name, info, level
    ):
        self.name = name
        self.info = info
        self.level = level

        self.category = info["category"]
        self.buff = info["buff"]

        if "condition" in info:
            self.condition = info["condition"]

        if "duration" in info:
            self.duration = info["duration"]

        if "probability" in info:
            self.probability = info["probability"]