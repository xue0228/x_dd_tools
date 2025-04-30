from constants import *
from actouts import *
from xddtools import get_dd_writer
from xddtools.entries import Project, Quirk, Item, Effect, UseItemChange
from xddtools.entries.colour import pink, skill_unselectable
from xddtools.enum import ProjectTag, QuirkClassification, QuirkTag, EffectTarget, ItemType, ItemID, STResistance

if __name__ == '__main__':
    project = Project(
        title="好感度怪癖",
        preview_icon_image="preview_icon.png",
        tags=[ProjectTag.GAMEPLAY_TWEAKS]
    )

    # 10%-100%的普通好感度怪癖
    normal_quirks_data = [
        (pink("好感度10%：初识"), pink("\n“相逢何必曾相识”"), "10%", [acc_1, def_1]),
        (pink("好感度20%：留意"), pink("\n“墙里秋千墙外道，墙外行人，墙里佳人笑”"), "20%", [acc_1, def_1, dmg_l3, dmg_h3, crit_1]),
        (pink("好感度30%：好奇"), pink("\n“和羞走，倚门回首，却把青梅嗅”"), "30%", [acc_2, def_2, dmg_l3, dmg_h3, crit_1]),
        (pink("好感度40%：牵挂"), pink("\n“此情无计可消除，才下眉头，却上心头”"), "40%", [acc_2, def_2, dmg_l4, dmg_h4, crit_1]),
        (pink("好感度50%：倾心"), pink("\n“身无彩凤双飞翼，心有灵犀一点通”"), "50%", [acc_2, def_2, dmg_l4, dmg_h4, crit_2]),
        (pink("好感度60%：钟情"), pink("\n“愿我如星君如月，夜夜流光相皎洁”"), "60%", [acc_2, def_2, dmg_l4, dmg_h4, crit_2, spd_1]),
        (pink("好感度70%：挚爱"), pink("\n“换我心，为你心，始知相忆深”"), "70%", [acc_3, def_3, dmg_l4, dmg_h4, crit_2, spd_1]),
        (pink("好感度80%：不渝"), pink("\n“曾经沧海难为水，除却巫山不是云”"), "80%", [acc_3, def_3, dmg_l5, dmg_h5, crit_2, spd_1]),
        (pink("好感度90%：同契"), pink("\n“死生契阔，与子成说；执子之手，与子偕老”"), "90%", [acc_3, def_3, dmg_l5, dmg_h5, crit_3, spd_1]),
        (pink("好感度100%：入骨"), pink("\n“只缘感君一回顾，使我思君朝与暮”"), "100%", [acc_3, def_3, dmg_l5, dmg_h5, crit_3, spd_2]),
    ]

    normal_quirks = [Quirk(
        str_quirk_name=data[0],
        str_quirk_description=data[1],
        str_ui_entering=data[2],
        buffs=data[3],
        analytics_enabled=True,
        show_explicit_buff_description=True,
        show_flavor_description=True,
        random_chance=0.5,
        is_positive=True,
        is_disease=False,
        classification=QuirkClassification.MENTAL,
        tags=[QuirkTag.CANT_LOCK],
        can_modify_in_activity=True,
        can_remove_with_camping_skill=False,
        can_be_replaced_by_new_quirk=False,
        evolution_duration_min=1,
        evolution_duration_max=999999
    ) for i, data in enumerate(normal_quirks_data)]

    # 为10%-90%的普通好感度怪癖设置进阶好感度
    for i in range(9):
        normal_quirks[i].evolution_class_id = normal_quirks[i + 1]
        normal_quirks[i].evolution_quirk_bark = f"好感度已提升10%！\n当前好感度：{i + 2}0%"

    # 真正生效的物品效果
    estate = Item(
        str_inventory_title="",
        effect=Effect(
            target=EffectTarget.PERFORMER,
            disease=normal_quirks[0]
        )
    )

    # 使用物品可以提升10%好感度
    for i in range(9):
        normal_quirks[i].use_item_changes = [
            UseItemChange(
                item_type=estate.item_type,
                item_id=estate,
                change_quirk_class_id=normal_quirks[i + 1],
                # change_quirk_bark=f"好感度已提升10%！当前好感度：{i + 2}0%"
            )
        ]

    # 机率获得好感度的信物
    supplies_data = [
        (f"小花\n{skill_unselectable('稀有信物')}", "有谁能拒绝一朵金灿灿的小花呢？\n(赠予英雄小概率提升10%好感度！)",
         "estate/inv_estate+Love_Token_A.png", 0.3, 10000, 10),
        (f"残念单剑\n{skill_unselectable('史诗信物')}",
         f"一剑一念，一念一人！\n(赠予英雄中概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予输出型英雄')}",
         "estate/inv_estate+Love_Token_B.png", 0.6, 25000, 2),
        (f"不朽重盾\n{skill_unselectable('史诗信物')}",
         f"因为太怕痛，就全点了防御力~\n(赠予英雄中概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予防御型英雄')}",
         "estate/inv_estate+Love_Token_C.png", 0.6, 25000, 2),
        (f"魔力法杖\n{skill_unselectable('史诗信物')}",
         f"只有魔法天赋极强的英雄才能使用它。\n(赠予英雄中概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予控制及dot伤害型英雄')}",
         "estate/inv_estate+Love_Token_D.png", 0.6, 25000, 2),
        (f"知识之书\n{skill_unselectable('史诗信物')}",
         f"不会真的有人喜欢读书吧？\n(赠予英雄中概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予治疗减压型英雄')}",
         "estate/inv_estate+Love_Token_E.png", 0.6, 25000, 2),
        (f"神明羽翼\n{skill_unselectable('传说信物')}",
         f"据传说，它能召唤强大而严肃的神明！\n(赠予英雄大概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予治增益/减益辅助型英雄')}",
         "estate/inv_estate+Love_Token_G.png", 0.9, 60000, 1),
        (f"恶魔头骨\n{skill_unselectable('传说信物')}",
         f"那么代价是什么呢？\n(赠予英雄大概率提升10%好感度或特化满好感度英雄)\n{skill_unselectable('推荐赠予强力输出型英雄')}",
         "estate/inv_estate+Love_Token_F.png", 0.9, 60000, 1),
    ]
    supplies = [Item(
        str_inventory_title=data[0],
        str_inventory_description=data[1],
        item_image=data[2],
        item_type=ItemType.SUPPLY,
        effect=Effect(
            target=EffectTarget.PERFORMER,
            chance=data[3],
            use_item_type=estate.item_type,
            use_item_id=estate
        ),
        # purchase_gold_value=data[4],
        purchase_gold_value=0,
        sell_gold_value=int(data[4] * 0.1),
        base_stack_limit=data[5],
        default_store_item_lists=[None, 99, 99, 99, 99, 99]
    ) for i, data in enumerate(supplies_data)]

    special_quirks_data = [
        # 名称、描述
        (pink("誓约：残念！"), f"+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{pink('羁绊物品')}：圣水",
         # 进化版怪癖的图标、Buff
         "overlays/tray_quirk.Love_Grade_X2.png", [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
         # 羁绊物品、进化后额外Buff
         ItemID.SUPPLY_HOLY_WATER, [buff_x_1, buff_x_2, buff_x_3],
         # 普通模式act_outs、进化后act_outs、进化台词普通到进化、进化台词进化到普通
         cst_x1, rec_x1, cst_x2, rec_x2, ["为吾主献出心脏！"], ["我的表现还不错吧~（脸红低头）"]),

        (pink("誓约：不朽！"), f"+3精准 +5闪避 +5%伤害\n+3%暴击 +2速度 +10%防御\n{pink('羁绊物品')}：绷带",
         "overlays/tray_quirk.Love_Grade_Y2.png", [acc_3, def_5, dmg_l5, dmg_h5, crit_3, spd_2, prot_10],
         ItemID.SUPPLY_BANDAGE, [buff_y_1, buff_y_2],
         cst_y1, rec_y1, cst_y2, rec_y2, ["虽然不想承认...但还是忍不住想守护你！"], ["别太得寸进尺了！（嘟嘴）"]),

        (pink("誓约：！"), f"+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{pink('羁绊物品')}：圣水",
         "overlays/tray_quirk.Love_Grade_X2.png", [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
         ItemID.SUPPLY_HOLY_WATER, [buff_x_1, buff_x_2, buff_x_3],
         cst_x1, rec_x1, cst_x2, rec_x2, ["我的魔法终于成功了！"], ["看来还是要再完善完善..."]),
        (pink("誓约：！"), f"+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{pink('羁绊物品')}：圣水",
         "overlays/tray_quirk.Love_Grade_X2.png", [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
         ItemID.SUPPLY_HOLY_WATER, [buff_x_1, buff_x_2, buff_x_3],
         cst_x1, rec_x1, cst_x2, rec_x2, ["不要小看读书人！（摘下眼镜）"], ["呜？被看到不淑女的样子了~（戴上眼镜）"]),
        (pink("誓约：！"), f"+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{pink('羁绊物品')}：圣水",
         "overlays/tray_quirk.Love_Grade_X2.png", [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
         ItemID.SUPPLY_HOLY_WATER, [buff_x_1, buff_x_2, buff_x_3],
         cst_x1, rec_x1, cst_x2, rec_x2, ["让汝们见识下神明真正的实力！"], ["呼呼，饿，想吃小鱼干~"]),
        (pink("誓约：！"), f"+3精准 +3闪避\n+8%伤害 +5%暴击 +2速度\n{pink('羁绊物品')}：圣水",
         "overlays/tray_quirk.Love_Grade_X2.png", [acc_3, def_3, dmg_l8, dmg_h8, crit_5, spd_2],
         ItemID.SUPPLY_HOLY_WATER, [buff_x_1, buff_x_2, buff_x_3],
         cst_x1, rec_x1, cst_x2, rec_x2, ["我的眼里只有领主呢！"], ["领主，今天怎么回来晚了？"])
    ]

    special_quirks = []
    special_quirks_tw = []
    for i, data in enumerate(special_quirks_data):
        special_quirks.append(Quirk(
            str_quirk_name=data[0],
            str_quirk_description=data[1],
            str_ui_entering="CALM",
            buffs=data[3] + [Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=resistance,
                amount=0.05,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HAS_ITEM_ID if isinstance(data[4], ItemID) else BuffRuleType.HAS_ITEM_TYPE,
                    rule_data_string=data[4]
                )
            ) for resistance in [
                STResistance.STUN,
                STResistance.BLEED,
                STResistance.POISON,
                STResistance.DEBUFF,
                STResistance.TRAP,
                STResistance.MOVE,
                STResistance.DISEASE
            ]],
            analytics_enabled=True,
            show_explicit_buff_description=True,
            show_flavor_description=True,
            random_chance=0,
            is_positive=True,
            is_disease=False,
            classification=QuirkClassification.MENTAL,
            tags=[QuirkTag.CANT_LOCK],
            can_modify_in_activity=True,
            can_remove_with_camping_skill=False,
            can_be_replaced_by_new_quirk=False,
            evolution_duration_min=31,
            evolution_duration_max=75,
            combat_start_turn_act_outs=data[6],
            reaction_act_outs=data[7],
            evolution_quirk_bark=data[10]
        ))

        special_quirks_tw.append(Quirk(
            str_quirk_name=data[0] + skill_unselectable("TW"),
            str_quirk_description=data[1],
            str_ui_entering="TW!",
            tray_quirk_image=data[2],
            buffs=data[3] + [Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=resistance,
                amount=0.05,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HAS_ITEM_ID if isinstance(data[4], ItemID) else BuffRuleType.HAS_ITEM_TYPE,
                    rule_data_string=data[4]
                )
            ) for resistance in [
                STResistance.STUN,
                STResistance.BLEED,
                STResistance.POISON,
                STResistance.DEBUFF,
                STResistance.TRAP,
                STResistance.MOVE,
                STResistance.DISEASE
            ]] + data[5],
            analytics_enabled=True,
            show_explicit_buff_description=True,
            show_flavor_description=True,
            random_chance=0,
            is_positive=True,
            is_disease=False,
            classification=QuirkClassification.MENTAL,
            tags=[QuirkTag.CANT_LOCK],
            can_modify_in_activity=True,
            can_remove_with_camping_skill=False,
            can_be_replaced_by_new_quirk=False,
            evolution_duration_min=22,
            evolution_duration_max=30,
            combat_start_turn_act_outs=data[8],
            reaction_act_outs=data[9],
            evolution_quirk_bark=data[11]
        ))

    # 为特殊怪癖添加进化和回退怪癖
    for i in range(len(special_quirks_data)):
        special_quirks[i].evolution_class_id = special_quirks_tw[i]
        special_quirks_tw[i].evolution_class_id = special_quirks[i]

    # 从好感度100%进化为特殊怪癖的台词
    change_quirk_barks = [
        ["此身，此剑，皆由您来掌控，因为您是我的爱，我的王...我唯一的光。",
         "当我沿着泥泞的道路来到这里，我本以为满是黑暗，但在您身上我看到了光明...请使用我吧，从今往后，我便是您的利刃。"],
        ["什，什么嘛...唉？这个是送我的吗？",
         "盾？习惯了就不重哟，毕竟…人家的力量还是很强的！"],
        ["啊...我们的关系变化真是魔法级别的...简直比魔法还像魔法，要知道我从未像如此，对一个人目不转睛。",
         "我的身体好像发生了某种进化，而触发反应的催化剂...是你的手吗？"],
        ["呼呼，要不要一起来读几首情诗呢，领主？",
         "领、领主...这种展开是不是该换个地方...啊啊我究竟在说什么！"],
        ["虽然是汝召唤了吾，但还请不要摸吾的翅膀~（撇嘴~）",
         "吾可以实现汝的愿望，唉？乱碰可不行..."],
        ["这身体的灼热、内心的鼓动……终于等到您了，领主",
         "是对其他女孩子做这种事，就要给您一点惩罚了哦。"]
    ]
    normal_quirks[9].use_item_changes = [
        UseItemChange(
            change_quirk_class_id=quirk,
            item_id=supplies[i + 1],
            item_type=supplies[i].item_type,
            change_quirk_bark=change_quirk_barks[i]
        ) for i, quirk in enumerate(special_quirks)
    ]

    # 普通怪癖、特殊怪癖、特殊怪癖TW
    total_quirks = normal_quirks + special_quirks + special_quirks_tw

    # 添加不兼容怪癖
    for quirk in total_quirks:
        quirk.incompatible_quirks = [q for q in total_quirks if q != quirk]

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entries(supplies)
    writer.add_entries(total_quirks)
    writer.export(MOD_NAME)
