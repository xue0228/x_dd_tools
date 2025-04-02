from xddtools.base import ProxyWriter
from xddtools.writers.animation import AnimationWriter
from xddtools.writers.buff import BuffWriter
from xddtools.writers.colour import ColourWriter, get_colour_writer
from xddtools.writers.effect import EffectWriter
from xddtools.writers.localization import LocalizationWriter, get_localization_writer
from xddtools.writers.project import ProjectWriter
from xddtools.writers.quirk import QuirkWriter
from xddtools.writers.trinket import TrinketWriter, TrinketSetWriter, TrinketRarityWriter
from xddtools.writers.item import ItemWriter
from xddtools.writers.trait import TraitWriter
from xddtools.writers.loot import LootTableWriter, get_common_overrides_loot_table_writer
from xddtools.writers.camping_skill import CampingSkillWriter
from xddtools.writers.actor_dot import ActorDotWriter
from xddtools.writers.hero import HeroWriter
from xddtools.writers.bank import BankWriter
from xddtools.writers.loot_monster import LootMonsterWriter


def get_dd_writer(prefix: str) -> ProxyWriter:
    writer = ProxyWriter(
        [
            ProjectWriter(prefix),
            TrinketWriter(prefix),
            TrinketSetWriter(prefix),
            TrinketRarityWriter(prefix),
            BuffWriter(prefix),
            EffectWriter(prefix),
            AnimationWriter(prefix),
            QuirkWriter(prefix),
            ItemWriter(prefix),
            TraitWriter(prefix),
            LootTableWriter(prefix),
            CampingSkillWriter(prefix),
            ActorDotWriter(prefix),
            BankWriter(prefix),
            HeroWriter(prefix),
            LootMonsterWriter(prefix),
            get_colour_writer(prefix),
            get_localization_writer(prefix),
        ]
    )
    return writer


# if __name__ == '__main__':
#     from xddtools.entries.loot_monster import LootMonster
#
#     w = get_dd_writer("xue")
#     lo = LootMonster(
#         loot=""
#     )
#     w.add_entry(lo)
#     w.export("test")
