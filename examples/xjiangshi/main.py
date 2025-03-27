import os.path

from xddtools import AutoName

MOD_NAME = "xjiangshi"
AutoName.set_default_prefix(MOD_NAME)

from xddtools.entries import Resistance, Hero, Weapon, Armour, ActivityModify, Mode, Animation, Effect, \
    HeroLocalization, Generation, Project, ActoutDisplay
from xddtools.enum import TagID, TownActivityType, QuirkType, EffectTarget, CurioResultType, ProjectTag
from xddtools.writers import get_dd_writer
from xddtools.entries.colour import heal_hp, debuff, skill_unselectable, riposte, mark

from skills import skills
from camping_skills import camping_skills


if __name__ == '__main__':
    project = Project(
        title="僵尸",
        preview_icon_image="other_image/preview_icon.png",
        tags=[ProjectTag.NEW_CLASS]
    )

    hero = Hero(
        entry_id=MOD_NAME,
        id_index=100,
        target_rank=1,
        resistances=Resistance(
            stun=0.0,
            poison=0.2,
            bleed=0.2,
            disease=0.5,
            move=0.2,
            debuff=0.4,
            death_blow=0.73,
            trap=0.2
        ),
        weapons=[
            Weapon(attack=0, damage_low=6, damage_high=12, critical_rate=0.01, speed=5),
            Weapon(attack=0, damage_low=10, damage_high=19, critical_rate=0.05, speed=7)
        ],
        armours=[
            Armour(defense=0, protection=0.04, hp=26, speed=0),
            Armour(defense=0, protection=0.12, hp=46, speed=0)
        ],
        weapon_images=[f"icons_equip/eqp_weapon_{i}.png" for i in range(5)],
        armour_images=[f"icons_equip/eqp_armour_{i}.png" for i in range(5)],
        guild_header_image_path="other_image/jiangshi_guild_header.png",
        portrait_roster_image_path="other_image/jiangshi_portrait_roster.png",
        tags=[TagID.HEAVY, TagID.NON_RELIGIOUS],
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
        base_mode=Mode(
            afflicted=Animation(anim_dir="anim/afflicted"),
            camp=Animation(anim_dir="anim/camp"),
            combat=Animation(anim_dir="anim/combat"),
            defend=Animation(anim_dir="anim/defend"),
            heroic=Animation(anim_dir="anim/heroic"),
            idle=Animation(anim_dir="anim/idle"),
            investigate=Animation(anim_dir="anim/investigate"),
            riposte=Animation(anim_dir="anim/attack_riposte"),
            walk=Animation(anim_dir="anim/walk")
        ),
        crit_effects=[Effect(
            target=EffectTarget.PERFORMER,
            curio_result_type=CurioResultType.POSITIVE,
            heal_stress=10
        )],
        skills=skills,
        generation=Generation(card_chance=100, number_of_cards_in_deck=100),
        actout_display=ActoutDisplay(
            attack_friendly_anim=skills[0].anim.id(),
            attack_friendly_fx=skills[0].fx.id(),
            attack_friendly_targchestfx=skills[0].targchestfx.id(),
            attack_friendly_sfx=f"/char/ally/{MOD_NAME}_{skills[0].id()}"
        ),
        hero_localization=HeroLocalization(
            hero_class_name="僵尸",
            blacksmith_verbose="僵尸用她的爪子撕咬敌人，让她甚至可以打破最坚固的盔甲:虽然她有一个年轻女子的外表，她可以用她的恐怖的一面让敌人措手不及",
            guild_verbose="僵尸是一种不死生物，能够用其非人的力量摧毁敌人的防御;虽然她的双眼失明，但她能够感知活人的呼吸，使她能够确定她的目标，并吸取他们的精气",
            camping_verbose="僵尸保留了她生前的大部分个性，用她的音乐天赋来安抚她新结识的“朋友”，尽管她经常在夜里静静地离开",
            weapon_upgrade="僵尸之爪",
            weapon_0="腐烂之手",
            weapon_1="再生之手",
            weapon_2="骇人之手",
            weapon_3="磨砺的利爪",
            weapon_4="“放血者”",
            armour_upgrade="僵尸符咒",
            armour_0="残破的符咒",
            armour_1="劣质的符咒",
            armour_2="修复的符咒",
            armour_3="未完成的符咒",
            armour_4="“敕令：随身保命”"
        )
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entry(hero)
    writer.add_entries(camping_skills)
    writer.add_entries([heal_hp, debuff, skill_unselectable, riposte, mark])
    writer.export(MOD_NAME)
