import yaml
import json
import sys
import traceback
import time
from datetime import datetime

engineData = json.load(open("engineData.json", "r"))
gameData = json.load(open("gameData.json", "r"))
dialogue = json.load(open("dialogue/en.json", "r"))
config = yaml.safe_load(open("config.yaml", "r"))

if config["System settings"]["Clear log on restart"]:
  with open("log.txt", "w") as f:
    f.write(f"{config["System settings"]["Log beginning string"]}{dialogue["system"]["events"]["starting"]} {datetime.now().strftime("%a %b %d %H:%M:%S")}\n")
    f.close()

def save():
  logEvent(dialogue["system"]["events"]["gameSaved"])

def handleError(code, excType=None, excValue=None, excTraceback=None, replace = []):
  msg = dialogue["system"]["errors"].get(code, "\n{red}An {bold}unknown error{clear}{red} has occurred!{clear}")
  styled = formatStyled(msg, replace = replace)
  raw = formatStyled(msg, True, replace)

  timestamp = datetime.now().strftime("%a %b %d %H:%M:%S.%f")[:-3]

  if config["System settings"]["Print errors"]:
    print(styled)

  if config["System settings"]["Print traceback"] and all([excType, excValue, excTraceback]):
    print("".join(traceback.format_exception(excType, excValue, excTraceback)))

  if config["System settings"]["Log errors"]:
    with open("log.txt", "a") as f:
      f.write(f"\n\n[{timestamp}] [!] {raw}\n")

  if config["System settings"]["Log traceback"] and all([excType, excValue, excTraceback]):
    with open("log.txt", "a") as f:
      f.write("\n\n--------------------\n")
      f.write(f"Exception occured at {timestamp}:")
      f.write(f"\n\n{"".join(traceback.format_exception(excType, excValue, excTraceback))}")
      f.write("--------------------\n")

def exceptionHook(excType, excValue, excTraceback):
  handleError("unhandledException", excType, excValue, excTraceback)

sys.excepthook = exceptionHook

def formatStyled(text, strip = False, replace = []):
  escapeCodes = engineData["escapeCodes"]
  replaceCode = engineData["replaceCode"]
  codeCount = text.count(replaceCode)
  replaceLength = len(replace)

  if codeCount != replaceLength:
    handleError("replaceCodeCountMismatch", replace=[codeCount, replaceLength, text]) # I know about recursion but I don't give a flying fuck because if you mess the stupid-easy strings up it's your own problem :3
    return None
  for val in replace:
    text = text.replace(replaceCode, str(val), 1)
  if not strip:
    for tag, code in escapeCodes.items():
      text = text.replace(tag, code)
    return text
  else:
    for tag, code in escapeCodes.items():
      text = text.replace(tag, "")
    return text

def logEvent(event):
  timestamp = datetime.now().strftime("%b %d %H:%M:%S.%f")[:-3]
  with open("log.txt", "a") as f:
    f.write(f"\n[{timestamp}] {event}")
  if config["System settings"]["Print logs"]:
    print(f"\n[{timestamp}] {event}")

logEvent(dialogue["system"]["events"]["loadedMainEngine"])