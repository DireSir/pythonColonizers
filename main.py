import engine
import engineCatan as ec

def mainLoop():
  engine.logEvent(engine.dialogue["system"]["events"]["mainLoopStarting"])
  Sir = ec.player("Sir")
  Sir.resources["sheep"] += 1
  Sir.resources["stone"] += 1
  Sir.resources["wheat"] += 1
  Sir.buyCard()
  ec.hexagon("wheat", 5).activate()
  engine.save()

if __name__ == "__main__":
  mainLoop()