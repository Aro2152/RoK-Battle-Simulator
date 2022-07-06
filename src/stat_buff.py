#!/usr/bin/env python3

# Authors: Damocles078
# Copyright (C) 2022 Damocles078


__all__ = ['StatBuff'] # from gear import * only imports Gear class

  
StatBuff = {
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