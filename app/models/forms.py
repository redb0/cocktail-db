from pydantic import BaseModel, field_validator


class SearchForm(BaseModel):
    search: str | None


class FiltersFrom(BaseModel):
    filters: list[int] | None = None

    @field_validator("filters", mode="before")
    @classmethod
    def _convert_list(cls, value: list[str] | list[int]) -> list[int]:
        return [int(i) for i in value]
