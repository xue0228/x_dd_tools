from enum import Enum


class ActorDotUpdateDurationType(Enum):
    """
    ActorDot不按回合或者其他常规方式计算持续时间，而是按触发的“次数”计算
    """
    # 进攻技能施展后的回合结束时触发
    # 所谓进攻技能，即目标为敌方的技能，即使技能本身无任何伤害。
    AFTER_TURN_ATTACK = "after_turn_attack"
    # 进攻技能的直接伤害击杀后的回合结束时触发
    AFTER_TURN_ATTACK_KILL = "after_turn_attack_kill"
    # 友方技能施展后的回合结束时触发
    # 友方技能同理，即目标为友方的技能。
    AFTER_TURN_FRIENDLY = "after_turn_friendly"
