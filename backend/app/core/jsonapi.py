from fastapi.responses import JSONResponse


class JSONAPIResponse(JSONResponse):
    media_type = "application/vnd.api+json"


def resource_object(tipo: str, id: str, attributes: dict, relationships: dict | None = None) -> dict:
    obj = {"type": tipo, "id": id, "attributes": attributes}
    if relationships:
        obj["relationships"] = relationships
    return obj


def single(tipo: str, id: str, attributes: dict, relationships: dict | None = None) -> dict:
    return {"jsonapi": {"version": "1.1"}, "data": resource_object(tipo, id, attributes, relationships)}


def collection(tipo: str, items: list[tuple[str, dict, dict | None]]) -> dict:
    return {
        "jsonapi": {"version": "1.1"},
        "data": [resource_object(tipo, id, attrs, rels) for id, attrs, rels in items],
    }


def relationship(tipo: str, id: str) -> dict:
    return {"data": {"type": tipo, "id": id}}


def errors(status: int, title: str, detail: str) -> dict:
    return {"errors": [{"status": str(status), "title": title, "detail": detail}]}