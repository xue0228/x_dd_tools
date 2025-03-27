from enum import Enum


class TrinketAwardCategory(Enum):
    DD = "dd"  # 极暗地牢	不要用这个
    TROPHY = "trophy"  # 奖品
    BATTLE = "battle"  # 战斗掉落	战斗以外的方式都不能获得
    UNIVERSAL = "universal"  # 多方式掉落	这个比较常用
    QUEST = "quest"  # 任务
    KICKSTARTER = "kickstarter"  # 输代码（这个我也不是很懂）


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


class DungeonID(Enum):
    CRYPTS = "crypts"  # 遗迹
    WEALD = "weald"  # 荒野
    WARRENS = "warrens"  # 兽窟
    COVE = "cove"  # 海湾
    COURTYARD = "courtyard"  # 庭院


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
