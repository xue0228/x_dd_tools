from enum import Enum


class ProjectVisibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    FRIENDS = "friends"


class ProjectUploadMode(Enum):
    DIRECT_UPLOAD = "direct_upload"
    COPY_AND_UPLOAD = "copy_and_upload"
    STRIP_AND_UPLOAD = "strip_and_upload"
    DONT_SUBMIT = "dont_submit"


class ProjectTag(Enum):
    GAMEPLAY_TWEAKS = "gameplay tweaks"
    OVERHAULS = "overhauls"
    TRINKETS = "trinkets"
    MONSTERS = "monsters"
    LOCALIZATION = "localization"
    UI = "ui"
    NEW_CLASS = "new class"
    CLASS_TWEAKS = "class tweaks"
    SKINS = "skins"
