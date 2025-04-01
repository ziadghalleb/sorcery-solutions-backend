from bson import ObjectId


def spell_helper(spell) -> dict:
    return {
        "id": str(spell["_id"]),
        "name": spell["name"],
        "spell": spell["spell"],
    }
