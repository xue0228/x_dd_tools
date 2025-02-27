from enum import Enum
from typing import Optional, Tuple, Union, Iterable, List

from xddtools.animation import Animation
from xddtools.base import BaseID
from xddtools.core import Mode
from xddtools.effects import Effect
from xddtools.enums import SkillHeadType, Level, SkillType, MonsterClass, HeroClass, InnerFx
from xddtools.target import Target, SELF, LAUNCH_ANY
from xddtools.utils import is_zero, float_to_percent_int, bool_to_lower_str


class Skill(BaseID):
    def __init__(
            self,
            skill_name: str,

            skill_head_type: SkillHeadType = SkillHeadType.COMBAT_SKILL,
            level: Level = Level.ZERO,
            skill_type: Optional[SkillType] = None,
            atk: float = 0.0,
            defence: float = 0.0,
            dmg: Union[float, Tuple[int, int]] = 0.0,
            crit: float = 0.0,
            move_back: int = 0,
            move_forward: int = 0,
            launch: Optional[Target] = None,
            target: Optional[Target] = None,

            heal: Optional[Tuple[int, int]] = None,
            required_performer_hp_range: Optional[Tuple[float, float]] = None,
            rank_damage_modifiers: Optional[Tuple[float, float, float, float]] = None,

            starting_cooldown: Optional[int] = None,
            per_battle_limit: Optional[int] = None,
            per_turn_limit: Optional[int] = None,
            extra_targets_count: Optional[int] = None,

            extra_targets_chance: Optional[float] = None,
            damage_heal_base_class_ids: Optional[Iterable[Union[MonsterClass, HeroClass, str]]] = None,

            effect_ids: Optional[Iterable[Union[Effect, str]]] = None,
            valid_modes_and_effects: Optional[Iterable[Tuple[
                Union[Mode, str], Optional[Iterable[Union[Effect, str]]]]
            ]] = None,

            is_continue_turn: bool = False,
            ignore_stealth: bool = False,
            ignore_guard: bool = False,
            ignore_protection: bool = False,
            generation_guaranteed: bool = False,
            is_user_selected_targets: bool = False,
            refresh_after_each_wave: bool = False,
            ignore_deathsdoor: bool = False,

            self_target_valid: bool = True,
            is_crit_valid: bool = True,
            can_be_riposted: bool = True,
            can_crit_heal: bool = True,
            is_knowledgeable: bool = True,
            is_stall_invalidating: bool = True,

            is_monster_rerank_valid_on_attack: Optional[bool] = None,
            is_monster_rerank_valid_on_friendly_presentation_end: Optional[bool] = None,
            is_monster_rerank_valid_on_friendly_post_result: Optional[bool] = None,

            # art
            icon: Optional[str] = None,
            anim: Union[Animation, str, InnerFx, None] = None,
            fx: Union[Animation, str, InnerFx, None] = None,
            targfx: Union[Animation, str, InnerFx, None] = None,
            targheadfx: Union[Animation, str, InnerFx, None] = None,
            targchestfx: Union[Animation, str, InnerFx, None] = None,
            misstargfx: Union[Animation, str, InnerFx, None] = None,
            misstargheadfx: Union[Animation, str, InnerFx, None] = None,
            misstargchestfx: Union[Animation, str, InnerFx, None] = None,
            custom_target_anim: Union[Animation, str, InnerFx, None] = None,

            area_pos_offset: Optional[Tuple[float, float]] = None,
            target_area_pos_offset: Optional[Tuple[float, float]] = None,

            custom_idle_anim_name: Union[Animation, str, InnerFx, None] = None,
            custom_idle_round_duration: Optional[int] = None,

            reset_source_stance: bool = True,
            reset_target_stance: bool = True,
            can_display_selection: bool = True,
            has_crit_vo: bool = True,
            can_display_skill_name: bool = True,

            nil: bool = False,
            hide_performer_health: bool = False,
            condensed_tooltip_stats: bool = False,
            condensed_tooltip_type: bool = False,
            condensed_tooltip_effects: bool = False,

            condensed_tooltip_effects_per_line: Optional[int] = None,

            can_display_performer_selection_after_turn: Optional[bool] = None
    ):
        if target is None:
            target = SELF
        if launch is None:
            launch = LAUNCH_ANY

        self.skill_head_type = skill_head_type
        self.level = level
        self.skill_type = skill_type
        self.atk = atk
        self.defence = defence
        self.dmg = dmg
        self.crit = crit
        self.move_back = move_back
        self.move_forward = move_forward
        self.launch = launch
        self.target = target
        self.heal = heal
        self.required_performer_hp_range = required_performer_hp_range
        self.rank_damage_modifiers = rank_damage_modifiers
        self.starting_cooldown = starting_cooldown
        self.per_battle_limit = per_battle_limit
        self.per_turn_limit = per_turn_limit
        self.extra_targets_count = extra_targets_count
        self.extra_targets_chance = extra_targets_chance
        self.effect_ids = effect_ids
        self.valid_modes_and_effects = valid_modes_and_effects
        self.damage_heal_base_class_ids = damage_heal_base_class_ids
        self.is_continue_turn = is_continue_turn
        self.ignore_stealth = ignore_stealth
        self.ignore_guard = ignore_guard
        self.ignore_protection = ignore_protection
        self.generation_guaranteed = generation_guaranteed
        self.is_user_selected_targets = is_user_selected_targets
        self.refresh_after_each_wave = refresh_after_each_wave
        self.ignore_deathsdoor = ignore_deathsdoor
        self.self_target_valid = self_target_valid
        self.is_crit_valid = is_crit_valid
        self.can_be_riposted = can_be_riposted
        self.can_crit_heal = can_crit_heal
        self.is_knowledgeable = is_knowledgeable
        self.is_stall_invalidating = is_stall_invalidating
        self.is_monster_rerank_valid_on_attack = is_monster_rerank_valid_on_attack
        self.is_monster_rerank_valid_on_friendly_presentation_end = is_monster_rerank_valid_on_friendly_presentation_end
        self.is_monster_rerank_valid_on_friendly_post_result = is_monster_rerank_valid_on_friendly_post_result

        self.icon = icon
        self.anim = anim
        self.fx = fx
        self.targfx = targfx
        self.targheadfx = targheadfx
        self.targchestfx = targchestfx
        self.misstargfx = misstargfx
        self.misstargheadfx = misstargheadfx
        self.misstargchestfx = misstargchestfx
        self.custom_target_anim = custom_target_anim
        self.area_pos_offset = area_pos_offset
        self.target_area_pos_offset = target_area_pos_offset
        self.custom_idle_anim_name = custom_idle_anim_name
        self.custom_idle_round_duration = custom_idle_round_duration
        self.condensed_tooltip_effects_per_line = condensed_tooltip_effects_per_line
        self.reset_source_stance = reset_source_stance
        self.reset_target_stance = reset_target_stance
        self.can_display_selection = can_display_selection
        self.has_crit_vo = has_crit_vo
        self.can_display_skill_name = can_display_skill_name
        self.nil = nil
        self.hide_performer_health = hide_performer_health
        self.condensed_tooltip_effects = condensed_tooltip_effects
        self.condensed_tooltip_stats = condensed_tooltip_stats
        self.condensed_tooltip_type = condensed_tooltip_type
        self.can_display_performer_selection_after_turn = can_display_performer_selection_after_turn
        super().__init__(name=skill_name)

    def _limited_extra_effects(self, effect_ids: List[str]) -> str:
        res = [f'{self.skill_head_type.value}: .id "{self.id}"']
        if self.skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {self.level.value}')
        if len(effect_ids) > 0:
            tem = " ".join([f'"{effect_id}"' for effect_id in effect_ids])
            res.append(f'.effect {tem}')
        return " ".join(res) + "\n"

    def _all_extra_effects(self, effects_ids: List[str]) -> str:
        result = ""
        # 遍历buff_ids，步长为8
        for i in range(0, len(effects_ids), 8):
            # 获取当前组的buff_ids（最多8个）
            current_buff_ids = effects_ids[i:i + 8]
            # 调用_limited_extra_buff_ids方法并添加结果
            result += self._limited_extra_effects(current_buff_ids)
        return result

    def _one_mode_effects(
            self,
            mode: Union[Mode, str],
            effects: Optional[Iterable[Union[Effect, str]]]
    ) -> str:
        res = [f'{self.skill_head_type.value}: .id "{self.id}"']
        if self.skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {self.level.value}')
        mode = mode.id if isinstance(mode, Mode) else mode
        res.append(f'.valid_modes {mode}')
        if effects is not None:
            res.append(f".{mode}_effects")
            for effect in effects:
                res.append(f'"{effect.id if isinstance(effect, Effect) else effect}"')
        return " ".join(res) + "\n"

    @property
    def info(self) -> str:
        res = [f'{self.skill_head_type.value}: .id "{self.id}"']
        if self.skill_head_type != SkillHeadType.SKILL:
            res.append(f'.level {self.level.value}')
        if self.skill_type is not None:
            res.append(f'.type "{self.skill_type.value}"')

        if not (isinstance(self.dmg, (float, int)) and is_zero(self.dmg)):
            res.append(f'.atk {float_to_percent_int(self.atk)}%')
            if not is_zero(self.defence):
                res.append(f'.def {float_to_percent_int(self.defence)}%')
            if isinstance(self.dmg, (list, tuple)):
                if self.skill_head_type != SkillHeadType.SKILL:
                    raise ValueError(f"only monster's dmg use tuple of two ints,hero use float")
                if len(self.dmg) != 2:
                    raise ValueError(f'dmg must be float or tuple of two ints')
                res.append(f'.dmg {self.dmg[0]} {self.dmg[1]}')
            else:
                if self.skill_head_type == SkillHeadType.SKILL:
                    raise ValueError(f"monster's dmg must use tuple of two ints as dmg range")
                res.append(f'.dmg {float_to_percent_int(self.dmg)}%')
            res.append(f'.crit {float_to_percent_int(self.crit)}%')

        if self.move_back != 0 or self.move_forward != 0:
            res.append(f'.move {self.move_back} {self.move_forward}')
        if self.launch is not None:
            res.append(f'.launch {self.launch}')
        if self.target is not None:
            res.append(f'.target {self.target}')

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
                res.append(f'{item.value if isinstance(item, Enum) else item}')

        # effects
        if self.effect_ids is not None:
            res.append(".effect")
        extra_effects = []
        effect_idx = 0
        for effect in self.effect_ids:
            effect = effect.id if isinstance(effect, Effect) else effect
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

        res = " ".join(res) + "\n" + self._all_extra_effects(extra_effects)
        if self.valid_modes_and_effects is not None:
            for mode, effects in self.valid_modes_and_effects:
                res += self._one_mode_effects(mode, effects)

        return res

    @property
    def art(self) -> str:
        res = [f'{self.skill_head_type.value}: .id "{self.id}"']

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
                if isinstance(v, Animation):
                    res.append(f'.{k} "{v.id}"')
                elif isinstance(v, InnerFx):
                    res.append(f'.{k} "{v.value}"')
                else:
                    res.append(f'.{k} "{v}"')

        none_tuple_float = {
            "area_pos_offset": self.area_pos_offset,
            "target_area_pos_offset": self.target_area_pos_offset,
        }
        for k, v in none_tuple_float.items():
            if v is not None:
                res.append(f'.{k} {v[0]} {v[1]}')

        if self.custom_idle_anim_name is not None:
            custom_idle_anim_name = self.custom_idle_anim_name.id \
                if isinstance(self.custom_idle_anim_name, Animation) else self.custom_idle_anim_name
            res.append(f'.custom_idle_anim_name "{custom_idle_anim_name}"')
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

        return " ".join(res) + "\n"

    def __str__(self):
        if self.level == Level.ZERO:
            return self.info + self.art
        else:
            return self.info
