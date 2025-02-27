from effects import *
from xddtools.act_outs import CombatStartTurn, Reaction
from xddtools.buff_rules import BRHasItemId, BRHasItemType
from xddtools.colour import buff, Colour, white, green, yellow, bleed, heal_hp, stun, stress, notable, blight, move, \
    debuff, virtue
from xddtools.enums import QuirkClassification, QuirkTag, STResistance, ItemID, CombatStartTurnActOuts, \
    ReactionActOuts, ItemType
from xddtools.items import Item
from xddtools.loot import LootTable, LootNothingEntry, LootItemEntry, generate_common_overrides_loot_tables, \
    LootTableEntry
from xddtools.quirks import Quirk, UseItemChange, quirk_transition_a_to_b_localization_id
from xddtools.writers import DDWriter, LootTableWriter

if __name__ == '__main__':
    # 定义地牢文件写入器
    dd_writer = DDWriter(MOD_NAME)

    # 定义特殊颜色
    recommend = Colour(name=auto_name.new_colour(), darkness=0.4, saturation=0.0)
    # 将本地化文件中需要用到的颜色添加到写入器中
    dd_writer.add_items((
        notable, recommend, white, green,
        yellow, bleed, heal_hp, stun,
        stress, buff, blight, move,
        debuff, virtue
    ))

    # 定义从10%到100%好感度的buff效果，生成对应的quirk
    quirks_normal_dict_list = [
        {
            "localization": (white("好感度10%"), "+1精准 +1闪避", "10%"),
            "buffs": (acc_1, def_1)
        },
        {
            "localization": (white("好感度20%"), "+1精准 +1闪避\n+3%伤害 +1%暴击", "20%"),
            "buffs": (acc_1, def_1, dmg_l3, dmg_h3, crit_1)
        },
        {
            "localization": (white("好感度30%"), "+2精准 +2闪避\n+3%伤害 +1%暴击", "30%"),
            "buffs": (acc_2, def_2, dmg_l3, dmg_h3, crit_1)
        },
        {
            "localization": (green("好感度40%"), "+2精准 +2闪避\n+4%伤害 +1%暴击", "40%"),
            "buffs": (acc_2, def_2, dmg_l4, dmg_h4, crit_1)
        },
        {
            "localization": (green("好感度50%"), "+2精准 +2闪避\n+4%伤害 +2%暴击", "50%"),
            "buffs": (acc_2, def_2, dmg_l4, dmg_h4, crit_2)
        },
        {
            "localization": (green("好感度60%"), "+2精准 +2闪避\n+4%伤害 +2%暴击 +1速度", "60%"),
            "buffs": (acc_2, def_2, dmg_l4, dmg_h4, crit_2, spd_1)
        },
        {
            "localization": (yellow("好感度70%"), "+3精准 +3闪避\n+4%伤害 +2%暴击 +1速度", "70%"),
            "buffs": (acc_3, def_3, dmg_l4, dmg_h4, crit_2, spd_1)
        },
        {
            "localization": (yellow("好感度80%"), "+3精准 +3闪避\n+5%伤害 +2%暴击 +1速度", "80%"),
            "buffs": (acc_3, def_3, dmg_l5, dmg_h5, crit_2, spd_1)
        },
        {
            "localization": (yellow("好感度90%"), "+3精准 +3闪避\n+5%伤害 +3%暴击 +1速度", "90%"),
            "buffs": (acc_3, def_3, dmg_l5, dmg_h5, crit_3, spd_1)
        },
        {
            "localization": (yellow("好感度100%"), "+3精准 +3闪避\n+5%伤害 +3%暴击 +2速度", "100%"),
            "buffs": (acc_3, def_3, dmg_l5, dmg_h5, crit_3, spd_2)
        }
    ]
    quirks_normal = [Quirk(
        quirk_name=auto_name.new_quirk(),
        analytics_enabled=True,
        random_chance=0.0,
        is_positive=True,
        is_disease=False,
        classification=QuirkClassification.PHYSICAL,
        tags=(QuirkTag.CANT_LOCK,),
        can_modify_in_activity=True,
        can_remove_with_camping_skill=False,
        can_be_replaced_by_new_quirk=False,
        **d
    ) for d in quirks_normal_dict_list]

    for i in range(10):
        quirks_normal[i].random_chance = 10 - i
    for i in range(9):
        quirks_normal[i].evolution_class_id = quirks_normal[i + 1]
        quirks_normal[i].evolution_duration_min = 1
        quirks_normal[i].evolution_duration_max = 999999

    # 定义六种特殊的进阶好感度
    quirks_special_dict_list = [
        {
            "localization": [
                bleed("誓约：残念！"),
                f'+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{notable("羁绊物品")}：圣水'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_X2.png",
            "buffs": [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
            "has_item": ItemID.SUPPLY_HOLY_WATER,
            "special_buffs": [
                buff_x_1, buff_x_2, buff_x_3,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'+20% {notable("破甲")}'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'对血量低于8%的敌人造成{bleed("处决")}伤害'
                # )
            ]
        },

        {
            "localization": [
                heal_hp("誓约：不朽！"),
                f'+3精准 +5闪避 +5%伤害\n+3%暴击 +2速度 +10%防御\n{notable("羁绊物品")}：绷带'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_Y2.png",
            "buffs": [acc_3, def_5, dmg_l5, dmg_h5, crit_3, spd_2, prot_10],
            "has_item": ItemID.SUPPLY_BANDAGE,
            "special_buffs": [
                buff_y_1, buff_y_2,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'-10%受到的伤害'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'永续{heal_hp("愈合")}1生命值'
                # )
            ]
        },

        {
            "localization": [
                stun("誓约：魔法！"),
                f'+3精准 +3闪避 +5%伤害\n'
                f'+3%暴击 +3速度 +10% {stun("眩晕")}/{bleed("流血")}/{blight("腐蚀")}概率\n'
                f'{notable("羁绊物品")}：解毒剂'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_Z2.png",
            "buffs": [
                acc_3, def_3, dmg_l5, dmg_h5, crit_3, spd_3,
                stun_10, bleed_10, poison_10,
            ],
            "has_item": ItemID.SUPPLY_ANTIVENOM,
            "special_buffs": [
                stun_10_first, bleed_10_first, poison_10_first, buff_z,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'+2速度'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'首先行动时+10% {stun("眩晕")}/{bleed("流血")}/{blight("腐蚀")}概率'
                # )
            ]
        },

        {
            "localization": [
                stress("誓约：知识！"),
                f'+3精准 +5闪避 +5%伤害 +3%暴击 +2速度\n'
                f'+10%生命/{stress("压力")}{heal_hp("治疗")} +20% {heal_hp("愈合")}效果\n'
                f'{notable("羁绊物品")}：食物'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_M2.png",
            "buffs": [
                acc_3, def_5, dmg_l5, dmg_h5, crit_3, spd_2,
                buff_m_1, buff_m_2, buff_m_3
            ],
            "has_item": ItemType.PROVISION,
            "special_buffs": [
                buff_m_4, buff_m_5, buff_m_6,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'对血量低于5%的英雄+33%生命/{stress("压力")}{heal_hp("治疗")}'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'-20%受到的{stress("压力")}伤害'
                # )
            ]
        },

        {
            "localization": [
                buff("誓约：神明！"),
                f'+5精准 +3闪避 +5%伤害 +3%暴击 +2速度\n'
                f'+10% {debuff("减益")}/{move("位移")}概率\n'
                f'{notable("羁绊物品")}：药草'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_O2.png",
            "buffs": [
                acc_5, def_3, dmg_l5, dmg_h5, crit_3, spd_2,
                buff_o_1, buff_o_2,
            ],
            "has_item": ItemID.SUPPLY_MEDICINAL_HERBS,
            "special_buffs": [
                buff_o_3,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'+10% {virtue("美德")}概率'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'提高{stun("赐福")}概率'
                # )
            ]
        },

        {
            "localization": [
                bleed("誓约：恶魔！"),
                f'+5精准 +5闪避\n'
                f'+8%伤害 +5%暴击 +3速度\n'
                f'{notable("羁绊物品")}：鸦片酊'
            ],
            "image_path": "overlays/tray_quirk.Love_Grade_N2.png",
            "buffs": [
                acc_5, def_5, dmg_l8, dmg_h8, crit_5, spd_3,
            ],
            "has_item": ItemID.SUPPLY_LAUDANUM,
            "special_buffs": [
                buff_n,
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'不再{bleed("自残")}'
                # ),
                # Buff(
                #     buff_name=auto_name.new_buff(),
                #     stat_type=BuffType.UPGRADE_DISCOUNT,
                #     stat_sub_type=auto_name.last_buff(),
                #     localization=f'{stress("心力衰竭")}时清空{stress("压力")}'
                # )
            ]
        },
    ]
    quirks_special = [Quirk(
        localization=(
            d["localization"][0],
            d["localization"][1],
            "CALM",
        ),
        buffs=tuple(d["buffs"] + [Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.RESISTANCE,
            stat_sub_type=resistance,
            amount=0.05,
            has_description=False,
            remove_if_not_active=False,
            buff_rule=BRHasItemId(d["has_item"]) if isinstance(d["has_item"], ItemID) else BRHasItemType(d["has_item"])
        ) for resistance in [
            STResistance.STUN,
            STResistance.BLEED,
            STResistance.POISON,
            STResistance.DEBUFF,
            STResistance.TRAP,
            STResistance.MOVE,
            STResistance.DISEASE,
        ]]),
        quirk_name=auto_name.new_quirk(),
        analytics_enabled=True,
        random_chance=0.0,
        is_positive=True,
        is_disease=False,
        classification=QuirkClassification.PHYSICAL,
        tags=(QuirkTag.CANT_LOCK,),
        can_modify_in_activity=True,
        can_remove_with_camping_skill=False,
        can_be_replaced_by_new_quirk=False,
        evolution_duration_min=31,
        evolution_duration_max=75,
        # evolution_duration_min=1,
        # evolution_duration_max=2,
    ) for d in quirks_special_dict_list]
    quirks_special2 = [Quirk(
        localization=(
            d["localization"][0] + recommend("TW"),
            d["localization"][1],
            "TW!",
        ),
        quirk_name=auto_name.new_quirk(),
        image_path=d["image_path"],
        buffs=tuple(d["buffs"] + [Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.RESISTANCE,
            stat_sub_type=resistance,
            amount=0.05,
            has_description=False,
            remove_if_not_active=False,
            buff_rule=BRHasItemId(d["has_item"]) if isinstance(d["has_item"], ItemID) else BRHasItemType(d["has_item"])
        ) for resistance in [
            STResistance.STUN,
            STResistance.BLEED,
            STResistance.POISON,
            STResistance.DEBUFF,
            STResistance.TRAP,
            STResistance.MOVE,
            STResistance.DISEASE,
        ]] + d["special_buffs"]),
        analytics_enabled=True,
        random_chance=0.0,
        is_positive=True,
        is_disease=False,
        classification=QuirkClassification.PHYSICAL,
        tags=(QuirkTag.CANT_LOCK,),
        can_modify_in_activity=True,
        can_remove_with_camping_skill=False,
        can_be_replaced_by_new_quirk=False,
        evolution_duration_min=22,
        evolution_duration_max=30,
        # evolution_duration_min=2,
        # evolution_duration_max=3,
    ) for d in quirks_special_dict_list]

    # 誓约：残念！ 互动演出
    quirks_special[0].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=89
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
            chance=1,
            number_value=0.20,
            string_value=effect_x_1,
            localization=("任何人都不许后退！", "即使是鲜血淋漓，也誓死捍卫吾主！")
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=5,
            string_value=effect_x_2,
            localization=(
                "无上吾主！万王之王！伟大旨意！启明恒星！",
                "挡在吾主路前的，即使是神明我也杀给你看。",
                "为了吾主！",
                "吾主即是我存在的意义。",
                "如果是没有吾主的世界，那就消失吧！"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=3,
            string_value=effect_x_3
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=1,
            string_value=effect_x_4
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=1,
            string_value=effect_x_5,
            localization=("领主？还需要我吗？", "领主！我没有背叛您！")
        ),
    )
    quirks_special[0].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_x_6,
            localization=(
                "您只管前进，我会为您承担一切痛楚，请不要停下脚步。",
                "就算此身腐朽，此剑断裂，我也不会停止对吾主之敌的征讨！",
                "我的光芒从未熄灭，吾主就在我的身边照耀！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_ATTACK_MISSED,
            chance=0.1,
            # chance=0.5,
            effect=effect_x_7,
            localization=(
                "别松懈！吾主还在看着！",
                "打起精神！你让我在吾主面前蒙羞！"
            )
        ),
    )
    quirks_special2[0].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=89
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
            chance=1,
            number_value=0.20,
            string_value=effect_x_1,
            localization=("任何人都不许后退！", "即使是鲜血淋漓，也誓死捍卫吾主！")
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=5,
            string_value=effect_x_2,
            localization=(
                "无上吾主！万王之王！伟大旨意！启明恒星！",
                "挡在吾主路前的，即使是神明我也杀给你看。",
                "为了吾主！",
                "吾主即是我存在的意义。",
                "如果是没有吾主的世界，那就消失吧！"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=3,
            string_value=effect_x_3
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=1,
            string_value=effect_x_4
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=1,
            string_value=effect_x_8,
            localization=("为了吾主！", "无上吾主！万王之王！伟大旨意！启明恒星！")
        ),
    )
    quirks_special2[0].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_x_6,
            localization=(
                "您只管前进，我会为您承担一切痛楚，请不要停下脚步。",
                "就算此身腐朽，此剑断裂，我也不会停止对吾主之敌的征讨！",
                "我的光芒从未熄灭，吾主就在我的身边照耀！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_ATTACK_MISSED,
            chance=0.1,
            # chance=0.5,
            effect=effect_x_7,
            localization=(
                "别松懈！吾主还在看着！",
                "打起精神！你让我在吾主面前蒙羞！"
            )
        ),
    )

    # 誓约：不朽！ 互动演出
    quirks_special[1].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=84
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=1,
            string_value=effect_y_1,
            localization=(
                "不许离开我！",
                "最讨厌你了！"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=15,
            string_value=effect_y_2,
            localization=(
                "这样就能提起精神，果然是些无可救药的家伙。",
                "才不是特意想帮你们的！"
            )
        ),
    )
    quirks_special[1].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_y_3,
            localization=(
                "没有...我才没有受伤...",
                "呜~领主，大笨蛋！！",
                "怪物什么的...最讨厌了！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect="Guard 1",
            localization=(
                "不要得意忘形了笨蛋！",
                "只是偶然想帮你的啦！",
                "别搞错了...才没有什么别的意思..."
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.01,
            # chance=0.5,
            effect=effect_y_4
        ),
    )
    quirks_special2[1].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=85
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=15,
            string_value=effect_y_2,
            localization=(
                "这样就能提起精神，果然是些无可救药的家伙。",
                "才不是特意想帮你们的！"
            )
        ),
    )
    quirks_special2[1].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_y_3,
            localization=(
                "没有...我才没有受伤...",
                "呜~领主，大笨蛋！！",
                "怪物什么的...最讨厌了！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.05,
            # chance=0.5,
            effect=effect_y_5,
            localization=(
                "没有...我才没有受伤...",
                "呜~领主，大笨蛋！！",
                "怪物什么的...最讨厌了！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect="Guard 1",
            localization=(
                "不要得意忘形了笨蛋！",
                "只是偶然想帮你的啦！",
                "别搞错了...才没有什么别的意思..."
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.01,
            # chance=0.5,
            effect=effect_y_4
        ),
    )

    # 誓约：魔法！ 互动演出
    quirks_special[2].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=75
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
            chance=1,
            number_value=0.20,
            string_value="STUN 3",
            localization=("啊...糟了，读错咒文了...", "啊，眼花了...")
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_1,
            localization=(
                "加一点毒蘑菇，再来一个旧鞋跟。",
                "来吧，它会让你很兴奋的！",
                "我的魔法会把你撕碎！",
                "这次使用什么魔法好呢？"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_2
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_3
        ),
    )
    quirks_special[2].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.01,
            # chance=0.5,
            effect="STUN 5",
            localization=(
                "烦人...",
                "催眠术！",
                "我对傻子的尸体不感兴趣。",
                "再闹腾下去，我就要用魔法强迫你听话了..."
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_z_4,
            localization=(
                "你的魔法无效！",
                "低级的魔法而已。"
            )
        ),
    )
    quirks_special2[2].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=76
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_1,
            localization=(
                "加一点毒蘑菇，再来一个旧鞋跟。",
                "来吧，它会让你很兴奋的！",
                "我的魔法会把你撕碎！",
                "这次使用什么魔法好呢？"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_2
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_z_3
        ),
    )
    quirks_special2[2].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.05,
            # chance=0.5,
            effect="STUN 6",
            localization=(
                "烦人...",
                "催眠术！",
                "我对傻子的尸体不感兴趣。",
                "再闹腾下去，我就要用魔法强迫你听话了..."
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_z_4,
            localization=(
                "你的魔法无效！",
                "低级的魔法而已。"
            )
        ),
    )

    # 誓约：知识！ 互动演出
    quirks_special[3].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=82
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.CHANGE_POS,
            chance=1,
            number_value=0,
            localization=("马失前蹄...了呢。", "呼呼，我似乎有点醉了~")
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_m_1,
            localization=(
                "微风拂过海面，蝉鸣漾入云间。",
                "我总在这里，与你共赏一轮明月。",
                "醉翁之意不在酒，在乎你我之间。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=8,
            string_value=effect_m_2,
            localization=(
                "桃之夭夭，灼灼其华。",
                "腐草为萤，耀采于月。",
                "林中落雨，秋前盛夏。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=1,
            string_value=effect_m_3,
            localization=(
                "你已被我看破！",
                "攻城为下，攻心为上。"
            )
        ),
    )
    quirks_special[3].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_m_4,
            localization=(
                "你还挺擅长趁虚而入...",
                "谈笑有鸿儒，往来无白丁。",
                "相鼠有皮，汝而无仪。"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.01,
            # chance=0.5,
            effect=effect_m_5
        ),
    )
    quirks_special2[3].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=83
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=8,
            string_value=effect_m_1,
            localization=(
                "微风拂过海面，蝉鸣漾入云间。",
                "我总在这里，与你共赏一轮明月。",
                "醉翁之意不在酒，在乎你我之间。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=8,
            string_value=effect_m_2,
            localization=(
                "桃之夭夭，灼灼其华。",
                "腐草为萤，耀采于月。",
                "林中落雨，秋前盛夏。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=1,
            string_value=effect_m_3,
            localization=(
                "你已被我看破！",
                "攻城为下，攻心为上。"
            )
        ),
    )
    quirks_special2[3].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_m_4,
            localization=(
                "你还挺擅长趁虚而入...",
                "谈笑有鸿儒，往来无白丁。",
                "相鼠有皮，汝而无仪。"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.01,
            # chance=0.5,
            effect=effect_m_5
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.05,
            # chance=0.5,
            effect=effect_m_6,
            localization=(
                "但凡不能杀死你的，最终都会使你变强。",
                "能被触碰到是确实存在的证明。"
            )
        ),
    )

    # 誓约：神明！ 互动演出
    quirks_special[4].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=66
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.MARK_SELF,
            chance=1,
            string_value="Mark Self",
            localization=("再摸、再摸吾就生气了！", "神明不需要信徒，而是信徒需要神明。")
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=3,
            string_value=effect_o_7,
            localization=(
                "心之所愿，定能如愿！",
                "神明之力，福荫人间！"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_1,
            localization=(
                "汝被强化了，快上~",
                "快显灵...不要给吾丢脸...（默默嘀咕着）",
                "汝笑什么？这可是神明的恩赐！",
                "嘲笑神明可是没有好鱼干吃的！（撇嘴~）"
                "快吃吧，这可是神明的鱼干。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_2
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_3
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_4
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_5
        )
    )
    quirks_special[4].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_o_6,
            localization=(
                "虽然吾不像其他神明一样强大，但仍能治愈这些低级咒术。",
                "吾可是神明，治愈这些低级咒术只是举手之劳。",
                "吾可是神明，不要小看我！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_MISSED,
            chance=0.02,
            # chance=0.5,
            effect=effect_o_8,
            localization=(
                "心之所愿，定能如愿！", "神明之力，福荫人间！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_ATTACK_HIT,
            chance=0.02,
            # chance=0.5,
            effect=effect_o_9,
            localization=(
                "心之所愿，定能如愿！", "神明之力，福荫人间！"
            )
        )
    )
    quirks_special2[4].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=64
            # chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
            chance=6,
            string_value=effect_o_7,
            localization=(
                "心之所愿，定能如愿！",
                "神明之力，福荫人间！"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_1,
            localization=(
                "汝被强化了，快上~",
                "快显灵...不要给吾丢脸...（默默嘀咕着）",
                "汝笑什么？这可是神明的恩赐！",
                "嘲笑神明可是没有好鱼干吃的！（撇嘴~）"
                "快吃吧，这可是神明的鱼干。"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_2
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_3
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_4
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=6,
            string_value=effect_o_5
        )
    )
    quirks_special2[4].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_HIT,
            chance=0.1,
            # chance=0.5,
            effect=effect_o_6,
            localization=(
                "虽然吾不像其他神明一样强大，但仍能治愈这些低级咒术。",
                "吾可是神明，治愈这些低级咒术只是举手之劳。",
                "吾可是神明，不要小看我！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_MISSED,
            chance=0.05,
            # chance=0.5,
            effect=effect_o_8,
            localization=(
                "心之所愿，定能如愿！", "神明之力，福荫人间！"
            )
        ),
        Reaction(
            name=ReactionActOuts.COMMENT_ALLY_ATTACK_HIT,
            chance=0.05,
            # chance=0.5,
            effect=effect_o_9,
            localization=(
                "心之所愿，定能如愿！", "神明之力，福荫人间！"
            )
        )
    )

    # 誓约：恶魔！ 互动演出
    quirks_special[5].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.RANDOM_COMMADN,
            chance=1,
            # chance=50,
            localization=(
                "这是为了让领主爱我所必须做的呢~",
                "不要阻止我将她们抹杀！",
                "杀了你，领主就会只看我一个人了"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.ATTACK_SELF,
            chance=99,
            number_value=0.05,
            string_value=effect_n_1,
            localization=(
                "不可以逃走哦~领主",
                "爱在染满鲜血的时候才是最美丽的呀！",
                "我会杀掉除领主外的所有人...",
                "哈~哈~哈（嘴角出血地笑着）",
                "千万千万不要背叛哟~",
                "你所喜欢的我都会抹杀，那样你就只能爱我了"
            )
        )
    )
    quirks_special[5].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.99,
            effect=effect_n_2,
            localization=(
                "像你这么恶心的怪物，怎么有资格站在领主的旁边",
                "你们也想要接近领主吗？！——呵呵呵",
                "太碍事了……不可原谅!"
            )
        ),
    )
    quirks_special2[5].combat_start_turn_act_outs = (
        CombatStartTurn(
            name=CombatStartTurnActOuts.NOTHING,
            chance=0
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.BUFF_PARTY,
            chance=1,
            # chance=50,
            string_value=effect_n_3,
            localization=(
                "你是无法反抗命运的...咦嘻嘻",
                "看过领主的女人都会被我杀死哦~"
            )
        ),
        CombatStartTurn(
            name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
            chance=99,
            string_value=effect_n_1,
            localization=(
                "不可以逃走哦~领主",
                "爱在染满鲜血的时候才是最美丽的呀！",
                "我会杀掉除领主外的所有人...",
                "哈~哈~哈（表情冰冷地笑着）",
                "千万千万不要背叛哟~",
                "你所讨厌的我都会抹杀，那样你就会爱我了"
            )
        )
    )
    quirks_special2[5].reaction_act_outs = (
        Reaction(
            name=ReactionActOuts.COMMENT_SELF_HIT,
            chance=0.99,
            effect=effect_n_2,
            localization=(
                "像你这么恶心的怪物，怎么有资格站在领主的旁边",
                "你们也想要接近领主吗？！——呵呵呵",
                "太碍事了……不可原谅!"
            )
        ),
    )

    # 获得及提升好感度的物品
    item_0 = Item(
        localization=(
            "稀有信物—小花",
            "有谁能拒绝一朵金灿灿的小花呢？\n（赠予英雄提升10%好感度！）"
        ),
        image_path="estate/inv_estate+Love_Token_A.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[0]
        ),
        base_stack_limit=20
    )
    item_1 = Item(
        localization=(
            "史诗信物—残念单剑",
            f"一剑一念，一念一人！\n"
            f"（赠予英雄提升30%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予输出型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_B.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[2]
        ),
        base_stack_limit=2
    )
    item_2 = Item(
        localization=(
            "史诗信物—不朽重盾",
            f"因为太怕痛，就全点了防御力~\n"
            f"（赠予英雄提升30%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予防御型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_C.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[2]
        ),
        base_stack_limit=2
    )
    item_3 = Item(
        localization=(
            "史诗信物—魔力法杖",
            f"只有魔法天赋极强的英雄才能使用它。\n"
            f"（赠予英雄提升30%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予控制及dot伤害型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_D.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[2]
        ),
        base_stack_limit=2
    )
    item_4 = Item(
        localization=(
            "史诗信物—知识之书",
            f"不会真的有人喜欢读书吧？\n"
            f"（赠予英雄提升30%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予治疗减压型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_E.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[2]
        ),
        base_stack_limit=2
    )
    item_5 = Item(
        localization=(
            "史诗信物—神明羽翼",
            f"据传说，它能召唤强大而严肃的神明！\n"
            f"（赠予英雄提升30%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予增益/减益辅助型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_G.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[2]
        ),
        base_stack_limit=2
    )
    item_6 = Item(
        localization=(
            "传说信物——恶魔头骨",
            f"为什么它的掉率那么低？？？\n"
            f"（赠予英雄提升100%好感度或特化满好感度英雄）\n"
            f"{recommend('推荐赠予强力输出型英雄')}"
        ),
        image_path="estate/inv_estate+Love_Token_F.png",
        effect=Effect(
            effect_name=auto_name.new_effect(),
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            item=True,
            disease=quirks_normal[9]
        ),
        base_stack_limit=2
    )

    # 使用物品提升好感度
    for i in range(9):
        quirks_normal[i].use_item_changes = (
            UseItemChange(
                item_type=item_0.item_type,
                item_id=item_0,
                change_quirk_class_id=quirks_normal[min(i + 1, 9)]
            ),
            UseItemChange(
                item_type=item_1.item_type,
                item_id=item_1,
                change_quirk_class_id=quirks_normal[min(i + 3, 9)]
            ),
            UseItemChange(
                item_type=item_2.item_type,
                item_id=item_2,
                change_quirk_class_id=quirks_normal[min(i + 3, 9)]
            ),
            UseItemChange(
                item_type=item_3.item_type,
                item_id=item_3,
                change_quirk_class_id=quirks_normal[min(i + 3, 9)]
            ),
            UseItemChange(
                item_type=item_4.item_type,
                item_id=item_4,
                change_quirk_class_id=quirks_normal[min(i + 3, 9)]
            ),
            UseItemChange(
                item_type=item_5.item_type,
                item_id=item_5,
                change_quirk_class_id=quirks_normal[min(i + 3, 9)]
            ),
            UseItemChange(
                item_type=item_6.item_type,
                item_id=item_6,
                change_quirk_class_id=quirks_normal[9]
            ),
        )
    # 100%好感度后使用特殊物品进化为特殊怪癖
    quirks_normal[9].use_item_changes = (
        UseItemChange(
            item_type=item_1.item_type,
            item_id=item_1,
            change_quirk_class_id=quirks_special[0]
        ),
        UseItemChange(
            item_type=item_2.item_type,
            item_id=item_2,
            change_quirk_class_id=quirks_special[1]
        ),
        UseItemChange(
            item_type=item_3.item_type,
            item_id=item_3,
            change_quirk_class_id=quirks_special[2]
        ),
        UseItemChange(
            item_type=item_4.item_type,
            item_id=item_4,
            change_quirk_class_id=quirks_special[3]
        ),
        UseItemChange(
            item_type=item_5.item_type,
            item_id=item_5,
            change_quirk_class_id=quirks_special[4]
        ),
        UseItemChange(
            item_type=item_6.item_type,
            item_id=item_6,
            change_quirk_class_id=quirks_special[5]
        ),
    )

    # 设置冲突怪癖
    total_quirks = [
        *quirks_normal,
        *quirks_special,
        *quirks_special2,
    ]
    for quirk in total_quirks:
        quirk.incompatible_quirks = [q for q in total_quirks if q != quirk]

    # 设置特殊怪癖的普通模式与亢奋模式之间相互转换
    for i in range(6):
        quirks_special[i].evolution_class_id = quirks_special2[i]
        quirks_special2[i].evolution_class_id = quirks_special[i]

    # 物品掉落
    loots = LootTable(
        name=MOD_NAME,
        loot_entries=(
            LootNothingEntry(chances=0),
            LootItemEntry(chances=100, item_type=item_0.item_type, item_id=item_0, amount=1),
            # LootItemEntry(chances=5, item_type=item_0.item_type, item_id=item_0, amount=1),
            LootItemEntry(chances=5, item_type=item_1.item_type, item_id=item_1, amount=1),
            LootItemEntry(chances=5, item_type=item_2.item_type, item_id=item_2, amount=1),
            LootItemEntry(chances=5, item_type=item_3.item_type, item_id=item_3, amount=1),
            LootItemEntry(chances=5, item_type=item_4.item_type, item_id=item_4, amount=1),
            LootItemEntry(chances=5, item_type=item_5.item_type, item_id=item_5, amount=1),
            LootItemEntry(chances=1, item_type=item_6.item_type, item_id=item_6, amount=1),
        )
    )
    a, s, w = generate_common_overrides_loot_tables()
    a.add_loot_entry(LootTableEntry(chances=8, loot_table_id=loots))
    s.add_loot_entry(LootTableEntry(chances=5, loot_table_id=loots))
    # a.add_loot_entry(LootTableEntry(chances=1000, loot_table_id=loots))
    # s.add_loot_entry(LootTableEntry(chances=1000, loot_table_id=loots))
    dd_writer.add_item(loots)
    LootTableWriter(
        name="common_overrides",
        loot_tables=(a, s, w)
    ).export(MOD_NAME)

    # 怪癖进化文本
    for i in range(9):
        dd_writer.add_item((
            quirk_transition_a_to_b_localization_id(quirks_normal[i], quirks_normal[i + 1]),
            f'好感度已提升10%！当前好感度：{i + 2}0%' if i + 2 < 10 else f'好感度已提升满！当前好感度：100%'
        ))
        dd_writer.add_item((
            quirk_transition_a_to_b_localization_id(quirks_normal[i], quirks_normal[min(i + 3, 9)]),
            f'好感度已提升30%！当前好感度：{i + 4}0%' if i + 4 < 10 else f'好感度已提升满！当前好感度：100%'
        ))
        dd_writer.add_item((
            quirk_transition_a_to_b_localization_id(quirks_normal[i], quirks_normal[9]),
            f'好感度已提升满！当前好感度：100%'
        ))

    dd_writer.add_items((
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[0]),
            "此身，此剑，皆由您来掌控，因为您是我的爱，我的王...我唯一的光。"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[0]),
            "当我沿着泥泞的道路来到这里，我本以为满是黑暗，但在您身上我看到了光明...请使用我吧，从今往后，我便是您的利刃。"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[1]),
            "什，什么嘛...唉？这个是送我的吗？"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[1]),
            "盾？习惯了就不重哟，毕竟…人家的力量还是很强的！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[2]),
            "啊...我们的关系变化真是魔法级别的...简直比魔法还像魔法，要知道我从未像如此，对一个人目不转睛。"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[2]),
            "我的身体好像发生了某种进化，而触发反应的催化剂...是你的手吗？"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[3]),
            "呼呼，要不要一起来读几首情诗呢，领主？"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[3]),
            "领、领主...这种展开是不是该换个地方...啊啊我究竟在说什么！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[4]),
            "虽然是汝召唤了吾，但还请不要摸吾的翅膀~（撇嘴~）"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[4]),
            "吾可以实现汝的愿望，唉？乱碰可不行..."
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[5]),
            "这身体的灼热、内心的鼓动……终于等到您了，领主"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_normal[9], quirks_special[5]),
            "是对其他女孩子做这种事，就要给您一点惩罚了哦。"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[0], quirks_special2[0]),
            "为吾主献出心脏！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[1], quirks_special2[1]),
            "虽然不想承认...但还是忍不住想守护你！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[2], quirks_special2[2]),
            "我的魔法终于成功了！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[3], quirks_special2[3]),
            "不要小看读书人！（摘下眼镜）"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[4], quirks_special2[4]),
            "让汝们见识下神明真正的实力！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special[5], quirks_special2[5]),
            "我的眼里只有领主呢！"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[0], quirks_special[0]),
            "我的表现还不错吧~（脸红低头）"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[1], quirks_special[1]),
            "别太得寸进尺了！（嘟嘴）"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[2], quirks_special[2]),
            "看来还是要再完善完善..."
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[3], quirks_special[3]),
            "呜？被看到不淑女的样子了~（戴上眼镜）"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[4], quirks_special[4]),
            "呼呼，饿，想吃小鱼干~"
        ),
        (
            quirk_transition_a_to_b_localization_id(quirks_special2[5], quirks_special[5]),
            "领主，今天怎么回来晚了？"
        ),
    ))

    # 将所有怪癖添加到DDWriter中
    dd_writer.add_items(total_quirks)
    # 导出MOD到指定文件夹中
    dd_writer.export(MOD_NAME)
