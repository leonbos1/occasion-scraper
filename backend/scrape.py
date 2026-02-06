from .scrapers import autoscout_json
from .extensions import session
from .models.blueprint import BluePrint

def start():
    autoscout_json.start()
    #gaspedaal.start()


def start_blueprint(blueprint_id: str):
    blueprint = session.query(BluePrint).filter_by(id=blueprint_id).first()
    if not blueprint:
        return False

    autoscout_json.scrape_blueprint(blueprint)
    return True