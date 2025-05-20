from constants import MOD_NAME
from hero import hero
from trinkets import trinkets, world_colour
from xddtools import get_dd_writer
from xddtools.entries import Project
from xddtools.enum import ProjectTag

if __name__ == '__main__':
    project = Project(
        title="灾厄",
        preview_icon_image="hero/preview_icon.png",
        tags=[ProjectTag.NEW_CLASS]
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entry(hero)
    writer.add_entry(world_colour)
    writer.add_entries(trinkets)
    writer.export(MOD_NAME)
