import subprocess
import yaml  # Vulnerable PyYAML import!

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import Spell, YAMLSpellbook
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


@app.get("/api/execute")
async def execute_command(command: str | None = None):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()

    return {"stdout": stdout, "stderr": stderr}


@app.post("/api/import_spellbook")
async def import_spellbook(spellbook: YAMLSpellbook):
    try:
        # Use yaml.load (vulnerable to arbitrary code execution)
        spells_data = yaml.load(spellbook.yaml_content, Loader=yaml.Loader)
        
        if not isinstance(spells_data, dict) or "spells" not in spells_data:
            raise ValueError("Invalid YAML format. Expected a 'spells' key.")

        imported_spells = []
        for spell_dict in spells_data["spells"]:
            result = await db.spells.insert_one(spell_dict)
            saved_spell = await db.spells.find_one({"_id": result.inserted_id})
            imported_spells.append(spell_helper(saved_spell))
            
        return {"imported_spells": imported_spells}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")
