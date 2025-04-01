from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import Spell
from database import db
from models import spell_helper

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/spells")
async def cast_spell(spell: Spell):
    spell_doc = spell.dict()
    result = await db.spells.insert_one(spell_doc)
    if result.inserted_id:
        saved_spell = await db.spells.find_one({"_id": result.inserted_id})
        return spell_helper(saved_spell)
    raise HTTPException(status_code=500, detail="Spell casting failed.")


@app.get("/api/spells")
async def get_all_spells():
    spells = []
    async for spell in db.spells.find():
        spells.append(spell_helper(spell))
    return spells
