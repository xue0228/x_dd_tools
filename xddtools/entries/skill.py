import os.path
from typing import Optional, Union, Tuple, List, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from xddtools.base import EffectEntry, ModeEntry, MonsterEntry, HeroEntry, get_entry_id, AnimationEntry, SkillEntry, \
    BankEntry
from xddtools.enum import HeroClass, MonsterClass
from xddtools.enum.skill import SkillHeadType, SkillType, InnerFx
from xddtools.name import AutoName
from xddtools.path import DATA_PATH
from xddtools.target import Target
from xddtools.utils import bool_to_lower_str, float_to_percent_int, is_zero, is_image


class ModeEffects(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    valid_mode: ModeEntry
    effects: Optional[Sequence[Union[EffectEntry, str]]] = None


class SkillInfo(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    atk: float = 0.0
    defence: float = 0.0
    dmg: Union[float, Tuple[int, int]] = 0.0
    crit: float = 0.0
    move_back: int = 0
    move_forward: int = 0

    heal: Optional[Tuple[int, int]] = None
    required_performer_hp_range: Optional[Tuple[float, float]] = None
    rank_damage_modifiers: Optional[Tuple[float, float, float, float]] = None

    starting_cooldown: Optional[int] = None
    per_battle_limit: Optional[int] = None
    per_turn_limit: Optional[int] = None
    extra_targets_count: Optional[int] = None

    extra_targets_chance: Optional[float] = None
    damage_heal_base_class_ids: Optional[Sequence[Union[MonsterClass, HeroClass, MonsterEntry, HeroEntry, str]]] = None

    effect_ids: Optional[Sequence[Union[EffectEntry, str]]] = None
    valid_modes_and_effects: Optional[Sequence[ModeEffects]] = None

    is_continue_turn: bool = False
    ignore_stealth: bool = False
    ignore_guard: bool = False
    ignore_protection: bool = False
    generation_guaranteed: bool = False
    is_user_selected_targets: bool = False
    refresh_after_each_wave: bool = False
    ignore_deathsdoor: bool = False

    self_target_valid: bool = True
    is_crit_valid: bool = True
    can_be_riposted: bool = True
    can_crit_heal: bool = True
    is_knowledgeable: bool = True
    is_stall_invalidating: bool = True

    is_monster_rerank_valid_on_attack: Optional[bool] = None
    is_monster_rerank_valid_on_friendly_presentation_end: Optional[bool] = None
    is_monster_rerank_valid_on_friendly_post_result: Optional[bool] = None

    @staticmethod
    def _limited_extra_effects(
            skill_head_type: SkillHeadType,
            entry_id: str,
            level: int,
            effect_ids: List[str]
    ) -> str:
        res = [f'{skill_head_type.value}: .id "{entry_id}"']
        if skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {level}')
        if len(effect_ids) > 0:
            tem = " ".join([f'"{effect_id}"' for effect_id in effect_ids])
            res.append(f'.effect {tem}')
        return " ".join(res)

    def _all_extra_effects(
            self,
            skill_head_type: SkillHeadType,
            entry_id: str,
            level: int,
            effects_ids: List[str]
    ) -> str:
        result = []
        # 遍历buff_ids，步长为8
        for i in range(0, len(effects_ids), 8):
            # 获取当前组的buff_ids（最多8个）
            current_buff_ids = effects_ids[i:i + 8]
            # 调用_limited_extra_buff_ids方法并添加结果
            result.append(self._limited_extra_effects(skill_head_type, entry_id, level, current_buff_ids))
        return "\n".join(result)

    @staticmethod
    def _one_mode_effects(
            skill_head_type: SkillHeadType,
            entry_id: str, level: int,
            mode_effects: ModeEffects
    ) -> str:
        mode = mode_effects.valid_mode
        effects = mode_effects.effects
        res = [f'{skill_head_type.value}: .id "{entry_id}"']
        if skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {level}')
        mode = get_entry_id(mode)
        res.append(f'.valid_modes {mode}')
        if effects is not None:
            res.append(f".{mode}_effects")
            for effect in effects:
                res.append(f'"{get_entry_id(effect)}"')
        return " ".join(res)

    def info(
            self,
            skill_head_type: SkillHeadType,
            skill_type: Optional[SkillType],
            launch: Optional[Target],
            target: Optional[Target],
            entry_id: str,
            level: int
    ) -> str:
        res = [f'{skill_head_type.value}: .id "{entry_id}"']
        if skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {level}')
        if skill_type is not None:
            res.append(f'.type "{skill_type.value}"')

        if not (isinstance(self.dmg, (float, int)) and is_zero(self.atk)):
            res.append(f'.atk {float_to_percent_int(self.atk)}%')
            if not is_zero(self.defence):
                res.append(f'.def {float_to_percent_int(self.defence)}%')
            if isinstance(self.dmg, (list, tuple)):
                if skill_head_type != SkillHeadType.SKILL:
                    raise ValueError(f"only monster's dmg use tuple of two ints,hero use float")
                if len(self.dmg) != 2:
                    raise ValueError(f'dmg must be float or tuple of two ints')
                res.append(f'.dmg {self.dmg[0]} {self.dmg[1]}')
            else:
                if skill_head_type == SkillHeadType.SKILL:
                    raise ValueError(f"monster's dmg must use tuple of two ints as dmg range")
                res.append(f'.dmg {float_to_percent_int(self.dmg)}%')
            res.append(f'.crit {float_to_percent_int(self.crit)}%')

        if self.move_back != 0 or self.move_forward != 0:
            res.append(f'.move {self.move_back} {self.move_forward}')
        if launch is not None:
            res.append(f'.launch {launch}')
        if target is not None:
            res.append(f'.target {target}')

        if self.heal is not None:
            if not isinstance(self.heal, (list, tuple)):
                raise ValueError(f'heal must be tuple of two ints')
            if len(self.heal) != 2:
                raise ValueError(f'heal must be tuple of two ints')
            res.append(f'.heal {self.heal[0]} {self.heal[1]}')

        if self.required_performer_hp_range is not None:
            if not isinstance(self.required_performer_hp_range, (list, tuple)):
                raise ValueError(f'required_performer_hp_range must be tuple of two floats')
            if len(self.required_performer_hp_range) != 2:
                raise ValueError(f'required_performer_hp_range must be tuple of two floats')
            res.append(f'.required_performer_hp_range '
                       f'{self.required_performer_hp_range[0]} {self.required_performer_hp_range[1]}')

        if self.rank_damage_modifiers is not None:
            if not isinstance(self.rank_damage_modifiers, (list, tuple)):
                raise ValueError(f'rank_damage_modifiers must be tuple of four floats')
            if len(self.rank_damage_modifiers) != 4:
                raise ValueError(f'rank_damage_modifiers must be tuple of four floats')
            res.append(f'.rank_damage_modifiers '
                       f'{self.rank_damage_modifiers[0]} {self.rank_damage_modifiers[1]} '
                       f'{self.rank_damage_modifiers[2]} {self.rank_damage_modifiers[3]}')

        none_int = {
            "starting_cooldown": self.starting_cooldown,
            "per_battle_limit": self.per_battle_limit,
            "per_turn_limit": self.per_turn_limit,
            "extra_targets_count": self.extra_targets_count,
        }
        for k, v in none_int.items():
            if v is not None:
                res.append(f'.{k} {v}')
        if self.extra_targets_chance is not None:
            if not 0 < self.extra_targets_chance <= 1:
                raise ValueError(f'extra_targets_chance must be float in range (0,1]')
            res.append(f'.extra_targets_chance {self.extra_targets_chance}')

        if self.damage_heal_base_class_ids is not None:
            res.append(f'.damage_heal_base_class_ids')
            for item in self.damage_heal_base_class_ids:
                res.append(f'{get_entry_id(item)}')

        # effects
        extra_effects = []
        if self.effect_ids is not None:
            res.append(".effect")
            effect_idx = 0
            for effect in self.effect_ids:
                effect = get_entry_id(effect)
                if effect_idx < 8:
                    res.append(f'"{effect}"')
                else:
                    extra_effects.append(effect)
                effect_idx += 1

        default_false = {
            "is_continue_turn": self.is_continue_turn,
            "ignore_stealth": self.ignore_stealth,
            "ignore_guard": self.ignore_guard,
            "ignore_protection": self.ignore_protection,
            "generation_guaranteed": self.generation_guaranteed,
            "is_user_selected_targets": self.is_user_selected_targets,
            "refresh_after_each_wave": self.refresh_after_each_wave,
            "ignore_deathsdoor": self.ignore_deathsdoor,
        }
        for k, v in default_false.items():
            if v:
                res.append(f'.{k} true')
        default_true = {
            "self_target_valid": self.self_target_valid,
            "is_crit_valid": self.is_crit_valid,
            "can_be_riposted": self.can_be_riposted,
            "can_crit_heal": self.can_crit_heal,
            "is_knowledgeable": self.is_knowledgeable,
            "is_stall_invalidating": self.is_stall_invalidating,
        }
        for k, v in default_true.items():
            if not v:
                res.append(f'.{k} false')
        default_none = {
            "is_monster_rerank_valid_on_attack": self.is_monster_rerank_valid_on_attack,
            "is_monster_rerank_valid_on_friendly_presentation_end":
                self.is_monster_rerank_valid_on_friendly_presentation_end,
            "is_monster_rerank_valid_on_friendly_post_result": self.is_monster_rerank_valid_on_friendly_post_result,
        }
        for k, v in default_none.items():
            if v is not None:
                res.append(f'.{k} {bool_to_lower_str(v)}')

        res = [" ".join(res)]
        if len(extra_effects) > 0:
            res.append(self._all_extra_effects(skill_head_type, entry_id, level, extra_effects))
        if self.valid_modes_and_effects is not None:
            for mode_effects in self.valid_modes_and_effects:
                res.append(self._one_mode_effects(skill_head_type, entry_id, level, mode_effects))

        return "\n".join(res)


class Skill(SkillEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    skill_head_type: SkillHeadType = SkillHeadType.COMBAT_SKILL
    skill_type: Optional[SkillType] = None
    launch: Optional[Target] = None
    target: Optional[Target] = None

    skill_info: Union[SkillInfo, Sequence[SkillInfo]]

    can_upgraded: bool = False  # len(skill_info) > 1 时始终为 True
    upgrade_golds: Sequence[int] = (1000, 250, 750, 1250, 2500)  # 确保 len(upgrade_golds) >= len(skill_info)

    skill_name: Optional[str] = None
    upgrade_tree_name: Optional[str] = None

    # art
    icon_image: Optional[str] = None
    icon: Optional[str] = None
    anim: Union[AnimationEntry, str, None] = None
    fx: Union[AnimationEntry, InnerFx, str, None] = None
    targfx: Union[AnimationEntry, InnerFx, str, None] = None
    targheadfx: Union[AnimationEntry, InnerFx, str, None] = None
    targchestfx: Union[AnimationEntry, InnerFx, str, None] = None
    misstargfx: Union[AnimationEntry, InnerFx, str, None] = None
    misstargheadfx: Union[AnimationEntry, InnerFx, str, None] = None
    misstargchestfx: Union[AnimationEntry, InnerFx, str, None] = None
    custom_target_anim: Union[AnimationEntry, InnerFx, str, None] = None

    area_pos_offset: Optional[Tuple[float, float]] = None
    target_area_pos_offset: Optional[Tuple[float, float]] = None

    custom_idle_anim_name: Union[AnimationEntry, str, None] = None
    custom_idle_round_duration: Optional[int] = None

    reset_source_stance: bool = True
    reset_target_stance: bool = True
    can_display_selection: bool = True
    has_crit_vo: bool = True
    can_display_skill_name: bool = True

    nil: bool = False
    hide_performer_health: bool = False
    condensed_tooltip_stats: bool = False
    condensed_tooltip_type: bool = False
    condensed_tooltip_effects: bool = False

    condensed_tooltip_effects_per_line: Optional[int] = None

    can_display_performer_selection_after_turn: Optional[bool] = None

    # sfx
    hit_sfx: Union[BankEntry, str, None] = None
    miss_sfx: Union[BankEntry, str, None] = None

    entry_id: str = Field(default_factory=lambda x: AutoName().new_skill(), frozen=True)

    @field_validator("icon_image")
    @classmethod
    def _check_icon_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    @model_validator(mode="after")
    def _check_after(self):
        if not isinstance(self.skill_info, SkillInfo):
            if len(self.skill_info) > 5:
                raise ValueError(f"skills only have 5 levels,but now have {len(self.skill_info)}")

        if self.skill_head_type == SkillHeadType.COMBAT_MOVE_SKILL:
            if self.icon is None:
                self.icon = "generic_move"
            if self.anim is None:
                self.anim = "idle"
        elif self.skill_head_type == SkillHeadType.RIPOSTE_SKILL:
            if self.anim is None:
                self.anim = "riposte"
            if self.targfx is None and self.targheadfx is None and self.targchestfx is None:
                self.targfx = InnerFx.BLOOD_SPLATTER
        else:
            if self.icon_image is None:
                self.icon_image = os.path.join(DATA_PATH, r"template/hero/unknown_skill.png")
            if self.icon is None:
                self.icon = self.id()
        return self

    def art(self) -> str:
        res = [f'{self.skill_head_type.value}: .id "{self.id()}"']

        none_str = {
            "icon": self.icon,
            "anim": self.anim,
            "fx": self.fx,
            "targfx": self.targfx,
            "targheadfx": self.targheadfx,
            "targchestfx": self.targchestfx,
            "misstargfx": self.misstargfx,
            "misstargchestfx": self.misstargchestfx,
            "custom_target_anim": self.custom_target_anim,
        }
        for k, v in none_str.items():
            if v is not None:
                res.append(f'.{k} "{get_entry_id(v)}"')

        none_tuple_float = {
            "area_pos_offset": self.area_pos_offset,
            "target_area_pos_offset": self.target_area_pos_offset,
        }
        for k, v in none_tuple_float.items():
            if v is not None:
                res.append(f'.{k} {v[0]} {v[1]}')

        if self.custom_idle_anim_name is not None:
            res.append(f'.custom_idle_anim_name "{get_entry_id(self.custom_idle_anim_name)}"')
            if self.custom_idle_round_duration is not None:
                res.append(f'.custom_idle_round_duration {self.custom_idle_round_duration}')

        default_true = {
            "reset_source_stance": self.reset_source_stance,
            "reset_target_stance": self.reset_target_stance,
            "can_display_selection": self.can_display_selection,
            "has_crit_vo": self.has_crit_vo,
            "can_display_skill_name": self.can_display_skill_name,
        }
        for k, v in default_true.items():
            if not v:
                res.append(f'.{k} false')

        default_false = {
            "nil": self.nil,
            "hide_performer_health": self.hide_performer_health,
            "condensed_tooltip_stats": self.condensed_tooltip_stats,
            "condensed_tooltip_type": self.condensed_tooltip_type,
            "condensed_tooltip_effects": self.condensed_tooltip_effects,
        }
        for k, v in default_false.items():
            if v:
                res.append(f'.{k} true')

        if self.condensed_tooltip_effects_per_line is not None:
            res.append(f'.condensed_tooltip_effects_per_line {self.condensed_tooltip_effects_per_line}')

        if self.can_display_performer_selection_after_turn is not None:
            res.append(f'.can_display_performer_selection_after_turn '
                       f'{bool_to_lower_str(self.can_display_performer_selection_after_turn)}')
        else:
            if self.target is not None and self.target.is_friend():
                res.append(f'.can_display_performer_selection_after_turn false')

        return " ".join(res)

    def info(self) -> str:
        if isinstance(self.skill_info, SkillInfo):
            skill_info = [self.skill_info]
        else:
            skill_info = self.skill_info
        res = [skill.info(
            self.skill_head_type,
            self.skill_type,
            self.launch,
            self.target,
            self.id(),
            i
        ) for i, skill in enumerate(skill_info)]
        return "\n".join(res)


if __name__ == '__main__':
    info = SkillInfo(
        atk=1,
        dmg=1,
        effect_ids=("e1", "e2", "e3", "e4", "e1", "e2", "e3", "e4", "e1", "e2", "e3", "e4"),
        valid_modes_and_effects=[
            ModeEffects(valid_mode="mode_0", effects=["e1", "e2", "e3", "e4"]),
            ModeEffects(valid_mode="mode_1"),
        ]
    )
    # info.effect_ids = ["e1", "e2", "e3", "e4", "e1", "e2", "e3", "e4", "e1", "e2", "e3", "e4"]
    print(info.effect_ids)
    s = Skill(skill_info=[info, info, info])
    print(s.skill_info[0].effect_ids)
    print(s.info())
    print(s.skill_info[0].effect_ids)
