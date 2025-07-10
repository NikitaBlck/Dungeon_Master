from dataclasses import dataclass
from enum import Enum

class spell_Names(Enum):

    FIREBALL = "Fireball"
    ICE_BLAST = "Ice blast"
    LIGHTNING_STRIKE = "Lightning strike"

class spell_class:
    def __init__(self, name: str, damage: int, mana_cost: int):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

@dataclass (frozen=True)
class all_spells_class:
    fireball_spell: spell_class
    iceBlast_spell: spell_class
    lightningStrike_spell: spell_class

all_spells = all_spells_class(
    fireball_spell=spell_class(name=spell_Names.FIREBALL, damage=40, mana_cost=10),
    iceBlast_spell=spell_class(name=spell_Names.ICE_BLAST, damage=80, mana_cost=25),
    lightningStrike_spell=spell_class(name=spell_Names.LIGHTNING_STRIKE, damage=120, mana_cost=50)
)

# Add this for fast lookup:
SPELL_LOOKUP = {spell.name: spell for spell in all_spells.__dict__.values()}

print(SPELL_LOOKUP)