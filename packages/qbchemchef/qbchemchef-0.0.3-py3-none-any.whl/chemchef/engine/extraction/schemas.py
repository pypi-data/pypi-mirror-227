from typing import Optional

from pydantic import BaseModel


class FieldSchema(BaseModel):
    field_name: str
    optional: bool
    multivalued: bool
    allowed_values: Optional[set[str]] = None
    example_values: Optional[set[str]] = None

    # Note: optional, multivalued and allowed_values are only a rough guideline for ChatGPT.
    # They are not rigorously enforced


class DocumentSchema(BaseModel):
    fields: list[FieldSchema]


class ParsedField(BaseModel):
    field_name: str
    values: set[str]


class ParsedDocument(BaseModel):
    fields: list[ParsedField]

    @property
    def field_names(self) -> set[str]:
        return {field.field_name for field in self.fields}

    def __getitem__(self, field_name: str) -> set[str]:
        for field in self.fields:
            if field.field_name == field_name:
                return field.values

        # Else, if field name not found:
        raise KeyError(f"Field name {field_name} not found in parsed document")

    def to_dict(self) -> dict[str, set[str]]:
        return {field.field_name: field.values for field in self.fields}
