#!/usr/bin/env python3

# Authors: Damocles078
# Copyright (C) 2022 Damocles078


__all__ = ['Gear'] # from gear import * only imports Gear class


class GearPiece():
    
    def __init__(self, name="None", type="None", iconic=False, crit=False) -> None:
        self.name = name
        self.type = type
        self.crit = crit
        self.iconic = iconic
        
        try:
            self.load()
        except PieceDoesNotExist:
            raise

    def __repr__(self) -> str:
        reprentation = [self.type, ":", self.name,'\n']
        reprentation.append("Crit" if self.crit else "Non Crit")
        reprentation.append("\n")
        reprentation.append("Iconic" if self.iconic else "Non Iconic")
        return(' '.join(reprentation))
    
    
    def load(self):
        raise PieceDoesNotExist(self.name, self.type)


class GearHelmPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="helm", *args, **kwargs)
        
        
class GearChestPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="chest", *args, **kwargs)


class GearWeaponPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="weapon", *args, **kwargs)


class GearGauntletPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="gauntlet", *args, **kwargs)


class GearLegsPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="legs", *args, **kwargs)


class GearBootsPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="boots", *args, **kwargs)


class GearAccessoryPiece(GearPiece):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(type="accessory", *args, **kwargs)
        
        
    def trigger_effect(self):
        pass
        
 
class Gear():
    
    def __init__(self, helm_name="None", 
                       chest_name="None", 
                       weapon_name="None", 
                       gauntlet_name="None", 
                       legs_name="None", 
                       boots_name="None", 
                       accessory1_name="None", 
                       accessory2_name="None",
                       helm_crit=False, 
                       chest_crit=False, 
                       weapon_crit=False, 
                       gauntlet_crit=False, 
                       legs_crit=False, 
                       boots_crit=False, 
                       accessory1_crit=False, 
                       accessory2_crit=False,
                       helm_iconic=False, 
                       chest_iconic=False, 
                       weapon_iconic=False, 
                       gauntlet_iconic=False, 
                       legs_iconic=False, 
                       boots_iconic=False, 
                       accessory1_iconic=False, 
                       accessory2_iconic=False) -> None:
        
        self._helm = GearHelmPiece(name=helm_name, 
                                   crit=helm_crit,
                                   iconic=helm_iconic)
        self._chest = GearChestPiece(name=chest_name, 
                                     crit=chest_crit,
                                     iconic=chest_iconic)
        self._weapon = GearWeaponPiece(name=weapon_name, 
                                   crit=weapon_crit,
                                   iconic=weapon_iconic)
        self._gauntlet = GearGauntletPiece(name=gauntlet_name, 
                                           crit=gauntlet_crit,
                                           iconic=gauntlet_iconic)
        self._legs = GearLegsPiece(name=legs_name, 
                                       crit=legs_crit,
                                       iconic=legs_iconic)
        self._boots = GearBootsPiece(name=boots_name, 
                                     crit=boots_crit,
                                     iconic=boots_iconic)
        self._accessory1 = GearAccessoryPiece(name=accessory1_name, 
                                              crit=accessory1_crit,
                                              iconic=accessory1_iconic)
        self._accessory2 = GearAccessoryPiece(name=accessory2_name, 
                                              crit=accessory2_crit,
                                              iconic=accessory2_iconic)
        self.compute_boost()
        
        
    def __iter__(self):
        return GearIterator(self)
    

    
    def __repr__(self) -> str:
        reprentation = "Gear pieces :\n"
        for piece in self:
            reprentation += "- " + piece.__repr__() + "\n"
        return(reprentation)
    
    
    def compute_boost(self):
        pass
        
      
class GearIterator():
    
    __pieces = ["_helm", "_chest", "_weapon", "_gauntlet", "_legs", "_boots", "_accessory1", "_accessory2"]
    
    def __init__(self, gear: Gear) -> None:
        self.gear = gear
        self.__piece_index = -1 # for loop calls __next__ right away
    
    
    def __next__(self) -> GearPiece:
        if self.__piece_index < len(self.__pieces)-1:
            self.__piece_index += 1
            return getattr(self.gear, self.__pieces[self.__piece_index])
        else:
            raise StopIteration
    

class PieceDoesNotExist(Exception): # Throw this when a piece is unknown at runtime (i.e. it is not in configuration files)
    
    def __init__(self, name="Unknown", type="Unknown") -> None:
        self.name = name
        self.type = type
        super().__init__(f'{self.name} of type {self.type} not found.')


def main():
    test = Gear(helm_crit=True, legs_iconic=True, boots_name="Custom_name")
    print(test)


if __name__=='__main__':
    main()