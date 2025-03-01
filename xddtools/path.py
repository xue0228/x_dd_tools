import os

BUFF_SAVE_DIR = os.path.join("shared", "buffs")
BUFF_FILE_EXTENSION = ".buffs.json"

QUIRK_SAVE_DIR = os.path.join("shared", "quirk")
QUIRK_IMAGE_SAVE_DIR = "overlays"
QUIRK_LIBRARY_FILE_EXTENSION = ".quirk_library.json"
QUIRK_ACTOUT_FILE_EXTENSION = ".quirk_act_outs.json"

TRAIT_SAVE_DIR = os.path.join("shared", "trait")
TRAIT_LIBRARY_FILE_EXTENSION = ".trait_library.json"

HERO_SAVE_DIR = "heroes"

EFFECT_SAVE_DIR = "effects"
EFFECT_FILE_EXTENSION = ".effects.darkest"

HERO_UPGRADE_SAVE_DIR = os.path.join("upgrades", "heroes")
HERO_UPGRADE_FILE_EXTENSION = ".upgrades.json"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
CONVERTER_PATH = os.path.normpath(os.path.join(DATA_PATH, "Spine.Converter.v1.0.5/Spine Converter v1.0.5.exe"))
LOCALIZE_PATH = os.path.normpath(os.path.join(DATA_PATH, "localize/localization.exe"))

TRINKET_SAVE_DIR = "trinkets"
TRINKET_IMAGE_SAVE_DIR = "panels/icons_equip/trinket"
TRINKET_ENTRY_FILE_EXTENSION = ".entries.trinkets.json"
TRINKET_RARITY_FILE_EXTENSION = ".rarities.trinkets.json"
TRINKET_STARTING_FILE_EXTENSION = ".starting.trinkets.json"
TRINKET_SET_FILE_EXTENSION = ".sets.trinkets.json"

LOCALIZATION_SAVE_DIR = "localization"
LOCALIZATION_FILE_EXTENSION = ".string_table.xml"

COLOUR_SAVE_DIR = "colours"
COLOUR_FILE_EXTENSION = ".colours.darkest"

ITEM_SAVE_DIR = "inventory"
ITEM_FILE_EXTENSION = ".inventory.items.darkest"
ITEM_IMAGE_SAVE_DIR = "panels/icons_equip"

LOOT_TABLE_SAVE_DIR = "loot"
LOOT_TABLE_FILE_EXTENSION = ".loot.json"

CAMPING_SKILL_SAVE_DIR = os.path.join("raid", "camping")
CAMPING_SKILL_FILE_EXTENSION = ".camping_skills.json"
CAMPING_SKILL_IMAGE_SAVE_DIR = os.path.join(CAMPING_SKILL_SAVE_DIR, "skill_icons")


if __name__ == '__main__':
    print(BUFF_SAVE_DIR)
