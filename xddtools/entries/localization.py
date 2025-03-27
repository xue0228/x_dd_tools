from pydantic import BaseModel, ConfigDict, Field, field_validator

from xddtools.base import LocalizationEntry


class Localization(LocalizationEntry, BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
    )

    entry_id: str = Field(..., min_length=1, max_length=64, pattern="^[a-zA-Z0-9_.]+$")
    text: str

    @field_validator("text")
    @classmethod
    def _check_text(cls, v: str):
        tem = v.split("\n")
        if len(tem) > 3:
            raise ValueError("Localization text can only contain up to 3 lines.")
        return v


if __name__ == '__main__':
    x = Localization(entry_id="5", text="4\n\n\n\n\n\n")
    print(x.id())
