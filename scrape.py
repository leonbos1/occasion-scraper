from .scrapers import autoscout, gaspedaal

def start():
    print("Starting scrapers")
    autoscout.start()
    #gaspedaal.start()