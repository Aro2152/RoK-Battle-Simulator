## Rise of Kingdoms **Combat Simulator**

#### The following is an attempt at creating a **Rise Of Kingdoms combat simulator**.<br /> The goal of this project is to be able to simulate battles accurately and play around with different buffs, skills or army combinations, in order to find out the ideal strategy for any scenario.

As of 06/05/22:

The following scenarios have been implemented:
- [x] 1v1
- [x] Single-troop-type-per-army combat
- [x] Primary and Secondary commanders
- [ ] Equipment
- [ ] Talents

The following commanders have been implemented:
- [x] Markswoman
- [ ] Ghenghis Khan

To Do:

    Foremost:
        - Support for primary skills with multiple effects

    Long term:
        - Add AoE support
        - Add Siege support
        - Add more commanders
        - Add multiple armies combat support
---

Things to do/confirm:
- "Clarity" Skill talent: does the 6 second countdown restarts when secondary commander active skill triggers?
- "All For One" Skill talent: Only the next acitve skill of the secondary commander is buffed? If silenced, will the bugg carry on to next cycle?
- If active skill rage requirement of secondary < active skill rage requirement of primary, (e.g. Khan as secondary) what happens?
- Does the active skill give as much rage as a normal attack?
- Is the excess rage really removed?
- Define which buffs/debuffs stack or not (e.g. Prime Scipio/Aethelflaed active skills)
- "Increase normal attack damage" means both normal attacks and counter attacks? (e.g. Joan 4th skill)