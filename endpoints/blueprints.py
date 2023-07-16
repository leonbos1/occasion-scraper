from fastapi import APIRouter
from extensions import Base, url, get_session
from models.blueprint import BluePrint
import datetime
from utills.security import get_api_key
from fastapi import Depends
from fastapi import Request

router = APIRouter()

@router.get("/blueprints")
def get_blueprints(api_key: str = Depends(get_api_key)):
    session = get_session()

    blueprints = session.query(BluePrint).all()

    session.close()

    return blueprints

@router.get("/blueprints/{blueprint_id}")
def get_blueprint(blueprint_id: str, api_key: str = Depends(get_api_key)):
    session = get_session()

    blueprint = session.query(BluePrint).filter(BluePrint.id == blueprint_id).first()

    session.close()

    return blueprint

@router.put("/blueprints/{blueprint_id}")
async def update_blueprint(blueprint_id: str, request: Request, api_key: str = Depends(get_api_key)):
    session = get_session()

    blueprint = session.query(BluePrint).filter(BluePrint.id == blueprint_id).first()

    body = await request.json()

    if blueprint is None:
        return None
    
    attributes = blueprint.attributes

    for attribute in attributes:
        value = body.get(attribute)
        if value != None:
            setattr(blueprint, attribute, value)

    session.commit()
    session.close()

    return "Blueprint updated"

@router.post("/blueprints")
async def create_blueprint(request: Request, api_key: str = Depends(get_api_key)):
    session = get_session()

    body = await request.json()

    blueprint = BluePrint(**body)

    session.add(blueprint)
    session.commit()
    session.close()

    return "Blueprint created"

@router.delete("/blueprints/{blueprint_id}")
def delete_blueprint(blueprint_id: str, api_key: str = Depends(get_api_key)):
    session = get_session()

    blueprint = session.query(BluePrint).filter(BluePrint.id == blueprint_id).first()

    session.delete(blueprint)
    session.commit()
    session.close()

    return "Blueprint deleted"