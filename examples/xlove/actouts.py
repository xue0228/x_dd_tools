from effects import *
from xddtools.entries import CombatStartTurn, Reaction
from xddtools.enum import CombatStartTurnActOuts, ReactionActOuts

# 誓约：残念！
cst_x1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=89
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
        chance=1,
        number_value=0.2,
        string_value=effect_x_1,
        act_out_barks=[
            "任何人都不许后退！",
            "即使是鲜血淋漓，也誓死捍卫吾主！"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=5,
        string_value=effect_x_2,
        act_out_barks=[
            "无上吾主！万王之王！伟大旨意！启明恒星！",
            "挡在吾主路前的，即使是神明我也杀给你看。",
            "为了吾主！",
            "吾主即是我存在的意义。",
            "如果是没有吾主的世界，那就消失吧！"
        ]
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
        act_out_barks=[
            "领主？还需要我吗？",
            "领主！我没有背叛您！"
        ]
    )
]
rec_x1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_x_6,
        act_out_barks=[
            "您只管前进，我会为您承担一切痛楚，请不要停下脚步。",
            "就算此身腐朽，此剑断裂，我也不会停止对吾主之敌的征讨！",
            "我的光芒从未熄灭，吾主就在我的身边照耀！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_ATTACK_MISSED,
        chance=0.1,
        # chance=1,
        effect=effect_x_7,
        act_out_barks=[
            "打起精神！你让我在吾主面前蒙羞！",
            "别松懈！吾主还在看着！"
        ]
    )
]
cst_x2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=89
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
        chance=1,
        number_value=0.2,
        string_value=effect_x_1,
        act_out_barks=[
            "任何人都不许后退！",
            "即使是鲜血淋漓，也誓死捍卫吾主！"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=5,
        string_value=effect_x_2,
        act_out_barks=[
            "无上吾主！万王之王！伟大旨意！启明恒星！",
            "挡在吾主路前的，即使是神明我也杀给你看。",
            "为了吾主！",
            "吾主即是我存在的意义。",
            "如果是没有吾主的世界，那就消失吧！"
        ]
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
        act_out_barks=[
            "为了吾主！", "无上吾主！万王之王！伟大旨意！启明恒星！"
        ]
    )
]
rec_x2 = rec_x1

# 誓约：不朽！
cst_y1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=84
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=1,
        string_value=effect_y_1,
        act_out_barks=[
            "不许离开我！",
            "最讨厌你了！"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=15,
        string_value=effect_y_2,
        act_out_barks=[
            "这样就能提起精神，果然是些无可救药的家伙。",
            "才不是特意想帮你们的！"
        ]
    )
]
rec_y1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_y_3,
        act_out_barks=[
            "没有...我才没有受伤...",
            "呜~领主，大笨蛋！！",
            "怪物什么的...最讨厌了！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.1,
        # chance=1,
        effect="Guard 1",
        act_out_barks=[
            "不要得意忘形了笨蛋！",
            "只是偶然想帮你的啦！",
            "别搞错了...才没有什么别的意思..."
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.01,
        # chance=1,
        effect=effect_y_4
    )
]
cst_y2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=85
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=15,
        string_value=effect_y_2,
        act_out_barks=[
            "这样就能提起精神，果然是些无可救药的家伙。",
            "才不是特意想帮你们的！"
        ]
    )
]
rec_y2 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.1,
        # chance=0,
        effect=effect_y_3,
        act_out_barks=[
            "没有...我才没有受伤...",
            "呜~领主，大笨蛋！！",
            "怪物什么的...最讨厌了！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.05,
        # chance=1,
        effect=effect_y_5
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.1,
        # chance=1,
        effect="Guard 1",
        act_out_barks=[
            "不要得意忘形了笨蛋！",
            "只是偶然想帮你的啦！",
            "别搞错了...才没有什么别的意思..."
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.01,
        # chance=1,
        effect=effect_y_4
    )
]

# 誓约：魔法！
cst_z1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=75
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.ATTACK_FRIENDLY,
        chance=1,
        number_value=0.2,
        string_value="STUN 3",
        act_out_barks=[
            "啊...糟了，读错咒文了...",
            "啊，眼花了..."
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=8,
        string_value=effect_z_1,
        act_out_barks=[
            "加一点毒蘑菇，再来一个旧鞋跟。",
            "来吧，它会让你很兴奋的！",
            "我的魔法会把你撕碎！",
            "这次使用什么魔法好呢？"
        ]
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
    )
]
rec_z1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.01,
        # chance=1,
        effect=effect_z_5,
        act_out_barks=[
            "烦人...",
            "催眠术！",
            "我对傻子的尸体不感兴趣。",
            "再闹腾下去，我就要用魔法强迫你听话了..."
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_z_4,
        act_out_barks=[
            "你的魔法无效！",
            "低级的魔法而已。"
        ]
    )
]
cst_z2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=76
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=8,
        string_value=effect_z_1,
        act_out_barks=[
            "加一点毒蘑菇，再来一个旧鞋跟。",
            "来吧，它会让你很兴奋的！",
            "我的魔法会把你撕碎！",
            "这次使用什么魔法好呢？"
        ]
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
    )
]
rec_z2 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.05,
        # chance=1,
        effect=effect_z_5,
        act_out_barks=[
            "烦人...",
            "催眠术！",
            "我对傻子的尸体不感兴趣。",
            "再闹腾下去，我就要用魔法强迫你听话了..."
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_z_4,
        act_out_barks=[
            "你的魔法无效！",
            "低级的魔法而已。"
        ]
    )
]

# 誓约：知识！
cst_m1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=82
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.CHANGE_POS,
        chance=1,
        number_value=0,
        act_out_barks=[
            "马失前蹄...了呢。",
            "呼呼，我似乎有点醉了~"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=8,
        string_value=effect_m_1,
        act_out_barks=[
            "微风拂过海面，蝉鸣漾入云间。",
            "我总在这里，与你共赏一轮明月。",
            "醉翁之意不在酒，在乎你我之间。"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=8,
        string_value=effect_m_2,
        act_out_barks=[
            "桃之夭夭，灼灼其华。",
            "腐草为萤，耀采于月。",
            "林中落雨，秋前盛夏。"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_PARTY,
        chance=1,
        # chance=10,
        string_value=effect_m_3,
        act_out_barks=[
            "你已被我看破！",
            "攻城为下，攻心为上。"
        ]
    )
]
rec_m1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_m_4,
        act_out_barks=[
            "你还挺擅长趁虚而入...",
            "谈笑有鸿儒，往来无白丁。",
            "相鼠有皮，汝而无仪。"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.01,
        # chance=1,
        effect=effect_m_5
    )
]
cst_m2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=83
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=8,
        string_value=effect_m_1,
        act_out_barks=[
            "微风拂过海面，蝉鸣漾入云间。",
            "我总在这里，与你共赏一轮明月。",
            "醉翁之意不在酒，在乎你我之间。"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=8,
        string_value=effect_m_2,
        act_out_barks=[
            "桃之夭夭，灼灼其华。",
            "腐草为萤，耀采于月。",
            "林中落雨，秋前盛夏。"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_PARTY,
        chance=1,
        string_value=effect_m_3,
        act_out_barks=[
            "你已被我看破！",
            "攻城为下，攻心为上。"
        ]
    )
]
rec_m2 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_m_4,
        act_out_barks=[
            "你还挺擅长趁虚而入...",
            "谈笑有鸿儒，往来无白丁。",
            "相鼠有皮，汝而无仪。"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.01,
        # chance=1,
        effect=effect_m_5
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.05,
        # chance=1,
        effect=effect_m_6,
        act_out_barks=[
            "但凡不能杀死你的，最终都会使你变强。",
            "能被触碰到是确实存在的证明。"
        ]
    )
]

# 誓约：神明！
cst_o1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=66
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.MARK_SELF,
        chance=1,
        act_out_barks=[
            "再摸、再摸吾就生气了！",
            "神明不需要信徒，而是信徒需要神明。"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=3,
        string_value=effect_o_7,
        act_out_barks=[
            "心之所愿，定能如愿！",
            "神明之力，福荫人间！"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_PARTY,
        chance=6,
        string_value=effect_o_1,
        act_out_barks=[
            "汝被强化了，快上~",
            "快显灵...不要给吾丢脸...（默默嘀咕着）",
            "汝笑什么？这可是神明的恩赐！",
            "嘲笑神明可是没有好鱼干吃的！（撇嘴~）"
            "快吃吧，这可是神明的鱼干。"
        ]
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
]
rec_o1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.1,
        # chance=1,
        effect=effect_o_6,
        act_out_barks=[
            "虽然吾不像其他神明一样强大，但仍能治愈这些低级咒术。",
            "吾可是神明，治愈这些低级咒术只是举手之劳。",
            "吾可是神明，不要小看我！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_MISSED,
        chance=0.02,
        # chance=1,
        effect=effect_o_8,
        act_out_barks=[
            "心之所愿，定能如愿！", "神明之力，福荫人间！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_ATTACK_HIT,
        chance=0.02,
        # chance=1,
        effect=effect_o_9,
        act_out_barks=[
            "心之所愿，定能如愿！", "神明之力，福荫人间！"
        ]
    )
]
cst_o2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=64
        # chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_RANDOM_PARTY_MEMBER,
        chance=6,
        string_value=effect_o_7,
        act_out_barks=[
            "心之所愿，定能如愿！",
            "神明之力，福荫人间！"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_PARTY,
        chance=6,
        string_value=effect_o_1,
        act_out_barks=[
            "汝被强化了，快上~",
            "快显灵...不要给吾丢脸...（默默嘀咕着）",
            "汝笑什么？这可是神明的恩赐！",
            "嘲笑神明可是没有好鱼干吃的！（撇嘴~）"
            "快吃吧，这可是神明的鱼干。"
        ]
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
]
rec_o2 = [
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_HIT,
        chance=0.5,
        # chance=1,
        effect=effect_o_6,
        act_out_barks=[
            "虽然吾不像其他神明一样强大，但仍能治愈这些低级咒术。",
            "吾可是神明，治愈这些低级咒术只是举手之劳。",
            "吾可是神明，不要小看我！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_MISSED,
        chance=0.05,
        # chance=1,
        effect=effect_o_8,
        act_out_barks=[
            "心之所愿，定能如愿！", "神明之力，福荫人间！"
        ]
    ),
    Reaction(
        name=ReactionActOuts.COMMENT_ALLY_ATTACK_HIT,
        chance=0.05,
        # chance=1,
        effect=effect_o_9,
        act_out_barks=[
            "心之所愿，定能如愿！", "神明之力，福荫人间！"
        ]
    )
]

# 誓约：恶魔！
cst_n1 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.RANDOM_COMMADN,
        chance=1,
        act_out_barks=[
            "这是为了让领主爱我所必须做的呢~",
            "不要阻止我将她们抹杀！",
            "杀了你，领主就会只看我一个人了"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.ATTACK_SELF,
        chance=99,
        number_value=0.05,
        string_value=effect_n_1,
        act_out_barks=[
            "不可以逃走哦~领主",
            "爱在染满鲜血的时候才是最美丽的呀！",
            "我会杀掉除领主外的所有人...",
            "哈~哈~哈（嘴角出血地笑着）",
            "千万千万不要背叛哟~",
            "你所喜欢的我都会抹杀，那样你就只能爱我了"
        ]
    )
]
rec_n1 = [
    Reaction(
        name=ReactionActOuts.COMMENT_SELF_HIT,
        chance=0.99,
        effect=effect_n_2,
        act_out_barks=[
            "像你这么恶心的怪物，怎么有资格站在领主的旁边",
            "你们也想要接近领主吗？！——呵呵呵",
            "太碍事了……不可原谅!"
        ]
    )
]
cst_n2 = [
    CombatStartTurn(
        name=CombatStartTurnActOuts.NOTHING,
        chance=0
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.BUFF_PARTY,
        chance=1,
        # chance=99,
        string_value=effect_n_3,
        act_out_barks=[
            "你是无法反抗命运的...咦嘻嘻",
            "看过领主的女人都会被我杀死哦~"
        ]
    ),
    CombatStartTurn(
        name=CombatStartTurnActOuts.STRESS_HEAL_SELF,
        chance=99,
        string_value=effect_n_1,
        act_out_barks=[
            "不可以逃走哦~领主",
            "爱在染满鲜血的时候才是最美丽的呀！",
            "我会杀掉除领主外的所有人...",
            "哈~哈~哈（表情冰冷地笑着）",
            "千万千万不要背叛哟~",
            "你所讨厌的我都会抹杀，那样你就会爱我了"
        ]
    )
]
rec_n2 = rec_n1
