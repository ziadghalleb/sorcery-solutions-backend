from pydantic import BaseModel


class Spell(BaseModel):
    name: str
    spell: str
