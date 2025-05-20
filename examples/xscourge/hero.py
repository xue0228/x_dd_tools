from constants import MOD_NAME
from modes import mode_base
from skills import skills
from xddtools.entries import Hero, Resistance, Weapon, Armour, ActivityModify, Effect, Buff, Generation, \
    ActoutDisplay, HealthBar, HeroLocalization, RaidStartingItem
from xddtools.enum import TagID, TownActivityType, QuirkType, EffectTarget, CurioResultType, BuffSource, BuffType, \
    InnerFx, ItemType, ItemID

hero = Hero(
    entry_id=MOD_NAME,
    id_index=101,
    target_rank=2,
    can_select_combat_skills=False,
    number_of_selected_combat_skills_max=12,
    resistances=Resistance(
        stun=0.6,
        poison=0.0,
        bleed=0.0,
        disease=0.6,
        move=0.4,
        debuff=0.4,
        death_blow=0.67,
        trap=0.1
    ),
    weapons=[
        Weapon(attack=0, damage_low=1, damage_high=11, critical_rate=-1, speed=8),
        Weapon(attack=0, damage_low=1, damage_high=21, critical_rate=-1, speed=10)
    ],
    armours=[
        Armour(defense=0.1, protection=0, hp=26, speed=0),
        Armour(defense=0.3, protection=0, hp=46, speed=0)
    ],
    weapon_images=[f"icons_equip/eqp_weapon_{i}.png" for i in range(5)],
    armour_images=[f"icons_equip/eqp_armour_{i}.png" for i in range(5)],
    guild_header_image_path="hero/Scourge_guild_header.png",
    portrait_roster_image_path="hero/Scourge_portrait_roster.png",
    tags=[TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE],
    can_self_party=False,
    activity_modifier=ActivityModify(
        activity_ids=[
            TownActivityType.BROTHEL,
            TownActivityType.BAR,
            TownActivityType.GAMBLING,
            TownActivityType.TREATMENT,
            TownActivityType.DISEASE_TREATMENT
        ],
        stress_removal_amount_low=50,
        stress_removal_amount_high=100
    ),
    quirk_modifier=[
        QuirkType.NEGATIVE_ENLIGHTENED,
        QuirkType.NEGATIVE_FLAGELLANT,
        QuirkType.NEGATIVE_UNQUIET_MIND,
        QuirkType.NEGATIVE_WITNESS,
        QuirkType.NEGATIVE_FAITHLESS,
        QuirkType.POSITIVE_MEDITATOR,
        QuirkType.NEGATIVE_GOD_FEARING,
        QuirkType.POSITIVE_WARRIOR_OF_LIGHT,
        QuirkType.NEGATIVE_DIURNAL,
        QuirkType.NEGATIVE_FEAR_OF_UNHOLY,
        QuirkType.NEGATIVE_LYGOPHOBIA,
        QuirkType.POSITIVE_PHOTOMANIA,
        QuirkType.POSITIVE_EARLY_RISER,
        QuirkType.NEGATIVE_NIGHT_BLINDNESS,
        QuirkType.NEGATIVE_SATANOPHOBIA,
        QuirkType.POSITIVE_SPIRITUAL,
        QuirkType.DISEASE_VAMPIRE_PASSIVE,
    ],
    base_mode=mode_base,
    crit_effects=[
        Effect(
            target=EffectTarget.PERFORMER,
            refreshes_skill_uses=True
        ),
        Effect(
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            buff_source_type=BuffSource.CRIT,
            duration=3,
            buff_ids=[
                Buff(
                    stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                    amount=0.2
                )
            ]
        )
    ],
    skills=skills,
    generation=Generation(card_chance=100, number_of_cards_in_deck=100, number_of_random_combat_skills=12),
    actout_display=ActoutDisplay(
        attack_friendly_anim="riposte",
        attack_friendly_targchestfx=InnerFx.BLOOD_SPLATTER
    ),
    health_bar=HealthBar(current_top="#FFC0CB"),
    raid_starting_hero_items=[
        RaidStartingItem(
            item_type=ItemType.SUPPLY,
            item_id=ItemID.SUPPLY_SKELETON_KEY,
            item_amount=1
        )
    ],
    hero_localization=HeroLocalization(
        hero_class_name="灾厄",
        blacksmith_verbose="",
        guild_verbose="",
        camping_verbose="",
        weapon_upgrade="镰斧",
        weapon_0="破烂的折叠镰刀",
        weapon_1="银质折叠镰斧",
        weapon_2="灵能镰斧",
        weapon_3="契约镰斧",
        weapon_4="“忠告”",
        armour_upgrade="装束",
        armour_0="赤身裸体",
        armour_1="简单的遮蔽",
        armour_2="合身的着装",
        armour_3="量身定制的装束",
        armour_4="“纵欲”"
    )
)
