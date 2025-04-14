from enum import Enum
from typing import Optional, Union, Sequence, Sequence, List

from pydantic import BaseModel, ConfigDict, Field

from xddtools.base import EffectEntry, QuirkEntry, Entry, HeroEntry, MonsterEntry, TrinketEntry, BuffEntry, ItemEntry, \
    get_entry_id, ModeEntry, ActorDotEntry
from xddtools.entries.buff import HealSource, BuffDurationType
from xddtools.entries.buff_rule import MonsterClass, HeroClass, MonsterType, QuirkType, ItemType
from xddtools.enum.buff import BuffType
from xddtools.enum.effect import EffectTarget, CurioResultType, BuffSource, DamageType, BuffStatType, DamageSourceType, \
    TrinketID, KeyStatus
from xddtools.name import AutoName
from xddtools.target import Target
from xddtools.utils import float_to_percent_int, float_to_percent_str, bool_to_lower_str


class Effect(EffectEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    target: EffectTarget
    spawn_target_actor_base_class_id: Union[MonsterClass, HeroClass, HeroEntry, MonsterEntry, str, None] = None
    curio_result_type: Optional[CurioResultType] = None

    shuffle_target: bool = False
    shuffle_party: bool = False
    instant_shuffle: bool = False

    chance: float = 1.0

    item: bool = False
    curio: bool = False
    cure: bool = False
    cure_bleed: bool = False
    cure_poison: bool = False
    clear_dot_stress: bool = False
    tag: bool = False
    untag: bool = False
    unstun: bool = False
    guard: Optional[bool] = None
    clear_guarding: bool = False
    clear_guarded: bool = False
    dot_shuffle: bool = False
    kill: bool = False
    immobilize: bool = False
    unimmobilize: bool = False
    uncontrol: bool = False
    capture: bool = False
    capture_remove_from_party: bool = False
    remove_vampire: bool = False
    cure_disease: bool = False
    stealth: bool = False
    unstealth: bool = False
    clear_debuff: bool = False
    clear_virtue: bool = False
    daze: bool = False
    undaze: bool = False
    riposte: Optional[bool] = None
    clear_riposte: bool = False
    performer_rank_target: bool = False

    riposte_on_hit_chance_add: Optional[float] = None
    riposte_on_miss_chance_add: Optional[float] = None
    riposte_on_hit_chance_multiply: Optional[float] = None
    riposte_on_miss_chance_multiply: Optional[float] = None
    riposte_effect: Optional[Sequence[Union[EffectEntry, str]]] = None

    riposte_validate: bool = True
    can_crit_heal: bool = True
    can_apply_on_death: Optional[bool] = None
    has_description: bool = True
    buff_is_clear_debuff_valid: bool = True

    swap_source_and_target: bool = False
    crit_doesnt_apply_to_roll: bool = False
    apply_once: bool = False
    apply_with_result: bool = False
    skill_instant: bool = False
    refreshes_skill_uses: bool = False
    individual_target_actor_rolls: bool = False
    skips_endless_wave_curio: bool = False

    dot_source: Optional[BuffSource] = None
    dot_bleed: Optional[int] = None
    dot_poison: Optional[int] = None
    dot_stress: Optional[int] = None
    dot_hp_heal: Optional[int] = None
    heal_stress: Optional[int] = None
    stress: Optional[int] = None
    heal: Optional[int] = None
    stun: Optional[int] = None
    torch_decrease: Optional[int] = None
    torch_increase: Optional[int] = None
    push: Optional[int] = None
    pull: Optional[int] = None
    control: Optional[int] = None
    health_damage: Optional[int] = None
    health_damage_blocks: Optional[int] = None

    virtue_blockable_chance: Optional[float] = None
    affliction_blockable_chance: Optional[float] = None

    heal_percent: Optional[float] = None
    source_heal_type: Optional[HealSource] = None
    steal_buff_stat_type: Optional[BuffStatType] = None
    steal_buff_source_type: Optional[BuffSource] = None
    kill_enemy_types: Union[MonsterType, str, None] = None
    disease: Union[QuirkType, QuirkEntry, str, None] = None
    set_mode: Union[ModeEntry, str, None] = None
    actor_dot: Union[ActorDotEntry, str, None] = None
    barks: Union[Sequence[str], str, None] = None
    damage_type: Optional[DamageType] = None
    damage_source_type: Optional[DamageSourceType] = None
    damage_source_data: Union[TrinketEntry, TrinketID, str, None] = None
    use_item_id: Union[ItemEntry, str, None] = None
    use_item_type: Optional[ItemType] = None
    rank_target: Optional[Target] = None
    clear_rank_target: Optional[Target] = None

    summon_monsters: Optional[Sequence[str]] = None
    summon_chances: Optional[Sequence[float]] = None
    summon_ranks: Optional[Sequence[Union[Target, str]]] = None
    summon_limits: Optional[Sequence[int]] = None
    summon_count: Optional[int] = None
    summon_erase_data_on_roll: Optional[bool] = None
    summon_can_spawn_loot: Optional[bool] = None
    summon_rank_is_previous_monster_class: Optional[bool] = None
    summon_does_roll_initiatives: Optional[bool] = None

    set_monster_class_id: Optional[str] = None
    set_monster_class_ids: Optional[Sequence[str]] = None
    set_monster_class_chances: Optional[Sequence[float]] = None
    set_monster_class_reset_hp: Optional[bool] = None
    set_monster_class_reset_buffs: Optional[bool] = None
    set_monster_class_carry_over_hp_min_percent: Optional[float] = None
    set_monster_class_clear_initiative: Optional[bool] = None
    set_monster_class_clear_monster_brain_cooldowns: Optional[bool] = None
    set_monster_class_reset_scale: Optional[bool] = None

    buff_type: Optional[BuffType] = None
    buff_sub_type: Union[Entry, Enum, str, None] = None
    buff_amount: Union[float, int, None] = None
    buff_duration_type: Optional[BuffDurationType] = None
    key_status: Optional[KeyStatus] = None
    monster_type: Union[MonsterType, str, None] = None

    buff_source_type: Optional[BuffSource] = None
    buff_ids: Optional[Sequence[Union[BuffEntry, str]]] = None

    combat_stat_buff: bool = False
    damage_low_multiply: Optional[float] = None
    damage_high_multiply: Optional[float] = None
    max_hp_multiply: Optional[float] = None
    attack_rating_add: Optional[float] = None
    crit_chance_add: Optional[float] = None
    defense_rating_add: Optional[float] = None
    protection_rating_add: Optional[float] = None

    damage_low_add: Optional[int] = None
    damage_high_add: Optional[int] = None
    max_hp_add: Optional[int] = None

    speed_rating_add: Optional[int] = None
    initiative_change: Optional[int] = None
    duration: Optional[int] = None

    on_hit: bool = True
    on_miss: bool = False
    queue: Optional[bool] = None

    entry_id: str = Field(default_factory=lambda x: AutoName().new_effect(), frozen=True)

    def bark_id(self) -> str:
        return f"str_bark_{self.id()}"

    def _one_line(self, buff_ids: Union[List[BuffEntry], List[str]]):
        res = [f'effect: .name "{self.id()}"']
        if self.spawn_target_actor_base_class_id is not None:
            res.append(f'.spawn_target_actor_base_class_id {self.spawn_target_actor_base_class_id}')
        res.append(f'.target "{self.target.value}"')
        if self.curio_result_type is not None:
            res.append(f'.curio_result_type "{self.curio_result_type.value}"')
        none = {
            "shuffletarget": self.shuffle_target,
            "shuffleparty": self.shuffle_party,
            "instant_shuffle": self.instant_shuffle,
        }
        for k, v in none.items():
            if v:
                res.append(f".{k}")
        res.append(f".chance {float_to_percent_int(self.chance)}%")

        one_zeros = {
            "item": self.item,
            "curio": self.curio,
            "cure": self.cure,
            "cure_bleed": self.cure_bleed,
            "cure_poison": self.cure_poison,
            "clearDotStress": self.clear_dot_stress,
            "tag": self.tag,
            "untag": self.untag,
            "unstun": self.unstun,
            "guard": self.guard,
            "clearguarding": self.clear_guarding,
            "clearguarded": self.clear_guarded,
            "dotShuffle": self.dot_shuffle,
            "kill": self.kill,
            "immobilize": self.immobilize,
            "unimmobilize": self.unimmobilize,
            "uncontrol": self.uncontrol,
            "capture": self.capture,
            "capture_remove_from_party": self.capture_remove_from_party,
            "remove_vampire": self.remove_vampire,
            "cure_disease": self.cure_disease,
            "stealth": self.stealth,
            "unstealth": self.unstealth,
            "clear_debuff": self.clear_debuff,
            "clearvirtue": self.clear_virtue,
            "daze": self.daze,
            "undaze": self.undaze,
            "riposte": self.riposte,
            "clear_riposte": self.clear_riposte,
            "performer_rank_target": self.performer_rank_target
        }
        for k, v in one_zeros.items():
            if v:
                res.append(f'.{k} 1')

        riposte_percent = {
            "riposte_on_hit_chance_add": self.riposte_on_hit_chance_add,
            "riposte_on_miss_chance_add": self.riposte_on_miss_chance_add,
            "riposte_on_hit_chance_multiply": self.riposte_on_hit_chance_add,
            "riposte_on_miss_chance_multiply": self.riposte_on_miss_chance_add,
        }
        for k, v in riposte_percent.items():
            if v is not None:
                res.append(f'.{k} {float_to_percent_int(v)}%')
        if self.riposte_effect is not None:
            tem = []
            for eft in self.riposte_effect:
                tem.append(f'"{get_entry_id(eft)}"')
            tem = " ".join(tem)
            res.append(f'.riposte_effect {tem}')

        if self.can_apply_on_death is None:
            if self.push is not None or self.pull is not None \
                    or self.shuffle_party or self.shuffle_target or self.instant_shuffle:
                can_apply_on_death = True
            else:
                can_apply_on_death = self.can_apply_on_death
        else:
            can_apply_on_death = self.can_apply_on_death
        if can_apply_on_death is not None:
            res.append(f'.can_apply_on_death {bool_to_lower_str(can_apply_on_death)}')

        true_false_display_false = {
            "riposte_validate": self.riposte_validate,
            "can_crit_heal": self.can_crit_heal,
            "has_description": self.has_description,
            "buff_is_clear_debuff_valid": self.buff_is_clear_debuff_valid
        }
        for k, v in true_false_display_false.items():
            if not v:
                res.append(f'.{k} false')

        true_false_display_ture = {
            "swap_source_and_target": self.swap_source_and_target,
            "crit_doesnt_apply_to_roll": self.crit_doesnt_apply_to_roll,
            "apply_once": self.apply_once,
            "apply_with_result": self.apply_with_result,
            "skill_instant": self.skill_instant,
            "refreshes_skill_uses": self.refreshes_skill_uses,
            "individual_target_actor_rolls": self.individual_target_actor_rolls,
            "skips_endless_wave_curio": self.skips_endless_wave_curio
        }
        for k, v in true_false_display_ture.items():
            if v:
                res.append(f'.{k} true')

        if self.dot_source is not None:
            res.append(f'.dotSource {self.dot_source.value}')
        int_value_larger_than_zero = {
            "dotBleed": self.dot_bleed,
            "dotPoison": self.dot_poison,
            "dotStress": self.dot_stress,
            "dotHpHeal": self.dot_hp_heal,
            "healstress": self.heal_stress,
            "stress": self.stress,
            "heal": self.heal,
            "stun": self.stun,
            "torch_decrease": self.torch_decrease,
            "torch_increase": self.torch_increase,
            "push": self.push,
            "pull": self.pull,
            "control": self.control,
            "health_damage": self.health_damage,
            "health_damage_blocks": self.health_damage_blocks
        }
        for k, v in int_value_larger_than_zero.items():
            if v is None:
                continue
            # if v <= 0:
            #     raise ValueError(f"{k} must be larger than 0")
            res.append(f'.{k} {v}')

        float_percent = {
            "virtue_blockable_chance": self.virtue_blockable_chance,
            "affliction_blockable_chance": self.affliction_blockable_chance
        }
        for k, v in float_percent.items():
            if v is not None:
                res.append(f'.{k} {float_to_percent_str(v)}%')

        if self.heal_percent is not None:
            res.append(f'.heal_percent {self.heal_percent}')
        if self.source_heal_type is not None:
            res.append(f'.source_heal_type {self.source_heal_type.value}')
        if self.steal_buff_stat_type is not None:
            res.append(f'.steal_buff_stat_type {self.steal_buff_stat_type.value}')
        if self.steal_buff_source_type is not None:
            res.append(f'.steal_buff_source_type {self.steal_buff_source_type.value}')
        if self.kill_enemy_types is not None:
            res.append(f'.kill_enemy_types {get_entry_id(self.kill_enemy_types)}')
        if self.disease is not None:
            res.append(f'.disease {get_entry_id(self.disease)}')
        if self.set_mode is not None:
            res.append(f'.set_mode {get_entry_id(self.set_mode)}')
        if self.actor_dot is not None:
            res.append(f'.actor_dot {get_entry_id(self.actor_dot)}')
        if self.barks is not None:
            res.append(f'.bark {self.bark_id()}')
        if self.damage_type is not None:
            res.append(f'.damage_type {self.damage_type.value}')
        if self.damage_source_type is not None:
            res.append(f'.damage_source_type {self.damage_source_type.value}')
        if self.damage_source_data is not None:
            res.append(f'.damage_source_data {get_entry_id(self.damage_source_data)}')
        if self.use_item_id is not None:
            res.append(f'.use_item_id {get_entry_id(self.use_item_id)}')
        if self.use_item_type is not None:
            res.append(f'use_item_type {self.use_item_type.value}')
        if self.rank_target is not None:
            res.append(f'.rank_target {self.rank_target}')
        if self.clear_rank_target is not None:
            res.append(f'.clear_rank_target {self.clear_rank_target}')

        if self.summon_monsters is not None and len(self.summon_monsters) > 0:
            res.append(".summon_monsters")
            for item in self.summon_monsters:
                res.append(f'{item}')
        if self.summon_chances is not None and len(self.summon_chances) > 0:
            res.append(".summon_chances")
            for item in self.summon_chances:
                res.append(f'{item}')
        if self.summon_ranks is not None and len(self.summon_ranks) > 0:
            res.append(".summon_ranks")
            for item in self.summon_ranks:
                res.append(f'{item}')
        if self.summon_limits is not None and len(self.summon_limits) > 0:
            res.append(".summon_limits")
            for item in self.summon_limits:
                res.append(f'{item}')
        if self.summon_count is not None:
            if self.summon_count <= 0:
                raise ValueError("summon_count must be larger than 0")
            res.append(f'.summon_count {self.summon_count}')
        if self.summon_erase_data_on_roll is not None:
            res.append(f'.summon_erase_data_on_roll {1 if self.summon_erase_data_on_roll else 0}')
        if self.summon_can_spawn_loot is not None:
            res.append(f'.summon_can_spawn_loot {bool_to_lower_str(self.summon_can_spawn_loot)}')
        if self.summon_rank_is_previous_monster_class is not None:
            res.append(f'.summon_rank_is_previous_monster_class '
                       f'{1 if self.summon_rank_is_previous_monster_class else 0}')
        if self.summon_does_roll_initiatives is not None:
            res.append(f'.summon_does_roll_initiatives {1 if self.summon_does_roll_initiatives else 0}')

        if self.set_monster_class_id is not None and self.set_monster_class_ids is not None:
            raise ValueError("set_monster_class_id and set_monster_class_ids cannot be set at the same time")
        if self.set_monster_class_id is not None or self.set_monster_class_ids is not None:
            if self.set_monster_class_id is not None:
                res.append(f'.set_monster_class_id {self.set_monster_class_id}')
            if self.set_monster_class_ids is not None and len(self.set_monster_class_ids) > 0:
                res.append(f'.set_monster_class_ids')
                for item in self.set_monster_class_ids:
                    res.append(f'{item}')
            if self.set_monster_class_chances is not None and len(self.set_monster_class_chances) > 0:
                res.append(f'.set_monster_class_chances')
                for item in self.set_monster_class_chances:
                    res.append(f'{item}')
            if self.set_monster_class_reset_hp is not None:
                res.append(f'.set_monster_class_reset_hp {1 if self.set_monster_class_reset_hp else 0}')
            if self.set_monster_class_reset_buffs is not None:
                res.append(f'.set_monster_class_reset_buffs {bool_to_lower_str(self.set_monster_class_reset_buffs)}')
            if self.set_monster_class_carry_over_hp_min_percent is not None:
                res.append(f'.set_monster_class_carry_over_hp_min_percent '
                           f'{self.set_monster_class_carry_over_hp_min_percent}')
            if self.set_monster_class_clear_initiative is not None:
                res.append(f'.set_monster_class_clear_initiative '
                           f'{bool_to_lower_str(self.set_monster_class_clear_initiative)}')
            if self.set_monster_class_clear_monster_brain_cooldowns is not None:
                res.append(f'.set_monster_class_clear_monster_brain_cooldowns '
                           f'{bool_to_lower_str(self.set_monster_class_clear_monster_brain_cooldowns)}')
            if self.set_monster_class_reset_scale is not None:
                res.append(f'.set_monster_class_reset_scale {bool_to_lower_str(self.set_monster_class_reset_scale)}')

        if self.buff_type is not None:
            res.append(f'.buff_type {self.buff_type.value}')
            if self.buff_sub_type is not None:
                res.append(f'.buff_sub_type {get_entry_id(self.buff_sub_type)}')
            if self.buff_amount is not None:
                res.append(f'.buff_amount {self.buff_amount}')
        if self.buff_duration_type is not None:
            res.append(f'.buff_duration_type {self.buff_duration_type.value}')
        if self.key_status is not None:
            res.append(f'.keyStatus {self.key_status.value}')
        if self.monster_type is not None:
            res.append(f'.monsterType {get_entry_id(self.monster_type)}')

        if self.buff_source_type is not None:
            res.append(f'.buff_source_type {self.buff_source_type.value}')

        if len(buff_ids) > 0:
            res.append(f".buff_ids")
            for buff in buff_ids:
                res.append(f'"{get_entry_id(buff)}"')

        if self.combat_stat_buff:
            res.append(f'.combat_stat_buff 1')
        float_percent = {
            "damage_low_multiply": self.damage_low_multiply,
            "damage_high_multiply": self.damage_high_multiply,
            "max_hp_multiply": self.max_hp_multiply,
            "attack_rating_add": self.attack_rating_add,
            "crit_chance_add": self.crit_chance_add,
            "defense_rating_add": self.defense_rating_add,
            "protection_rating_add": self.protection_rating_add
        }
        for k, v in float_percent.items():
            if v is not None:
                res.append(f'.{k} {float_to_percent_str(v)}%')
        float_direct = {
            "damage_low_add": self.damage_low_add,
            "damage_high_add": self.damage_high_add,
            "max_hp_add": self.max_hp_add
        }
        for k, v in float_direct.items():
            if v is not None:
                res.append(f'.{k} {v}')

        int_value = {
            "speed_rating_add": self.speed_rating_add,
            "initiative_change": self.initiative_change,
            "duration": self.duration
        }
        for k, v in int_value.items():
            if v is not None:
                res.append(f'.{k} {v}')

        if self.queue is None:
            if self.push is not None or self.pull is not None \
                    or self.shuffle_target or self.shuffle_party or self.instant_shuffle:
                queue = False
            else:
                queue = True
        else:
            queue = self.queue

        true_false_display_all = {
            "on_hit": self.on_hit,
            "on_miss": self.on_miss,
            "queue": queue
        }
        for k, v in true_false_display_all.items():
            res.append(f'.{k} {bool_to_lower_str(v)}')

        return " ".join(res)

    def __str__(self):
        if self.buff_ids is None:
            return self._one_line([])
        i = 0
        buff_ids = []
        res = []
        for buff in self.buff_ids:
            buff_ids.append(buff)
            if (i + 1) % 8 == 0:
                res.append(self._one_line(buff_ids))
                buff_ids = []
            i += 1
        if len(buff_ids) > 0:
            res.append(self._one_line(buff_ids))
        return "\n".join(res)


if __name__ == '__main__':
    e = Effect(
        target=EffectTarget.PERFORMER,
        buff_ids=[
            "test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8",
            "test9", "test10", "test11", "test12", "test13", "test14", "test15", "test16",
            "test17", "test18", "test19", "test20", "test21", "test22", "test23", "test24",
            "test25", "test26", "test27", "test28", "test29", "test30", "test31", "test32",
            "test33", "test34", "test35", "test36", "test37", "test38", "test39", "test40",
            "test41", "test42",
        ],
        combat_stat_buff=True,
        damage_low_multiply=1,
    )
    print(e)
