from enum import Enum


class BuffType(Enum):
    HP_HEAL_AMOUNT = "hp_heal_amount"  # 治疗施加量的固定值改变
    HP_HEAL_PERCENT = "hp_heal_percent"  # 治疗施加量的百分比改变
    HP_HEAL_RECEIVED_PERCENT = "hp_heal_received_percent"  # 受到的治疗施加量的百分比改变
    COMBAT_STAT_MULTIPLY = "combat_stat_multiply"  # 战斗状态百分比改变
    COMBAT_STAT_ADD = "combat_stat_add"  # 战斗状态固定值改变
    RESISTANCE = "resistance"  # 抗性
    POISON_CHANCE = "poison_chance"  # 腐蚀施加率
    BLEED_CHANCE = "bleed_chance"  # 流血施加率
    STRESS_DMG_PERCENT = "stress_dmg_percent"  # 造成压力伤害（百分比）
    STRESS_DMG_RECEIVED_PERCENT = "stress_dmg_received_percent"  # 受到的压力伤害（百分比），
    # 如dd火炬：启示：-100%所受压力（实际上最低受压只能降低到-80%）
    STRESS_HEAL_PERCENT = "stress_heal_percent"  # 造成压力治疗效果（百分比）
    STRESS_HEAL_RECEIVED_PERCENT = "stress_heal_received_percent"  # 受到的压力治疗效果（百分比）
    PARTY_SURPRISE_CHANCE = "party_surprise_chance"  # 队伍惊慌概率（百分比）
    MONSTERS_SURPRISE_CHANCE = "monsters_surprise_chance"  # 怪物惊慌概率（百分比）
    AMBUSH_CHANCE = "ambush_chance"  # 夜袭概率（百分比）
    SCOUTING_CHANCE = "scouting_chance"  # 侦查概率（百分比）
    STARVING_DAMAGE_PERCENT = "starving_damage_percent"  # 挨饿时受到的伤害（百分比）
    UPGRADE_DISCOUNT = "upgrade_discount"  # 被称为【打折】类buff，因为其作用是在进行装备和技能升级时打折
    DAMAGE_RECEIVED_PERCENT = "damage_received_percent"  # 受到的伤害（百分比），俗称“硬减伤”（相对于防御的减伤而言），
    # 如dd火炬：启示：-100%所受伤害（这个可以达到-100%的效果）
    DEBUFF_CHANCE = "debuff_chance"  # 减益施加率（百分比）
    RESOLVE_CHECK_PERCENT = "resolve_check_percent"  # 美德概率（百分比）
    STUN_CHANCE = "stun_chance"  # 眩晕施加率（百分比）
    MOVE_CHANCE = "move_chance"  # 位移施加率（百分比）
    REMOVE_NEGATIVE_QUIRK_CHANCE = "remove_negative_quirk_chance"  # 移除红癖的概率（百分比）
    FOOD_CONSUMPTION_PERCENT = "food_consumption_percent"  # 食物消耗（百分比），如+100%食物消耗，-100%食物消耗
    RESOLVE_XP_BONUS_PERCENT = "resolve_xp_bonus_percent"  # 砺练值（百分比）
    ACTIVITY_SIDE_EFFECT_CHANCE = "activity_side_effect_chance"  # 小镇活动效果施加率（百分比）
    VAMPIRE_EVOLUTION_DURATION = "vampire_evolution_duration"  # 猩红诅咒进化时间改变
    QUIRK_EVOLUTION_DEATH_IMMUNE = "quirk_evolution_death_immune"  # 免疫怪癖的进化到死亡的效果
    DISABLE_COMBAT_SKILL_ATTRIBUTE = "disable_combat_skill_attribute"  # 禁用技能属性
    GUARD_BLOCKED = "guard_blocked"  # 无法被守护（amount为1）
    TAG_BLOCKED = "tag_blocked"  # 无法被标记（amount为1）
    IGNORE_PROTECTION = "ignore_protection"  # 无视防御（百分比，如amount为0.4，则为40%穿甲）
    IGNORE_STEALTH = "ignore_stealth"  # 无视潜行（amount为1）
    CRIT_RECEIVED_CHANCE = "crit_received_chance"  # 受到暴击的概率（百分比）
    RIPOSTE = "riposte"  # 反击
    TAG = "tag"  # buff写法的标记效果（注意与effect写法的标记效果互相区分）
    GUARDED = "guarded"  # buff写法的守护效果（由于守护需要被守护者与守护者建立联系，故buff写法的守护其实没有实际守护效果）
    VAMPIRE = "vampire"  # buff写法的猩红诅咒效果？已弃用
    STEALTH = "stealth"  # buff写法的潜行效果
    HP_DOT_BLEED = "hp_dot_bleed"  # 此即buff写法的流血、腐蚀、愈合、恐惧、扰乱，注意与effect写法的相应效果互相区分。
    HP_DOT_POISON = "hp_dot_poison"  # 只有当remove_if_not_active设置为true时，规则才起作用，如果不满足规则条件，buff则会立即消失，
    HP_DOT_HEAL = "hp_dot_heal"  # 即不存在“既存在，又不生效的流血、腐蚀、愈合、恐惧、扰乱”。
    STRESS_DOT = "stress_dot"  #
    SHUFFLE_DOT = "shuffle_dot"  #
    TORCH_INCREASE_PERCENT = "torch_increase_percent"  # 火把提供亮度增加（百分比）
    TORCH_DECREASE_PERCENT = "torch_decrease_percent"  # 火把提供亮度减少（百分比） （警告：当火把亮度减少的倍率小于-100%时，减亮度会溢出，使亮度被加满）
    TORCHLIGHT_BURN_PERCENT = "torchlight_burn_percent"  # 自农场dlc更新后，0是该buff数值的基准点，任何站位都能触发，数值高于0：火把烧得更快，数值低于0：火把烧得更慢
    STRESS_ON_MISS = "stress_on_miss"  # 技能被闪避时自身加压
    STRESS_FROM_IDLE_IN_TOWN = "stress_from_idle_in_town"  # 城镇闲置时自身压力
    SHARD_REWARD_PERCENT = "shard_reward_percent"  # 星晶尘埃战利品的给予数量
    SHARD_CONSUME_PERCENT = "shard_consume_percent"  # 星晶尘埃战利品的被星晶雇佣兵拿取回扣的比例
    DAMAGE_REFLECT_PERCENT = "damage_reflect_percent"  # 伤害反弹（原版的老兵的水晶盾）
    HP_DOT_BLEED_DURATION_RECEIVED_PERCENT = "hp_dot_bleed_duration_received_percent"  # 流血所受时间改变（百分比）（仅对effect写法流血有效）
    HP_DOT_BLEED_DURATION_PERCENT = "hp_dot_bleed_duration_percent"  # 流血施加时间改变（百分比）（仅对effect写法流血有效）
    HP_DOT_BLEED_AMOUNT_RECEIVED_PERCENT = "hp_dot_bleed_amount_received_percent"  # 流血所受量改变（固定值）（仅对effect写法流血有效）
    HP_DOT_BLEED_AMOUNT_PERCENT = "hp_dot_bleed_amount_percent"  # 流血施加量改变（固定值）（仅对effect写法流血有效）
    HP_DOT_POISON_DURATION_RECEIVED_PERCENT = "hp_dot_poison_duration_received_percent"  # 腐蚀所受时间改变（百分比）（仅对effect写法腐蚀有效）
    HP_DOT_POISON_DURATION_PERCENT = "hp_dot_poison_duration_percent"  # 腐蚀施加时间改变（百分比）（仅对effect写法腐蚀有效）
    HP_DOT_POISON_AMOUNT_RECEIVED_PERCENT = "hp_dot_poison_amount_received_percent"  # 腐蚀所受量改变（固定值）（仅对effect写法腐蚀有效）
    HP_DOT_POISON_AMOUNT_PERCENT = "hp_dot_poison_amount_percent"  # 腐蚀施加量改变（固定值）（仅对effect写法腐蚀有效）
    STRESS_DOT_DURATION_RECEIVED_PERCENT = "stress_dot_duration_received_percent"  # 恐惧所受时间改变（百分比）（仅对effect写法恐惧有效）
    STRESS_DOT_DURATION_PERCENT = "stress_dot_duration_percent"  # 恐惧施加时间改变（百分比）（仅对effect写法恐惧有效）
    STRESS_DOT_AMOUNT_RECEIVED_PERCENT = "stress_dot_amount_received_percent"  # 恐惧所受量改变（固定值）（仅对effect写法恐惧有效）
    STRESS_DOT_AMOUNT_PERCENT = "stress_dot_amount_percent"  # 恐惧施加量改变（固定值）（仅对effect写法恐惧有效）
    HP_HEAL_DOT_DURATION_RECEIVED_PERCENT = "hp_heal_dot_duration_received_percent"  # 瘴合所受时间改变（百分比）（仅对effect写法瘴合有效）
    HP_HEAL_DOT_DURATION_PERCENT = "hp_heal_dot_duration_percent"  # 愈合施加时间改变（百分比）（仅对effect写法瘴合有效）
    HP_HEAL_DOT_AMOUNT_RECEIVED_PERCENT = "hp_heal_dot_amount_received_percent"  # 瘴合所受量改变（固定值）（仅对effect写法瘴合有效）
    HP_HEAL_DOT_AMOUNT_PERCENT = "hp_heal_dot_amount_percent"  # 愈合施加量改变（固定值）（仅对effect写法瘴合有效）
    SHUFFLE_DOT_DURATION_RECEIVED_PERCENT = "shuffle_dot_duration_received_percent"  # 扰乱所受时间改变（百分比）（仅对effect写法扰乱有效）
    SHUFFLE_DOT_DURATION_PERCENT = "shuffle_dot_duration_percent"  # 扰乱施加时间改变（百分比）（仅对effect写法扰乱有效）
    GUARD_DURATION_RECEIVED_PERCENT = "guard_duration_received_percent"  # 守护所受时间改变（百分比）
    # （仅对effect写法守护有效，不过buff写法守护本身也没有意义）
    GUARD_DURATION_PERCENT = "guard_duration_percent"  # 守护施加时间改变（百分比）（同上）
    CURE_BLEED_RECEIVED_CHANCE = "cure_bleed_received_chance"  # 治愈流血的所受成功率
    CURE_POISON_RECEIVED_CHANCE = "cure_poison_received_chance"  # 治愈腐蚀的所受成功率
    CURE_BLEED_CHANCE = "cure_bleed_chance"  # 治愈流血的施加成功率
    CURE_POISON_CHANCE = "cure_poison_chance"  # 治愈腐蚀的施加成功率
    RANDOM_TARGET_FRIENDLY_CHANCE = "random_target_friendly_chance"  # 友方技能的目标随机化概率
    RANDOM_TARGET_ATTACK_CHANCE = "random_target_attack_chance"  # 进攻技能的目标随机化概率
    TRANSFER_DEBUFF_FROM_ATTACKER_CHANCE = "transfer_debuff_from_attacker_chance"  # 被攻击时，自动触发“从攻击者身上转移减益到自身”这种效果的概率
    TRANSFER_BUFF_FROM_ATTACKER_CHANCE = "transfer_buff_from_attacker_chance"  # 被攻击时，自动触发“从攻击者身上转移增益到自身”这种效果的概率
    QUIRK_TAG_EVOLUTION_DURATION = "quirk_tag_evolution_duration"  # 怪癖进化时间的改变
    DEATHBLOW_CHANCE = "deathblow_chance"  # 致死几率，然而修正不了来自怪物的反伤的致死率，也无法干涉任意来源的dot伤害的致死率
    HEARTATTACK_STRESS_HEAL_PERCENT = "heartattack_stress_heal_percent"  # 心力衰竭时的压力治疗
    IGNORE_GUARD = "ignore_guard"  # 无视守护（amount=1）
    BUFF_DURATION_PERCENT = "buff_duration_percent"  # 不仅影响buff，还影响debuff，持续技能，标记，守护等，因此务必慎用，使用不当将导致永久buff等意外。
    RIPOSTE_DURATION_PERCENT = "riposte_duration_percent"  # 反击施加时间改变（百分比）（仅对effect写法反击有效）


class BuffDurationType(Enum):
    ROUND = "round"  # 小回合，每次行动后扣除1
    COMBAT_END = "combat_end"  # 每场战斗结束
    QUEST_END = "quest_end"  # 副本结束
    QUEST_COMPLETE = "quest_complete"  # 副本完成
    QUEST_NOT_COMPLETE = "quest_not_complete"  # 副本未完成
    ACTIVITY_END = "activity_end"  # 城镇活动结束
    IDLE_START_TOWN_VISIT = "idle_start_town_visit"  # 城镇闲置过周
    TILL_REMOVE = "till_remove"  # 直到移除
    NONE = "none"  # 无
    BEFORE_TURN = "before_turn"  # 个人回合开始之前，dot的默认持续方式
    AFTER_TURN = "after_turn"  # 个人回合结束之后，大部分情况下效果等同round
    AFTER_ROUND = "after_round"  # 整轮之后（俗称大回合），敌我双方所以目标行动均已结束


class HealSource(Enum):
    """
    effect: .source_heal_type
    buff: hp_heal_amount
    buff: hp_heal_percent
    buff: hp_heal_received_percent
    不同的治疗源类型除了用于迂回的差异外，也意味着不同的治疗暴击率，注意治疗暴击率永远是恒定的，不受任何外部改变
    """
    HERO_SKILL = "hero_skill"  # 单目标的英雄治疗技能
    HERO_SKILL_MULTI_TARGET = "hero_skill_multi_target"  # 多目标的英雄治疗技能
    MONSTER_SKILL = "monster_skill"  # 单目标的怪物治疗技能
    MONSTER_SKILL_MULTI_TARGET = "monster_skill_multi_target"  # 多目标的怪物治疗技能
    CAMP_SKILL = "camp_skill"  # 单目标的扎营治疗技能
    CAMP_SKILL_MULTI_TARGET = "camp_skill_multi_target"  # 多目标的扎营治疗技能
    COMPANION = "companion"  # 同伴（不是指英雄队伍，而是指溺水船长和溺水船员的特殊治疗机制）
    EAT = "eat"  # 吃食物治疗
    ACT_OUT = "act_out"  # 美德折磨怪癖的actout行为
    DAMAGE_HEAL = "damage_heal"  # 伤害回复（真吸血），配合skill下的.damage_heal_base_class_ids代码使用
    EFFECT = "effect"  # 效果
    FLASHBACK = "flashback"  # 闪回（破盾蛇梦）
    DOT = "dot"  # 愈合


class StressSource(Enum):
    """
    buff: stress_dmg_received_percent
    buff: stress_dmg_percent
    buff: stress_heal_percent
    buff: stress_heal_received_percent
    """
    HUNGER = "hunger"  # 饥饿
    DEATH_BLOW = "death_blow"  # 致死
    HERO_CRIT = "hero_crit"  # 英雄暴击减压
    HERO_KILLING_BLOW = "hero_killing_blow"  # 英雄击杀减压
    MODE = "mode"  # 模式加压（咒缚）
    CONTROL = "control"  # 心控加压（塞壬）
    UNKNOWN = "unkown"  # 未知（是的，这里红钩有个拼写错误）
    TOWN_IDLE = "town_idle"  # 城镇闲置减压和加压
    QUEST_FAIL = "quest_fail"  # 任务失败加压
    PASS = "pass"  # 跳过回合加压
    CAMPING_RELIEVE_STRESS = "camping_relieve_stress"  # 扎营减少压力
    CAMPING_EAT = "camping_eat"  # 扎营时吃东西减压
    TILE = "tile"  # 徒手挖墙加压
    RETREAT = "retreat"  # 撤退加压
    EFFECT = "effect"  # 效果
    CAPTURE = "capture"  # 抓人加压（巫婆锅、狂信者木桩、溺水船员勾锚）
    MONSTER_CRIT = "monster_crit"  # 怪物暴击加压


class STCombatStatMultiply(Enum):
    MAX_HP = "max_hp"  # 最大生命值增加（百分比）
    DAMAGE_LOW = "damage_low"  # 最小伤害增加（百分比）
    DAMAGE_HIGH = "damage_high"  # 最大伤害增加（百分比）
    ATTACK_RATING = "attack_rating"  # 命中倍率（百分比）
    CRIT_CHANCE = "crit_chance"  # 暴击倍率（百分比）
    DEFENSE_RATING = "defense_rating"  # 闪避倍率（百分比）
    PROTECTION_RATING = "protection_rating"  # 防御倍率（百分比）
    SPEED_RATING = "speed_rating"  # 速度倍率（百分比）


class STCombatStatAdd(Enum):
    MAX_HP = "max_hp"  # 最大生命值增加（固定值）
    # 注意：当通过倒扣最大生命值的方式使得英雄为0时进入死门 deaths_door: enter_effects 不会触发
    # 注意：当治疗使得英雄生命值为0时进入死门 rule 为 ondeathsdoorenter 的buff不会激活
    DAMAGE_LOW = "damage_low"  # 最小伤害增加（固定值）
    DAMAGE_HIGH = "damage_high"  # 最大伤害增加（固定值）
    ATTACK_RATING = "attack_rating"  # 命中增加（固定值）
    CRIT_CHANCE = "crit_chance"  # 暴击增加（固定值）
    DEFENSE_RATING = "defense_rating"  # 闪避增加（固定值）
    PROTECTION_RATING = "protection_rating"  # 防御增加（固定值）
    SPEED_RATING = "speed_rating"  # 速度增加（固定值）
    RIPOSTE_ON_HIT_CHANCE = "riposte_on_hit_chance"  # 被攻击时（被命中时）自身触发反击的概率
    RIPOSTE_ON_MISS_CHANCE = "riposte_on_miss_chance"  # 被攻击时（被闪避时）自身触发反击的概率


class STResistance(Enum):
    STUN = "stun"  # 眩晕抗性（面板最高500%）
    MOVE = "move"  # 位移抗性（面板最高500%）
    POISON = "poison"  # 腐蚀抗性（面板最高500%）
    BLEED = "bleed"  # 流血抗性（面板最高500%）
    DISEASE = "disease"  # 疾病抗性（面板最高95%）
    DEBUFF = "debuff"  # 减益抗性（面板最高500%）
    DEATH_BLOW = "death_blow"  # 死门抗性（面板最高87%）
    TRAP = "trap"  # 解除陷阱的概率（面板最高500%）


class STActivitySideEffectChance(Enum):
    ADD_CURRENCY = "add_currency"  # 赢钱（赌场）
    REMOVE_CURRENCY = "remove_currency"  # 输钱
    ADD_TRINKET = "add_trinket"  # 增加饰品
    REMOVE_TRINKET = "remove_trinket"  # 丢失饰品
    ACTIVITY_LOCK = "activity_lock"  # 延长活动（比如冥想时多加一周）
    APPLY_BUFF = "apply_buff"  # 获得buff（一般是负面的多。。。）
    GO_MISSING = "go_missing"  # 玩失踪


class STDisableCombatSkillAttribute(Enum):
    HEAL = "heal"  # 禁用治疗
    BUFF = "buff"  # 禁用增益
    DEBUFF = "debuff"  # 禁用减益
    BLEED = "bleed"  # 禁用流血
    POISON = "poison"  # 禁用腐蚀
    STUN = "stun"  # 禁用眩晕
    TAG = "tag"  # 禁用标记
    STRESS = "stress"  # 禁用压力（减压也算）
    MOVE = "move"  # 禁用位移
    DISEASE = "disease"  # 禁用疾病（注意：已证实并不存在禁用疾病这个子类别！）
    GUARD = "guard"  # 禁用守护（有额外的盾牌破碎图标显示，无论此buff的amount为多少，都会显示此图标）
    DAZE = "daze"  # 禁用迷乱
