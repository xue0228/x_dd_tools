import os.path
from typing import Union, Sequence, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from xddtools.entries.animation import Animation
from xddtools.name import AutoName
from xddtools.base import JsonData, EffectEntry, get_entry_id, ActorDotEntry, AnimationEntry
from xddtools.enum.actor_dot import ActorDotUpdateDurationType
from xddtools.path import DATA_PATH


class DurationElement(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    completion_chance: float = 0.0  # 1.0为必定发生
    completion_effects: Sequence[Union[EffectEntry, str]] = Field(default_factory=list)
    increment_effects: Sequence[Union[EffectEntry, str]] = Field(default_factory=list)

    def get_dict(self) -> dict:
        return {
            "completion_chance": self.completion_chance,
            "completion_effects": [get_entry_id(effect) for effect in self.completion_effects],
            "increment_effects": [get_entry_id(effect) for effect in self.increment_effects]
        }


class ActorDot(JsonData, ActorDotEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    update_duration_type: ActorDotUpdateDurationType
    duration_elements: Sequence[DurationElement] = Field(default_factory=list)

    fx: Optional[AnimationEntry] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_actor_dot(), frozen=True)

    @field_validator("fx")
    @classmethod
    def _check_fx(cls, v: Optional[AnimationEntry]):
        if v is None:
            v = Animation(
                anim_dir=os.path.join(DATA_PATH, r"template/actor_dot/tempest"),
                need_rename=False,
                is_fx=True
            )

        if isinstance(v, Animation):
            tem = set(v.animations)
            if tem != {"idle", "increment", "onset", "release"}:
                raise ValueError(f"Animation {v.id()} must have animations: idle, increment, onset, release")
        return v

    def get_dict(self) -> dict:
        return {
            "id": self.id(),
            "update_duration_type": self.update_duration_type.value,
            "duration_elements": [duration_element.get_dict() for duration_element in self.duration_elements]
        }
