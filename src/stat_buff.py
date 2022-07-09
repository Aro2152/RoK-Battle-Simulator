#!/usr/bin/env python3

# Authors: Damocles078
# Copyright (C) 2022 Damocles078


__all__ = ['Buff']

#TODO make an actual class out of this

from copy import deepcopy


class TroopBuff():
    
    def __init__(self) -> None:
        self.all = 0
        self.infantry = 0
        self.cavalry = 0
        self.archer = 0
        self.siege = 0
        
        
    def __add__(self, other):
        if type(other) != TroopBuff:
            raise Exception(f"Operation __add__ between TroopBuff and {type(other)} is not defined")
        else:
            sum = TroopBuff()
            for attribute in self.__dict__.keys():
                setattr(sum, attribute, getattr(self, attribute)+getattr(other, attribute))
            return(sum)
        
        
    def __setitem__(self, name, value):
        if type(value) not in [int, float]:
            raise Exception(f"{value} is not an acceptable value for a troop buff")
        else:
            if name in self.__dict__:
                setattr(self, name, value)
            else:
                raise Exception(f"{name} is not an attribute of TroopBuff")
            
            
    def __getitem__(self, name):
        if name in self.__dict__:
            return(getattr(self, name))
        else:
            raise Exception(f"{name} is not an attribute of TroopBuff")
        
        
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    
    def __iter__(self):
        return(TroopBuffIterator(self))
    
    
    def apply_all_to_types(self):
        
        applied = deepcopy(self)
        for type in self.__dict__:
            if type != "all":
                setattr(applied, type, getattr(self, type) + self.all)
            else:
                applied.all = self.all
        return(applied)
    
    
class TroopBuffIterator():
    
    def __init__(self, object) -> None:
        self.object = object
        self.key_list = list(object.__dict__.keys())
        self.index = -1
    
    def __next__(self):
        self.index += 1
        if self.index < len(self.key_list):
            return (self.key_list[self.index])
        else:
            raise StopIteration
        
class Buff():
    
    def __init__(self) -> None:
        self.attack = TroopBuff()
        self.defense = TroopBuff()
        self.health = TroopBuff()
        self.march_speed = TroopBuff()
        self.base_attack = TroopBuff()
        self.base_defense = TroopBuff()
        self.base_health = TroopBuff()
        self.damage = 0
        self.skill_damage = 0
        self.additional_skill_damage = 0
        self.reduce_damage_taken = 0
        self.reduce_skill_damage_taken = 0
        self.reduce_counter_attack_damage_taken = 0
        self.normal_attack_damage = 0
        self.counter_attack_damage = 0
        self.damage_to_barbarians = 0
        
        
    def __add__(self, other):
        if type(other) != Buff:
            raise Exception(f"Operation __add__ between Buff and {type(other)} is not defined")
        else:
            sum = Buff()
            for attribute in self.__dict__.keys():
                setattr(sum, attribute, getattr(self, attribute)+getattr(other, attribute))
            return(sum)
        
        
    def __setitem__(self, name, value):
        if type(value) not in [int, float, TroopBuff]:
            raise Exception(f"{value} is not an acceptable value for a troop buff")
        else:
            if name in self.__dict__:
                setattr(self, name, value)
            else:
                raise Exception(f"{name} is not an attribute of TroopBuff")
            
            
    def __getitem__(self, name):
        if name in self.__dict__:
            return(getattr(self, name))
        else:
            raise Exception(f"{name} is not an attribute of TroopBuff")


    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def __iter__(self):
        return(BuffIterator(self))
    
    
    def apply_all_to_types(self):
        
        applied = deepcopy(self)
        for troop_type in self.__dict__:
            if type(troop_type) == TroopBuff:
                setattr(applied, troop_type, getattr(self,troop_type).apply_all_to_types())
        return(applied)
        
    
    
class BuffIterator():
    
    def __init__(self, object) -> None:
        self.object = object
        self.key_list = list(object.__dict__.keys())
        self.index = -1
    
    def __next__(self):
        self.index += 1
        if self.index < len(self.key_list):
            return (self.key_list[self.index])
        else:
            raise StopIteration