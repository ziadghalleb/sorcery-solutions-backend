from pydantic import BaseModel


class Spell(BaseModel):
    name: str
    spell: str

class YAMLSpellbook(BaseModel):
    yaml_content: str
