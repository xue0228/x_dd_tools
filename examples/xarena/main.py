import os

MOD_NAME = "xarena"
os.environ["AUTO_NAME_PREFIX"] = MOD_NAME

from xddtools import get_dd_writer
from xddtools.magic import ALL_HEROES

from xddtools.entries import Project, LootTable, Loot, CampingSkill, CampingSkillEffect, Buff
from xddtools.enum import ProjectTag, ItemType, ItemID, CampingSkillEffectType, CampingSkillSelection, BuffType, \
    STResistance, BuffDurationType

if __name__ == '__main__':
    project = Project(
        title="斗技场饰品扎营技能",
        # preview_icon_image="preview_icon.png",
        tags=[ProjectTag.GAMEPLAY_TWEAKS]
    )

    # 补给品掉落表
    supply_loot = LootTable(loot_entries=[
        Loot(chances=0),
        Loot(chances=1, item_type=ItemType.PROVISION, item_id="", item_amount=2),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_ANTIVENOM, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_BANDAGE, item_amount=1),
        Loot(chances=0, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_HOLY_WATER, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_LAUDANUM, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_MEDICINAL_HERBS, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SHOVEL, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SKELETON_KEY, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_TORCH, item_amount=1),
        Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SPICE, item_amount=1)
    ])

    # 货币掉落表
    heirloom_loot = LootTable(loot_entries=[
        Loot(chances=0),
        Loot(chances=3, item_type=ItemType.GOLD, item_id="", item_amount=1000),
        Loot(chances=3, item_type=ItemType.SHARD, item_id="", item_amount=10),
        Loot(chances=5, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_BUST, item_amount=1),
        Loot(chances=5, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_CREST, item_amount=1),
        Loot(chances=5, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_DEED, item_amount=1),
        Loot(chances=5, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_PORTRAIT, item_amount=1),
        Loot(chances=0, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_BLUEPRINT, item_amount=1),
        Loot(chances=1, item_type=ItemType.HEIRLOOM, item_id=ItemID.HEIRLOOM_MEMORY, item_amount=1),
    ])

    # 总掉落表
    supply = LootTable(loot_entries=[
        Loot(chances=10),
        Loot(chances=2, trinket_rarity="arena_SP"),
        # Loot(chances=200, trinket_rarity="arena_SP"),
        Loot(chances=44, loot_table_id=supply_loot),
        Loot(chances=44, loot_table_id=heirloom_loot)
    ])

    camping_skill = CampingSkill(
        camping_skill_name="死斗",
        camping_skill_image="preview_icon.png",
        str_camping_skill_barks=["鲜血！胜利！", "我就是斗技场之王！", "荣耀即吾命！"],
        cost=1,
        use_limit=2,
        hero_classes=ALL_HEROES,
        effects=[
            CampingSkillEffect(
                effect_type=CampingSkillEffectType.LOOT,
                sub_type=supply,
                amount=1,
                selection=CampingSkillSelection.SELF,
                effect_tooltip="获得死斗战利品"
            ),
            CampingSkillEffect(
                effect_type=CampingSkillEffectType.BUFF,
                sub_type=Buff(
                    stat_type=BuffType.RESISTANCE,
                    stat_sub_type=STResistance.DEATH_BLOW,
                    amount=0.1,
                    duration_type=BuffDurationType.QUEST_END,
                    duration=1,
                    is_clear_debuff_valid=False
                ),
                amount=-0.20,
                chance=0.8,
                selection=CampingSkillSelection.SELF
            )
        ]
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entry(camping_skill)
    writer.export(MOD_NAME)
