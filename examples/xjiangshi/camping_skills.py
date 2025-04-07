from xddtools.entries import CampingSkill, CampingSkillEffect
from xddtools.entries.camping_skill import pep_talk, encourage
from xddtools.enum import CampingSkillEffectType, CampingSkillBuffSubType, CampingSkillSelection

HERO_NAME = "xjiangshi"

# first_aid.hero_classes = [HERO_NAME]
pep_talk.hero_classes = [HERO_NAME]
encourage.hero_classes = [HERO_NAME]

camp_0 = CampingSkill(
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.2
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_BLEEDING,
        )
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_ji_first_aid.png",
    camping_skill_name="处理伤口",
    str_camping_skill_barks=[
        "鲜红的血液，真好啊。",
        "流血都是小事，没烂就行，交给我吧。",
        "怎么处理的来着？",
        "绕一圈，再绕一圈，再绕一圈……"
    ],
    sfx="audio/jiangshi_calistics {d691c16f-ee8d-4ac2-8a0d-9883aea1a946}.wav"
)

camp_1 = CampingSkill(
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.15,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY_OTHER
        )
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_jiangsh_pep_talk.png",
    camping_skill_name="鬼新娘",
    str_camping_skill_barks=[
        "*哼歌声*"
    ],
    sfx="audio/jiangshi_ghost_bride {775bf0c9-96ca-4c50-a030-a3cfc593f169}.wav"
)

camp_2 = CampingSkill(
    cost=5,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DEATHS_DOOR_RECOVERY_BUFFS
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=10
        )
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_jiangshi_encourage.png",
    camping_skill_name="吟诵",
    str_camping_skill_barks=[
        "我常常在皇帝面前表演。",
        "只是一些让我们放松的音乐。",
        "有人需要什么吗？",
        "我哥哥和我在这方面是出了名的。"
    ],
    sfx="audio/jiangshi_recital {ebb8a6d3-b428-4448-bd39-26961a41ef34}.wav"
)

camp_3 = CampingSkill(
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF_PARTY,
            amount=2,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MOVE_RESIST_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        )
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_jiangshi_stretch.png",
    camping_skill_name="软体功",
    str_camping_skill_barks=[
        "我有一种必须做早操的状况。",
        "请稍等，我的关节有点僵硬。",
        "先做些热身，我就好了……",
        "我永远都不知道为什么我会这么僵硬。"
    ],
    sfx="audio/jiangshi_talisman {4ac3e8d5-599f-4753-a0b3-b062372c0621}.wav"
)

camp_4 = CampingSkill(
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLEED_RESIST_BUFF,
            amount=0.25,
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLIGHT_RESIST_BUFF,
            amount=0.25,
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MOVE_RESIST_BUFF,
            amount=0.25,
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEBUFF_RESIST_BUFF,
            amount=0.25,
        ),
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_jiangshi_talisman.png",
    camping_skill_name="法宝",
    str_camping_skill_barks=[
        "我们的父亲教过我们这些符咒。",
        "也许这个能治好你的病。",
        "看看我记不记得是怎么写的。",
        "有人随身携带黄色纸吗？"
    ],
    sfx="audio/jiangshi_talisman {4ac3e8d5-599f-4753-a0b3-b062372c0621}.wav"
)

camp_5 = CampingSkill(
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_FRONT_RANK,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_FRONT_RANK,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SCOUTING_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        )
    ),
    hero_classes=[HERO_NAME],
    camping_skill_image="skill_icons/camp_skill_jiangshi_prowl.png",
    camping_skill_name="夜游",
    str_camping_skill_barks=[
        "嘘，我听到了什么。",
        "我从来不喜欢夜晚，但有什么东西驱使我向前走。",
        "我感觉到一些东西，我会回来的。",
        "别担心，出去走走就好。"
    ],
    sfx="audio/jiangshi_prowl {13b03383-3879-4876-9949-69a072baae63}.wav"
)

camping_skills = [
    pep_talk,
    encourage,
    camp_0,
    camp_1,
    camp_2,
    camp_3,
    camp_4,
    camp_5
]
