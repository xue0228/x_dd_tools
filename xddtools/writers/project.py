import os.path
from typing import List

from xddtools.base import BaseWriter, Entry, ProjectEntry
from xddtools.entries.project import Project
from xddtools.path import DATA_PATH
from xddtools.utils import write_str_to_file, resize_image_keep_ratio


class ProjectWriter(BaseWriter):
    def __init__(self, prefix: str = ""):
        super().__init__(
            prefix=prefix
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, ProjectEntry)

    def add_entry(self, entry: Project) -> List[Entry]:
        if entry in self._entries:
            return []

        if len(self._entries) > 0:
            raise Exception("Only one project entry allowed")
        self._entries.append(entry)
        return []

    def export(self, root_dir: str = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"
        for entry in self._entries:  # type: Project
            file = os.path.join(root_dir, "project.xml")
            res = [write_str_to_file(file, str(entry))]
            if entry.preview_icon_image is None:
                image_path = os.path.join(DATA_PATH, "template/project/preview_icon.png")
            else:
                image_path = entry.preview_icon_image
            file = os.path.join(root_dir, "preview_icon.png")
            res.append(resize_image_keep_ratio(image_path, file, (512, 512)))
            return res
        return []


if __name__ == '__main__':
    from xddtools.entries.project import Project

    p = Project(title="test")
    w = ProjectWriter("test")
    w.add_entry(p)
    w.add_entry(Project(title="tt"))
    w.export("xue")
