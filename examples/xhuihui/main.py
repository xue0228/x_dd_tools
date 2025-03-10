from effects import *
from skills import skill_0s, skill_1s, skill_2s, skill_3s, skill_move
from quirk import huihui_quirk

from xddtools.colour import buff, notable
from xddtools.animation import Animation
from xddtools.buff_rules import BRMonsterSize
from xddtools.buffs import Buff
from xddtools.effects import Effect, TooltipEffect
from xddtools.enums import EffectTarget, CurioResultType, BuffSource, BuffType, Level, SkillHeadType, SkillType, \
    STDisableCombatSkillAttribute, BuffDurationType, STCombatStatAdd, STCombatStatMultiply
from xddtools.name import AutoName
from xddtools.skills import Skill
from xddtools.target import LAUNCH_ANY, LAUNCH_34, ALL_ENEMY
from xddtools.writers import DDWriter
from xddtools.writers.hero import Mode, Hero, Resistance, Weapon, Armour, Generation, ActoutDisplay, HeroLocalization

MOD_NAME = "xhuihui"
dd_writer = DDWriter(MOD_NAME, preview_icon_file="others/preview_icon.png")
auto_name = AutoName(MOD_NAME)
mode = Mode(
    mode_name="",
    afflicted=Animation("anim/afflicted", ""),
    camp=Animation("anim/camp", ""),
    combat=Animation("anim/combat", ""),
    death=Animation("anim/death", ""),
    defend=Animation("anim/defend", ""),
    heroic=Animation("anim/heroic", ""),
    idle=Animation("anim/idle", ""),
    investigate=Animation("anim/investigate", ""),
    walk=Animation("anim/walk", ""),
)

hero_localization = HeroLocalization(
    hero_class_name="爆裂魔法使",
    blacksmith_verbose="惠惠的装备体现了她爆裂般的魔法。她的魔杖上刻印着复杂的符文，"
                       "能轻易引导并放大她的魔力，使她能够释放毁灭性的爆裂魔法。她的饰有金色装饰的深红色长袍，象征着她炽热的冒险精神。",
    guild_verbose="惠惠拥有无与伦比的爆裂魔法。只要轻声咏唱咒语，她就能散发出巨大的力量，释放出毁灭性的爆裂魔法。"
                  "她对能力的精确控制使她能够将她的魔法引导到集中的爆炸。即使战斗使用次数有限，但她的爆裂魔法会留下持久的影响，将敌人和周围的景物毁灭殆尽。",
    camping_verbose="惠惠释放的爆裂魔法只是她强大的魔力的小小体现，这得益于她调皮和可靠的伙伴逗之助和作为红魔一族特殊的眼瞳。"
                    "她神奇的视力赋予了她非凡的洞察魔力，使她能够准确地发现敌人的弱点并策划如何精确地攻击。",
    weapon_upgrade="魔杖",
    weapon_0="破损魔杖",
    weapon_1="学徒魔杖",
    weapon_2="法师魔杖",
    weapon_3="大魔法师魔杖",
    weapon_4="“红魔法杖”",
    armour_upgrade="长袍",
    armour_0="破烂长袍",
    armour_1="学徒长袍",
    armour_2="法师长袍",
    armour_3="大魔法师长袍",
    armour_4="“红魔法袍”"
)

monster_size_effect = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    chance=1,
    apply_once=True,
    buff_ids=(
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(2),
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(2),
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(3),
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(3),
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(4),
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.25,
            remove_if_not_active=True,
            buff_rule=BRMonsterSize(4),
        ),
    )
)

hero = Hero(
    hero_name=MOD_NAME,
    id_index=100,
    resistances=Resistance(
        stun=0.3, poison=0.3, bleed=0.4, disease=0.3,
        move=0.2, debuff=0.5, death_blow=0.67, trap=0.3,
    ),
    crit_effects=(
        crit_effect,
    ),
    target_rank=3,
    weapons=(
        Weapon(
            level=Level.ZERO,
            attack=0,
            damage_low=6,
            damage_high=11,
            critical_rate=0.02,
            speed=7,
        ),
        Weapon(
            level=Level.FOUR,
            attack=0,
            damage_low=11,
            damage_high=20,
            critical_rate=0.06,
            speed=9,
        ),
    ),
    armours=(
        Armour(
            level=Level.ZERO,
            defense=0.075,
            protection=0,
            hp=26,
            speed=0
        ),
        Armour(
            level=Level.FOUR,
            defense=0.275,
            protection=0,
            hp=46,
            speed=0
        ),
    ),
    weapon_image_path=(
        "icons_equip/eqp_weapon_0.png",
        "icons_equip/eqp_weapon_1.png",
        "icons_equip/eqp_weapon_2.png",
        "icons_equip/eqp_weapon_3.png",
        "icons_equip/eqp_weapon_4.png",
    ),
    armour_image_path=(
        "icons_equip/eqp_armour_0.png",
        "icons_equip/eqp_armour_1.png",
        "icons_equip/eqp_armour_2.png",
        "icons_equip/eqp_armour_3.png",
        "icons_equip/eqp_armour_4.png",
    ),
    guild_header_image_path="others/arch_wizard_guild_header.png",
    portrait_roster_image_path="others/arch_wizard_portrait_roster.png",
    can_select_combat_skills=True,
    number_of_selected_combat_skills_max=4,
    can_self_party=False,
    generation=Generation(number_of_cards_in_deck=1, card_chance=1000),
    actout_display=ActoutDisplay(
        attack_friendly_anim=Animation("anim/attack", auto_name.new_anim()),
        attack_friendly_targchestfx="blood_splatter",
    ),
    base_mode=mode,
    dd_writer=dd_writer,
    hero_localization=hero_localization,
    skills=(
        skill_move,
        *skill_0s,
        *skill_1s,
        *skill_2s,
        *skill_3s,
    ),
)

if __name__ == '__main__':
    dd_writer.add_items((buff, notable, huihui_quirk))
    hero.export(MOD_NAME)
    dd_writer.export(MOD_NAME)
