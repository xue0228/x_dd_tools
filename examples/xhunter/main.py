from xddtools.buff_rules import BRLightBelow, BRHasQuirk
from xddtools.buffs import Buff
from xddtools.colour import notable, buff
from xddtools.effects import Effect
from xddtools.enums import EffectTarget, CurioResultType, BuffType, STCombatStatMultiply, HealSource, \
    STCombatStatAdd, TrinketRarityType, TrinketTriggerType, QuirkType
from xddtools.name import AutoName
from xddtools.trinket import TrinketEntry
from xddtools.writers import DDWriter

if __name__ == '__main__':
    MOD_NAME = "xhunter"
    auto_name = AutoName(MOD_NAME)
    dd_writer = DDWriter(MOD_NAME)
    dd_writer.add_items((notable, buff))
    # localization_writer = get_base_localization_writer(name=MOD_NAME)
    # buff_writer = BuffWriter(name=MOD_NAME, localization_writer=localization_writer)
    # effect_writer = EffectWriter(name=MOD_NAME, buff_writer=buff_writer)
    # colour_writer = ColourWriter(name=MOD_NAME)
    # trinket_writer = Trinket(
    #     name=MOD_NAME,
    #     buff_writer=buff_writer,
    #     effect_writer=effect_writer,
    #     localization_writer=localization_writer,
    #     is_test=True
    # )
    # colour_writer.add_items((
    #     notable,
    #     buff,
    # ))

    # trinket_rarity = TrinketRarity(
    #     rarity_name=auto_name.new_rarity(),
    #     image_path=os.path.join(DATA_PATH, "template/trinket/rarity_comet.png"),
    #     award_category=TrinketAwardCategory.TROPHY,
    #     insert_before=TrinketRarityType.CROW,
    #     localization="水晶"
    # )
    trinket_rarity = TrinketRarityType.COMET

    t1 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="贮忆枷锁",
        image_path="trinket/inv_trinket+cometenhance1.png",
        rarity=trinket_rarity,
        shard=25,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.RESOLVE_XP_BONUS_PERCENT,
                amount=-1,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.10,
            )
        )
    )
    t2 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="汲光透镜",
        image_path="trinket/inv_trinket+cometenhance2.png",
        rarity=trinket_rarity,
        shard=35,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.SCOUTING_CHANCE,
                amount=0.20,
                buff_rule=BRLightBelow(1)
            ),
        )
    )
    t3 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization='“下一口”',
        image_path="trinket/inv_trinket+cometenhance3.png",
        rarity=trinket_rarity,
        shard=15,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                stat_sub_type=HealSource.EAT,
                amount=1,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                amount=0.1,
            )
        )
    )
    t4 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="湛蓝戒指",
        image_path="trinket/inv_trinket+cometenhance4.png",
        rarity=trinket_rarity,
        shard=35,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=-0.75,
            ),
        ),
        special_effects={
            TrinketTriggerType.FRIENDLY_SKILL: (
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.TARGET,
                    dot_hp_heal=2,
                    duration=2,
                    on_miss=True
                ),
            )
        }
    )
    t5 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="侥幸铸币",
        image_path="trinket/inv_trinket+cometenhance5.png",
        rarity=trinket_rarity,
        shard=35,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.SCOUTING_CHANCE,
                amount=0.35,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.PARTY_SURPRISE_CHANCE,
                amount=0.35,
            )
        )
    )
    t6 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="碎心晶剑",
        image_path="trinket/inv_trinket+cometenhance6.png",
        rarity=trinket_rarity,
        shard=75,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.GUARD_BLOCKED,
                amount=1,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
                amount=1,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                amount=1,
            )
        )
    )
    t7 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="晶石护卫",
        image_path="trinket/inv_trinket+cometenhance7.png",
        rarity=trinket_rarity,
        shard=75,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                amount=-0.25,
            ),
        ),
        special_effects={
            TrinketTriggerType.FRIENDLY_SKILL: (
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.PERFORMER,
                    health_damage_blocks=1,
                    on_miss=True,
                    apply_once=True
                ),
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.TARGET,
                    clear_guarding=True,
                    clear_guarded=True,
                    on_miss=True,
                    has_description=False
                ),
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.PERFORMER,
                    clear_guarding=True,
                    clear_guarded=True,
                    on_miss=True,
                    has_description=False
                ),
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.TARGET,
                    curio_result_type=CurioResultType.POSITIVE,
                    guard=True,
                    on_miss=True,
                    apply_once=True,
                    duration=3
                )
            )
        }
    )
    t8 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="传世琼浆",
        image_path="trinket/inv_trinket+cometenhance8.png",
        rarity=trinket_rarity,
        shard=75,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=0.20,
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=0.20,
                buff_rule=BRHasQuirk(QuirkType.POSITIVE_HIPPOCRATIC, localization=f'{notable("悬壶济世")}')
            ),
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.UPGRADE_DISCOUNT,
                stat_sub_type=auto_name.last_trinket(),
                localization=f'友军技能：{buff("增益自身")}：获得{notable("悬壶济世")} (2%%)'
            )
        ),
        special_effects={
            TrinketTriggerType.FRIENDLY_SKILL: (
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.PERFORMER,
                    curio_result_type=CurioResultType.POSITIVE,
                    chance=0.02,
                    disease=QuirkType.POSITIVE_HIPPOCRATIC,
                    apply_once=True,
                    has_description=False
                ),
            )
        }
    )
    t9 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="幽燃风灯",
        image_path="trinket/inv_trinket+cometenhance9.png",
        rarity=trinket_rarity,
        shard=35,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.AMBUSH_CHANCE,
                amount=-1,
            ),
        ),
        special_effects={
            TrinketTriggerType.FRIENDLY_SKILL: (
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.TARGET,
                    heal_stress=2,
                    clear_dot_stress=True,
                ),
            )
        }
    )
    t10 = TrinketEntry(
        trinket_name=auto_name.new_trinket(),
        localization="贪餍食客",
        image_path="trinket/inv_trinket+cometenhance10.png",
        rarity=trinket_rarity,
        shard=75,
        limit=1,
        buffs=(
            Buff(
                buff_name=auto_name.new_buff(),
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.SPEED_RATING,
                amount=3,
            ),
        ),
        special_effects={
            TrinketTriggerType.FRIENDLY_SKILL: (
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.PERFORMER,
                    curio_result_type=CurioResultType.NEGATIVE,
                    duration=3,
                    apply_once=True,
                    buff_ids=(
                        Buff(
                            buff_name=auto_name.new_buff(),
                            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                            amount=0.35,
                        ),
                        Buff(
                            buff_name=auto_name.new_buff(),
                            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                            amount=0.35,
                        ),
                        Buff(
                            buff_name=auto_name.new_buff(),
                            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                            stat_sub_type=STCombatStatMultiply.CRIT_CHANCE,
                            amount=0.10,
                        )
                    )
                ),
                Effect(
                    effect_name=auto_name.new_effect(),
                    target=EffectTarget.PERFORMER_GROUP_OTHER,
                    curio_result_type=CurioResultType.NEGATIVE,
                    duration=3,
                    apply_once=True,
                    buff_ids=(
                        Buff(
                            buff_name=auto_name.new_buff(),
                            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                            amount=-0.15,
                        ),
                        Buff(
                            buff_name=auto_name.new_buff(),
                            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                            amount=-0.15,
                        )
                    )
                )
            )
        }
    )

    # trinket_writer.add_items((
    #     t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
    # ))
    # colour_writer.export(MOD_NAME)
    # trinket_writer.export(MOD_NAME, export_other_writers=True)

    dd_writer.add_items((
        t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
    ))
    dd_writer.export(MOD_NAME)
