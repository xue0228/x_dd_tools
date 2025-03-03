from enum import Enum


class Level(Enum):
    ZERO = 0  # 初始等级
    ONE = 1  # 升级一次
    TWO = 2  # 升级两次
    THREE = 3  # 升级三次
    FOUR = 4  # 升级四次


class UpgradeRequirementCode(Enum):
    ZERO = 0  # 装备升级一次后生效
    ONE = 1  # 装备升级两次后生效
    TWO = 2  # 装备升级三次后生效
    THREE = 3  # 装备升级四次后生效


class SkillType(Enum):
    MELEE = "melee"  # 近战
    RANGED = "ranged"  # 远程
    MOVE = "move"  # 官方公共移动技能
    TELEPORT = "teleport"  # 传送（DD3白细胞柄和农场沉睡使者）


class EffectTarget(Enum):
    # 自身（不依赖调用方所提供的目标）
    PERFORMER = "performer"
    # 我方全体（不依赖于调用方所提供的目标）
    PERFORMER_GROUP = "performer_group"
    # 除自身以外的其他人（不依赖于调用方所提供的目标）
    PERFORMER_GROUP_OTHER = "performer_group_other"
    # 目标
    TARGET = "target"
    # 目标全体
    TARGET_GROUP = "target_group"
    # 除目标以外的其他人
    TARGET_GROUP_OTHER = "target_group_other"
    # 目标对面的队伍全体，其施加的减益一律不过减益抗性，与一般效果的“同侧不过抗，异侧需过抗”不同
    TARGET_ENEMY_GROUP = "target_enemy_group"
    # 环境，修改火把亮度时使用该状态
    GLOBAL = "global"


class CurioResultType(Enum):
    POSITIVE = "positive"  # 奇物互动结果使用正面动画
    NEGATIVE = "negative"  # 奇物互动结果使用负面动画
    NEUTRAL = "neutral"  # 奇物互动结果使用中性动画
    NONE = "none"  # 奇物互动结果不使用动画


class Selection(Enum):
    YES = 1
    NO = 0


class MonsterType(Enum):
    UNHOLY = "unholy"  # 邪祟
    MAN = "man"  # 人类
    BEAST = "beast"  # 野兽
    ELDRITCH = "eldritch"  # 异魔
    VAMPIRE = "vampire"  # 血裔
    HUST = "hust"  # 瘪壳怪（农场怪的专属种族）
    CORPSE = "corpse"  # 尸体


class BuffStatType(Enum):
    HP_DOT_BLEED = "hp_dot_bleed"
    HP_DOT_POISON = "hp_dot_poison"
    HP_DOT_HEAL = "hp_dot_heal"
    STRESS_DOT = "stress_dot"
    SHUFFLE_DOT = "shuffle_dot"


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


class BuffSource(Enum):
    """
    effect: .steal_buff_source_type（源类型）
    effect: .dotSource
    effect: .buff_source_type
    """
    # 技能所施加的buff，包含effect形式dot
    SKILL = "bsrc_skill"
    # 未指定
    NOTSPECIFIED = "bsrc_notspecified"
    # 折磨
    AFFLICTION = "bsrc_affliction"
    # 美德
    VIRTUE = "bsrc_virtue"
    # 道具（此源的buff不会被扎营清除，建议需要buff不被扎营清除时，设置此源）
    ITEM = "bsrc_item"
    # 奇物
    CURIO = "bsrc_curio"
    # 疾病
    DISEASE = "bsrc_disease"
    # 反击
    RIPOSTE = "bsrc_riposte"
    # 扎营（此源中的“恐惧”类型buff不会被鸦片酊消除）
    CAMPINGSKILL = "bsrc_campingskill"
    # 怪癖
    QUIRK = "bsrc_quirk"
    # 饰品
    TRINKET = "bsrc_trinket"
    # 饰品套装
    TRINKET_SET = "bsrc_trinket_set"
    # skill instant相关
    INSTANT_SKILL = "bsrc_instantSkill"
    # 偷这个源，就可以把【被守护】这个状态偷走
    GUARD = "bsrc_guard"
    # 死门减益（红骷髅图标）
    DEATHSDOOR = "bsrc_deathsdoor"
    # 重创减益（白骷髅图标）
    DEATHSDOOR_RECOVERY = "bsrc_deathsdoor_recovery"
    # 心衰减益（白骷髅图标）
    DEATHSDOOR_RECOVERY_HEART_ATTACK = "bsrc_deathsdoor_recovery_heart_attack"
    # 任务失败
    QUEST_FAILURE = "bsrc_quest_failure"
    # 同伴（原版：投锚手出来给船长上的buff就是这个类型）
    COMPANION = "bsrc_companion"
    # 眩晕解除后提供的buff
    STUN = "bsrc_stun"
    # 城镇活动提供的buff
    TOWN = "bsrc_town"
    # 建筑的buff
    DISTRICT = "bsrc_district"
    # 火把环境增减益
    TORCHSETTINGS = "bsrc_torchsettings"
    # 暴击提供的buff
    CRIT = "bsrc_crit"
    # 饰品附加效果
    TRINKET_ADDITIONAL_EFFECT = "bsrc_trinket_additional_effect"
    # 战斗修饰（真光环）
    BATTLE_MODIFIER = "bsrc_battle_modifier"
    # 拒绝再次进入（DD本的余生不回规则）（红折磨图标）
    NEVER_AGAIN = "bsrc_never_again"
    # 猩红诅咒提供的buff
    VAMPIRE = "bsrc_vampire"
    # 城镇事件提供的buff（注意与bsrc_town区分）（铃铛图标）
    TOWN_EVENT = "bsrc_town_event"
    # 夜袭开始触发（参考破盾者夜袭开始的持续压力）（此源中的“恐惧”类型buff不会被鸦片酊消除）
    # （此buff源已被开发者约定为真驱散迂回要素，请注意不要在此源中存储需要长期生效的buff）
    FLASHBACK_START = "bsrc_flashback_start"
    # 夜袭结束触发
    FLASHBACK_RESULT = "bsrc_flashback_result"
    # 完成极暗地牢的英雄
    COMPLETED_DARKEST_DUNGEON_QUEST_PARTY_HERO = "bsrc_completed_darkest_dungeon_quest_party_hero"
    # 任务修饰
    QUEST_MODIFIER = "bsrc_quest_modifier"
    # 最后行动的英雄（马戏团DLC）（此buff源已被开发者约定为真驱散迂回要素，请注意不要在此源中存储需要长期生效的buff）
    LAST_HERO = "bsrc_last_hero"


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


class DamageType(Enum):
    """
    effect: .damage_type
    某些伤害类型不明所以，恐为测试版本残留，已被红钩弃用
    """
    UNKNOWN = "unknown"  # 未知
    TRAP = "trap"  # 陷阱
    OBSTACLE = "obstacle"  # 障碍
    HUNGER = "hunger"  # 饥饿
    ATTACK = "attack"  # 攻击
    BLEED = "bleed"  # 流血
    HEALING = "healing"  # 治疗
    POISONED = "poisoned"  # 腐蚀
    CAPTOR = "captor"  # 被锅和狂信者的柱子抓住时
    DDEXIT = "ddexit"  # dd地牢撤退？
    TOWNEXIT = "townexit"  # 撤退回城？
    DEATH = "death"  # 死亡
    HEART_ATTACK = "heartattack"  # 心衰
    THE_BLOOD = "theblood"  # 非猩红诅咒英雄喝血酿承受伤害
    EFFECT = "effect"  # 效果
    QUIRK_EVOLUTION_DEATH = "quirkevolutiondeath"  # 猩红诅咒凋零而死
    REFLECT = "reflect"  # 反伤
    RIPOSTE = "riposte"  # 反击
    ADDITIONAL_EFFECT = "additionaleffect"  # 额外效果
    SUPPLY = "supply"  # 消耗品
    QUEST_ITEM = "quest_item"  # 任务道具
    TRINKET = "trinket"  # 饰品
    ESTATE_CURRENCY = "estate_currency"  # 祖产货币
    JOURNAL_PAGE = "journal_page"  # 日志文件
    TORCH = "torch"  # 火把
    SHOVEL = "shovel"  # 铲子


class DamageSource(Enum):
    """
    effect: .damage_source_type
    """
    UNKNOWN = "unknown"  # 未知
    HUNGER = "hunger"  # 饥饿
    TRAP = "trap"  # 陷阱
    OBSTACLE = "obstacle"  # 障碍，挖墙
    FRIENDLY = "friendly"  # 友方技能
    MONSTER = "monster"  # 怪物
    HERO = "hero"  # 英雄
    FRIENDLY_QUIRK_ACTOUT = "friendly_quirk_actout"  # 基于怪癖的友方actout行为
    FRIENDLY_TRAIT_ACTOUT = "friendly_trait_actout"  # 基于美德折磨的友方actout行为
    ITEM = "item"  # 道具
    EFFECT = "effect"  # 效果
    QUIRK = "quirk"  # 怪癖
    REFLECT = "reflect"  # 反伤
    TRINKET = "trinket"  # 饰品
    ESTATE = "estate"  # 祖产道具


class TrinketTriggerType(Enum):
    """
    饰品效果触发器
    """
    # On Attack (target: monster)
    # 攻击技能额外效果
    # 此effect的target指向作为技能目标的目标怪物
    ATTACK_SKILL = "attack_skill_additional_effects"

    # Friendly Skill (target: ally)
    # 友方技能额外效果
    # 此effect的target指向作为技能目标的目标英雄
    FRIENDLY_SKILL = "friendly_skill_additional_effects"

    # On Monster Kill (target: hero)
    # 怪物被击杀时饰品装备者获得额外效果
    # 此effect的target指向饰品触发者的英雄本人
    KILL_PERFORMER = "kill_performer_additional_effects"

    # On Monster Kill (target: all monsters)
    # 怪物被击杀时所有怪物获得额外效果
    # 此effect的target指向每一个怪物（target本身对怪物群体而无需target_group）
    KILL_ALL_MONSTERS = "kill_all_monsters_additional_effects"

    # On Monster Kill (target: party)
    # 怪物被击杀时友方全体获得额外效果
    # 此effect的target指向每一个英雄（target本身对英雄群体而无需target_group）
    KILL_ALL_HEROES = "kill_all_heroes_additional_effects"

    # Hero Killed (target: party)
    # 人物被击杀时友方全体获得额外效果
    # 此effect的target指向每一个英雄（target本身对英雄群体而无需target_group）
    WAS_KILL_ALL_HEROES = "was_kill_all_heroes_additional_effects"

    # Hero Killed (target: all monsters)
    # 人物被击杀时所有怪物获得额外效果
    # 此effect的target指向每一个怪物（target本身对怪物群体而无需target_group）
    WAS_KILL_ALL_MONSTERS = "was_kill_all_monsters_additional_effects"

    # Hero Was Hit (target: attacker | performer: hero)
    # 被打时额外效果
    # 此effect的target指向攻击者的怪物
    # 此effect的performer指向饰品触发者的英雄本人
    WAS_HIT = "was_hit_additional_effects"

    # Hero Was Hit (target: party | performer: hero)
    # 饰品携带者被打时友方全体获得额外效果
    # 此effect的target指向每一个英雄（target本身对英雄群体而无需target_group）
    # 此effect的performer指向饰品触发者的英雄本人
    WAS_HIT_ALL_HEROES = "was_hit_all_heroes_additional_effects"

    # Hero Was Hit (target: all monsters | performer: hero)
    # 饰品携带者被打时所有怪物获得额外效果
    # 此effect的target指向每一个怪物（target本身对怪物群体而无需target_group）
    # 此effect的performer指向饰品触发者的英雄本人
    WAS_HIT_ALL_MONSTERS = "was_hit_all_monsters_additional_effects"

    # On Melee Attack (target: monster)
    # 怪物被近战技能命中时获得额外效果
    # 此effect的target指向作为技能目标的怪物
    MELEE_ATTACK_SKILL = "melee_attack_skill_additional_effects"

    # On Ranged Attack (target: monster)
    # 怪物被远程技能命中时获得额外效果
    # 此effect的target指向作为技能目标的目标怪物
    RANGED_ATTACK_SKILL = "ranged_attack_skill_additional_effects"

    # On Crit (target: monster)
    # 怪物被暴击时
    # 此effect的target指向作为技能目标的目标怪物
    ATTACK_CRIT = "attack_crit_additional_effects"

    # On Riposte (target: monster)
    # 反击命中时
    # 此effect的target指向作为反击目标的目标怪物
    RIPOSTE_SKILL = "riposte_skill_additional_effects"


class ActorStatus(Enum):
    TAGGED = "tagged"
    POISONED = "poisoned"
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    VIRTUED = "virtued"
    AFFLICTED = "afflicted"


class KeyStatus(Enum):
    TAGGED = "tagged"
    POISONED = "poisoned"
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    DAZED = "dazed"
    TRANSFORMED = "transformed"  # 转变？传送？已废弃


class DungeonID(Enum):
    CRYPTS = "crypts"  # 遗迹
    WEALD = "weald"  # 荒野
    WARRENS = "warrens"  # 兽窟
    COVE = "cove"  # 海湾
    COURTYARD = "courtyard"  # 庭院


class TownActivityType(Enum):
    MEDITATION = "meditation"  # 冥想
    PRAYER = "prayer"  # 祈祷
    FLAGELLATION = "flagellation"  # 苦修
    BAR = "bar"  # 酒吧
    GAMBLING = "gambling"  # 赌博
    BROTHEL = "brothel"  # 妓院
    TREATMENT = "treatment"  # 疗养院的怪癖治疗
    DISEASE_TREATMENT = "disease_treatment"  # 疗养院的疾病治疗


class QuirkType(Enum):
    # 本体怪癖
    DISEASE_BAD_HUMOURS = "bad_humours"  # 体液失衡
    DISEASE_BULIMIC = "bulimic"  # 易饥症
    DISEASE_CREEPING_COUGH = "creeping_cough"  # 剧烈咳嗽
    DISEASE_ENNUI = "ennui"  # 倦怠症
    DISEASE_HEMOPHILIA = "hemophilia"  # 血友病
    DISEASE_HYSTERICAL_BLINDNESS = "hysterical_blindness"  # 癔病性失明
    DISEASE_LETHARGY = "lethargy"  # 嗜睡症
    DISEASE_RABIES = "rabies"  # 狂犬病
    DISEASE_SCURVY = "scurvy"  # 败血症
    DISEASE_SPOTTED_FEVER = "spotted_fever"  # 斑疹热
    DISEASE_STOMACH_CRAMP = "stomach_cramp"  # 内脏痉挛
    DISEASE_SYPHILIS = "syphilis"  # 梅毒
    DISEASE_TAPEWORM = "tapeworm"  # 绦虫病
    DISEASE_TETANUS = "tetanus"  # 破伤风
    DISEASE_THE_AGUE = "the_ague"  # 疟疾
    DISEASE_THE_BLACK_PLAGUE = "the_black_plague"  # 黑死病
    DISEASE_THE_FITS = "the_fits"  # 癫痫
    DISEASE_THE_RED_PLAGUE = "the_red_plague"  # 红热病
    DISEASE_THE_RUNS = "the_runs"  # 腹泻
    DISEASE_THE_WORRIES = "the_worries"  # 忧郁症
    DISEASE_VAMPIRIC_SPIRITS = "vampiric_spirits"  # 渴血症
    DISEASE_VERTIGO = "vertigo"  # 头晕
    DISEASE_WASTING_SICKNESS = "wasting_sickness"  # 慢性疾病

    POSITIVE_ACCURATE = "accurate"  # 致命
    POSITIVE_ARMOR_HAGGLER = "armor_haggler"  # 护甲匠
    POSITIVE_BACK_TRACKER = "back_tracker"  # 退路追随者
    POSITIVE_CLOTTER = "clotter"  # 富血
    POSITIVE_CLUTCH_HITTER = "clutch_hitter"  # 绝境击杀
    POSITIVE_CORVIDS_EYE = "corvids_eye"  # 乌鸦之眼
    POSITIVE_CORVIDS_GRACE = "corvids_grace"  # 乌鸦之雅
    POSITIVE_CORVIDS_RESILIENCE = "corvids_resilience"  # 乌鸦之健
    POSITIVE_COVE_ADVENTURER = "cove_adventurer"  # 海湾冒险者
    POSITIVE_COVE_EXPLORER = "cove_explorer"  # 海湾探险家
    POSITIVE_COVE_SCROUNGER = "cove_scrounger"  # 海湾拾荒者
    POSITIVE_COVE_TACTICIAN = "cove_tactician"  # 海湾战术家
    POSITIVE_EAGLE_EYE = "eagle_eye"  # 锐利鹰眼
    POSITIVE_EARLY_RISER = "early_riser"  # 早起者
    POSITIVE_EVASIVE = "evasive"  # 灵活
    POSITIVE_FAST_HEALER = "fast_healer"  # 快速治疗
    POSITIVE_FATED = "fated"  # 宿命
    POSITIVE_GIFT_OF_THE_HEALER = "gift_of_the_healer"  # 医生天赋
    POSITIVE_HARD_NOGGIN = "hard_noggin"  # 千杯不醉
    POSITIVE_HARD_SKINNED = "hard_skinned"  # 表皮硬化
    POSITIVE_HATRED_OF_BEAST = "hatred_of_beast"  # 仇恨野兽
    POSITIVE_HATRED_OF_ELDRITCH = "hatred_of_eldritch"  # 仇恨异魔
    POSITIVE_HATRED_OF_MAN = "hatred_of_man"  # 仇恨人类
    POSITIVE_HATRED_OF_UNHOLY = "hatred_of_unholy"  # 仇恨邪秽
    POSITIVE_IMPROVED_BALANCE = "improved_balance"  # 身体平衡
    POSITIVE_IRREPRESSIBLE = "irrepressible"  # 义气高涨
    POSITIVE_LAST_GASP = "last_gasp"  # 最后一搏
    POSITIVE_LURKER = "lurker"  # 潜伏者
    POSITIVE_MEDITATOR = "meditator"  # 冥想者
    POSITIVE_NATURAL_EYE = "natural_eye"  # 自然之眼
    POSITIVE_NATURAL_SWING = "natural_swing"  # 挥舞自然
    POSITIVE_NIGHT_OWL = "night_owl"  # 夜猫子
    POSITIVE_NYMPHOMANIA = "nymphomania"  # 好色之徒
    POSITIVE_ON_GUARD = "on_guard"  # 警惕戒备
    POSITIVE_PHOTOMANIA = "photomania"  # 喜光
    POSITIVE_PRECISION_STRIKER = "precision_striker"  # 精准打击
    POSITIVE_QUICK_REFLEXES = "quick_reflexes"  # 反应快速
    POSITIVE_QUICKDRAW = "quickdraw"  # 快速出鞘
    POSITIVE_RESILIENT = "resilient"  # 强韧
    POSITIVE_ROBUST = "robust"  # 粗健
    POSITIVE_RUINS_ADVENTURER = "ruins_adventurer"  # 遗迹冒险者
    POSITIVE_RUINS_EXPLORER = "ruins_explorer"  # 遗迹探索者
    POSITIVE_RUINS_SCROUNGER = "ruins_scrounger"  # 遗迹拾荒者
    POSITIVE_RUINS_TACTICIAN = "ruins_tactician"  # 遗迹战术家
    POSITIVE_SECOND_WIND = "second_wind"  # 重振旗鼓
    POSITIVE_SKILLED_GAMBLER = "skilled_gambler"  # 赌博老手
    POSITIVE_SLAYER_OF_BEAST = "slayer_of_beast"  # 野兽克星
    POSITIVE_SLAYER_OF_ELDRITCH = "slayer_of_eldritch"  # 异魔克星
    POSITIVE_SLAYER_OF_MAN = "slayer_of_man"  # 人类克星
    POSITIVE_SLAYER_OF_UNHOLY = "slayer_of_unholy"  # 邪秽克星
    POSITIVE_SLUGGER = "slugger"  # 重击者
    POSITIVE_STEADY = "steady"  # 镇定
    POSITIVE_STOUT = "stout"  # 强壮
    POSITIVE_STRESS_FASTER = "stress_faster"  # 应激性厌食癖
    POSITIVE_THICK_BLOODED = "thick_blooded"  # 气血稳健
    POSITIVE_TOUGH = "tough"  # 坚韧
    POSITIVE_UNERRING = "unerring"  # 正中靶心
    POSITIVE_UNYIELDING = "unyielding"  # 倔强不屈
    POSITIVE_WARREN_ADVENTURER = "warren_adventurer"  # 兽窟冒险者
    POSITIVE_WARREN_EXPLORER = "warren_explorer"  # 兽窟探险家
    POSITIVE_WARREN_SCROUNGER = "warren_scrounger"  # 兽窟拾荒者
    POSITIVE_WARREN_TACTICIAN = "warren_tactician"  # 兽窟战术家
    POSITIVE_WARRIOR_OF_LIGHT = "warrior_of_light"  # 光明战士
    POSITIVE_WEALD_ADVENTURER = "weald_adventurer"  # 荒野冒险者
    POSITIVE_WEALD_EXPLORER = "weald_explorer"  # 荒野探险家
    POSITIVE_WEALD_SCROUNGER = "weald_scrounger"  # 荒野拾荒者
    POSITIVE_WEALD_TACTICIAN = "weald_tactician"  # 荒野战术家
    POSITIVE_WEAPONS_HAGGLER = "weapons_haggler"  # 武器匠

    NEGATIVE_ABLUTOMANIA = "ablutomania"  # 洁癖
    NEGATIVE_ALCOHOLISM = "alcoholism"  # 酒鬼
    NEGATIVE_ANEMIC = "anemic"  # 贫血
    NEGATIVE_AUTOMATONOPHOBIA = "automatonophobia"  # 人像恐惧症
    NEGATIVE_BAD_GAMBLER = "bad_gambler"  # 赌术糟糕
    NEGATIVE_BLOODTHIRSTY = "bloodthirsty"  # 嗜血
    NEGATIVE_CALM = "calm"  # 平静
    NEGATIVE_CLAUSTROPHOBIA = "claustrophobia"  # 幽闭恐惧症
    NEGATIVE_CLUMSY = "clumsy"  # 笨拙
    NEGATIVE_COMPULSIVE = "compulsive"  # 强迫症
    NEGATIVE_CORVIDS_APPETITE = "corvids_appetite"  # 鸦之嗜食
    NEGATIVE_CORVIDS_BLINDNESS = "corvids_blindness"  # 鸦之盲目
    NEGATIVE_CORVIDS_CURIOSITY = "corvids_curiosity"  # 鸦之好奇
    NEGATIVE_COVE_PHOBE = "cove_phobe"  # 海湾恐惧症
    NEGATIVE_CURIOUS = "curious"  # 好奇
    NEGATIVE_DACNOMANIA = "dacnomania"  # 杀人狂
    NEGATIVE_DARK_TEMPTATION = "dark_temptation"  # 痴迷黑暗
    NEGATIVE_DEMONOMANIA = "demonomania"  # 魔怔
    NEGATIVE_DEVIANT_TASTES = "deviant_tastes"  # 重口味
    NEGATIVE_DIPSOMANIA = "dipsomania"  # 酗酒
    NEGATIVE_DIURNAL = "diurnal"  # 日落而息
    NEGATIVE_DUD_HITTER = "dud_hitter"  # 绝境失心
    NEGATIVE_EGOMANIA = "egomania"  # 自恋狂
    NEGATIVE_ENLIGHTENED = "enlightened"  # 冥想启迪
    NEGATIVE_FAITHLESS = "faithless"  # 失去信念
    NEGATIVE_FEAR_OF_BEAST = "fear_of_beast"  # 惧怕野兽
    NEGATIVE_FEAR_OF_ELDRITCH = "fear_of_eldritch"  # 惧怕异魔
    NEGATIVE_FEAR_OF_MAN = "fear_of_man"  # 惧怕人类
    NEGATIVE_FEAR_OF_UNHOLY = "fear_of_unholy"  # 畏惧邪秽
    NEGATIVE_FLAGELLANT = "flagellant"  # 苦修
    NEGATIVE_FLAWED_RELEASE = "flawed_release"  # 击发缺陷
    NEGATIVE_FRAGILE = "fragile"  # 脆弱
    NEGATIVE_GAMBLER = "gambler"  # 赌徒
    NEGATIVE_GOD_FEARING = "god_fearing"  # 敬神
    NEGATIVE_GUILTY_CONSCIENCE = "guilty_conscience"  # 内疚
    NEGATIVE_HAGIOMANIA = "hagiomania"  # 宗教狂热
    NEGATIVE_HIEROMANIA = "hieromania"  # 瞻礼狂
    NEGATIVE_HYLOMANIA = "hylomania"  # 贪财
    NEGATIVE_INACCURATE = "inaccurate"  # 失准
    NEGATIVE_KLEPTOMANIAC = "kleptomaniac"  # 盗窃癖
    NEGATIVE_KNOWN_CHEAT = "known_cheat"  # 知名老千
    NEGATIVE_LAZY_EYE = "lazy_eye"  # 怠惰之眼
    NEGATIVE_LOVE_INTEREST = "love_interest"  # 多情
    NEGATIVE_LYGOPHOBIA = "lygophobia"  # 惧暗
    NEGATIVE_MERCURIAL = "mercurial"  # 喜怒无常
    NEGATIVE_NECROMANIA = "necromania"  # 恋尸癖
    NEGATIVE_NERVOUS = "nervous"  # 紧张
    NEGATIVE_NIGHT_BLINDNESS = "night_blindness"  # 夜盲
    NEGATIVE_NOCTURNAL = "nocturnal"  # 夜行动物
    NEGATIVE_OFF_GUARD = "off_guard"  # 措手不及
    NEGATIVE_PARANORMANIA = "paranormania"  # 热衷异象
    NEGATIVE_PHENGOPHOBIA = "phengophobia"  # 畏光
    NEGATIVE_PLUTOMANIA = "plutomania"  # 敛财狂
    NEGATIVE_RESOLUTION = "resolution"  # 戒酒
    NEGATIVE_RUINS_PHOBE = "ruins_phobe"  # 遗迹恐惧症
    NEGATIVE_RUMINATOR = "ruminator"  # 沉思者
    NEGATIVE_SATANOPHOBIA = "satanophobia"  # 恶魔恐惧症
    NEGATIVE_SCATTERING = "scattering"  # 靶心偏差
    NEGATIVE_SENSITIVE_TO_LIGHT = "sensitive_to_light"  # 畏光
    NEGATIVE_SHOCKER = "shocker"  # 大惊小怪
    NEGATIVE_SICKLY = "sickly"  # 病弱
    NEGATIVE_SITIOMANIA = "sitiomania"  # 嗜好食物
    NEGATIVE_SLOW_REFLEXES = "slow_reflexes"  # 反应迟钝
    NEGATIVE_SLOWDRAW = "slowdraw"  # 慢速出鞘
    NEGATIVE_SOFT = "soft"  # 柔弱
    NEGATIVE_STRESS_EATER = "stress_eater"  # 应激性暴食癖
    NEGATIVE_SUICIDAL = "suicidal"  # 求生意识弱
    NEGATIVE_THANATOPHOBIA = "thanatophobia"  # 死亡恐惧症
    NEGATIVE_THE_YIPS = "the_yips"  # 莽撞
    NEGATIVE_THIN_BLOODED = "thin_blooded"  # 气血稀薄
    NEGATIVE_TORN_ROTATOR_CUFF = "torn_rotator_cuff"  # 肩膀损伤
    NEGATIVE_TUCKERED_OUT = "tuckered_out"  # 精疲力尽
    NEGATIVE_UNQUIET_MIND = "unquiet_mind"  # 焦躁心灵
    NEGATIVE_WARREN_PHOBE = "warren_phobe"  # 兽穴恐惧症
    NEGATIVE_WEAK_GRIP = "weak_grip"  # 腕力虚弱
    NEGATIVE_WEALD_PHOBE = "weald_phobe"  # 荒野恐惧症
    NEGATIVE_WINDED = "winded"  # 疲软
    NEGATIVE_WITNESS = "witness"  # 目击证人
    NEGATIVE_ZOOPHOBIA = "zoophobia"  # 动物恐惧症

    AUTOPHOBIA = "autophobia"  # 孤独恐惧症
    COVE_MASTER = "cove_master"  # 海湾专家
    COVE_SURVIVOR = "cove_survivor"  # 海湾求生家
    CRUELTY_CONSCIOUS = "cruelty_conscious"  # 残忍意愿
    DARKEST_DUNGEON_ADVENTURER = "darkest_dungeon_adventurer"  # 极暗地牢冒险家
    DARKEST_DUNGEON_EXPLORER = "darkest_dungeon_explorer"  # 极暗地牢探索者
    DARKEST_DUNGEON_MASTER = "darkest_dungeon_master"  # 极暗地牢大师
    DARKEST_DUNGEON_PHOBE = "darkest_dungeon_phobe"  # 极暗地牢恐惧者
    DARKEST_DUNGEON_SCROUNGER = "darkest_dungeon_scrounger"  # 极暗地牢拾荒者
    DARKEST_DUNGEON_SURVIVOR = "darkest_dungeon_survivor"  # 极暗地牢求生家
    DARKEST_DUNGEON_TACTICIAN = "darkest_dungeon_tactician"  # 极暗地牢战术家
    DEVOUT = "devout"  # 虔诚
    DISORGANIZED = "disorganized"  # 组织混乱
    DOUBLE_VISION = "double_vision"  # 重影
    GAVE_IT_ALL = "gave_it_all"  # 激情
    IN_THE_ZONE = "in_the_zone"  # 专心致志
    INSPIRED = "inspired"  # 雄心
    LIGHT_SLEEPER = "light_sleeper"  # 光之沉睡者
    NECROPHOBIA = "necrophobia"  # 恐尸症
    ORGANIZED = "organized"  # 处变不惊
    PACK_MULE = "pack_mule"  # 驮骡之负
    PREDATOR = "predator"  # 铁血
    RUINS_MASTER = "ruins_master"  # 遗迹专家
    RUINS_SURVIVOR = "ruins_survivor"  # 遗迹生存者
    SURVIVALIST = "survivalist"  # 生存专家
    TITHER = "tither"  # 宗教捐赠狂
    TOO_BOASTFUL = "too_boastful"  # 自负
    TOOTHEACHE = "tootheache"  # 牙痛
    WARREN_MASTER = "warren_master"  # 兽窟专家
    WARREN_SURVIVOR = "warren_survivor"  # 兽窟求生家
    WEALD_MASTER = "weald_master"  # 荒野专家
    WEALD_SURVIVOR = "weald_survivor"  # 荒野求生家

    # 庭院 DLC
    DISEASE_VAMPIRE_BLOOD_LUST = "disease_vampire_blood_lust"  # 猩红诅咒（血怒！）
    DISEASE_VAMPIRE_CRAVE = "disease_vampire_crave"  # 猩红诅咒（渴血）
    DISEASE_VAMPIRE_PASSIVE = "disease_vampire_passive"  # 猩红诅咒
    DISEASE_VAMPIRE_WASTING = "disease_vampire_wasting"  # 猩红诅咒（凋零）

    # 农场 DLC
    DISEASE_GREY_ROT = "grey_rot"  # 灰霉菌
    DISEASE_SKY_TAINT = "sky_taint"  # 天空污染

    POSITIVE_TWILIGHT_DREAMER = "twilight_dreamer"  # 暮光之梦
    POSITIVE_LUMINOUS = "luminous"  # 光芒四射
    POSITIVE_SCYTHEMASTER = "scythemaster"  # 用刀大师
    POSITIVE_HUSK_SLAYER = "husk_slayer"  # 瘪壳杀手
    POSITIVE_ALIEN_EYE = "alien_eye"  # 棱镜之眼
    POSITIVE_ALIEN_PRECISION = "alien_precision"  # 棱镜准度
    POSITIVE_ALIEN_SPEED = "alien_speed"  # 棱镜速度
    POSITIVE_ALIEN_FORCE = "alien_force"  # 棱镜力量
    POSITIVE_ALIEN_CALM = "alien_calm"  # 棱镜镇定
    POSITIVE_ALIEN_PURITY = "alien_purity"  # 棱镜纯度
    POSITIVE_ALIEN_HEALING = "alien_healing"  # 棱镜凝固
    POSITIVE_ALIEN_SOLIDITY = "alien_solidity"  # 棱镜坚固
    POSITIVE_ALIEN_STABILITY = "alien_stability"  # 棱镜稳定
    POSITIVE_ALIEN_ISOLATION = "alien_isolation"  # 棱镜隔离
    POSITIVE_NATURAL = "natural"  # 自然
    POSITIVE_FAIRWEATHER_FIGHTER = "fairweather_fighter"  # 晴天战士
    POSITIVE_HOT_TO_TROT = "hot_to_trot"  # 急不可待
    POSITIVE_DAREDEVIL = "daredevil"  # 胆大妄为
    POSITIVE_MUSICAL = "musical"  # 音乐
    POSITIVE_SPIRITUAL = "spiritual"  # 精神
    POSITIVE_GOTHIC = "gothic"  # 哥特
    POSITIVE_HIPPOCRATIC = "hippocratic"  # 悬壶济世
    POSITIVE_GIFTED = "gifted"  # 天才

    NEGATIVE_FADING = "fading"  # 衰退
    NEGATIVE_ASHEN = "ashen"  # 苍白
    NEGATIVE_SHARD_HUNGRY = "shard_hungry"  # 碎片雇佣兵
    NEGATIVE_GERMOPHOBE = "germophobe"  # 洁癖
    NEGATIVE_NERVOUS_BLEEDER = "nervous_bleeder"  # 伤口撒盐
    NEGATIVE_PERFECTIONIST = "perfectionist"  # 完美主义
    NEGATIVE_RISKTAKER = "risktaker"  # 冒险
    NEGATIVE_ANTSY = "antsy"  # 焦虑
    NEGATIVE_IMPOSTER_SYNDROME = "imposter_syndrome"  # 负担症候
    NEGATIVE_TONE_DEAF = "tone_deaf"  # 音盲
    NEGATIVE_SCIENTIFIC = "scientific"  # 科学
    NEGATIVE_ASCETIC = "ascetic"  # 苦行
    NEGATIVE_INFIRM = "infirm"  # 体弱多病
    NEGATIVE_BAD_HEALER = "bad_healer"  # 治疗无效


class MonsterClass(Enum):
    # 本体
    ANCESTOR_BIG = "ancestor_big"  # 先祖
    ANCESTOR_FLAWED = "ancestor_flawed"  # 瑕疵复制体
    ANCESTOR_HEART = "ancestor_heart"  # 黑暗之心
    ANCESTOR_NEBULA = "ancestor_nebula"  # 绝对的虚无
    ANCESTOR_PERFECT = "ancestor_perfect"  # 完美复制体
    ANCESTOR_POD = "ancestor_pod"  # 孕育之心
    ANCESTOR_SMALL = "ancestor_small"  # 先祖
    BLOATED_CORPSE = "bloated_corpse"  # 溺亡行尸
    BRIGAND_BARREL = "brigand_barrel"  # 炸药桶
    BRIGAND_BLOOD = "brigand_blood"  # 土匪放血者
    BRIGAND_CANNON = "brigand_cannon"  # 土匪8磅炮
    BRIGAND_CUTTHROAT = "brigand_cutthroat"  # 土匪割喉者
    BRIGAND_FUSEMAN = "brigand_fuseman"  # 土匪点火者
    BRIGAND_FUSILIER = "brigand_fusilier"  # 土匪火枪手
    BRIGAND_HUNTER = "brigand_hunter"  # 土匪猎杀者
    BRIGAND_RAIDER = "brigand_raider"  # 土匪洗劫者
    BRIGAND_SAPPER = "brigand_sapper"  # 匪首“头狼”
    CARRION_EATER = "carrion_eater"  # 腐肉吞吃者
    CARRION_EATER_BIG = "carrion_eater_big"  # 大型腐肉吞吃者
    CAULDRON = "cauldron"  # 大锅
    CAULDRON_EMPTY = "cauldron_empty"  # 大锅（空）
    CAULDRON_FULL = "cauldron_full"  # 大锅（满）
    CELL_BATTLE = "cell_battle"  # 抗体
    CELL_WHITE = "cell_white"  # 白细胞柄
    COLLECTOR = "collector"  # 收集者
    COLLECTOR_BATTLE = "collector_battle"  # 被收集的强盗
    COLLECTOR_PROTECT = "collector_protect"  # 被收集的老兵
    COLLECTOR_SHAMAN = "collector_shaman"  # 被收集的修女
    CORPSE = "corpse"  # 尸骸
    CORPSE_LARGE = "corpse_large"  # 大型尸骸
    CRONE = "crone"  # 巫妪
    CROW = "crow"  # 无情尖叫魔
    CULTIST_BRAWLER = "cultist_brawler"  # 邪教暴徒
    CULTIST_HARPY = "cultist_harpy"  # 飞升女巫
    CULTIST_ORGIASTIC = "cultist_orgiastic"  # 狂喜的教众
    CULTIST_SHROUDED = "cultist_shrouded"  # 邪教祭司
    CULTIST_WARLORD = "cultist_warlord"  # 飞升教士
    CULTIST_WITCH = "cultist_witch"  # 邪教侍僧
    CYST = "cyst"  # 巨噬胞体
    DROWNED_ANCHOR = "drowned_anchor"  # 溺亡拉绳手
    DROWNED_ANCHORED = "drowned_anchored"  # 溺亡拉绳手
    DROWNED_CAPTAIN = "drowned_captain"  # 淹浸船员
    DROWNED_PIRATE = "drowned_pirate"  # 微醺怨鬼
    ECTOPLASM = "ectoplasm"  # 胞质体
    ECTOPLASM_LARGE = "ectoplasm_large"  # 大型胞质体
    ERRANT_FLESH_BAT = "errant_flesh_bat"  # 螅肉
    ERRANT_FLESH_DOG = "errant_flesh_dog"  # 血肉猎犬
    FISHMAN_CRABBY = "fishman_crabby"  # 巨钳潮蟹
    FISHMAN_HARPOON = "fishman_harpoon"  # 深潜群居者
    FISHMAN_SHAMAN = "fishman_shaman"  # 深潜萨满
    FORMLESS_GUARD = "formless_guard"  # 未成之血肉
    FORMLESS_MELEE = "formless_melee"  # 未成之血肉
    FORMLESS_RANGED = "formless_ranged"  # 未成之血肉
    FORMLESS_WEAK = "formless_weak"  # 未成之血肉
    FUNGAL_ARTILLERY = "fungal_artillery"  # 真菌孢子炮
    FUNGAL_BLOAT = "fungal_bloat"  # 真菌刮擦者
    GARGOYLE = "gargoyle"  # 石像鬼
    GHOUL = "ghoul"  # 食尸鬼
    HAG = "hag"  # 巫婆
    JELLYFISH = "jellyfish"  # 蛰针水母
    MADMAN = "madman"  # 疯子
    MAGGOT = "maggot"  # 蛆虫
    NECROMANCER = "necromancer"  # 死灵法师
    NEST = "nest"  # 尖叫魔巢穴
    OCTOTANK = "octotank"  # 深潜守卫
    PEW_LARGE = "pew_large"  # 长椅路障
    PEW_MEDIUM = "pew_medium"  # 开裂的长椅
    PEW_SMALL = "pew_small"  # 碎裂的长椅
    PROPHET = "prophet"  # 聒噪的先知
    RABID_DOG = "rabid_dog"  # 袭人狂狗
    SHAMBLER = "shambler"  # 跛行者
    SHAMBLER_TENTACLE = "shambler_tentacle"  # 跛行衍生
    SHUFFLER = "shuffler"  # "错乱恐魔"
    SIREN = "siren"  # 海妖塞壬
    SKELETON_ARBALIST = "skeleton_arbalist"  # 骸骨弩手
    SKELETON_BEARER = "skeleton_bearer"  # 骸骨旗手
    SKELETON_BISHOP = "skeleton_bishop"  # 骸骨主教
    SKELETON_CAPTAIN = "skeleton_captain"  # 骸骨队长
    SKELETON_COMMON = "skeleton_common"  # 骸骨暴民
    SKELETON_COURTIER = "skeleton_courtier"  # 骸骨官僚
    SKELETON_DEFENDER = "skeleton_defender"  # 骸骨抵御者
    SKELETON_MILITIA = "skeleton_militia"  # 骸骨战士
    SKELETON_SPEAR = "skeleton_spear"  # 骸骨矛手
    SNAIL_URCHIN = "snail_urchin"  # 深海蛆虫
    SPIDER_SPITTER = "spider_spitter"  # 喷毒蛛
    SPIDER_WEBBER = "spider_webber"  # 结网蛛
    SWINE_DRUMMER = "swine_drummer"  # 猪人鼓手
    SWINE_PIGLET = "swine_piglet"  # 威尔伯
    SWINE_PRINCE = "swine_prince"  # 猪人王子
    SWINE_REAVER = "swine_reaver"  # 猪人切割者
    SWINE_SKIVER = "swine_skiver"  # 迷窟追猎者
    SWINE_SLASHER = "swine_slasher"  # 猪人钩手
    SWINE_WRETCH = "swine_wretch"  # 猪人残废
    SWINETAUR = "swinetaur"  # 猪人骑士
    TEMPLAR_MELEE = "templar_melee"  # 圣堂斗士
    TEMPLAR_MELEE_MB = "templar_melee_mb"  # 圣堂护法
    TEMPLAR_RANGED = "templar_ranged"  # 圣堂狙手
    TEMPLAR_RANGED_MB = "templar_ranged_mb"  # 圣堂军阀
    TOTEM_ATTACK = "totem_attack"  # 恶性增生物
    TOTEM_GUARD = "totem_guard"  # 良性增生物
    UNCLEAN_GIANT = "unclean_giant"  # 不洁巨人
    VIRAGO_HATEFUL = "virago_hateful"  # 林中恶妇
    VIRAGO_SHROOM = "virago_shroom"  # 死疽真菌

    # 庭院 DLC
    BARON = "baron"  # 男爵
    BODY_AVERAGE = "body_average"  # 躯体
    BODY_BLOATED = "body_bloated"  # 胀血的躯体
    BODY_EMACIATED = "body_emaciated"  # 瘦弱的躯体
    BULRUSH = "bulrush"  # 灯心草
    CASTELLAN = "castellan"  # 守门人
    CATTAIL = "cattail"  # 香蒲
    CHEVALIER = "chevalier"  # 骑士
    COUNTESS = "countess"  # 伯爵夫人
    COURTESAN = "courtesan"  # 舞女
    CROCODILE = "crocodile"  # 鳄鱼
    CURTAIN = "curtain"  # 未使用
    ESQUIRE = "esquire"  # 绅士
    FANATIC = "fanatic"  # 狂信者
    PARASITE = "parasite"  # 寄生虫
    PYRE_EMPTY = "pyre_empty"  # 木桩
    PYRE_FULL = "pyre_full"  # 木桩
    STATUE_HAND = "statue_hand"  # 血泉之源
    STATUE_HEAD = "statue_head"  # 花园守卫
    STATUE_SHIELD = "statue_shield"  # 石盾
    STEWARD = "steward"  # 男仆
    SYCOPHANT = "sycophant"  # 谄媚者
    TICK_ZOMBIE = "tick_zombie"  # 乞血者
    VISCOUNT = "viscount"  # 子爵

    # 农场 DLC
    COCOON = "cocoon"  # 冰封工人
    FARMER = "farmer"  # 农场工人
    MILLER = "miller"  # 磨坊主
    PLOWHORSE = "plowhorse"  # 犁马
    REVENANT = "revenant"  # 沉睡使者
    SCARECROW = "scarecrow"  # 稻草人
    FOREMAN = "foreman"  # 工头
    CORPSE_CRYSTAL_LARGE = "corpse_crystal_large"  # 水晶畸变
    THING = "thing"  # 星空怪
    CORPSE_CRYSTAL = "corpse_crystal"  # 水晶畸变
    GATEKEEPER = "gatekeeper"  # 沉睡者之梦
    GALAXY = "galaxy"  # 沉睡者
    SPIRE = "spire"  # 破裂水晶怪
    SEED_BLACK = "seed_black"  # 创伤畸变
    SEED_PURPLE = "seed_purple"  # 短暂畸变
    SEED_GREY = "seed_grey"  # 金刚石畸变
    SEED_RED = "seed_red"  # 不稳定畸变
    SEED_YELLOW = "seed_yellow"  # 瘟疫畸变
    SEEDLING_BLACK = "seedling_black"  # 未完成的畸变
    SEEDLING_RED = "seedling_red"  # 未完成的畸变
    SEEDLING_PURPLE = "seedling_purple"  # 未完成的畸变
    SEEDLING_YELLOW = "seedling_yellow"  # 未完成的畸变
    SEEDLING_GREY = "seedling_grey"  # 未完成的畸变
    SPROUT = "sprout"  # 焦点怪
    COM_CROCODILE = "com_crocodile"  # 鳄鱼
    COM_BULRUSH = "com_bulrush"  # 灯心草
    COM_CATTAIL = "com_cattail"  # 香蒲


class HeroClass(Enum):
    CRUSADER = "crusader"  # 十字军
    BOUNTY_HUNTER = "bounty_hunter"  # 赏金猎人
    VESTAL = "vestal"  # 修女
    PLAGUE_DOCTOR = "plague_doctor"  # 瘟疫医生
    GRAVE_ROBBER = "grave_robber"  # 盗墓贼
    OCCULTIST = "occultist"  # 神秘学者
    HIGHWAYMAN = "highwayman"  # 强盗
    HELLION = "hellion"  # 蛮族战士
    JESTER = "jester"  # 小丑
    LEPER = "leper"  # 麻风剑客
    ARBALEST = "arbalest"  # 弩手
    MAN_AT_ARMS = "man_at_arms"  # 老兵
    HOUNDMASTER = "houndmaster"  # 驯犬师
    ABOMINATION = "abomination"  # 咒缚者
    ANTIQUARIAN = "antiquarian"  # 古董商人
    MUSKETEER = "musketeer"  # 火枪手
    SHIELDBREAKER = "shieldbreaker"  # 破盾者
    FLAGELLANT = "flagellant"  # 苦修


class ItemType(Enum):
    GEM = "gem"  # 宝石
    GOLD = "gold"  # 金币
    HEIRLOOM = "heirloom"  # 祖产
    SUPPLY = "supply"  # 补给
    PROVISION = "provision"  # 食物
    QUEST_ITEM = "quest_item"  # 任务物品
    ROPE = "rope"  # 绳索，游戏中似乎没见过
    ESTATE = "estate"  # 战利品，类似蛇鳞、庭院邀请函这种道具
    ESTATE_CURRENCY = "estate_currency"  # 重要战利品，目前只在庭院中出现，男爵、子爵、伯爵夫人的邀请函
    TRINKET = "trinket"  # 饰品
    TRINKET_UNLOCK = "trinket_unlock"  # 特殊饰品，目前只有焮炙护符属于此类
    JEWELLERY = "jewellery"  # 珠宝，这个分类不知是否真实存在，在汉化文件中只出现过一次 jewellerybronze_necklace


class ItemID(Enum):
    GEM_ANCIENT_IDOL = "ancient_idol"  # 黄麻挂毯
    GEM_ANTIQRELIC = "antiqrelic"  # 稀有古董
    GEM_ANTIQRELICSMALL = "antiqrelicsmall"  # 小古董
    GEM_CITRINE = "citrine"  # 黄水晶
    GEM_EMERALD = "emerald"  # 绿宝石
    GEM_JADE = "jade"  # 翡翠
    GEM_ONYX = "onyx"  # 玛瑙
    GEM_PEWRELIC = "pewrelic"  # 神圣的板凳碎片
    GEM_RUBY = "ruby"  # 红宝石
    GEM_SAPPHIRE = "sapphire"  # 蓝宝石
    GEM_TRAPEZOHEDRON = "trapezohedron"  # 谜一般的多方晶体

    HEIRLOOM_BUST = "bust"  # 雕像
    HEIRLOOM_CREST = "crest"  # 纹章
    HEIRLOOM_DEED = "deed"  # 地契
    HEIRLOOM_PORTRAIT = "portrait"  # 画像
    HEIRLOOM_URN = "urn"  # 先祖的瓮
    HEIRLOOM_BLUEPRINT = "blueprint"  # 蓝图
    HEIRLOOM_MEMORY = "memory"  # 记忆

    SUPPLY_ANTIVENOM = "antivenom"  # 解毒剂
    SUPPLY_BANDAGE = "bandage"  # 绷带
    SUPPLY_DOG_TREATS = "dog_treats"  # 狗粮
    SUPPLY_FIREWOOD = "firewood"  # 木柴
    SUPPLY_HOLY_WATER = "holy_water"  # 圣水
    SUPPLY_LAUDANUM = "laudanum"  # 鸦片酊
    SUPPLY_MEDICINAL_HERBS = "medicinal_herbs"  # 药草
    SUPPLY_ROPE = "rope"  # 绳索
    SUPPLY_SHOVEL = "shovel"  # 铁铲
    SUPPLY_SKELETON_KEY = "skeleton_key"  # 万能钥匙
    SUPPLY_TORCH = "torch"  # 火把
    SUPPLY_SPICE = "spice"  # 碎片尘埃

    QUEST_ITEM_ANCESTOR_PORTRAIT = "ancestor_portrait"  # 先祖的肖像画
    QUEST_ITEM_ANCESTORS_CRATE = "ancestors_crate"  # 先祖的遗物
    QUEST_ITEM_ANTIVENOM = "antivenom"  # 强力消毒剂 [任务物品]
    QUEST_ITEM_BEACON_LIGHT = "beacon_light"  # 赞颂之手
    QUEST_ITEM_ELDRITCH_LANTERN = "eldritch_lantern"  # 松果状的腺体 [任务物品]
    QUEST_ITEM_GRAIN_SACK = "grain_sack"  # 谷物袋
    QUEST_ITEM_HOLY_RELIC = "holy_relic"  # 神圣的遗物
    QUEST_ITEM_HOLY_WATER = "holy_water"  # 神圣精华 [任务物品]
    QUEST_ITEM_MEDICINES = "medicines"  # 药物
    QUEST_ITEM_PICKAXE = "pickaxe"  # 鹤嘴锄 [任务物品]
    QUEST_ITEM_KEY1 = "key1"  # 愤怒之匙（红色）
    QUEST_ITEM_KEY2 = "key2"  # 歉疚之匙（黄色）
    QUEST_ITEM_KEY3 = "key3"  # 背弃之匙（绿色）
    QUEST_ITEM_KEY4 = "key4"  # 反思之匙（蓝色）
    QUEST_ITEM_TORCH_QUEST = "torch_quest"  # 速燃火把

    ESTATE_CRIMSON_COURT_INVITATION = "crimson_court_invitation"  # 邀请函
    ESTATE_THE_BLOOD = "the_blood"  # 血酿
    ESTATE_THE_CURE = "the_cure"  # 解药
    ESTATE_SNAKE_SCALE = "snake_scale"  # 护体之鳞

    ESTATE_CURRENCY_CRIMSON_COURT_INVITATION_A = "crimson_court_invitation_A"  # 男爵的邀请函
    ESTATE_CURRENCY_CRIMSON_COURT_INVITATION_B = "crimson_court_invitation_B"  # 子爵的邀请函
    ESTATE_CURRENCY_CRIMSON_COURT_INVITATION_C = "crimson_court_invitation_C"  # 伯爵夫人的邀请函

    JEWELLERY_BRONZE_NECKLACE = "bronze_necklace"  # 青铜项链


class TrinketID(Enum):
    # 本体
    DD_TRINKET = "dd_trinket"  # 焮炙护符

    ACCURACY_STONE = "accuracy_stone"  # 命中魔石
    AGILE_TALON = "agile_talon"  # 敏捷之爪
    AGILITY_WHISTLE = "agility_whistle"  # 迅捷尖哨
    ANCESTORS_BOTTLE = "ancestors_bottle"  # 先祖的药瓶
    ANCESTORS_CANDLE = "ancestors_candle"  # 先祖的蜡烛
    ANCESTORS_COAT = "ancestors_coat"  # 先祖的外套
    ANCESTORS_HANDKERCHIEF = "ancestors_handkerchief"  # 先祖的手帕
    ANCESTORS_LANTERN = "ancestors_lantern"  # 先祖的灯笼
    ANCESTORS_MAP = "ancestors_map"  # 先祖的地图
    ANCESTORS_MOUSTACHE_CREAM = "ancestors_moustache_cream"  # 先祖的刮胡膏
    ANCESTORS_MUSKET_BALL = "ancestors_musket_ball"  # 先祖的弹丸
    ANCESTORS_PEN = "ancestors_pen"  # 先祖的蘸水笔
    ANCESTORS_PISTOL = "ancestors_pistol"  # 先祖的手枪
    ANCESTORS_PORTRAIT = "ancestors_portrait"  # 先祖的肖像画
    ANCESTORS_SCROLL = "ancestors_scroll"  # 先祖的卷轴
    ANCESTORS_SHOVEL = "ancestors_shovel"  # 先祖的铁铲
    ANCESTORS_SIGNET_RING = "ancestors_signet_ring"  # 先祖的家印戒指
    ANCESTORS_TENTACLE_IDOL = "ancestors_tentacle_idol"  # 先祖的触须魔偶
    ANTIQ_1 = "antiq_1"  # 弹珠袋子
    ANTIQ_2 = "antiq_2"  # 血课奖章
    ANTIQ_3 = "antiq_3"  # 甲壳圣像
    ANTIQ_4 = "antiq_4"  # 舰队弗罗林
    ANTIQ_5 = "antiq_5"  # 生命之烛
    ARCHERS_RING = "archers_ring"  # 射手戒指
    BEAST_SLAYERS_RING = "beast_slayers_ring"  # 野兽克星戒指
    BERSERK_CHARM = "berserk_charm"  # 狂暴吊坠
    BERSERK_MASK = "berserk_mask"  # 狂暴面具
    BLASPHEMOUS_VIAL = "blasphemous_vial"  # 亵渎魔瓶
    BLEED_AMULET = "bleed_amulet"  # 鲜血项链
    BLEED_CHARM = "bleed_charm"  # 血腥挂坠
    BLEED_STONE = "bleed_stone"  # 流血魔石
    BLEEDING_PENDANT = "bleeding_pendant"  # 流血吊坠
    BLIGHT_AMULET = "blight_amulet"  # 蚀毒项链
    BLIGHT_CHARM = "blight_charm"  # 抗毒挂坠
    BLIGHT_STONE = "blight_stone"  # 中毒魔石
    BLOOD_CHARM = "blood_charm"  # 血腥挂坠
    BLOODIED_FETISH = "bloodied_fetish"  # 染血玩偶
    BLOODTHIRST_RING = "bloodthirst_ring"  # 渴血之戒
    BLOODY_DICE = "bloody_dice"  # 血腥骰子
    BLOODY_HERB = "bloody_herb"  # 血腥毒草
    BOOK_OF_CONSTITUTION = "book_of_constitution"  # 构造之书
    BOOK_OF_HOLINESS = "book_of_holiness"  # 圣洁之书
    BOOK_OF_HOLY_HEALING = "book_of_holy_healing"  # 治疗圣典
    BOOK_OF_INTUITION = "book_of_intuition"  # 直觉之书
    BOOK_OF_RAGE = "book_of_rage"  # 愤怒之书
    BOOK_OF_RELAXATION = "book_of_relaxation"  # 安神之书
    BOOK_OF_SANITY = "book_of_sanity"  # 理智之书
    BOSS_CANNON = "boss_cannon"  # 点火人的引燃棒
    BOSS_CREW = "boss_crew"  # 船长的铃铛
    BOSS_FLESH = "boss_flesh"  # 血肉之心
    BOSS_HAG = "boss_hag"  # 巫婆的汤勺
    BOSS_NECROMANCER = "boss_necromancer"  # 死灵法师的尖领
    BOSS_PROPHET = "boss_prophet"  # 先知的眼睛
    BOSS_SIREN = "boss_siren"  # 塞壬的螺号
    BOSS_TASSLE = "boss_tassle"  # “头狼”挂坠
    BOSS_WILBUR = "boss_wilbur"  # 威利伯的旗帜
    BRAWLERS_GLOVES = "brawlers_gloves"  # 斗士手套
    BRIGHT_TAMBOURINE = "bright_tambourine"  # 光明手鼓
    BULLS_EYE_BANDANA = "bulls_eye_bandana"  # 标靶头巾
    BULLS_EYE_HAT = "bulls_eye_hat"  # 靶心帽子
    CALMING_CRYSTAL = "calming_crystal"  # 安定水晶
    CAMOUFLAGE_CLOAK = "camouflage_cloak"  # 伪装斗篷
    CAMPERS_HELMET = "campers_helmet"  # 营寨头盔
    CANNON_5 = "cannon_5"  # 塞壬的螺号
    CAUTION_CLOAK = "caution_cloak"  # 警戒斗篷
    CHIRURGEONS_CHARM = "chirurgeons_charm"  # 医者挂坠
    CLEANSING_CRYSTAL = "cleansing_crystal"  # 净化水晶
    CLEANSING_EYEPATCH = "cleansing_eyepatch"  # 纯净眼罩
    COLLECTOR_1 = "collector_1"  # 迪斯马的头颅
    COLLECTOR_2 = "collector_2"  # 巴利斯坦的头颅
    COLLECTOR_3 = "collector_3"  # 朱妮娅的头颅
    COMMANDERS_ORDERS = "commanders_orders"  # 军令状
    CREST_OF_1100 = "crest_of_1100"  # 1100的胸章
    CREST_OF_THE_1100 = "crest_of_the_1100"  # 1100的胸章
    CREW_5 = "crew_5"  # 船长的铃铛
    CRITICAL_DICE = "critical_dice"  # 暴击骰子
    CRITICAL_STONE = "critical_stone"  # 暴击魔石
    CROW_EYE = "crow_eye"  # 膨胀的鸦眼
    CROW_TAILFEATHER = "crow_tailfeather"  # 褪落的尾翼
    CROW_TALON = "crow_talon"  # 结痂的鸦爪
    CROW_WINGFEATHER = "crow_wingfeather"  # 褪落的翼羽
    CUDGEL_WEIGHT = "cudgel_weight"  # 警署闷棍
    CURSED_BUCKLE = "cursed_buckle"  # 坚定带扣
    CURSED_INCENSE = "cursed_incense"  # 诅咒焚香
    DAMAGE_STONE = "damage_stone"  # 伤害魔石
    DARK_BRACER = "dark_bracer"  # 暗黑护腕
    DARK_CROWN = "dark_crown"  # 暗黑王冠
    DARK_TAMBOURINE = "dark_tambourine"  # 黑暗手鼓
    DAZZLING_CHARM = "dazzling_charm"  # 闪亮挂坠
    DEBUFF_AMULET = "debuff_amulet"  # 衰弱项链
    DEBUFF_CHARM = "debuff_charm"  # 避邪挂坠
    DEBUFF_STONE = "debuff_stone"  # 减益魔石
    DEFENDERS_SEAL = "defenders_seal"  # 防御印记
    DEMONS_CAULDRON = "demons_cauldron"  # 恶魔坩埚
    DETERIORATING_BRACER = "deteriorating_bracer"  # 恶化护腕
    DISEASE_CHARM = "disease_charm"  # 瘟疫护坠
    DISEASED_HERB = "diseased_herb"  # 抗病香草
    DODGE_STONE = "dodge_stone"  # 闪避魔石
    DODGY_SHEATH = "dodgy_sheath"  # 狡诈剑鞘
    DOUBLE_EDGED_PENDANT = "double_edged_pendant"  # 双刃吊坠
    DRIFTERS_BUCKLE = "drifters_buckle"  # 流浪汉的皮带扣
    ELDRITCH_KILLING_INCENSE = "eldritch_killing_incense"  # 诛魔焚香
    ELDRITCH_SLAYERS_RING = "eldritch_slayers_ring"  # 异魔克星戒指
    EVASION_INCENSE = "evasion_incense"  # 闪避熏香
    FASTING_SEAL = "fasting_seal"  # 斋戒徽记
    FEATHER_CRYSTAL = "feather_crystal"  # 轻羽水晶
    FLASHFIRE_GUNPOWDER = "flashfire_gunpowder"  # 速燃火药
    FLESH_5 = "flesh_5"  # 土匪的点火棍
    FOCUS_RING = "focus_ring"  # 专注戒指
    FORTUNATE_ARMLET = "fortunate_armlet"  # 幸运臂环
    GAMBLERS_CHARM = "gamblers_charm"  # 赌徒挂坠
    GUARDIANS_SHIELD = "guardians_shield"  # 守卫盾牌
    HAG_5 = "hag_5"  # 威尔伯的旗帜
    HASTE_CHALICE = "haste_chalice"  # 迅捷圣杯
    HEALING_ARMLET = "healing_armlet"  # 治疗臂章
    HEALTH_STONE = "health_stone"  # 生命魔石
    HEAVENS_HAIRPIN = "heavens_hairpin"  # 天堂发髻
    HEAVY_BOOTS = "heavy_boots"  # 沉重长靴
    HELLS_HAIRPIN = "hells_hairpin"  # 地狱发髻
    HEROS_RING = "heros_ring"  # 英雄戒指
    HOLY_ORDERS = "holy_orders"  # 神圣祷文
    HUNTERS_TALON = "hunters_talon"  # 猎手之爪
    IMMUNITY_MASK = "immunity_mask"  # 免疫面具
    KNIGHTS_CREST = "knights_crest"  # 骑士饰章
    LEGENDARY_BRACER = "legendary_bracer"  # 传奇护腕
    LIFE_CRYSTAL = "life_crystal"  # 生命水晶
    LONGEVITY_EYEPATCH = "longevity_eyepatch"  # 强壮眼罩
    LUCKY_DICE = "lucky_dice"  # 幸运骰子
    LUCKY_TALISMAN = "lucky_talisman"  # 幸运护符
    MADMAN_1 = "madman_1"  # 叹咏乐盒
    MADMAN_2 = "madman_2"  # 序曲乐盒
    MADMAN_3 = "madman_3"  # 渐响乐盒
    MAN_SLAYERS_RING = "man_slayers_ring"  # 人类克星戒指
    MARTYRS_SEAL = "martyrs_seal"  # 殉道者徽记
    MEDICS_BOOTS = "medics_boots"  # 医疗之靴
    MEDICS_GREAVES = "medics_greaves"  # 治疗护胫
    MOON_CLOAK = "moon_cloak"  # 月光斗篷
    MOON_RING = "moon_ring"  # 月光戒指
    MOVE_AMULET = "move_amulet"  # 错位项链
    MOVE_CHARM = "move_charm"  # 错位挂坠
    MOVE_STONE = "move_stone"  # 位移魔石
    NECROMANCER_5 = "necromancer_5"  # 死灵法师的尖领
    PADLOCK_1 = "padlock_1"  # 耐心枷锁
    PADLOCK_2 = "padlock_2"  # 变身枷锁
    PADLOCK_3 = "padlock_3"  # 守护枷锁
    PADLOCK_4 = "padlock_4"  # 狂怒枷锁
    PADLOCK_5 = "padlock_5"  # 抑制枷锁
    PARALYZERS_CREST = "paralyzers_crest"  # 制裁饰章
    POISONED_HERB = "poisoned_herb"  # 剧毒草药
    POISONING_BUCKLE = "poisoning_buckle"  # 强盗的皮带扣
    PROFANE_SCROLL = "profane_scroll"  # 亵圣卷轴
    PROPHET_5 = "prophet_5"  # 巫婆的汤勺
    PROTECTION_STONE = "protection_stone"  # 防御魔石
    PROTECTIVE_COLLAR = "protective_collar"  # 防护项圈
    QUICK_DRAW_CHARM = "quick_draw_charm"  # 先行挂坠
    QUICKENING_SATCHEL = "quickening_satchel"  # 迅捷背包
    RAIDERS_TALISMAN = "raiders_talisman"  # 摸金符
    RAMPART_SHIELD = "rampart_shield"  # 防壁巨盾
    RECKLESS_CHARM = "reckless_charm"  # 蛮力挂坠
    RECOVERY_CHALICE = "recovery_chalice"  # 贞洁圣杯
    RECOVERY_CHARM = "recovery_charm"  # 恢复挂坠
    ROTGUT_CENSER = "rotgut_censer"  # 腐烂香炉
    SACRED_SCROLL = "sacred_scroll"  # 神圣卷轴
    SACRIFICIAL_CAULDRON = "sacrificial_cauldron"  # 献祭坩埚
    SCOUTING_WHISTLE = "scouting_whistle"  # 侦察尖哨
    SEER_STONE = "seer_stone"  # 贤者之石
    SEERS_SATCHEL = "seers_satchel"  # 恶毒背包
    SELFISH_ARMLET = "selfish_armlet"  # 救赎臂章
    SELFISH_PENDANT = "selfish_pendant"  # 自私吊坠
    SHARPENING_SHEATH = "sharpening_sheath"  # 锋利的剑鞘
    SHIMMERING_CLOAK = "shimmering_cloak"  # 闪烁斗篷
    SIREN_5 = "siren_5"  # 血肉之心
    SLIPPERY_BOOTS = "slippery_boots"  # 光滑长靴
    SLY_EYEPATCH = "sly_eyepatch"  # 狡诈眼罩
    SNAKE_OIL = "snake_oil"  # 蛇油
    SNIPERS_RING = "snipers_ring"  # 狙击戒指
    SOLAR_BRACER = "solar_bracer"  # 光明护腕
    SOLAR_CROWN = "solar_crown"  # 光明王冠
    SPEED_STONE = "speed_stone"  # 速度魔石
    SPIKED_COLLAR = "spiked_collar"  # 尖刺项圈
    STEADY_BRACER = "steady_bracer"  # 稳固护腕
    STUN_AMULET = "stun_amulet"  # 眩晕项链
    STUN_CHARM = "stun_charm"  # 眩晕挂坠
    STUN_STONE = "stun_stone"  # 眩晕魔石
    STUNNING_SATCHEL = "stunning_satchel"  # 厌物背包
    STURDY_BOOTS = "sturdy_boots"  # 强壮之靴
    STURDY_GREAVES = "sturdy_greaves"  # 稳固护胫
    SUN_CLOAK = "sun_cloak"  # 日光斗篷
    SUN_RING = "sun_ring"  # 日光戒指
    SURGICAL_GLOVE = "surgical_glove"  # 手术手套
    SURVIVAL_GUIDE = "survival_guide"  # 生存指南
    SWIFT_CLOAK = "swift_cloak"  # 迅捷斗篷
    SWORDSMANS_CREST = "swordsmans_crest"  # 剑士饰章
    TENACITY_RING = "tenacity_ring"  # 坚韧戒指
    TOUGH_RING = "tough_ring"  # 强韧戒指
    UNHOLY_SLAYERS_RING = "unholy_slayers_ring"  # 邪秽克星戒指
    UNMOVABLE_HELMET = "unmovable_helmet"  # 稳固头盔
    VENGEFUL_BOOTS = "vengeful_boots"  # 复仇之靴
    VENGEFUL_GREAVES = "vengeful_greaves"  # 复仇护胫
    WARRIORS_BRACER = "warriors_bracer"  # 勇士护腕
    WARRIORS_CAP = "warriors_cap"  # 勇士头盔
    WILBUR_5 = "wilbur_5"  # 先知的眼球
    WITCHS_VIAL = "witchs_vial"  # 巫师药瓶
    WORRYSTONE = "worrystone"  # 忘忧石
    WOUNDING_HELMET = "wounding_helmet"  # 嗜戮头盔
    WRATHFUL_BANDANA = "wrathful_bandana"  # 愤怒头巾
    WRATHFUL_HAT = "wrathful_hat"  # 暴怒帽子
    YOUTH_CHALICE = "youth_chalice"  # 青春圣杯

    # 庭院 DLC
    AMULET_OF_ANNOYANCE = "amulet_of_annoyance"  # 恼怒挂坠
    CC_BOSS_BARON = "cc_boss_baron"  # 男爵的鞭子
    CC_BOSS_COUNTESS = "cc_boss_countess"  # 伯爵夫人的扇子
    CC_BOSS_VISCOUNT = "cc_boss_viscount"  # 子爵的香料
    CC_COVEN_SIGNET = "cc_coven_signet"  # 宴会图章
    CC_CRIMSON_TINCTURE = "cc_crimson_tincture"  # 先祖的佳酿
    CC_CRYSTAL_SNIFTER = "cc_crystal_snifter"  # 猩红鼻烟
    CC_DAZZLING_MIRROR = "cc_dazzling_mirror"  # 耀眼的镜子
    CC_MANTRA_OF_FASTING = "cc_mantra_of_fasting"  # 斋戒符咒
    CC_PAGAN_TALISMAN = "cc_pagan_talisman"  # 渎神符饰
    CC_QUICKSILVER_SALVE = "cc_quicksilver_salve"  # 水银药膏
    CC_RAT_CARCASS = "cc_rat_carcass"  # 老鼠的遗骸
    CC_SCULPTORS_TOOLS = "cc_sculptors_tools"  # 雕塑家的工具
    CC_SET_ABOM_SHAMEFUL_SHROUD = "cc_set_abom_shameful_shroud"  # 屈辱披风
    CC_SET_ABOM_WROUGHT_OSMOND_CHAINS = "cc_set_abom_wrought_osmond_chains"  # 神护锁链
    CC_SET_ANTI_THE_MASTERS_ESSENCE = "cc_set_anti_the_masters_essence"  # 主人的精华
    CC_SET_ANTI_TWO_OF_THE_THREE = "cc_set_anti_two_of_the_three"  # 三相之二
    CC_SET_ARB_CHILDHOOD_TREASURE = "cc_set_arb_childhood_treasure"  # 童年的宝藏
    CC_SET_ARB_SHARPSHOOTERS_STRING_WAX = "cc_set_arb_sharpshooters_string_wax"  # 睡前故事
    CC_SET_BH_CRIME_LORDS_MOLARS = "cc_set_bh_crime_lords_molars"  # 黑道老大的臼齿
    CC_SET_BH_VOW_OF_REVENGE = "cc_set_bh_vow_of_revenge"  # 充满仇恨的杀戮名单
    CC_SET_CRU_GLITTERING_SPAULDERS = "cc_set_cru_glittering_spaulders"  # 闪亮的肩甲
    CC_SET_CRU_SIGNED_CONSCRIPTION = "cc_set_cru_signed_conscription"  # 签署的动员章
    CC_SET_FLAG_CHIPPED_TOOTH = "cc_set_flag_chipped_tooth"  # 断裂的牙齿
    CC_SET_FLAG_SHARD_OF_GLASS = "cc_set_flag_shard_of_glass"  # 玻璃碎片
    CC_SET_GR_ABSINTHE = "cc_set_gr_absinthe"  # 苦艾酒
    CC_SET_GR_SHARPENED_LETTER_OPENER = "cc_set_gr_sharpened_letter_opener"  # 锋利的开信刀
    CC_SET_HEL_LIONESS_WARPAINT = "cc_set_hel_lioness_warpaint"  # 雌狮战痕
    CC_SET_HEL_MARK_OF_THE_OUTCAST = "cc_set_hel_mark_of_the_outcast"  # 放逐印记
    CC_SET_HIGH_BLOODIED_NECKERCHIEF = "cc_set_high_bloodied_neckerchief"  # 染血围巾
    CC_SET_HIGH_SHAMEFUL_LOCKET = "cc_set_high_shameful_locket"  # 羞耻吊坠
    CC_SET_HM_DAMNING_EVIDENCE = "cc_set_hm_damning_evidence"  # 腐败之证
    CC_SET_HM_LAWMANS_BADGE = "cc_set_hm_lawmans_badge"  # 破损警章
    CC_SET_JEST_TASTING_CUP = "cc_set_jest_tasting_cup"  # 暴君的品酒杯
    CC_SET_JEST_TYRANTS_FINGERBONE = "cc_set_jest_tyrants_fingerbone"  # 暴君的指骨
    CC_SET_LEP_LAST_WILL_AND_TESTAMENT = "cc_set_lep_last_will_and_testament"  # 临终遗嘱
    CC_SET_LEP_TIN_FLUTE = "cc_set_lep_tin_flute"  # 长笛
    CC_SET_MAA_OLD_UNIT_BANNER = "cc_set_maa_old_unit_banner"  # 旧役旗标
    CC_SET_MAA_TOY_SOLDIER = "cc_set_maa_toy_soldier"  # 玩具士兵
    CC_SET_MUSK_FIRST_PLACE_TROPHY = "cc_set_musk_first_place_trophy"  # 次等奖杯
    CC_SET_MUSK_SILVER_BULLET = "cc_set_musk_silver_bullet"  # 银制枪弹
    CC_SET_OCC_BLOOD_PACT = "cc_set_occ_blood_pact"  # 血之契约
    CC_SET_OCC_VIAL_OF_SAND = "cc_set_occ_vial_of_sand"  # 一瓶黄沙
    CC_SET_PD_CODEX_OF_PLAGUES = "cc_set_pd_codex_of_plagues"  # 第40号实验的记录
    CC_SET_PD_DISSECTION_KIT = "cc_set_pd_dissection_kit"  # 解剖工具
    CC_SET_VEST_ATONEMENT_BEADS = "cc_set_vest_atonement_beads"  # 赎罪念珠
    CC_SET_VEST_SALACIOUS_DIARY = "cc_set_vest_salacious_diary"  # 背德日记
    FLAG_1 = "flag_1"  # 永恒领环
    FLAG_2 = "flag_2"  # 苦难领环
    FLAG_3 = "flag_3"  # 惩罚头巾
    FLAG_4 = "flag_4"  # 复生领环
    FLAG_5 = "flag_5"  # 裂心头巾
    SHIELD_OF_SHOCKING = "shield_of_shocking"  # 震撼盾牌

    # 农场 DLC
    COM_HEL_THIRSTING_BLADE = "com_hel_thirsting_blade"  # 嗜血之刃
    COM_ARB_KEENING_BOLTS = "com_arb_keening_bolts"  # 锐利箭矢
    COM_MSK_ICOSAHEDRIC_BALLS = "com_msk_icosahedric_balls"  # 超级火枪子弹
    COM_ANT_SMOKING_SKULL = "com_ant_smoking_skull"  # 冒烟颅骨
    COM_PD_ASHEN_DISTILLATION = "com_pd_ashen_distillation"  # 尘埃蒸馏
    COM_VES_HERETICAL_PASSAGES = "com_ves_heretical_passages"  # 异教文章
    COM_CRU_NON_EUCLIDEAN_HILT = "com_cru_non_euclidean_hilt"  # 非欧刀柄
    COM_MAA_MIRROR_SHIELD = "com_maa_mirror_shield"  # 镜罩
    COM_OCC_ELDER_SIGN = "com_occ_elder_sign"  # 石化颅骨
    COM_LENS_OF_COMET = "com_lens_of_comet"  # 彗星透镜
    COM_MILDREDSLOCKET = "com_mildredslocket"  # 米尔德里德的吊坠
    COM_BH_MASK_OF_TIMELESS = "com_bh_mask_of_timeless"  # 永恒面具
    COM_HWY_CRYSTALLINE_GUNPOWDER = "com_hwy_crystalline_gunpowder"  # 晶体火药
    COM_LEP_CRYSTALIZED_AMULET = "com_lep_crystalized_amulet"  # 石化护身符
    COM_SB_SPECTRAL_SPEARTIP = "com_sb_spectral_speartip"  # 幽灵矛尖
    COM_HND_HUSKFANG_WHISTLE = "com_hnd_huskfang_whistle"  # 瘪牙尖哨
    COM_FLAG_ACIDIC_HUSK_ICHOR = "com_flag_acidic_husk_ichor"  # 酸性灵液
    COM_COMET_CLUSTER_PENDANT = "com_comet_cluster_pendant"  # 水晶簇吊坠
    COM_JES_DIRGE_FOR_DEVOURED = "com_jes_dirge_for_devoured"  # 吞噬者挽歌
    COM_ABOM_BROKEN_KEY = "com_abom_broken_key"  # 破损钥匙
    COM_GRV_HUSKCLAW_TOXIN = "com_grv_huskclaw_toxin"  # 珍贵药剂
    COM_COMET_SEED_PENDANT = "com_comet_seed_pendant"  # 水晶吊坠
    COM_MILLERS_PIPE = "com_millers_pipe"  # 磨坊主的烟斗
    COM_COAT_MANY_COLOURS = "com_coat_many_colours"  # 彩色外套
    COM_PRISMATIC_HEART_CRYSTAL = "com_prismatic_heart_crystal"  # 棱镜心形水晶
    COM_THING_FANG = "com_thing_fang"  # 怪物的水晶牙
    COM_THING_HIDE = "com_thing_hide"  # 怪物相移皮肤
    COM_THING_EYE = "com_thing_eye"  # 怪物迷人的眼睛

    # 破盾者 DLC
    SB_1 = "sb_1"  # 蛇毒之瓶
    SB_2 = "sb_2"  # 闪光蛇鳞
    SB_3 = "sb_3"  # 舞者的缠足布
    SB_4 = "sb_4"  # 利牙矛尖
    SB_5 = "sb_5"  # 坚皮衣甲
    SB_SET_1 = "sb_set_1"  # 黑耀石匕首
    SB_SET_2 = "sb_set_2"  # 被切断的手


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
    STRESS_DMG_RECEIVED_PERCENT = "stress_dmg_received_percent"  # 受到的压力伤害（百分比），如dd火炬：启示：-100%所受压力（实际上最低受压只能降低到-80%）
    STRESS_HEAL_PERCENT = "stress_heal_percent"  # 造成压力治疗效果（百分比）
    STRESS_HEAL_RECEIVED_PERCENT = "stress_heal_received_percent"  # 受到的压力治疗效果（百分比）
    PARTY_SURPRISE_CHANCE = "party_surprise_chance"  # 队伍惊慌概率（百分比）
    MONSTERS_SURPRISE_CHANCE = "monsters_surprise_chance"  # 怪物惊慌概率（百分比）
    AMBUSH_CHANCE = "ambush_chance"  # 夜袭概率（百分比）
    SCOUTING_CHANCE = "scouting_chance"  # 侦查概率（百分比）
    STARVING_DAMAGE_PERCENT = "starving_damage_percent"  # 挨饿时受到的伤害（百分比）
    UPGRADE_DISCOUNT = "upgrade_discount"  # 被称为【打折】类buff，因为其作用是在进行装备和技能升级时打折
    DAMAGE_RECEIVED_PERCENT = "damage_received_percent"  # 受到的伤害（百分比），俗称“硬减伤”（相对于防御的减伤而言），如dd火炬：启示：-100%所受伤害（这个可以达到-100%的效果）
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
    GUARD_DURATION_RECEIVED_PERCENT = "guard_duration_received_percent"  # 守护所受时间改变（百分比）（仅对effect写法守护有效，不过buff写法守护本身也没有意义）
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


class SkillHeadType(Enum):
    SKILL = "skill"
    COMBAT_SKILL = "combat_skill"
    COMBAT_MOVE_SKILL = "combat_move_skill"
    RIPOSTE_SKILL = "riposte_skill"


class TagID(Enum):
    BOSS = "boss"
    LIGHT = "light"
    HEAVY = "heavy"
    RELIGIOUS = "religious"
    NON_RELIGIOUS = "non-religious"
    HOUSE_OF_THE_YELLOW_HAND = "house_of_the_yellow_hand"
    TRAINING_RING = "training_ring"
    LIBRARY = "library"
    OUTSIDERS_BONFIRE = "outsiders_bonfire"


class DeathFx(Enum):
    DEATH_SMALL = "death_small"
    DEATH_MEDIUM = "death_medium"
    DEATH_LARGE = "death_large"
    DEATH_LARGE_BOSS = "death_large_boss"
    DEATH_CORPSE_MEDIUM = "death_corpse_medium"


class TrinketRarityType(Enum):
    DARKEST_DUNGEON = "darkest_dungeon"  # 极暗地牢	DD1任务奖励（火炬）
    TROPHY = "trophy"  # 猎获	冠军boss任务必得（好像每个boss只能拿一个）
    ANCESTRAL_SHAMBLER = "ancestral_shambler"  # 先祖（跛行者）	击败跛行者
    ANCESTRAL = "ancestral"  # 先祖	大型冠军本任务必得或庭院高级本乞丐概率获得
    CROW = "crow"  # 乌鸦	尖叫魔事件获得（死亡丢失8饰品不算）
    COURTIER = "courtier"  # 骸骨官僚	大型本骸骨官僚极低概率掉落（好像是个大酒杯？）
    COLLECTOR = "collector"  # 收藏家	收藏家概率掉落或密门宝箱概率掉落（头颅系列）
    MADMAN = "madman"  # 疯子	任何难度下疯子极小概率掉落（八音盒系列）
    KICKSTARTER = "kickstarter"  # 赞助者	代码输入获得
    VERY_RARE = "very_rare"  # 非常稀有	这都快烂大街了就不用问了吧。。。
    RARE = "rare"  # 稀有
    UNCOMMON = "uncommon"  # 优良
    COMMON = "common"  # 普通
    VERY_COMMON = "very_common"
    COMET = "comet"  # 水晶	水晶商店购买
    MILDRID = "mildred"  # 米尔德里德	农场主妻子赠送（就是那个吊坠）
    THING = "thing"  # 星空	星空怪极低概率掉落（反正我一个都没刷出来过）
    CRIMSON_COURT = "crimson_court"  # 猩红庭院	庭院任务、庭院宝箱、庭院boss必掉


class TrinketAwardCategory(Enum):
    DD = "dd"  # 极暗地牢	不要用这个
    TROPHY = "trophy"  # 奖品
    BATTLE = "battle"  # 战斗掉落	战斗以外的方式都不能获得
    UNIVERSAL = "universal"  # 多方式掉落	这个比较常用
    QUEST = "quest"  # 任务
    KICKSTARTER = "kickstarter"  # 输代码（这个我也不是很懂）


class LocalizationLanguage(Enum):
    ENGLISH = "english"  # 英语
    FRENCH = "french"  # 法国
    GERMAN = "german"  # 德国
    SPANISH = "spanish"  # 西班牙
    BRAZILIAN = "brazilian"  # 巴西
    RUSSIAN = "russian"  # 俄罗斯
    POLISH = "polish"  # 波兰
    CZECH = "czech"  # 捷克
    ITALIAN = "italian"  # 意大利
    SCHINESE = "schinese"  # 简体中文（中国）
    JAPANESE = "japanese"  # 日本
    KOREANB = "koreanb"  # 韩国（推测应为朝鲜语，但根据提供的信息保持原样）
    KOREANA = "koreana"  # 韩国


class InnerFx(Enum):
    ANIM_SNIPPETS = "anim_snippets"
    ANTIVENOM = "antivenom"
    ATTACK_OVERLAY = "attack_overlay"
    BANDAGE = "bandage"
    BLOOD_SPLATTER = "blood_splatter"
    BUILDING_UPGRADE_PULSE = "building_upgrade_pulse"
    CAMPFIRE = "campfire"
    CHARACTER_DISPLAY_FLESHLUMP = "character_display_fleshlump"
    COMBAT = "combat"
    CURE_TARGET = "cure_target"
    DEATH_CORPSE_MEDIUM = "death_corpse_medium"
    DEATH_LARGE = "death_large"
    DEATH_LARGE_BOSS = "death_large_boss"
    DEATH_MEDIUM = "death_medium"
    DEATH_SMALL = "death_small"
    DOG_TREATS = "dog_treats"
    DUNGEON_PROGRESS = "dungeon_progress"
    ESTATE_ACTIVITY_LOG = "estate_activity_log"
    ESTATE_DISTRICTS = "estate_districts"
    ESTATE_EXCLAMATION = "estate_exclamation"
    ESTATE_GLOSSARY = "estate_glossary"
    ESTATE_GOLD_PILE = "estate_gold_pile"
    ESTATE_HEIRLOOM_EXCHANGE = "estate_heirloom_exchange"
    ESTATE_REALM_INVENTORY = "estate_realm_inventory"
    ESTATE_SETTINGS = "estate_settings"
    ESTATE_TOWN_EVENT = "estate_town_event"
    FORMLESS_MUTATE = "formless_mutate"
    HALO = "halo"
    HOLY_WATER = "holy_water"
    INTERACTION_CURIO = "interaction_curio"
    LAUDANUM = "laudanum"
    MAP_RADAR = "map_radar"
    MARK_TARGET = "mark_target"
    MEDICINAL_HERBS = "medicinal_herbs"
    MONSTER_SPAWN = "monster_spawn"
    PARTY_COMBO = "party_combo"
    PURCHASE_DISTRICT = "purchase_district"
    QUEST_COMPLETE_CREST = "quest_complete_crest"
    QUEST_COMPLETE_SEAL = "quest_complete_seal"
    RAID_RESULTS_LOOT_GLOW = "raid_results_loot_glow"
    RAID_RESULTS_QUIRK_REVEAL = "raid_results_quirk_reveal"
    RAID_RESULTS_RESOLVE_PULSE = "raid_results_resolve_pulse"
    RED_HOOK_LOGO = "red_hook_logo"
    ROUND_INDICATOR = "round_indicator"
    SAVE_ENVELOPE = "save_envelope"
    SCOUT_HALLWAY = "scout_hallway"
    SCOUT_ROOM = "scout_room"
    SKILL_STRENGTH_PIP = "skill_strength_pip"
    STRESS_CLOUD = "stress_cloud"
    TITLES = "titles"
    TORCH = "torch"
    TORCH_FLAME = "torch_flame"
    TORCH_LOAD = "torch_load"
    TORCH_SPARKS = "torch_sparks"
    TOWN_ABBEY_LEVEL01 = "town_abbey_level01"
    TOWN_ABBEY_LEVEL02 = "town_abbey_level02"
    TOWN_ABBEY_LEVEL03 = "town_abbey_level03"
    TOWN_ABBEY_LOCKED = "town_abbey_locked"
    TOWN_BLACKSMITH_LEVEL01 = "town_blacksmith_level01"
    TOWN_BLACKSMITH_LEVEL02 = "town_blacksmith_level02"
    TOWN_BLACKSMITH_LEVEL03 = "town_blacksmith_level03"
    TOWN_BLACKSMITH_LOCKED = "town_blacksmith_locked"
    TOWN_CAMPING_TRAINER_LEVEL01 = "town_camping_trainer_level01"
    TOWN_CAMPING_TRAINER_LEVEL02 = "town_camping_trainer_level02"
    TOWN_CAMPING_TRAINER_LEVEL03 = "town_camping_trainer_level03"
    TOWN_CAMPING_TRAINER_LOCKED = "town_camping_trainer_locked"
    TOWN_CIRCUS_LEVEL01 = "town_circus_level01"
    TOWN_CIRCUS_LOCKED = "town_circus_locked"
    TOWN_EVENT_ABSENT_ABBOT = "town_event_absent_abbot"
    TOWN_EVENT_ALL_SAINTS_DAY = "town_event_all_saints_day"
    TOWN_EVENT_ARCHERY_TOURNEY = "town_event_archery_tourney"
    TOWN_EVENT_BONUS_RECRUITS = "town_event_bonus_recruits"
    TOWN_EVENT_BUMPER_CROP = "town_event_bumper_crop"
    TOWN_EVENT_BUSKING = "town_event_busking"
    TOWN_EVENT_CAREGIVERS_CONVENTION = "town_event_caregivers_convention"
    TOWN_EVENT_CELL_CLEANING = "town_event_cell_cleaning"
    TOWN_EVENT_DAY_OF_THE_DEAD = "town_event_day_of_the_dead"
    TOWN_EVENT_EAT_THE_RICH = "town_event_eat_the_rich"
    TOWN_EVENT_EMPTY_KEGS = "town_event_empty_kegs"
    TOWN_EVENT_GIBBOUS_MOON = "town_event_gibbous_moon"
    TOWN_EVENT_LABOUR_FORCE = "town_event_labour_force"
    TOWN_EVENT_LAUNDRY_DAY = "town_event_laundry_day"
    TOWN_EVENT_LAYING_LOW = "town_event_laying_low"
    TOWN_EVENT_MARDI_GRAS = "town_event_mardi_gras"
    TOWN_EVENT_MEDICAL_BREAKTHROUGH = "town_event_medical_breakthrough"
    TOWN_EVENT_MILITIA_TRAINING = "town_event_militia_training"
    TOWN_EVENT_NEW_SHIPMENT = "town_event_new_shipment"
    TOWN_EVENT_NOISY_REPAIRS = "town_event_noisy_repairs"
    TOWN_EVENT_NOMAD_NEW_YEAR = "town_event_nomad_new_year"
    TOWN_EVENT_RATS_AMONG_US = "town_event_rats_among_us"
    TOWN_EVENT_RAY_OF_SUNLIGHT = "town_event_ray_of_sunlight"
    TOWN_EVENT_ROBBERY = "town_event_robbery"
    TOWN_EVENT_THE_PLAGUE = "town_event_the_plague"
    TOWN_EVENT_TINKERS_DAY = "town_event_tinkers_day"
    TOWN_EVENT_TOWN_FAIR = "town_event_town_fair"
    TOWN_GRAVEYARD = "town_graveyard"
    TOWN_GROUND = "town_ground"
    TOWN_GUILD_LEVEL01 = "town_guild_level01"
    TOWN_GUILD_LEVEL02 = "town_guild_level02"
    TOWN_GUILD_LEVEL03 = "town_guild_level03"
    TOWN_GUILD_LOCKED = "town_guild_locked"
    TOWN_NOMAD_WAGON_LEVEL01 = "town_nomad_wagon_level01"
    TOWN_NOMAD_WAGON_LEVEL02 = "town_nomad_wagon_level02"
    TOWN_NOMAD_WAGON_LEVEL03 = "town_nomad_wagon_level03"
    TOWN_NOMAD_WAGON_LOCKED = "town_nomad_wagon_locked"
    TOWN_SANITARIUM_LEVEL01 = "town_sanitarium_level01"
    TOWN_SANITARIUM_LEVEL02 = "town_sanitarium_level02"
    TOWN_SANITARIUM_LEVEL03 = "town_sanitarium_level03"
    TOWN_SANITARIUM_LOCKED = "town_sanitarium_locked"
    TOWN_STAGE_COACH_LEVEL01 = "town_stage_coach_level01"
    TOWN_STAGE_COACH_LEVEL02 = "town_stage_coach_level02"
    TOWN_STAGE_COACH_LEVEL03 = "town_stage_coach_level03"
    TOWN_STATUE_LEVEL01 = "town_statue_level01"
    TOWN_STATUE_LEVEL02 = "town_statue_level02"
    TOWN_STATUE_LEVEL03 = "town_statue_level03"
    TOWN_TAVERN_LEVEL01 = "town_tavern_level01"
    TOWN_TAVERN_LEVEL02 = "town_tavern_level02"
    TOWN_TAVERN_LEVEL03 = "town_tavern_level03"
    TOWN_TAVERN_LOCKED = "town_tavern_locked"
    TRINKET_SPARKLE = "trinket_sparkle"
    WOOD_SPLINTER = "wood_splinter"


class QuirkClassification(Enum):
    PHYSICAL = "physical"
    MENTAL = "mental"


class CurioTag(Enum):
    # 本体
    NONE = "None"
    FOOD = "Food"
    UNHOLY = "Unholy"
    WORSHIP = "Worship"
    TREASURE = "Treasure"
    TORTURE = "Torture"
    ALL = "All"
    FOUNTAIN = "Fountain"
    REFLECTIVE = "Reflective"
    BODY = "Body"
    DRINK = "Drink"
    HAUNTED = "Haunted"
    # CC
    CCRAVE = "CCrave"


class QuirkTag(Enum):
    VAMPIRE = "vampire"
    VAMPIRE_PASSIVE = "vampire_passive"
    SINGLETON = "singleton"
    REMOVE_ON_DEATH = "remove_on_death"
    CANT_LOCK = "cant_lock"
    CONTAGIOUS_IMMUNE = "contagious_immune"


class CombatStartTurnActOuts(Enum):
    NOTHING = "nothing"
    BARK_STRESS = "bark_stress"
    CHANGE_POS = "change_pos"
    IGNORE_COMMAND = "ignore_command"
    RANDOM_COMMADN = "random_command"
    RETREAT_FROM_COMBAT = "retreat_from_combat"
    ATTACK_FRIENDLY = "attack_friendly"
    ATTACK_SELF = "attack_self"
    MARK_SELF = "mark_self"
    STRESS_HEAL_SELF = "stress_heal_self"
    STRESS_HEAL_PARTY = "stress_heal_party"
    BUFF_RANDOM_PARTY_MEMBER = "buff_random_party_member"
    BUFF_PARTY = "buff_party"
    HEAL_SELF = "heal_self"
    CONSUME_ITEM = "consume_item"


class ReactionActOuts(Enum):
    BLOCK_MOVE = "block_move"
    BLOCK_HEAL = "block_heal"
    BLOCK_BUFF = "block_buff"
    BLOCK_EFFECT = "block_effect"
    BLOCK_ITEM = "block_item"
    BLOCK_COMBAT_RETREAT = "block_combat_retreat"
    BLOCK_CAMPING_MEAL = "block_camping_meal"
    BLOCK_CAMPING_SKILL_PERFORMER = "block_camping_skill_performer"
    BLOCK_CAMPING_SKILL_TARGET = "block_camping_skill_target"
    COMMENT_SELF_HIT = "comment_self_hit"
    COMMENT_SELF_MISSED = "comment_self_missed"
    COMMENT_ALLY_HIT = "comment_ally_hit"
    COMMENT_ALLY_MISSED = "comment_ally_missed"
    COMMENT_ALLY_ATTACK_HIT = "comment_ally_attack_hit"
    COMMENT_ALLY_ATTACK_MISSED = "comment_ally_attack_missed"
    COMMENT_MOVE = "comment_move"
    COMMENT_CURIO_INTERACTION = "comment_curio_interaction"
    COMMENT_TRAP_TRIGGERED = "comment_trap_triggered"


class LootType(Enum):
    NOTHING = "nothing"
    ITEM = "item"
    TABLE = "table"
    JOURNAL_PAGE = "journal_page"


class ProjectVisibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    FRIENDS = "friends"


class ProjectUploadMode(Enum):
    DIRECT_UPLOAD = "direct_upload"
    COPY_AND_UPLOAD = "copy_and_upload"
    STRIP_AND_UPLOAD = "strip_and_upload"
    DONT_SUBMIT = "dont_submit"


class ProjectTag(Enum):
    GAMEPLAY_TWEAKS = "gameplay tweaks"
    OVERHAULS = "overhauls"
    TRINKETS = "trinkets"
    MONSTERS = "monsters"
    LOCALIZATION = "localization"
    UI = "ui"
    NEW_CLASS = "new class"
    CLASS_TWEAKS = "class tweaks"
    SKINS = "skins"


class CampingSkillEffectType(Enum):
    BUFF = "buff"
    HEALTH_HEAL_MAX_HEALTH_PERCENT = "health_heal_max_health_percent"
    HEALTH_DAMAGE_MAX_HEALTH_PERCENT = "health_damage_max_health_percent"
    STRESS_HEAL_AMOUNT = "stress_heal_amount"
    STRESS_DAMAGE_AMOUNT = "stress_damage_amount"
    REMOVE_BLEEDING = "remove_bleeding"
    REMOVE_POISON = "remove_poison"
    REMOVE_DEATHS_DOOR_RECOVERY_BUFFS = "remove_deaths_door_recovery_buffs"
    REMOVE_DISEASE = "remove_disease"
    REDUCE_TORCH = "reduce_torch"
    REDUCE_AMBUSH_CHANCE = "reduce_ambush_chance"
    LOOT = "loot"
    ITEM = "item"


class CampingSkillBuffSubType(Enum):
    CAMPING_PARTY_SURPRISE = "campingPartySurprise"
    CAMPING_MONSTERS_SURPRISE = "campingMonstersSurprise"
    CAMPING_SCOUTING_BUFF = "campingScoutingBuff"
    CAMPING_HEAL_RECEIVED_BUFF = "campingHealReceivedBuff"

    CAMPING_SPD_BUFF_PARTY = "campingSPDBuffParty"

    CAMPING_ACC_BUFF_RANGED = "campingACCBuffRanged"
    CAMPING_CRIT_BUFF_RANGED = "campingCRITBuffRanged"
    CAMPING_DMG_LOW_BUFF_RANGED = "campingDMGLowBuffRanged"
    CAMPING_DMG_HIGH_BUFF_RANGED = "campingDMGHighBuffRanged"

    CAMPING_ACC_BUFF_MELEE = "campingACCBuffMelee"
    CAMPING_CRIT_BUFF_MELEE = "campingCRITBuffMelee"  # 推测有
    CAMPING_DMG_LOW_BUFF_MELEE = "campingDMGLowBuffMelee"
    CAMPING_DMG_HIGH_BUFF_MELEE = "campingDMGHighBuffMelee"

    CAMPING_ACC_BUFF = "campingACCBuff"
    CAMPING_CRIT_BUFF = "campingCRITBuff"
    CAMPING_SPD_BUFF = "campingSPDBuff"
    CAMPING_DEF_BUFF = "campingDEFBUFF"
    CAMPING_PROT_BUFF = "campingPROTBuff"
    CAMPING_DMG_LOW_BUFF = "campingDMGLowBuff"
    CAMPING_DMG_HIGH_BUFF = "campingDMGHighBuff"

    CAMPING_BLIGHT_RESIST_BUFF = "campingBlightResistBuff"
    CAMPING_BLEED_RESIST_BUFF = "campingBleedResistBuff"
    CAMPING_DISEASE_RESIST_BUFF = "campingDiseaseResistBuff"
    CAMPING_STRESS_RESIST_BUFF = "campingStressResistBuff"
    CAMPING_MOVE_RESIST_BUFF = "campingMoveResistBuff"
    CAMPING_DEBUFF_RESIST_BUFF = "campingDebuffResistBuff"

    CAMPING_DMG_LOW_BUFF_LARGE_MONSTERS = "campingDMGLowBuffLargeMonsters"
    CAMPING_DMG_HIGH_BUFF_LARGE_MONSTERS = "campingDMGHighBuffLargeMonsters"
    CAMPING_ACC_BUFF_LARGE_MONSTERS = "campingACCBuffLargeMonsters"

    CAMPING_DMG_LOW_BUFF_FRONT_RANK = "campingDMGLowBuffFrontRank"
    CAMPING_DMG_HIGH_BUFF_FRONT_RANK = "campingDMGHighBuffFrontRank"
    CAMPING_DMG_LOW_BUFF_NOT_FRONT_RANK = "campingDMGLowBuffNotFrontRank"
    CAMPING_DMG_HIGH_BUFF_NOT_FRONT_RANK = "campingDMGHighBuffNotFrontRank"


class CampingSkillEffectRequirement(Enum):
    AFFLICTED = "afflicted"
    HAS_DEATHS_DOOR_RECOVERY_BUFFS = "has_deaths_door_recovery_buffs"
    RELIGIOUS = "religious"
    NOT_RELIGIOUS = "not_religious"


class CampingSkillSelection(Enum):
    SELF = "self"
    INDIVIDUAL = "individual"
    PARTY = "party"
    PARTY_OTHER = "party_other"


if __name__ == '__main__':
    print(isinstance(STCombatStatMultiply.MAX_HP, Enum))
