from xddtools import AutoName

MOD_NAME = "xstress"
AutoName.set_default_prefix(MOD_NAME)

from xddtools.enum import ProjectTag, EffectTarget, ItemType
from xddtools.entries import Project, Effect, Item
from xddtools.writers import get_dd_writer

if __name__ == '__main__':
    project = Project(
        title="压力刷新",
        tags=[ProjectTag.GAMEPLAY_TWEAKS]
    )

    item_1 = Item(
        str_inventory_title="天使的拥抱",
        str_inventory_description="戴上这个光环或许会有好事发生",
        item_image="imgs/heroic.png",
        effect=Effect(
            target=EffectTarget.PERFORMER,
            heal_stress=200
        ),
        item_type=ItemType.SUPPLY,
        base_stack_limit=99,
        purchase_gold_value=1000,
        # purchase_shard_value=10,
        # raid_starting_item_lists=[None, 0, 0, 0, 0, 0],
        # default_store_item_lists=[None, 6, 9, 12, 15, 12],
        sell_gold_value=1000,
        estate_can_be_provision=False
    )

    item_2 = Item(
        str_inventory_title="恶魔的低语",
        str_inventory_description="戴上这个光环或许会有坏事发生",
        item_image="imgs/afflicted.png",
        effect=Effect(
            target=EffectTarget.PERFORMER,
            stress=200
        ),
        item_type=ItemType.SUPPLY,
        base_stack_limit=99,
        purchase_gold_value=1000,
        sell_gold_value=1000,
        estate_can_be_provision=False
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entries([item_1, item_2])
    writer.export(MOD_NAME)
