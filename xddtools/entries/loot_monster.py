from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.entries.effect import Effect
from xddtools.enum import EffectTarget
from xddtools.name import AutoName
from xddtools.base import LootMonsterEntry, LootTableEntry, EffectEntry, get_entry_id


class LootMonster(LootMonsterEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    loot: Union[LootTableEntry, str]
    count: int = 1
    spawn_effects: Optional[Sequence[Union[EffectEntry, str]]] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_loot_monster(), frozen=True)

    @model_validator(mode="after")
    def _check_after(self):
        if self.spawn_effects is None:
            self.spawn_effects = [Effect(
                target=EffectTarget.PERFORMER,
                kill_enemy_types=self.id()
            )]
        else:
            tem = [effect for effect in self.spawn_effects]
            tem.append(Effect(
                target=EffectTarget.PERFORMER,
                kill_enemy_types=self.id()
            ))
        return self

    def info(self) -> str:
        res = f'display: .size 0\n' \
              f'enemy_type: .id "{self.id()}"\n' \
              f'stats: .hp 1 .def 0% .prot 0 .spd 1 ' \
              f'.stun_resist 0% .poison_resist 0% .bleed_resist 0% .debuff_resist 0% .move_resist 0%\n' \
              f'personality: .prefskill -1\n' \
              f'loot: .code "{get_entry_id(self.loot)}" .count {self.count}\n' \
              f'initiative: .number_of_turns_per_round 0\n' \
              f'monster_brain: .id default\n' \
              f'battle_modifier: .accelerate_stall_penalty False .disable_stall_penalty False .can_surprise False ' \
              f'.can_be_surprised True .always_surprise False .always_be_surprised False .can_be_summon_rank True\n' \
              f'wave_spawning: .prefers_front True\n' \
              f'spawn: .effects '
        if self.spawn_effects is not None:
            res += " ".join([get_entry_id(effect) for effect in self.spawn_effects])
        return res

    def art(self) -> str:
        return "commonfx: .deathfx death_medium"


if __name__ == '__main__':
    loot = LootMonster(
        loot="",
        count=0
    )
    print(loot.info())
