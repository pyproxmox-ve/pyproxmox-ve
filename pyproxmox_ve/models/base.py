from pydantic import BaseModel, ConfigDict


def normalize_keys(string: str) -> str:
    return string.replace("_", "-")


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(
        allow_population_by_field_name=True,
        alias_generator=normalize_keys,
        use_enum_values=True,
    )
