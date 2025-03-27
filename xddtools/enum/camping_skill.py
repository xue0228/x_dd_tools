from enum import Enum


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
