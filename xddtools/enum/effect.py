from enum import Enum


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


class BuffStatType(Enum):
    HP_DOT_BLEED = "hp_dot_bleed"
    HP_DOT_POISON = "hp_dot_poison"
    HP_DOT_HEAL = "hp_dot_heal"
    STRESS_DOT = "stress_dot"
    SHUFFLE_DOT = "shuffle_dot"


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


class DamageSourceType(Enum):
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


class KeyStatus(Enum):
    TAGGED = "tagged"
    POISONED = "poisoned"
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    DAZED = "dazed"
    TRANSFORMED = "transformed"  # 转变？传送？已废弃


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
