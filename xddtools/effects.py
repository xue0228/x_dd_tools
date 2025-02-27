import hashlib
import os.path
from enum import Enum
from typing import Optional, Union, Tuple, Iterable, List, Any

from PIL import Image, ImageDraw, ImageFont

from xddtools.animation import Animation
from xddtools.base import BaseID
from xddtools.buff_rules import BRSkill
from xddtools.buffs import Buff
from xddtools.enums import EffectTarget, HeroClass, CurioResultType, MonsterClass, BuffSource, HealSource, \
    BuffStatType, MonsterType, QuirkType, DamageType, DamageSource, TrinketID, \
    ItemType, BuffType, BuffDurationType, KeyStatus
from xddtools.path import DATA_PATH
from xddtools.target import Target
from xddtools.utils import float_to_percent_int, float_to_percent_str, \
    bool_to_lower_str, copy_dir


class Effect(BaseID):
    def __init__(
            self,
            effect_name: str,

            target: EffectTarget,
            spawn_target_actor_base_class_id: Optional[Union[MonsterClass, HeroClass, str]] = None,
            curio_result_type: Optional[CurioResultType] = None,

            shuffle_target: bool = False,
            shuffle_party: bool = False,
            instant_shuffle: bool = False,

            chance: float = 1.0,

            item: bool = False,
            curio: bool = False,
            cure: bool = False,
            cure_bleed: bool = False,
            cure_poison: bool = False,
            clear_dot_stress: bool = False,
            tag: bool = False,
            untag: bool = False,
            unstun: bool = False,
            guard: Optional[bool] = None,
            clear_guarding: bool = False,
            clear_guarded: bool = False,
            dot_shuffle: bool = False,
            kill: bool = False,
            immobilize: bool = False,
            unimmobilize: bool = False,
            uncontrol: bool = False,
            capture: bool = False,
            capture_remove_from_party: bool = False,
            remove_vampire: bool = False,
            cure_disease: bool = False,
            stealth: bool = False,
            unstealth: bool = False,
            clear_debuff: bool = False,
            clear_virtue: bool = False,
            daze: bool = False,
            undaze: bool = False,
            riposte: Optional[bool] = None,
            clear_riposte: bool = False,
            performer_rank_target: bool = False,

            riposte_on_hit_chance_add: Optional[float] = None,
            riposte_on_miss_chance_add: Optional[float] = None,
            riposte_on_hit_chance_multiply: Optional[float] = None,
            riposte_on_miss_chance_multiply: Optional[float] = None,
            riposte_effect: Union[Any, str, None] = None,

            riposte_validate: bool = True,
            can_crit_heal: bool = True,
            can_apply_on_death: bool = True,
            has_description: bool = True,
            buff_is_clear_debuff_valid: bool = True,

            swap_source_and_target: bool = False,
            crit_doesnt_apply_to_roll: bool = False,
            apply_once: bool = False,
            apply_with_result: bool = False,
            skill_instant: bool = False,
            refreshes_skill_uses: bool = False,
            individual_target_actor_rolls: bool = False,
            skips_endless_wave_curio: bool = False,

            dot_source: Optional[BuffSource] = None,
            dot_bleed: Optional[int] = None,
            dot_poison: Optional[int] = None,
            dot_stress: Optional[int] = None,
            dot_hp_heal: Optional[int] = None,
            heal_stress: Optional[int] = None,
            stress: Optional[int] = None,
            heal: Optional[int] = None,
            stun: Optional[int] = None,
            torch_decrease: Optional[int] = None,
            torch_increase: Optional[int] = None,
            push: Optional[int] = None,
            pull: Optional[int] = None,
            control: Optional[int] = None,
            health_damage: Optional[int] = None,
            health_damage_blocks: Optional[int] = None,

            virtue_blockable_chance: Optional[float] = None,
            affliction_blockable_chance: Optional[float] = None,

            heal_percent: Optional[float] = None,
            source_heal_type: Optional[HealSource] = None,
            steal_buff_stat_type: Optional[BuffStatType] = None,
            steal_buff_source_type: Optional[BuffSource] = None,
            kill_enemy_types: Union[MonsterType, str, None] = None,
            disease: Union[QuirkType, BaseID, str, None] = None,
            set_mode: Optional[str] = None,
            actor_dot: Optional[str] = None,
            bark: Optional[str] = None,
            damage_type: Optional[DamageType] = None,
            damage_source_type: Optional[DamageSource] = None,
            damage_source_data: Union[TrinketID, str, None] = None,
            use_item_id: Optional[str] = None,
            use_item_type: Optional[ItemType] = None,
            rank_target: Optional[Target] = None,
            clear_rank_target: Optional[Target] = None,

            summon_monsters: Optional[Tuple[str]] = None,
            summon_chances: Optional[Tuple[float]] = None,
            summon_ranks: Optional[Tuple[Target]] = None,
            summon_limits: Optional[Tuple[int]] = None,
            summon_count: Optional[int] = None,
            summon_erase_data_on_roll: Optional[bool] = None,
            summon_can_spawn_loot: Optional[bool] = None,
            summon_rank_is_previous_monster_class: Optional[bool] = None,
            summon_does_roll_initiatives: Optional[bool] = None,

            set_monster_class_id: Optional[str] = None,
            set_monster_class_ids: Optional[Tuple[str]] = None,
            set_monster_class_chances: Optional[Tuple[float]] = None,
            set_monster_class_reset_hp: Optional[bool] = None,
            set_monster_class_reset_buffs: Optional[bool] = None,
            set_monster_class_carry_over_hp_min_percent: Optional[float] = None,
            set_monster_class_clear_initiative: Optional[bool] = None,
            set_monster_class_clear_monster_brain_cooldowns: Optional[bool] = None,
            set_monster_class_reset_scale: Optional[bool] = None,

            buff_type: Optional[BuffType] = None,
            buff_sub_type: Union[Enum, str, None] = None,
            buff_amount: Union[float, int, None] = None,
            buff_duration_type: Optional[BuffDurationType] = None,
            key_status: Optional[KeyStatus] = None,
            monster_type: Union[MonsterType, str, None] = None,

            buff_source_type: Optional[BuffSource] = None,
            buff_ids: Optional[Iterable[Union[Buff, str]]] = None,

            combat_stat_buff: bool = False,
            damage_low_multiply: Optional[float] = None,
            damage_high_multiply: Optional[float] = None,
            max_hp_multiply: Optional[float] = None,
            attack_rating_add: Optional[float] = None,
            crit_chance_add: Optional[float] = None,
            defense_rating_add: Optional[float] = None,
            protection_rating_add: Optional[float] = None,

            damage_low_add: Optional[int] = None,
            damage_high_add: Optional[int] = None,
            max_hp_add: Optional[int] = None,

            speed_rating_add: Optional[int] = None,
            initiative_change: Optional[int] = None,
            duration: Optional[int] = None,

            on_hit: bool = True,
            on_miss: bool = False,
            queue: bool = True
    ):
        """
        初始化，此注释由 AI 生成，可能存在部分错误
        :param target: 目标类型，定义了effect的施法目标，如自身、单体目标、群体目标等
        :param spawn_target_actor_base_class_id: 在怪物的spawn行内的effect中生效，指定此effect的目标（仅限于spawn行）
        :param curio_result_type: 奇物互动结果使用正面/负面/中性动画，仅在与奇物互动时有意义
        :param shuffle_target: 是否对目标进行乱位
        :param shuffle_party: 是否对全体进行乱位
        :param instant_shuffle: 是否对目标进行即时乱位
        :param chance: effect的生效概率，1表示100%生效
        :param item: 是否作为物品使用效果
        :param curio: 是否作为奇物互动效果
        :param cure: 是否清除流血和腐蚀
        :param cure_bleed: 是否清除流血
        :param cure_poison: 是否清除腐蚀
        :param clear_dot_stress: 是否移除惊恐
        :param tag: 是否标记目标
        :param untag: 是否移除标记
        :param unstun: 是否移除眩晕
        :param guard: 是否守护目标（需指定守护类型，如正向守护或反向守护）
        :param clear_guarding: 是否清除守护（提供守护的一方）
        :param clear_guarded: 是否清除被守护状态（被守护的一方）
        :param dot_shuffle: 是否对目标施加持续乱位
        :param kill: 是否杀死目标
        :param immobilize: 是否禁锢目标（位移无效）
        :param unimmobilize: 是否解除禁锢
        :param uncontrol: 是否解除心控
        :param capture: 是否捕捉目标
        :param capture_remove_from_party: 是否将被捕捉目标从队伍中移除
        :param remove_vampire: 是否移除猩红诅咒
        :param cure_disease: 是否移除任何疾病
        :param stealth: 是否潜行
        :param unstealth: 是否显踪
        :param clear_debuff: 是否清除有is_clear_debuff_valid true属性的buff
        :param clear_virtue: 是否清除美德
        :param daze: 是否晕眩（马戏团DLC中的迷乱状态）
        :param undaze: 是否解除晕眩
        :param riposte: 是否开启反击
        :param clear_riposte: 是否清除反击
        :param performer_rank_target: 是否在先知的rank_target技能中使用（落石）
        :param riposte_on_hit_chance_add: 自身被打时触发反击的概率（数值）
        :param riposte_on_miss_chance_add: 自身闪避时触发反击的概率（数值）
        :param riposte_on_hit_chance_multiply: 自身被打时触发反击的倍率（百分比）
        :param riposte_on_miss_chance_multiply: 自身闪避时触发反击的倍率（百分比）
        :param riposte_effect: 反击附带的效果（经过测试这里只能写一个effect，多个effect只有第一个生效）
        :param riposte_validate: 是否可被反击（该effect无视反击代码已被弃用，请使用skill的无视反击代码）
        :param can_crit_heal: 治疗是否可以暴击，单疗暴击为12%，群疗暴击为5%
        :param can_apply_on_death: 是否允许在目标死亡时应用此effect（默认为True）
        :param has_description: 是否允许effect显示描述（默认为True）
        :param buff_is_clear_debuff_valid: buff清除debuff是否有效
        :param swap_source_and_target: 是否交换施法者和目标
        :param crit_doesnt_apply_to_roll: 暴击是否不适用于此effect的概率计算
        :param apply_once: 是否只生效一次
        :param apply_with_result: 是否在同queue中将时序往前挪动一个层次
        :param skill_instant: 是否为技能即时效果（无视chance，点按技能按钮立即执行）
        :param refreshes_skill_uses: 是否刷新限制技能的使用次数
        :param individual_target_actor_rolls: 是否单独针对每个目标得出effect执行结果
        :param skips_endless_wave_curio: 奇物是否跳过无尽本中的波次
        :param dot_source: 给effect中施加的dot设置buff源类型
        :param dot_bleed: 流血伤害
        :param dot_poison: 腐蚀伤害
        :param dot_stress: 持续压力
        :param dot_hp_heal: 愈合
        :param heal_stress: 压力治疗
        :param stress: 压力伤害
        :param heal: 治疗量
        :param stun: 眩晕回合数
        :param torch_decrease: 火把亮度减少
        :param torch_increase: 火把亮度增加
        :param push: 击退格数
        :param pull: 拉前格数
        :param control: 心控回合数
        :param health_damage: 真实伤害
        :param health_damage_blocks: 护体格挡
        :param virtue_blockable_chance: 目标美德时，该effects被阻挡而不生效的概率
        :param affliction_blockable_chance: 目标折磨时，该effects被阻挡而不生效的概率
        :param heal_percent: 治疗最大生命值百分比
        :param source_heal_type: 治疗源类型
        :param steal_buff_stat_type: 偷取特定类型的buff至effect发起者
        :param steal_buff_source_type: 偷取特定源类型的buff和dot至effect发起者
        :param kill_enemy_types: 移除指定类型的怪物（如清除尸体或秒杀特定种族怪物）
        :param disease: 赋予疾病或怪癖
        :param set_mode: 进入模式（如变身）
        :param actor_dot: 对目标赋予ActorDot
        :param bark: 喊话
        :param damage_type: 伤害类型
        :param damage_source_type: 伤害源类型
        :param damage_source_data: 伤害源数据（怪物小类id或饰品id）
        :param use_item_id: 调用虚拟道具id的同名effect
        :param use_item_type: 调用虚拟道具的种类
        :param rank_target: 目标站位，接受‘@’和‘~’，不接受‘？’
        :param clear_rank_target: 清除目标站位
        :param summon_monsters: 召唤怪物的小类id列表
        :param summon_chances: 召唤怪物的概率列表
        :param summon_ranks: 召唤怪物的站位列表
        :param summon_limits: 召唤怪物的上限列表
        :param summon_count: 召唤怪物的数量
        :param summon_erase_data_on_roll: 是否在召唤时清除数据
        :param summon_can_spawn_loot: 召唤物是否可以掉落战利品
        :param summon_rank_is_previous_monster_class: 召唤物的召唤位置是否为召唤者的位置
        :param summon_does_roll_initiatives: 召唤物是否立即获得剩余行动回合
        :param set_monster_class_id: 变身为指定怪物的小类id
        :param set_monster_class_ids: 变身候选的怪物小类id列表
        :param set_monster_class_chances: 变身候选的概率列表
        :param set_monster_class_reset_hp: 变身后是否重置怪物生命
        :param set_monster_class_reset_buffs: 变身后是否重置怪物buff
        :param set_monster_class_carry_over_hp_min_percent: 变身后延续当前血量的最小百分比
        :param set_monster_class_clear_initiative: 变身后是否重置行动点
        :param set_monster_class_clear_monster_brain_cooldowns: 变身后是否重置怪物AI冷却
        :param set_monster_class_reset_scale: 变身后是否重置怪物比例
        :param buff_type: 增减益类型
        :param buff_sub_type: 增减益子类型
        :param buff_amount: 增减益数值
        :param buff_duration_type: 增减益持续类型
        :param key_status: 目标状态（如标记、流血、腐蚀等）
        :param monster_type: 目标怪物类型
        :param buff_source_type: 增减益源类型
        :param buff_ids: 施加的buff列表
        :param combat_stat_buff: 是否为使用时才触发的buff
        :param damage_low_multiply: 最低伤害增加百分比
        :param damage_high_multiply: 最高伤害增加百分比
        :param max_hp_multiply: 最大生命值增加百分比
        :param attack_rating_add: 命中增加数值
        :param crit_chance_add: 暴击增加数值
        :param defense_rating_add: 闪避增加数值
        :param protection_rating_add: 防御增加数值
        :param damage_low_add: 最低伤害增加固定值
        :param damage_high_add: 最高伤害增加固定值
        :param max_hp_add: 最大生命值增加固定值
        :param speed_rating_add: 速度增加固定值
        :param initiative_change: 行动点数变化
        :param duration: buff持续回合数
        :param on_hit: 技能命中时此effect是否生效
        :param on_miss: 技能未命中时此effect是否生效
        :param queue: effect的执行顺序（queue false的effect先于queue true的effect执行）
        :param effect_name: effect的名称
        :return
        """
        self.target = target
        self.chance = chance
        self.set_mode = set_mode
        self.skill_instant = skill_instant
        self.swap_source_and_target = swap_source_and_target
        self.curio_result_type = curio_result_type
        self.item = item
        self.curio = curio
        self.shuffle_target = shuffle_target
        self.shuffle_party = shuffle_party
        self.instant_shuffle = instant_shuffle
        self.heal = heal
        self.heal_percent = heal_percent
        self.can_crit_heal = can_crit_heal
        self.source_heal_type = source_heal_type
        self.dot_bleed = dot_bleed
        self.dot_poison = dot_poison
        self.dot_stress = dot_stress
        self.dot_hp_heal = dot_hp_heal
        self.heal_stress = heal_stress
        self.stress = stress
        self.actor_dot = actor_dot
        self.dot_source = dot_source
        self.cure = cure
        self.cure_bleed = cure_bleed
        self.cure_poison = cure_poison
        self.clear_dot_stress = clear_dot_stress
        self.tag = tag
        self.untag = untag
        self.daze = daze
        self.undaze = undaze
        self.unstun = unstun
        self.clear_riposte = clear_riposte
        self.dot_shuffle = dot_shuffle
        self.uncontrol = uncontrol
        self.kill = kill
        self.immobilize = immobilize
        self.unimmobilize = unimmobilize
        self.remove_vampire = remove_vampire
        self.cure_disease = cure_disease
        self.refreshes_skill_uses = refreshes_skill_uses
        self.stealth = stealth
        self.unstealth = unstealth
        self.clear_virtue = clear_virtue
        self.capture = capture
        self.capture_remove_from_party = capture_remove_from_party
        self.clear_debuff = clear_debuff
        self.buff_is_clear_debuff_valid = buff_is_clear_debuff_valid
        self.stun = stun
        self.pull = pull
        self.push = push
        self.control = control
        self.health_damage = health_damage
        self.health_damage_blocks = health_damage_blocks
        self.initiative_change = initiative_change
        self.disease = disease
        self.kill_enemy_types = kill_enemy_types
        self.monster_type = monster_type
        self.bark = bark
        self.guard = guard
        self.clear_guarding = clear_guarding
        self.clear_guarded = clear_guarded
        self.torch_decrease = torch_decrease
        self.torch_increase = torch_increase
        self.use_item_id = use_item_id
        self.use_item_type = use_item_type
        self.skips_endless_wave_curio = skips_endless_wave_curio
        self.riposte = riposte
        self.riposte_on_miss_chance_add = riposte_on_miss_chance_add
        self.riposte_on_hit_chance_add = riposte_on_hit_chance_add
        self.riposte_on_miss_chance_multiply = riposte_on_miss_chance_multiply
        self.riposte_on_hit_chance_multiply = riposte_on_hit_chance_multiply
        self.riposte_effect = riposte_effect
        self.duration = duration
        self.steal_buff_stat_type = steal_buff_stat_type
        self.steal_buff_source_type = steal_buff_source_type
        self.combat_stat_buff = combat_stat_buff
        self.damage_low_multiply = damage_low_multiply
        self.damage_high_multiply = damage_high_multiply
        self.max_hp_multiply = max_hp_multiply
        self.damage_low_add = damage_low_add
        self.damage_high_add = damage_high_add
        self.max_hp_add = max_hp_add
        self.attack_rating_add = attack_rating_add
        self.crit_chance_add = crit_chance_add
        self.defense_rating_add = defense_rating_add
        self.protection_rating_add = protection_rating_add
        self.speed_rating_add = speed_rating_add
        self.buff_type = buff_type
        self.buff_sub_type = buff_sub_type
        self.buff_amount = buff_amount
        self.buff_duration_type = buff_duration_type
        self.key_status = key_status
        self.buff_ids = buff_ids
        self.buff_source_type = buff_source_type
        self.damage_type = damage_type
        self.damage_source_data = damage_source_data
        self.damage_source_type = damage_source_type
        self.individual_target_actor_rolls = individual_target_actor_rolls
        self.apply_once = apply_once
        self.on_hit = on_hit
        self.on_miss = on_miss
        self.crit_doesnt_apply_to_roll = crit_doesnt_apply_to_roll
        self.can_apply_on_death = can_apply_on_death
        self.queue = queue
        self.apply_with_result = apply_with_result
        self.virtue_blockable_chance = virtue_blockable_chance
        self.affliction_blockable_chance = affliction_blockable_chance
        self.has_description = has_description
        self.riposte_validate = riposte_validate
        self.summon_monsters = summon_monsters
        self.summon_chances = summon_chances
        self.summon_ranks = summon_ranks
        self.summon_limits = summon_limits
        self.summon_count = summon_count
        self.summon_erase_data_on_roll = summon_erase_data_on_roll
        self.summon_can_spawn_loot = summon_can_spawn_loot
        self.summon_rank_is_previous_monster_class = summon_rank_is_previous_monster_class
        self.summon_does_roll_initiatives = summon_does_roll_initiatives
        self.rank_target = rank_target
        self.clear_rank_target = clear_rank_target
        self.performer_rank_target = performer_rank_target
        self.set_monster_class_id = set_monster_class_id
        self.set_monster_class_ids = set_monster_class_ids
        self.set_monster_class_chances = set_monster_class_chances
        self.set_monster_class_reset_hp = set_monster_class_reset_hp
        self.set_monster_class_reset_buffs = set_monster_class_reset_buffs
        self.set_monster_class_carry_over_hp_min_percent = set_monster_class_carry_over_hp_min_percent
        self.set_monster_class_clear_initiative = set_monster_class_clear_initiative
        self.set_monster_class_clear_monster_brain_cooldowns = set_monster_class_clear_monster_brain_cooldowns
        self.set_monster_class_reset_scale = set_monster_class_reset_scale
        self.spawn_target_actor_base_class_id = spawn_target_actor_base_class_id
        super().__init__(name=effect_name)

    def _one_line(self, buff_ids: Union[List[Buff], List[str]]):
        res = f'effect: .name "{self.id}"'
        if self.spawn_target_actor_base_class_id is not None:
            res += f' .spawn_target_actor_base_class_id {self.spawn_target_actor_base_class_id}'
        res += f' .target "{self.target.value}"'
        if self.curio_result_type is not None:
            res += f' .curio_result_type "{self.curio_result_type.value}"'
        none = {
            "shuffletarget": self.shuffle_target,
            "shuffleparty": self.shuffle_party,
            "instant_shuffle": self.instant_shuffle,
        }
        for k, v in none.items():
            if v:
                res += f" .{k}"
        res += f" .chance {float_to_percent_int(self.chance)}%"

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
                res += f' .{k} 1'

        riposte_percent = {
            "riposte_on_hit_chance_add": self.riposte_on_hit_chance_add,
            "riposte_on_miss_chance_add": self.riposte_on_miss_chance_add,
            "riposte_on_hit_chance_multiply": self.riposte_on_hit_chance_add,
            "riposte_on_miss_chance_multiply": self.riposte_on_miss_chance_add,
        }
        for k, v in riposte_percent.items():
            if v is not None:
                res += f' .{k} {float_to_percent_int(v)}%'
        if self.riposte_effect is not None:
            riposte_effect = self.riposte_effect.id \
                if isinstance(self.riposte_effect, Effect) else self.riposte_effect
            res += f' .riposte_effect "{riposte_effect}"'

        true_false_display_false = {
            "riposte_validate": self.riposte_validate,
            "can_crit_heal": self.can_crit_heal,
            "can_apply_on_death": self.can_apply_on_death,
            "has_description": self.has_description,
            "buff_is_clear_debuff_valid": self.buff_is_clear_debuff_valid
        }
        for k, v in true_false_display_false.items():
            if not v:
                res += f' .{k} false'

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
                res += f' .{k} true'

        if self.dot_source is not None:
            res += f' .dotSource {self.dot_source.value}'
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
            if v <= 0:
                raise ValueError(f"{k} must be larger than 0")
            res += f' .{k} {v}'

        float_percent = {
            "virtue_blockable_chance": self.virtue_blockable_chance,
            "affliction_blockable_chance": self.affliction_blockable_chance
        }
        for k, v in float_percent.items():
            if v is not None:
                res += f' .{k} {float_to_percent_str(v)}%'

        if self.heal_percent is not None:
            res += f' .heal_percent {self.heal_percent}'
        if self.source_heal_type is not None:
            res += f' .source_heal_type {self.source_heal_type.value}'
        if self.steal_buff_stat_type is not None:
            res += f' .steal_buff_stat_type {self.steal_buff_stat_type.value}'
        if self.steal_buff_source_type is not None:
            res += f' .steal_buff_source_type {self.steal_buff_source_type.value}'
        if self.kill_enemy_types is not None:
            kill_enemy_types = self.kill_enemy_types.value \
                if isinstance(self.kill_enemy_types, MonsterType) else self.kill_enemy_types
            res += f' .kill_enemy_types {kill_enemy_types}'
        if self.disease is not None:
            if isinstance(self.disease, QuirkType):
                disease = self.disease.value
            elif isinstance(self.disease, BaseID):
                disease = self.disease.id
            else:
                disease = self.disease
            res += f' .disease {disease}'
        if self.set_mode is not None:
            res += f' .set_mode {self.set_mode}'
        if self.actor_dot is not None:
            res += f' .actor_dot {self.actor_dot}'
        if self.bark is not None:
            res += f' .bark {self.bark}'
        if self.damage_type is not None:
            res += f' .damage_type {self.damage_type.value}'
        if self.damage_source_type is not None:
            res += f' .damage_source_type {self.damage_source_type.value}'
        if self.damage_source_data is not None:
            damage_source_data = self.damage_source_data.value \
                if isinstance(self.damage_source_data, TrinketID) else self.damage_source_data
            res += f' .damage_source_data {damage_source_data}'
        if self.use_item_id is not None:
            res += f' .use_item_id {self.use_item_id}'
            if self.use_item_type is not None:
                res += f' use_item_type {self.use_item_type.value}'
        if self.rank_target is not None:
            res += f' .rank_target {self.rank_target}'
        if self.clear_rank_target is not None:
            res += f' .clear_rank_target {self.clear_rank_target}'

        if self.summon_monsters is not None and len(self.summon_monsters) > 0:
            res += " .summon_monsters"
            for item in self.summon_monsters:
                res += f' {item}'
        if self.summon_chances is not None and len(self.summon_chances) > 0:
            res += " .summon_chances"
            for item in self.summon_chances:
                res += f' {item}'
        if self.summon_ranks is not None and len(self.summon_ranks) > 0:
            res += " .summon_ranks"
            for item in self.summon_ranks:
                res += f' {item}'
        if self.summon_limits is not None and len(self.summon_limits) > 0:
            res += " .summon_limits"
            for item in self.summon_limits:
                res += f' {item}'
        if self.summon_count is not None:
            if self.summon_count <= 0:
                raise ValueError("summon_count must be larger than 0")
            res += f' .summon_count {self.summon_count}'
        if self.summon_erase_data_on_roll is not None:
            res += f' .summon_erase_data_on_roll {1 if self.summon_erase_data_on_roll else 0}'
        if self.summon_can_spawn_loot is not None:
            res += f' .summon_can_spawn_loot {1 if self.summon_can_spawn_loot else 0}'
        if self.summon_rank_is_previous_monster_class is not None:
            res += f' .summon_rank_is_previous_monster_class {1 if self.summon_rank_is_previous_monster_class else 0}'
        if self.summon_does_roll_initiatives is not None:
            res += f' .summon_does_roll_initiatives {1 if self.summon_does_roll_initiatives else 0}'

        if self.set_monster_class_id is not None and self.set_monster_class_ids is not None:
            raise ValueError("set_monster_class_id and set_monster_class_ids cannot be set at the same time")
        if self.set_monster_class_id is not None or self.set_monster_class_ids is not None:
            if self.set_monster_class_id is not None:
                res += f' .set_monster_class_id {self.set_monster_class_id}'
            if self.set_monster_class_ids is not None and len(self.set_monster_class_ids) > 0:
                res += f' .set_monster_class_ids'
                for item in self.set_monster_class_ids:
                    res += f' {item}'
            if self.set_monster_class_chances is not None and len(self.set_monster_class_chances) > 0:
                res += f' .set_monster_class_chances'
                for item in self.set_monster_class_chances:
                    res += f' {item}'
            if self.set_monster_class_reset_hp is not None:
                res += f' .set_monster_class_reset_hp {1 if self.set_monster_class_reset_hp else 0}'
            if self.set_monster_class_reset_buffs is not None:
                res += f' .set_monster_class_reset_buffs {bool_to_lower_str(self.set_monster_class_reset_buffs)}'
            if self.set_monster_class_carry_over_hp_min_percent is not None:
                res += f' .set_monster_class_carry_over_hp_min_percent ' \
                       f'{self.set_monster_class_carry_over_hp_min_percent}'
            if self.set_monster_class_clear_initiative is not None:
                res += f' .set_monster_class_clear_initiative ' \
                       f'{bool_to_lower_str(self.set_monster_class_clear_initiative)}'
            if self.set_monster_class_clear_monster_brain_cooldowns is not None:
                res += f' .set_monster_class_clear_monster_brain_cooldowns ' \
                       f'{bool_to_lower_str(self.set_monster_class_clear_monster_brain_cooldowns)}'
            if self.set_monster_class_reset_scale is not None:
                res += f' .set_monster_class_reset_scale {bool_to_lower_str(self.set_monster_class_reset_scale)}'

        if self.buff_type is not None:
            res += f' .buff_type {self.buff_type.value}'
            if self.buff_sub_type is not None:
                res += f' .buff_sub_type ' \
                       f'{self.buff_sub_type.value if isinstance(self.buff_sub_type, Enum) else self.buff_sub_type}'
            if self.buff_amount is not None:
                res += f' .buff_amount {self.buff_amount}'
            if self.buff_duration_type is not None:
                res += f' .buff_duration_type {self.buff_duration_type.value}'
            if self.key_status is not None:
                res += f' .keyStatus {self.key_status.value}'
            if self.monster_type is not None:
                res += f' .monsterType ' \
                       f'{self.monster_type.value if isinstance(self.monster_type, MonsterType) else self.monster_type}'

        if self.buff_source_type is not None:
            res += f' .buff_source_type {self.buff_source_type.value}'

        if len(buff_ids) > 0:
            res += f" .buff_ids"
            for buff in buff_ids:
                if isinstance(buff, Buff):
                    buff_id = buff.id
                else:
                    buff_id = buff
                res += f' "{buff_id}"'

        if self.combat_stat_buff:
            res += f' .combat_stat_buff 1'
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
                res += f' .{k} {float_to_percent_str(v)}%'
        float_direct = {
            "damage_low_add": self.damage_low_add,
            "damage_high_add": self.damage_high_add,
            "max_hp_add": self.max_hp_add
        }
        for k, v in float_direct.items():
            if v is not None:
                res += f' .{k} {v}'

        int_value = {
            "speed_rating_add": self.speed_rating_add,
            "initiative_change": self.initiative_change,
            "duration": self.duration
        }
        for k, v in int_value.items():
            if v is not None:
                res += f' .{k} {v}'

        true_false_display_all = {
            "on_hit": self.on_hit,
            "on_miss": self.on_miss,
            "queue": self.queue
        }
        for k, v in true_false_display_all.items():
            res += f' .{k} {bool_to_lower_str(v)}'

        return res + "\n"

    def __str__(self):
        if self.buff_ids is None:
            return self._one_line([])
        i = 0
        buff_ids = []
        res = ""
        for buff in self.buff_ids:
            buff_ids.append(buff)
            if (i + 1) % 8 == 0:
                res += self._one_line(buff_ids)
                buff_ids = []
            i += 1
        if len(buff_ids) > 0:
            res += self._one_line(buff_ids)
        return res


class SkillBarkEffect(Effect):
    def __init__(
            self,
            effect_name: str,
            buff_name: str,
            skill_name: str,
            bark_text: str,
            fx_dir: Optional[str] = None,
            font_path: Optional[str] = None,
            font_size: int = 60,
            text_color: Optional[Tuple[int, int, int]] = None,
            y_offset: int = -5,
    ):
        self._bark_text = bark_text
        if fx_dir is None:
            fx_dir = f"./.temp/{hashlib.md5(bark_text.encode()).hexdigest()}"

        template_path = os.path.join(DATA_PATH, "template/fx/skill_bark")
        copy_dir(template_path, fx_dir)

        self._anim = Animation(
            anim_name=skill_name,
            anim_dir=fx_dir
        )
        self._draw_text(
            self._anim.png_path,
            font_path,
            font_size,
            text_color,
            y_offset
        )

        super().__init__(
            effect_name=effect_name,
            target=EffectTarget.PERFORMER,
            chance=1.01,
            skill_instant=True,
            buff_source_type=BuffSource.NOTSPECIFIED,
            buff_duration_type=BuffDurationType.BEFORE_TURN,
            duration=1,
            on_hit=True,
            on_miss=True,
            queue=False,
            has_description=False,
            apply_once=True,
            buff_ids=(Buff(
                buff_name=buff_name,
                stat_type=BuffType.UPGRADE_DISCOUNT,
                stat_sub_type=skill_name,
                remove_on_battle_complete=True,
                is_clear_debuff_valid=False,
                fx=self._anim,
                buff_rule=BRSkill(skill_name)
            ),)
        )

    def _draw_text(
            self,
            image_path: str,
            font_path: Optional[str] = None,
            font_size: int = 60,
            text_color: Optional[Tuple[int, int, int]] = None,
            y_offset: int = -5,
    ):
        if font_path is None:
            font_path = os.path.join(DATA_PATH, "template/font/TianZhenWuXieShouJinTi-2.ttf")
        if text_color is None:
            text_color = (154, 0, 0)

        image = Image.open(image_path)
        width, height = image.size
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)

        bbox = draw.textbbox((0, 0), self._bark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - 30 - text_width) / 2
        y = (height - text_height) / 2 + y_offset

        draw.text((x, y), self._bark_text, fill=text_color, font=font)
        image.save(image_path)


if __name__ == '__main__':
    eft = SkillBarkEffect(bark_text="树干猛击")
    eft.add_skill_id("xue_yi_wei")
    print(eft)
    print(eft.buff_ids[0])
