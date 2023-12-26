from pydantic import BaseModel, ConfigDict


def normalize_keys(string: str) -> str:
    return string.replace("_", "-")


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=normalize_keys,
        use_enum_values=True,
    )


class ProxmoxBaseModelWithoutAlias(BaseModel):
    """Use this class when most attributes shouldn't be serialized using alias generator."""

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )
