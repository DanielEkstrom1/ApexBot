import random
import requests
import os


def handle_response(message) -> str:
    APIKEY = os.getenv('APIKEY')
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hello!'

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return "`!map - Check the current map and the Next map!` \n`!crafting - Check whats in the replicator!`"

    if p_message == '!crafting':
        return formatCraftingResponse(APIKEY)

    if p_message == '!map':
        return formatMapResponse(APIKEY)
    
    if p_message == '!test':
        return "Hello this is a ttest"


def formatMapResponse(APIKEY) -> str:
    result = ""
    response = requests.get(
        f"https://api.mozambiquehe.re/maprotation?auth={APIKEY}&version=2").json()
    for i in response["ranked"]:
        map = response["ranked"][i]["map"]
        started = list(response["ranked"][i]["readableDate_start"][len(
            response["ranked"][i]["readableDate_start"]) - 8:])
        started[1] = str(int(started[1]) + 2)

        ends = list(response["ranked"][i]["readableDate_end"][len(
            response["ranked"][i]["readableDate_end"]) - 8:])
        ends[1] = str(int(ends[1]) + 2)

        result += f'{i.capitalize()} Map: {map} \nStarted: {"".join(started)} \nEnds: {"".join(ends)} \n\n'
    return result


def formatCraftingResponse(APIKEY) -> str:
    results = ""
    checked = True
    response = requests.get(
        "https://api.mozambiquehe.re/crafting?auth={APIKEY}").json()
    for i in response:
        if checked:
            results += f'↓ {i["bundleType"].capitalize()} ↓ \n'
            if (i["bundleType"] == "permanent"):
                checked = False
        for j in i["bundleContent"]:
            if j["itemType"]["name"] != "ammo":
                results += f'{j["itemType"]["name"].capitalize().replace("_", " ")} \n'
    return results
