from xddtools import AutoName

MOD_NAME = "xhunter"
AutoName.set_default_prefix(MOD_NAME)

from xddtools.entries.colour import notable, skill_unselectable
from xddtools.enum import ProjectTag, BuffType, STCombatStatMultiply, BuffRuleType, ActorStatus, TrinketRarityType, \
    HealSource, TrinketTriggerType, EffectTarget, STCombatStatAdd, QuirkType
from xddtools.entries import TrinketSet, Trinket, Project, Buff, BuffRule, Effect, TrinketEffect
from xddtools.writers import get_dd_writer

if __name__ == '__main__':
    project = Project(
        title="猎领秘藏",
        preview_icon_image="preview_icon.png",
        tags=[ProjectTag.TRINKETS]
    )

    t_set = TrinketSet(
        str_inventory_set_title="“猎领秘藏”",
        buffs=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                amount=0.2,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.ACTOR_STATUS,
                    rule_data_string=ActorStatus.TAGGED
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                amount=0.2,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.ACTOR_STATUS,
                    rule_data_string=ActorStatus.TAGGED
                )
            )
        ]
    )

    t1 = Trinket(
        str_inventory_title_trinket="贮忆枷锁",
        inv_trinket_image="trinket/inv_trinket+cometenhance1.png",
        rarity=TrinketRarityType.COMET,
        shard=25,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.RESOLVE_XP_BONUS_PERCENT,
                amount=-1,
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.10,
            )
        ]
    )

    t2 = Trinket(
        str_inventory_title_trinket="汲光透镜",
        inv_trinket_image="trinket/inv_trinket+cometenhance2.png",
        rarity=TrinketRarityType.COMET,
        shard=35,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.SCOUTING_CHANCE,
                amount=0.2,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.LIGHT_BELOW,
                    rule_data_float=1
                )
            )
        ]
    )

    t3 = Trinket(
        str_inventory_title_trinket="“下一口”",
        inv_trinket_image="trinket/inv_trinket+cometenhance3.png",
        rarity=TrinketRarityType.COMET,
        shard=15,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                stat_sub_type=HealSource.EAT,
                amount=1
            ),
            Buff(
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                amount=0.1
            )
        ]
    )

    t4 = Trinket(
        str_inventory_title_trinket="湛蓝戒指",
        inv_trinket_image="trinket/inv_trinket+cometenhance4.png",
        rarity=TrinketRarityType.COMET,
        shard=35,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=-0.75
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        dot_hp_heal=2,
                        duration=2,
                        on_miss=True
                    )
                ]
            )
        ]
    )

    t5 = Trinket(
        str_inventory_title_trinket="侥幸铸币",
        inv_trinket_image="trinket/inv_trinket+cometenhance5.png",
        rarity=TrinketRarityType.COMET,
        shard=35,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.SCOUTING_CHANCE,
                amount=0.35
            ),
            Buff(
                stat_type=BuffType.PARTY_SURPRISE_CHANCE,
                amount=0.35
            )
        ]
    )

    t6 = Trinket(
        str_inventory_title_trinket="碎心晶剑",
        inv_trinket_image="trinket/inv_trinket+cometenhance6.png",
        rarity=TrinketRarityType.COMET,
        shard=75,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.GUARD_BLOCKED
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
                amount=1
            ),
            Buff(
                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                amount=1
            )
        ]
    )

    t7 = Trinket(
        str_inventory_title_trinket="晶石护卫",
        inv_trinket_image="trinket/inv_trinket+cometenhance7.png",
        rarity=TrinketRarityType.COMET,
        shard=75,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                amount=-0.25
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        health_damage_blocks=1,
                        on_miss=True,
                        apply_once=True
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        clear_guarding=True,
                        clear_guarded=True,
                        on_miss=True,
                        apply_once=True,
                        has_description=False
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        clear_guarding=True,
                        clear_guarded=True,
                        on_miss=True,
                        has_description=False
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        guard=True,
                        on_miss=True,
                        duration=3
                    )
                ]
            )
        ]
    )

    t8 = Trinket(
        str_inventory_title_trinket="传世琼浆",
        inv_trinket_image="trinket/inv_trinket+cometenhance8.png",
        rarity=TrinketRarityType.COMET,
        shard=75,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=0.2
            ),
            Buff(
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=0.2,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HAS_QUIRK,
                    rule_data_string=QuirkType.POSITIVE_HIPPOCRATIC,
                    rule_data_string_tooltip=notable("悬壶济世")
                )
            ),
            Buff(
                stat_type=BuffType.UPGRADE_DISCOUNT,
                stat_sub_type=AutoName().new_sub_type(),
                buff_stat_tooltip=f"友方技能：自身：获得{notable('悬壶济世')}{skill_unselectable('(2%%基础概率)')}"
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        chance=0.02,
                        disease=QuirkType.POSITIVE_HIPPOCRATIC,
                        apply_once=True,
                        has_description=False
                    )
                ]
            )
        ]
    )

    t9 = Trinket(
        str_inventory_title_trinket="幽燃风灯",
        inv_trinket_image="trinket/inv_trinket+cometenhance9.png",
        rarity=TrinketRarityType.COMET,
        shard=35,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.AMBUSH_CHANCE,
                amount=-1
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        heal_stress=2,
                        clear_dot_stress=True
                    )
                ]
            )
        ]
    )

    t10 = Trinket(
        str_inventory_title_trinket="贪餍食客",
        inv_trinket_image="trinket/inv_trinket+cometenhance10.png",
        rarity=TrinketRarityType.COMET,
        shard=75,
        set_id=t_set,
        buffs=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.SPEED_RATING,
                amount=3
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        duration=3,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                                amount=0.35
                            ),
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                                amount=0.35
                            ),
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.CRIT_CHANCE,
                                amount=0.1
                            )
                        ]
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP_OTHER,
                        duration=3,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                                amount=-0.15
                            ),
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                                amount=-0.15
                            )
                        ]
                    )
                ]
            )
        ]
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entries([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
    writer.export(MOD_NAME)
