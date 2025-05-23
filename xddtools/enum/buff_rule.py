from enum import Enum


class BuffRuleType(Enum):
    # 只需要 rule_type
    ALWAYS = "always"  # 常驻生效（大部分buff都是这个条件）
    RIPOSTE = "riposte"  # 触发自身反击后生效
    RANGED_ONLY = "rangedonly"  # 远程技能（ranged），在进攻者身上才能根据技能类型激活
    MELEE_ONLY = "meleeonly"  # 近战技能（melee），在进攻者身上才能根据技能类型激活
    FIRST_ROUND_ONLY = "firstroundonly"  # 场战斗的第一回合，更严格说是第一【整轮】即第一个“大回合”期间
    IN_CAMP = "in_camp"  # 扎营
    IN_ROOM = "in_room"  # 在房间
    IN_CORRIDOR = "in_corridor"  # 在走廊
    AT_DEATHS_DOOR = "at_deaths_door"  # 处于死门时
    VIRTUED = "virtued"  # 美德时
    AFFLICTED = "afflicted"  # 折磨时
    IN_VAMPIRE = "in_vampire"  # 有猩红诅咒时
    TARGET_IS_VAMPIRE = "target_is_vampire"  # 目标具有猩红诅咒时
    WALKING_BACKWARDS = "walking_backwards"  # 在走廊后退时
    IN_GUARDED = "in_guarded"  # 被守护
    TARGET_IS_GUARDED = "target_is_guarded"  # 目标被守护时
    IS_GUARDING = "is_guarding"  # 提供守护时
    TARGET_IS_GUARDING = "target_is_guarding"  # 目标是提供守护的单位
    IS_STEALTHED = "is_stealthed"  # 潜行时
    TARGET_IS_STEALTHED = "target_is_stealthed"  # 目标潜行时
    NO_TRINKETS = "no_trinkets"  # 自身没有佩戴任何饰品时
    ACTIVATED_LAST = "activated_last"  # 最后行动，马戏团专属buff,经测试在单机模式依然生效
    ACTIVATED_FIRST = "activated_first"  # 首先行动，马戏团专属buff,经测试在单机模式依然生效
    ON_DEATHS_DOOR_ENTER = "ondeathsdoorenter"  # 进入死门时（触发英雄info的死门进入代码时），由扣除生命值上限导致的进入死门，不会触发此rule

    # 需要 rule_type 和 string
    """
    对某个技能有效（非skill期间时，修饰的buff不会工作）（对反击技能不生效）
    """
    SKILL = "skill"

    """
    技能或effect的作用目标具有特定的状态时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    经测试，dazed不可用
    """
    ACTOR_STATUS = "actorStatus"

    """
    for "if virtued/afflicted" use virtued or afflicted rules
    对于美德时和折磨时的状态，要使用美德时和折磨时的触发条件
    is_actor_status指对自身状态的判定
    经测试，dazed不可用
    在地牢探索中，此rule的判定时间是战斗内外，每时每刻
    """
    IS_ACTOR_STATUS = "is_actor_status"

    """
    副本（遗迹、海湾等，内容填入区域ID）
    """
    IN_DUNGEON = "in_dungeon"

    """
    城镇活动，冥想、赌博等
    """
    IN_ACTIVITY = "in_activity"

    """
    技能或effect的作用目标具有特定的monster type时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    """
    MONSTER_TYPE = "monsterType"

    """
    【被】某类怪物攻击时
    attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
    配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
    """
    ATTACKING_MONSTER_TYPE = "attacking_monster_type"

    """
    有某个怪癖（疾病也可以）时
    """
    HAS_QUIRK = "has_quirk"

    """
    技能或effect的作用目标的id匹配时激活此rule修饰的buff，当反转目标时，buff挂在对方身上，id填自身的monster【大类id】或英雄职业id。
    此种buff在effect指向多个目标时，会根据每个目标单独判定，因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，
    此buff将会单独【干涉】【符合rule的单位】的技能或effect流程。
    """
    ACTOR_BASE_CLASS = "actor_base_class"

    """
    在某个模式下
    """
    IN_MODE = "in_mode"

    """
    背包内有某个物品时（如绷带、草药等）
    """
    HAS_ITEM_ID = "has_item_id"

    """
    背包内有某类物品时（如补给品、宝石等道具类别）
    """
    HAS_ITEM_TYPE = "has_item_type"

    # 需要 rule_type 和 float
    """
    技能或effect的作用目标的size（体型）【大于等于】特定值时激活此rule修饰的buff。此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    怪物的info文件中，size可以写0，这种召唤物被称为“size0”，可以利用其召唤后的spawn: effect玩出很多花样，之后通过kill_enemy_types自灭即可
    注意：size0不显示大多数动画效果，死亡时可能触发老祖语音，在场上时常常会遮挡敌方4个位置中的一个，使得鼠标无法选中此位置，因此需要尽快自灭。
    注意：当行动结束后才会更新动画，而不结束回合的技能不会更新动画，这意味着在不结束回合的技能中，即使size0自灭，它仍然会因为动画未更新而遮挡区域
    """
    MONSTER_SIZE = "monsterSize"

    """
    站位：0，1，2，3
    注意该rule自0起，0才是一号位rank 1
    """
    IN_RANK = "in_rank"

    """
    below：低于百分比
    above:高于百分比
    """
    HP_BELOW = "hpbelow"
    HP_ABOVE = "hpabove"
    LIGHT_BELOW = "lightbelow"
    LIGHT_ABOVE = "lightabove"
    STRESS_BELOW = "stress_below"
    STRESS_ABOVE = "stress_above"
    TARGET_HP_ABOVE = "target_hpabove"
    TARGET_HP_BELOW = "target_hpbelow"

    # 需要 rule_type、string 和 float
    """
    例子：血裔的镜子
    这个是场上有血裔时携带者+4速的buff
    {
        "id" : "cc_trinket_speed_vs_vamps",
        "stat_type" : "combat_stat_add",
        "stat_sub_type" : "speed_rating",
        "amount" : 4,
        "remove_if_not_active" : false,
        "rule_type" : "monster_type_count_min",
        "is_false_rule" : false,
        "rule_data" : {
            "float" : 1,         这里写怪物的最少个数（别写0，写0这辈子都不生效）
            "string" : "vampire" 这里写怪物类型
        }
    },
    注意一点：
    1.attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
    配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
    2.monster_type_count_min为场上有某类怪时触发，属于条件向buff，
    其他buff都能使用该条件，但速度buff尤其适合使用该条件。
    3.monster_type_count_min在怪物侧不适用（详见本表标题）
    4.monster_type_count_min不会计算size为0的单位
    因速度判定是每个大回合（火把里的数字）开始，而不是挨打或者进攻，哪怕速度真的配其他两个有效，你也只有攻击和挨打瞬间提速，无法影响大回合开始，导致提速等于没提。
    """
    MONSTER_TYPE_COUNT_MIN = "monster_type_count_min"


class ActorStatus(Enum):
    TAGGED = "tagged"
    POISONED = "poisoned"
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    VIRTUED = "virtued"
    AFFLICTED = "afflicted"


class DungeonType(Enum):
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


class MonsterType(Enum):
    UNHOLY = "unholy"  # 邪祟
    MAN = "man"  # 人类
    BEAST = "beast"  # 野兽
    ELDRITCH = "eldritch"  # 异魔
    VAMPIRE = "vampire"  # 血裔
    HUST = "hust"  # 瘪壳怪（农场怪的专属种族）
    CORPSE = "corpse"  # 尸体


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
    SHARD = "shard"  # 水晶碎片


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
