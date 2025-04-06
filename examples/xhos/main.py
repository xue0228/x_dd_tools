from xddtools import AutoName, get_dd_writer
from xddtools.entries import Project, Loot, TrinketEffect, Trinket, TrinketRarity, Colour, LootMonster, LootTable, \
    Effect, Buff, Item, BuffRule, TrinketSet, Bank, Animation, ActorDot, DurationElement
from xddtools.entries.buff_rule import BuffRuleType
from xddtools.enum import ProjectTag, TrinketRarityType, TrinketTriggerType, TrinketAwardCategory, EffectTarget, \
    BuffDurationType, BuffType, STCombatStatMultiply, STCombatStatAdd, ActorStatus, BuffSource, \
    ActorDotUpdateDurationType
from xddtools.magic import get_summon_loot_monster_effect, get_hero_fx_sfx_buff, get_str_tooltip_effect, \
    get_title_effect, copy_and_rename_hero_fx, get_trinket_effect_sfx

MOD_NAME = "xhos"
AutoName.set_default_prefix(MOD_NAME)

if __name__ == '__main__':
    # MOD 信息
    project = Project(
        title="风暴英雄饰品包",
        preview_icon_image="others/storm_ui_bundles_h15_bconchampionshipbundle.png",
        tags=[ProjectTag.TRINKETS]
    )
    # 写入器
    writer = get_dd_writer(MOD_NAME)

    # 饰品稀有度
    trinket_rarity = TrinketRarity(
        award_category=TrinketAwardCategory.TROPHY,
        insert_before=TrinketRarityType.CROW,
        # trinket_rarity_title=hos_colour(text="风暴英雄"),
        trinket_rarity_title="风暴英雄",
        rarity_image="trinket/rarity_hos.png"
    )

    # 定义饰品稀有度颜色
    # 饰品稀有度的名称中不能有颜色标签，而是要通过定义与饰品稀有度同名的颜色来实现自定义颜色功能
    hos_colour = Colour(
        entry_id=trinket_rarity.id(),
        rgba=(64, 188, 239, 255)
        # rgba="#40bcef"
    )

    trinket_set = TrinketSet(
        str_inventory_set_title="See you in the Nexus!",
        buffs=[
            Buff(
                stat_type=BuffType.PARTY_SURPRISE_CHANCE,
                amount=1
            ),
            Buff(
                stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
                amount=1
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=1
            )
        ]
    )

    item_0 = Item(
        effect=Effect(
            target=EffectTarget.PERFORMER_GROUP,
            dot_hp_heal=1,
            duration=3
        ),
        base_stack_limit=2,
        sell_gold_value=1000,
        estate_can_be_provision=False,
        item_image="item/item_unknown2.png",
        str_inventory_title="恢复之球",
        str_inventory_description="不吃球，你打什么风暴英雄？",
        fx=Animation(anim_dir="fx/cure_target"),
        sfx=Bank(audio="audio/SpiderQueen_Draft_BanRed00.ogg"),
    )

    # 用于实现击杀掉落的虚拟怪物
    loot_monster_0 = LootMonster(
        loot=LootTable(
            loot_entries=[
                Loot(chances=83),
                Loot(trinket_rarity=trinket_rarity, chances=2),
                Loot(
                    item_type=item_0.item_type,
                    item_id=item_0,
                    item_amount=1,
                    chances=15
                )
            ]
        )
    )

    # 水晶饰品，佩戴后击杀怪物有几率获得风暴英雄饰品
    trinket_0 = Trinket(
        rarity=TrinketRarityType.COMET,
        set_id=trinket_set,
        shard=0,
        limit=1,
        buffs=[
            Buff(
                stat_type=BuffType.PARTY_SURPRISE_CHANCE,
                amount=-0.2
            ),
            Buff(
                stat_type=BuffType.RESOLVE_CHECK_PERCENT,
                amount=0.2
            ),
            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/RavenLord_PlayerRejoin00.ogg"))
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.KILL_PERFORMER,
                effects=[
                    get_summon_loot_monster_effect(loot_monster_0),
                    Effect(
                        target=EffectTarget.TARGET,
                        duration=1,
                        buff_ids=[
                            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/RavenLord_SpreeMax00.ogg"),
                                                 duration=1)]
                    ),
                    get_str_tooltip_effect(f"机率获得{hos_colour(text='风暴英雄')}饰品或恢复之球", target=EffectTarget.TARGET)
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.KILL_ALL_HEROES,
                effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        buff_duration_type=BuffDurationType.QUEST_END,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.RESOLVE_XP_BONUS_PERCENT,
                                amount=0.05
                            )
                        ]
                    )
                ]
            )
        ],
        str_inventory_title_trinket="风暴要火！",
        inv_trinket_image="trinket/storm_ui_glues_store_bundle_heroes.png"
    )

    item_1 = Item(
        effect=Effect(
            target=EffectTarget.PERFORMER,
            heal_percent=0.05,
            heal_stress=5
        ),
        base_stack_limit=100,
        sell_gold_value=500,
        estate_can_be_provision=False,
        item_image="item/item_unknown.png",
        str_inventory_title="黑暗灵魂石",
        str_inventory_description="曾经有个战士以为把灵魂石插在自己额头上还可以安然无恙，这真是个无聊可悲的故事。",
        fx=Animation(anim_dir="fx/cure_target_red"),
        sfx=Bank(audio="audio/Diablo_Healed_Evo00.ogg"),
    )

    loot_monster_1 = LootMonster(
        loot=LootTable(
            loot_entries=[
                Loot(chances=1),
                Loot(
                    item_type=item_1.item_type,
                    item_id=item_1,
                    item_amount=1,
                    chances=1
                ),
                Loot(
                    item_type=item_1.item_type,
                    item_id=item_1,
                    item_amount=2,
                    chances=1
                )
            ]
        )
    )

    # 风暴英雄饰品，迪亚波罗
    trinket_1 = Trinket(
        rarity=trinket_rarity,
        set_id=trinket_set,
        price=0,
        limit=1,
        buffs=[
            Buff(
                stat_type=BuffType.STUN_CHANCE,
                amount=0.4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=0
                )
            ),
            Buff(
                stat_type=BuffType.STUN_CHANCE,
                amount=0.4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=1
                )
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=0
                )
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=1
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.MAX_HP,
                amount=0.1,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HAS_ITEM_ID,
                    rule_data_string=item_1,
                    rule_data_string_tooltip="黑暗灵魂石"
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
                amount=0.1,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HAS_ITEM_ID,
                    rule_data_string=item_1
                )
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            ),
            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/Diablo_Pissed00.ogg"))
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.KILL_PERFORMER,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="黑暗灵魂石",
                        text_color=(64, 188, 239),
                        target=EffectTarget.TARGET,
                        sfx=Bank(audio="audio/Diablo_Kill04.ogg")
                    ),
                    get_summon_loot_monster_effect(loot_monster_1),
                    get_str_tooltip_effect("机率获得黑暗灵魂石", target=EffectTarget.TARGET)
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.MELEE_ATTACK_SKILL,
                effects=[
                    get_title_effect(hero="xjiangshi", text="暗影冲锋", text_color=(64, 188, 239)),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        pull=3,
                        queue=False
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1,
                        push=3,
                        stun=1
                    )
                ]
            )
        ],
        str_inventory_title_trinket="迪亚波罗",
        inv_trinket_image="trinket/storm_lootspray_static_carbots_diablo.png"
    )

    # 风暴英雄饰品，缝合怪
    trinket_2 = Trinket(
        str_inventory_title_trinket="缝合怪",
        inv_trinket_image="trinket/storm_lootspray_static_carbots_stitches.png",
        rarity=trinket_rarity,
        set_id=trinket_set,
        price=0,
        limit=1,
        buffs=[
            Buff(
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                amount=0.4
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.1,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=0
                )
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.2,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=1
                )
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.3,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=2
                )
            ),
            Buff(
                stat_type=BuffType.MOVE_CHANCE,
                amount=0.4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=3
                )
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            ),
            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/Stitches_IntroBoast00.ogg"))
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.MELEE_ATTACK_SKILL,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="屠钩",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/Stitches_Taunt_Evo00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1,
                        pull=3
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.5,
                        tag=True
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_CRIT,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="吞噬",
                        text_color=(64, 188, 239),
                        # sfx=Bank(audio="audio/Stitches_Healed01.ogg")
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        heal_percent=0.1
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        buff_duration_type=BuffDurationType.QUEST_END,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.HP_DOT_POISON_AMOUNT_PERCENT,
                                amount=0.1
                            )
                        ]
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.WAS_HIT_ALL_MONSTERS,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="恶臭胆汁",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/Stitches_Ping_Danger00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1.4,
                        dot_poison=1,
                        duration=3
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        cure_poison=True
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="援手屠钩",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/Stitches_Ping_AssistHero00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        shuffle_target=True,
                        queue=False
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.5,
                        health_damage_blocks=1
                    ),
                    "Clear Guard Performer",
                    "Clear Guard Target",
                    "MAA Guard 1"
                ]
            )
        ]
    )

    # 风暴英雄饰品，诺娃
    trinket_3 = Trinket(
        str_inventory_title_trinket="诺娃",
        inv_trinket_image="trinket/storm_lootspray_static_carbots_nova.png",
        rarity=trinket_rarity,
        set_id=trinket_set,
        price=0,
        limit=1,
        buffs=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
                amount=0.05,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IS_STEALTHED
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IS_STEALTHED
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.SPEED_RATING,
                amount=4,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IS_STEALTHED
                )
            ),
            Buff(
                stat_type=BuffType.IGNORE_GUARD,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IS_STEALTHED
                )
            ),
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
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
                amount=1,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.TARGET_HP_BELOW,
                    rule_data_float=0.1
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.TARGET_HP_BELOW,
                    rule_data_float=0.1
                )
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            ),
            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/Nova_Pissed00.ogg"))
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.WAS_HIT,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="幽灵协议",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/Nova_Ping_Retreat00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        stealth=True,
                        duration=1
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1.4,
                        combat_stat_buff=True,
                        attack_rating_add=-0.15,
                        duration=2
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.RANGED_ATTACK_SKILL,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="精准狙击",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/Nova_UI_Lockin00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        buff_duration_type=BuffDurationType.QUEST_END,
                        duration=1,
                        apply_once=True,
                        buff_source_type=BuffSource.ITEM,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                                amount=0.1,
                                buff_rule=BuffRule(
                                    rule_type=BuffRuleType.RANGED_ONLY
                                )
                            ),
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                                amount=0.1,
                                buff_rule=BuffRule(
                                    rule_type=BuffRuleType.RANGED_ONLY
                                )
                            ),
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_ADD,
                                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                                amount=-0.02,
                                buff_rule=BuffRule(
                                    rule_type=BuffRuleType.RANGED_ONLY
                                )
                            )
                        ]
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        steal_buff_source_type=BuffSource.ITEM,
                        on_hit=False,
                        on_miss=True,
                        has_description=False,
                        apply_once=True
                    ),
                    get_str_tooltip_effect("移除所有物品增益", on_hit=False, on_miss=True),
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        tag=True,
                        duration=2,
                        apply_once=True,
                        on_miss=True
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        tag=True,
                        duration=1
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.KILL_PERFORMER,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="三连击",
                        text_color=(64, 188, 239),
                        # 攻击和击杀音效最好只选一个，否则攻击造成击杀时会播放两个音效，影响观感
                        # sfx=Bank(audio="audio/Nova_KillSpreeEnd00.ogg"),
                        target=EffectTarget.TARGET
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1,
                        initiative_change=1,
                        apply_once=True
                    ),
                    get_str_tooltip_effect("获得额外回合", target=EffectTarget.TARGET, on_hit=False, on_miss=False),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1,
                        duration=2,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_ADD,
                                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                                amount=-2,
                                is_clear_debuff_valid=False,
                                buff_rule=BuffRule(
                                    rule_type=BuffRuleType.MELEE_ONLY
                                )
                            )
                        ]
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.5,
                        duration=2,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_ADD,
                                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                                amount=-2,
                                is_clear_debuff_valid=False,
                                buff_rule=BuffRule(
                                    rule_type=BuffRuleType.RANGED_ONLY
                                )
                            )
                        ]
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.FRIENDLY_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        apply_once=True,
                        on_miss=True,
                        duration=1,
                        buff_ids=[
                            get_hero_fx_sfx_buff("xjiangshi", sfx=Bank(audio="audio/Nova_Pissed08.ogg"), duration=1)
                        ]
                    )
                ]
            ),
            # TrinketEffect(
            #     trigger=TrinketTriggerType.ATTACK_CRIT,
            #     effects=[
            #         Effect(
            #             target=EffectTarget.PERFORMER,
            #             apply_once=True,
            #             on_miss=True,
            #             duration=1,
            #             buff_ids=[
            #                 get_hero_fx_sfx_buff("xjiangshi", sfx=Bank(audio="audio/Nova_Pissed10.ogg"), duration=1)
            #             ]
            #         )
            #     ]
            # ),
            TrinketEffect(
                trigger=TrinketTriggerType.MELEE_ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        apply_once=True,
                        on_miss=True,
                        duration=1,
                        buff_ids=[
                            get_hero_fx_sfx_buff("xjiangshi", sfx=Bank(audio="audio/Nova_ByeBye00.ogg"), duration=1)
                        ]
                    )
                ]
            ),
        ]
    )

    actor_dot_0 = ActorDot(
        update_duration_type=ActorDotUpdateDurationType.AFTER_TURN_ATTACK,
        fx=Animation(
            anim_dir="fx/fire",
            is_fx=True,
            need_rename=False,
            hero_name="xjiangshi"
        ),
        duration_elements=[
            DurationElement(
                completion_chance=0.5,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=5
                    )
                ],
                increment_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=100,
                        combat_stat_buff=True,
                        speed_rating_add=-4,
                        duration=2
                    )
                ]
            ),
            DurationElement(
                completion_chance=0.5,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=10
                    )
                ],
                increment_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=100,
                        combat_stat_buff=True,
                        speed_rating_add=-4,
                        duration=2
                    )
                ]
            ),
            DurationElement(
                completion_chance=1,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=15
                    )
                ]
            )
        ]
    )

    actor_dot_1 = ActorDot(
        update_duration_type=ActorDotUpdateDurationType.AFTER_TURN_ATTACK,
        fx=Animation(
            anim_dir="fx/fire",
            is_fx=True,
            need_rename=False,
            hero_name="xjiangshi"
        ),
        duration_elements=[
            DurationElement(
                completion_chance=0.5,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=5
                    ),
                    Effect(
                        target=EffectTarget.TARGET_GROUP_OTHER,
                        chance=0.25,
                        actor_dot=actor_dot_0
                    )
                ],
                increment_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=100,
                        combat_stat_buff=True,
                        speed_rating_add=-4,
                        duration=2
                    )
                ]
            ),
            DurationElement(
                completion_chance=0.5,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=10
                    ),
                    Effect(
                        target=EffectTarget.TARGET_GROUP_OTHER,
                        chance=0.5,
                        actor_dot=actor_dot_0
                    )
                ],
                increment_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=100,
                        combat_stat_buff=True,
                        speed_rating_add=-4,
                        duration=2
                    )
                ]
            ),
            DurationElement(
                completion_chance=1,
                completion_effects=[
                    Effect(
                        target=EffectTarget.TARGET,
                        health_damage=15
                    ),
                    Effect(
                        target=EffectTarget.TARGET_GROUP_OTHER,
                        chance=0.75,
                        actor_dot=actor_dot_0
                    )
                ]
            )
        ]
    )

    # 风暴英雄饰品，凯尔萨斯
    trinket_4 = Trinket(
        str_inventory_title_trinket="凯尔萨斯",
        inv_trinket_image="trinket/storm_lootspray_static_carbots_kaelthas.png",
        rarity=trinket_rarity,
        set_id=trinket_set,
        price=0,
        limit=1,
        buffs=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
                amount=0.25,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.HP_BELOW,
                    rule_data_float=0.4
                ),
                # fx=get_title_fx(
                #     hero="xjiangshi",
                #     text="魔隐者",
                #     text_color=(64, 188, 239)
                # ),
                # fx_onset_sfx=Bank(audio="audio/KaelthasBase_KillDiablo00.ogg")
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=2
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=3
                )
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            ),
            get_hero_fx_sfx_buff(hero="xjiangshi", sfx=Bank(audio="audio/KaelthasBase_Pissed13.ogg"))
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.RANGED_ATTACK_SKILL,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="活体炸弹",
                        text_color=(64, 188, 239),
                        sfx=Bank(audio="audio/KaelthasBase_IntroBoast00.ogg")
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.75,
                        actor_dot=actor_dot_1,
                        has_description=False
                    ),
                    get_str_tooltip_effect("概率施加活体炸弹", target=EffectTarget.PERFORMER, on_hit=True, on_miss=False)
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_CRIT,
                effects=[
                    get_title_effect(
                        hero="xjiangshi",
                        text="引力失效",
                        text_color=(64, 188, 239),
                        # sfx=Bank(audio="audio/KaelthasBase_Taunt02.ogg")
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1.4,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.COMBAT_STAT_ADD,
                                stat_sub_type=STCombatStatAdd.SPEED_RATING,
                                amount=-100
                            ),
                            Buff(
                                stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
                                amount=0.2
                            )
                        ]
                    )
                ]
            ),
            get_trinket_effect_sfx("xjiangshi", TrinketTriggerType.MELEE_ATTACK_SKILL,
                                   Bank(audio="audio/KaelthasBase_Ultimate1Used01.ogg")),
            get_trinket_effect_sfx("xjiangshi", TrinketTriggerType.WAS_HIT,
                                   Bank(audio="audio/KaelthasBase_Ping_AssistMe01.ogg")),
            # get_trinket_effect_sfx("xjiangshi", TrinketTriggerType.KILL_PERFORMER,
            #                        Bank(audio="audio/KaelthasBase_KillSpreeEnd00.ogg")),
            get_trinket_effect_sfx("xjiangshi", TrinketTriggerType.FRIENDLY_SKILL,
                                   Bank(audio="audio/KaelthasBase_IntroResponse_Illidan00.ogg"))
        ]
    )

    writer.add_entry(project)
    writer.add_entry(hos_colour)
    writer.add_entries([loot_monster_0, loot_monster_1])
    writer.add_entries([trinket_0, trinket_1, trinket_2, trinket_3, trinket_4])

    writer.export(MOD_NAME)
    copy_and_rename_hero_fx("xhos/heroes/xjiangshi")
