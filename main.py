import random
import time
import os
import html
import base64
import datetime

# MISCELLANEOUS TOOLBOX (VARIABLES)


class colors:
    yellow = "\033[93m"
    gray = "\033[90m"
    cyan = "\033[96m"
    green = "\033[92m"
    endc = "\033[0m"
    bold = "\033[1m"
    ul = "\033[4m"
    red = "\033[31m"
    blue = "\033[34m"
    orange = "\033[42m\033[34m\033[1m"
    purple = "\033[35m"
    itl = "\033[3m"


play = True
iterations = 0
storeIter = 0
width = 11
height = 11
hidden = []
roomMap = []
yPos = 5
xPos = 5
enterStore = False
exported = False
pinfo = {
    "coins": 20,
    "lives": 0,
    "current_chance": [1, 6],
    "attack_chance": 6,
    "weapon": "✊fist✊",
    "maxLives": 0,
}


# ALL ARRAYS IN RELATION TO DUNGEON
room_types = [
    [0, "large room with a flickering neon store sign and a bored shopkeeper"],
    [1, "room with spiderwebs"],
    [2, "dark room"],
    [3, "long corridor"],
    [4, "stone walled room"],
    [5, "room with icky goo"],
    [6, "black room with claw scratches"],
    [7, "green hallway"],
    [8, "blue hallway"],
    [9, "rectangular wood room"],
    [10, "stone hallway"],
    [11, "room with dirt and moss"],
    [12, "ash covered room"],
    [13, "room with the logo of Nord Anglia Education"],
    [14, "room with a portrait of Elon Musk"],
    [15, "dark hallway with flickering lights"],
    [16, "corridor with an eerie blue glow"],
    [17, "blue circular room"],
    [18, "room made of red bricks"],
    [19, "rotating platform"],
    [20, "room with eerie sounds saying Binguuuuuus"],
    [
        21,
        "room filled with complicated math problems and 'Tanish' inscribed in cursive on the wall",
    ],
    [22, "room filled with AK-84s with paper bullets"],
    [23, "room completely flooded knee-high with water"],
    [24, "room made up of poisonous chocolate"],
    [25, "corridor full of fake money"],
]


# Overall Strength can range from 1 to 5 for monsters
# [letter0,xpos1,ypos2, lives3, name4,lives_prize5,coins_prize6,attack_dice7,missing_chance8,overall strength9]
# Note that xpos1 and ypos2 are out of use.
mons = [
    ["g", 4, 6, 5, f"🟢{colors.green}green slime{colors.endc}🟢", 0, 13, [1, 5], 8, 1],
    ["o", 8, 8, 10, f"👹{colors.green}ogre{colors.endc}👹", 0, 8, [1, 6], 7, 2],
    [
        "t",
        1,
        1,
        16,
        f"📚{colors.green}textbook monster sir{colors.endc}📚",
        0,
        20,
        [1, 15],
        8,
        3,
    ],
    ["🕷", 1, 1, 14, f"🕷{colors.green}giant spider{colors.endc}🕷", 0, 12, [2, 14], 7, 3],
    ["d", 1, 7, 23, f"🐉{colors.green}dragon{colors.endc}🐉", 10, 50, [2, 12], 6, 4],
    [ "m", 4,6, 42, f"💀{colors.green}monster overlord{colors.endc}💀", 15, 100, [3, 20], 5, 5,]
]

# [emoji000,name111,avoiding chance (roll higher out of 20)222, min dmg333, max dmg444,criterian555]
traps = [
    ["📌", "📌📌pushpins📌📌 spring up from the floor", 7, 2, 9, [1, 2]],
    ["🎯", "🎯darts🎯 shoot from the walls", 10, 3, 12, [2, 3]],
    ["🐟", "🐟piranhas🐟 drop on top of you", 15, 2, 9, [2, 3, 4]],
    ["🔥", "a blast of 🔥🔥fire🔥🔥 erupts from the floor", 12, 5, 16, [3, 4]],
    [
        "%",
        "a large 🗿🗿Easter Island head🗿🗿 falls from the ceiling",
        14,
        8,
        23,
        [4, 5],
    ],
]

# [flagem0,type1,locked2,lock_dffclty3,trapped4,trap_indx5,itemindx6,coins[min,max]7,destroyed8,criterians9]
# type is randomly decided later
sizes = [
    "huge",
    "big",
    "small",
    "medium",
    "python-shaped",
    "microscopic",
    "gigantic",
    "monstrous",
    "golden",
    "silver",
    "wooden",
]
chests = [
    ["🚩", "", False, 0, False, -1, [], [7, 22], False, [1, 2]],
    ["🏁", "", True, 12, False, -1, [], [18, 31], False, [2, 3]],
    ["🏳️", "", False, 0, True, 2, [1], [18, 31], False, [2, 3, 4]],
    ["🏴‍☠️", "", False, 0, True, 0, [2], [20, 40], False, [3, 4]],
    ["🎌", "", True, 7, True, 1, [3], [29, 51], False, [4, 5]],
    ["🏳️‍🌈", "", True, 11, True, 3, [4], [10, 20], False, [5]],
]

# [sym,crits,description,where you end up]
exits = [
    # ['⬆', [4,5], "stairs leading up.", "escaped to a desolate land of lava with a small sign saying 'Mustafar'"],
    # ['🧿', [2,3], "portal with '2+1=ok' written on it.", "back to the store"],
    # ['🚦', [4,5], "light in the distance.", "in a bright room with a green creature"]
    ["⬆", [4, 5], "stairs leading up.", "in heaven"],
    ["🧿", [2, 3], "portal with '2+1=ok' written on it.", "back to the store"],
    ["🚦", [4, 5], "light in the distance.", "in a planet without oxygen"],
]

# attack dice is pinfo[current_chance] if not changed
# [id0,coins to pay1, what you get in words2, lives_prize3,attack_dice4,missing chance reduction5,sellable6,knownAs7]
store = [
    [1, 2, "a healthy meal🥗", 5, pinfo["current_chance"], 0, False],
    [
        2,
        35,
        "a short sword with attack chance 2-12🔪🔪",
        0,
        [1, 12],
        0,
        True,
        "🔪short sword🔪",
    ],
    [
        3,
        60,
        "a powerful hammer with attack chance 3-18🔨🔨",
        0,
        [3, 18],
        0,
        True,
        "🔨powerful hammer🔨",
    ],
    [
        4,
        100,
        "a huge, sharp sword with attack chance 5-30⚔️⚔️",
        0,
        [5, 30],
        0,
        True,
        "⚔️huge & great sword⚔️",
    ],
    [
        5,
        48,
        "Training with great swordsman Ali Baba -- reduce missing chance by 10%.🎓",
        0,
        pinfo["current_chance"],
        1,
        False,
    ],
    [
        6,
        105,
        "Training with the greatly revered swordsman Dumbledore -- reduce missing chance by 30%.🎓🎓🎓",
        0,
        pinfo["current_chance"],
        3,
        False,
    ],
    [
        7,
        250,
        "Red lightsaber with infinite attack chance.🟥",
        0,
        pinfo["current_chance"],
        3,
        False,
        "🟥red lightsaber🟥",
    ],
    [
        8,
        250,
        "Green lightsaber with infinite attack chance.🟩",
        0,
        pinfo["current_chance"],
        3,
        False,
        "🟩green lightsaber🟩",
    ],
]


# COMPLETE TOOLBOX (FUNCTIONS)


def tinput(toAsk):
    print("\033[?25h", end="")  # SHOW CURSOR
    tor = input(f"{toAsk} -------⏩  ")
    print("\033[?25l", end="")  # HIDE CURSOR
    return tor


def inputNum(question: str, min: int, max: int):
    num = tinput(question)
    while num not in [str(xb) for xb in range(min, max + 1)]:
        num = tinput(
            f"\n{colors.red}{colors.bold}'{num}' is not a correct answer for this number.\n{colors.endc}{question}"
        )
    num = int(num)
    return int(num)


def touching(sym):
    global yPos
    global xPos
    if hidden[yPos][xPos] == sym:
        return True
    else:
        return False


def dice(minmax):
    return random.randint(minmax[0], minmax[1])


def removeFromBoard(sym):
    for row in range(height):
        for col in range(width):
            if hidden[row][col] == sym:
                hidden[row][col] = "_"


def isascii(s):
    return len(s) == len(s.encode())


def print_hidden():
    # print((" __")*width)
    # for row in hidden:
    #   print("|"+" |".join(row)+"|")
    print("\n")


def printDict(dicti):
    if dicti == pinfo:
        time.sleep(1)
        printCoins()
        time.sleep(1)
        printLives()
        time.sleep(1)
        printMissingChance()
        time.sleep(1)
        printCurrentChance()
        time.sleep(1)
        return
    for key, value in dicti.items():
        print(f"\t{colors.bold}{key}{colors.endc}: {colors.itl}{value}{colors.endc}")


def encodeb64(txt):
    message_bytes = txt.encode("ascii", errors="xmlcharrefreplace")
    base64_bytes = base64.b64encode(message_bytes)
    return str(base64_bytes.decode("ascii", errors="xmlcharrefreplace"))


def decodeb64(txt):
    base64_bytes = txt.encode("ascii", errors="xmlcharrefreplace")
    message_bytes = base64.b64decode(base64_bytes)
    return str(message_bytes.decode("ascii", errors="xmlcharrefreplace"))


def distance_from(yx, yy, tx, ty):
    y_dist = abs(yx - tx)
    x_dist = abs(yy - ty)
    ans = round((y_dist**2 + x_dist**2) ** 0.5)
    return ans


def check_distance(dist):
    if dist <= 1:
        return 1
    elif dist <= 2:
        return 2
    elif dist <= 3:
        return 3
    elif dist <= 4:
        return 4
    else:
        return 5


def timestamp():
    nowe = datetime.datetime.now()
    return nowe.strftime("%c")


def printCoins():
    print(
        f"{colors.yellow}{colors.bold}You currently have 💰{pinfo['coins']}.{colors.endc}\n"
    )


def printLives():
    print(
        f"{colors.red}{colors.bold}You currently have {pinfo['lives']} out of {pinfo['maxLives']} lives.{colors.endc}\n"
    )


def printMissingChance():
    print(
        f"{colors.cyan}{colors.bold}Your current missing chance is {pinfo['attack_chance']}0%. (the lower it is the better){colors.endc}\n"
    )


def printCurrentChance():
    print(
        f"{colors.blue}{colors.bold}Your current attack chance is between {str(pinfo['current_chance'][0])} and {str(pinfo['current_chance'][1])}.\n\nYour equipped weapon is a {colors.bold}{pinfo['weapon']}.{colors.endc}\n"
    )


def printe(x):
    print(x)
    time.sleep(1)


def printLine():
    print(f"{colors.purple}~{colors.endc}" * os.get_terminal_size()[0])


# SETUP RANDOM DUNGEON
def set_chest_pos():
    global hidden
    y = random.randint(0, height - 1)
    x = random.randint(0, width - 1)
    for ch in chests:
        while (hidden[y][x] != "_") or (
            check_distance(distance_from(x, y, 5, 5)) not in ch[9]
        ):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
        hidden[y][x] = ch[0]


def set_mons_pos():
    global hidden
    y = random.randint(0, height - 1)
    x = random.randint(0, width - 1)
    for mon in mons:
        while (hidden[y][x] != "_") or (
            check_distance(distance_from(x, y, 5, 5)) != mon[9]
        ):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
        hidden[y][x] = mon[0]


def set_exit_pos():
    y = random.randint(0, height - 1)
    x = random.randint(0, width - 1)
    global hidden
    for ex in exits:
        while (hidden[y][x] != "_") or (
            check_distance(distance_from(x, y, 5, 5)) not in ex[1]
        ):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
        hidden[y][x] = ex[0]


def set_trap_pos():
    global hidden
    y = random.randint(0, height - 1)
    x = random.randint(0, width - 1)
    for tr in traps:
        for repeatSame in range(2):
            while (hidden[y][x] != "_") or (
                check_distance(distance_from(x, y, 5, 5)) not in tr[5]
            ):
                y = random.randint(0, height - 1)
                x = random.randint(0, width - 1)
            hidden[y][x] = tr[0]


# Import and Export Save
def exportSave():
    saveName = tinput(
        f"{colors.cyan}{colors.itl}What would you like to name your save?\n(Must be within 20 characters)\n(Recommended to enter your Name){colors.endc}\n"
    )
    while len(saveName) > 20 or not (isascii(saveName)) or ("|" in saveName):
        saveName = tinput(
            f"\n{colors.red}{colors.bold}Please keep the name within 20 characters{colors.endc}\n\n{colors.cyan}{colors.itl}What would you like to name your save?{colors.endc}\n"
        )
    savePW = tinput(
        f"{colors.cyan}{colors.itl}Please enter a 4 to 16 character password to protect your data. \n(Write it down or memorize it)\nNo spaces are allowed. {colors.endc}\n"
    )
    while (
        (len(savePW) not in range(4, 17))
        or (" " in savePW)
        or (not isascii(savePW))
        or ("|" in savePW)
    ):
        savePW = tinput(
            f"\n{colors.red}{colors.bold}Please enter a valid password.{colors.endc}\n\n{colors.cyan}{colors.itl}Please enter a 7 to 16 character password to protect your data.\nNo spaces are allowed. {colors.endc}\n"
        )

    def mapPut(givenMap):
        toRet = ["&".join(b) for b in givenMap]
        return "!".join(toRet)

    storePut = "!".join([str(int(itm[0])) for itm in store])
    pinfoPut = ["&".join([the, str(pinfo[the])]) for the in pinfo]
    pinfoPut = "!".join(pinfoPut)
    finalSS = f"|psw:{savePW}|name:{saveName}|time:{timestamp()}|map:{mapPut(hidden)}|yPos:{yPos}|xPos:{xPos}|pinfo:{pinfoPut}|storeIter:{storeIter}|iterations:{iterations}|roomMap:{mapPut(roomMap)}|store:{storePut}|"
    finalSS = encodeb64(finalSS)
    txtFile = open("saveStates.txt", "a")
    txtFile.write(f"\n###{finalSS}")
    txtFile.close()


def importSave():
    global hidden, yPos, xPos, pinfo, storeIter, iterations, roomMap, store
    optDict = {}
    lins = []
    txtFile = open("saveStates.txt", "r")
    # Decoding & seperating the parts of each line
    for lin in txtFile.readlines():
        if lin.startswith("###"):
            lins.append((decodeb64(lin.strip("###"))).split("|"))
    txtFile.close()
    # Converting it to a list of dictionaries
    for lin in range(len(lins)):
        for lint in range(len(lins[lin])):
            lins[lin][lint] = lins[lin][lint].split(":", 1)
            if len(lins[lin][lint]) < 2:
                lins[lin][lint] = ["", ""]
            lins[lin][lint][1] = html.unescape(lins[lin][lint][1])
        lins[lin] = dict(lins[lin])
    # Making a way to print the save states to user
    for lin in range(len(lins)):
        optDict[f"{colors.blue}Save State {lin + 1}{colors.endc}"] = (
            f"{colors.blue}{lins[lin]['name']} ({lins[lin]['time']}){colors.endc}"
        )
    # Asking Process
    print(
        f"{colors.blue}{colors.itl}Please enter a saved state from the following options:{colors.endc}\n"
    )
    printDict(optDict)
    if len(optDict.keys()) == 0:
        print(
            f"\t{colors.blue}{colors.bold}There are currently no saved states. Please restart the game.{colors.endc}"
        )
        global play
        play = False
        return
    else:
        chsn = (
            inputNum(
                f"\n{colors.blue}{colors.bold}Enter the corresponding number here. (ex: '1'). Enter '0' to cancel. {colors.endc}",
                0,
                len(lins),
            )
        ) - 1
        if chsn == -1:
            play = False
            return
        chosenState = lins[chsn]
        enteredPSW = tinput(
            f"\n{colors.blue}{colors.bold}Enter the exact corresponding password here. (If forgotten, your saved state shall be lost) {colors.endc}"
        )
        while enteredPSW != chosenState["psw"]:
            print(
                f"{colors.red}{colors.bold}That is not the correct password.{colors.endc}"
            )
            print(
                f"{colors.blue}{colors.itl}Please try again and enter a saved state from the following options:{colors.endc}\n"
            )
            printDict(optDict)
            chsn = (
                inputNum(
                    f"\n{colors.blue}{colors.bold}Enter the corresponding number here. (ex: '1') {colors.endc}",
                    1,
                    len(lins),
                )
            ) - 1
            chosenState = lins[chsn]
            enteredPSW = tinput(
                f"\n{colors.blue}{colors.bold}Enter the exact corresponding password here. (If forgotten, your saved state shall be lost) {colors.endc}"
            )
        # As soon as the password becomes right
        print(
            f"\n\n{colors.green}{colors.bold}That is the correct password!{colors.endc}"
        )

        def mapTake(givenMap):
            toRet = chosenState[givenMap].split("!")
            return [rw.split("&") for rw in toRet]

        hidden = mapTake("map")
        yPos = int(chosenState["yPos"])
        xPos = int(chosenState["xPos"])
        roomMap = mapTake("roomMap")
        currentStoreItms = [int(idd) for idd in chosenState["store"].split("!")]
        newStore = []
        for itm in store:
            if itm[0] in currentStoreItms:
                newStore.append(itm)
        store = newStore
        storeIter = int(chosenState["storeIter"])
        iterations = int(chosenState["iterations"])
        pinfo = dict(mapTake("pinfo"))
        pinfo["current_chance"] = [
            int(pinfo["current_chance"].split(",")[0].strip("[")),
            int(pinfo["current_chance"].split(",")[1].strip("]")),
        ]
        pinfo["attack_chance"] = int(pinfo["attack_chance"])
        pinfo["maxLives"] = int(pinfo["maxLives"])
        pinfo["lives"] = int(pinfo["lives"])
        pinfo["coins"] = int(pinfo["coins"])
        print("\n")
        print(f"{colors.green}{colors.itl}Loading saved state{colors.endc}", end="\r")
        time.sleep(1)
        print(
            f"\r{colors.green}{colors.itl}Loading saved state.{colors.itl}{colors.endc}",
            end="\r",
        )
        time.sleep(1)
        print(
            f"\r{colors.green}{colors.itl}Loading saved state..{colors.itl}{colors.endc}",
            end="\r",
        )
        time.sleep(1)
        print(
            f"\r{colors.green}{colors.itl}Loading saved state...{colors.itl}{colors.endc}"
        )
        time.sleep(1)
        print(
            f"\n\n{colors.green}{colors.bold}Your saved game from earlier has been loaded!{colors.endc}"
        )


# INITIALISE BOARDS


def hidden_init():
    global hidden
    hidden = []
    for i in range(height):
        hidden.append(["_"] * width)
    set_mons_pos()
    set_exit_pos()
    set_trap_pos()
    set_chest_pos()
    hidden[5][5] = "#"


def set_rooms():
    global roomMap, room_types
    roomsLeft = [b for b in room_types[1:]]
    for room in room_types:
        room[1] = f"{room[1]}."
    for i in range(height):
        roomMap.append(["_"] * width)
    for row in range(height):
        for col in range(width):
            if roomsLeft == []:
                roomsLeft = [b for b in room_types[1:]]
            chsnRoom = random.choice(roomsLeft)
            roomsLeft.remove(chsnRoom)
            roomMap[row][col] = str(chsnRoom[0])
    roomMap[5][5] = "0"


# MAIN INITIALISATION FUNCTION


def initialise():
    global pinfo
    print("\033[?25l", end="")  # HIDE CURSOR
    printLine()
    print(
        f"{' ' * (round((os.get_terminal_size()[0]) / 2) - 15)}{colors.purple}{colors.bold}Welcome to Dungeon Adventure!{colors.endc}{' ' * (round((os.get_terminal_size()[0]) / 2) - 15)}"
    )
    printLine()
    print(
        f"{colors.green}{colors.bold}{colors.itl}Would you like to import a saved state or start a new adventure?{colors.endc}"
    )
    printDict(
        {
            f"{colors.green}1{colors.endc}": f"{colors.green}Start a New Adventure{colors.endc}",
            f"{colors.green}2{colors.endc}": f"{colors.green}Import a Saved State{colors.endc}",
        }
    )
    chosenStart = inputNum(
        f"{colors.green}{colors.bold}{colors.itl}Enter the corresponding number to your option.{colors.endc}",
        1,
        2,
    )
    if chosenStart == 1:
        hidden_init()
        set_rooms()
        time.sleep(1)
        print("\n\n")
        printMissingChance()
        time.sleep(1)
        printCurrentChance()
        time.sleep(1)
        print(
            f"{colors.bold}Let's roll for maximum lives (Random from 26-50).{colors.endc}"
        )
        time.sleep(1)
        pinfo["maxLives"] = random.randint(26, 50)
        pinfo["lives"] = pinfo["maxLives"]
        printLives()
        time.sleep(1)
        print(f"{colors.bold}Let's roll for starting coins (Random from 30-80).")
        time.sleep(1)
        pinfo["coins"] = random.randint(30, 80)
        printCoins()
        time.sleep(1)
    elif chosenStart == 2:
        importSave()
        if play == False:
            return
        time.sleep(1)
        printMissingChance()
        time.sleep(1)
        printCurrentChance()
        time.sleep(1)
        printLives()
        time.sleep(1)
        printCoins()
        time.sleep(1)
        print(
            f"{colors.purple}{colors.bold}By the way, you have moved {iterations} times by now!{colors.endc}"
        )
        time.sleep(1)


# MOVING FUNCTION
def walls():
    if yPos == 0:
        print("There is a stone wall up, so you cannot move there next.")
    if yPos == 9:
        print("There is a stone wall down, so you cannot move there next.")
    if xPos == 9:
        print("There is a stone wall right, so you cannot move there next.")
    if xPos == 0:
        print("There is a stone wall left, so you cannot move there next.")


def move(dir, its):
    global yPos
    global xPos
    if dir == "up" and yPos > 0:
        yPos -= 1
        walls()
        return True
    elif dir == "down" and yPos < 9:
        yPos += 1
        walls()
        return True
    elif dir == "right" and xPos < 9:
        xPos += 1
        walls()
        return True
    elif dir == "left" and xPos > 0:
        xPos -= 1
        walls()
        return True
    elif dir == "stats":
        printDict(pinfo)
        print(
            f"{colors.purple}{colors.bold}By the way, you have moved {its} times by now!{colors.endc}"
        )
        print(
            f"\n\n{colors.blue}Attack chance shows how much damage you can deal from min to max.\n{colors.cyan}Your missing chance shows how much you can miss, and it is out of 10.{colors.endc}\n\n\n"
        )
        walls()
        return False
    elif dir in ["you are nice", "nice", "nice game"]:
        print("\nThank you!")
        specialPrize = random.randint(1, 5)
        if specialPrize in [4, 5]:
            nice_prize = random.randint(10, 30)
            pinfo["coins"] += nice_prize
            print(
                f"Wow! The dungeon gratefully leaves a bag of {nice_prize} coins for you."
            )
            printCoins()
        walls()
        return False
    elif dir == "store" and touching("#"):
        global enterStore
        enterStore = True
        walls()
        return False
    elif dir == "export":
        exportSave()
        global play, exported
        play = False
        exported = True
        walls()
        return False
    else:
        print(f"{colors.red}{colors.bold}That is not a valid response.{colors.endc}")
        walls()
        return False


# TRAP FUNCTION


def trapped(tinfo):
    print("As soon as you enter the room, {}.".format(tinfo[1]))
    time.sleep(1)
    print(
        "Avoiding the trap requires you to roll \na {} or higher on a 20-sided die.".format(
            tinfo[2]
        )
    )
    time.sleep(1)
    rolled = random.randint(1, 20)
    print("You rolled a {}.".format(rolled))
    time.sleep(1)
    if rolled >= tinfo[2]:
        print("You avoided the trap! Woohoo!")
    else:
        damage = random.randint(tinfo[3], tinfo[4])
        print("Aw snap! The trap hits you for {} damage.".format(damage))
        time.sleep(1)
        pinfo["lives"] -= damage
        if pinfo["lives"] <= 0:
            return "dead"
        else:
            printLives()
    removeFromBoard(tinfo[0])
    return "ok"


# CHEST FUNCTIONS


def open_chest(cinfo):
    cinfo = chests[chests.index(cinfo)]
    # cinfo[5] = random.randint(0, len(traps) - 1)
    if cinfo[2]:
        printe(
            "This chest is locked. You have to roll {} or higher to pick the lock.".format(
                cinfo[3]
            )
        )
        unlock_roll = random.randint(1, 20)
        printe("You rolled a {}.".format(unlock_roll))
        if unlock_roll >= cinfo[3]:
            printe("Yay you unlocked it!")
        else:
            printe("Aw! You failed!")
            printe("A booming voice suddenly says 'Locked chests must GO!!!'. 💨Poof💨")
            cinfo[8] = True
            return "failed"
    if cinfo[4]:
        printe("This chest is trapped! Tun tun tun.")
        the_trap = traps[cinfo[5]]
        printe("As soon as you open the chest, {}.".format(the_trap[1]))
        printe(
            "Avoiding it requires you to roll a {} or higher on a 20-sided die.".format(
                the_trap[2]
            )
        )
        rolled = random.randint(1, 20)
        printe(f"You rolled {rolled}.")
        if rolled >= the_trap[2]:
            printe("You successfully avoided the trap!")
        else:
            printe("You failed and the trap damages you.")
            damage = random.randint(the_trap[3], the_trap[4])
            pinfo["lives"] -= damage
            if pinfo["lives"] <= 0:
                return "dead"
            printe(
                "You took {} damage and have {} left.".format(damage, pinfo["lives"])
            )
    get_chest_prize(cinfo)
    return "ok"


def get_chest_prize(cinfo):
    global pinfo
    printe("You search the chest.")
    if cinfo[7][0] > 0:
        gold = random.randint(cinfo[7][0], cinfo[7][1])
        printe("You find {} gold in the chest and take it.".format(gold))
        pinfo["coins"] += gold
        printCoins()
    if len(cinfo[6]) > 0:
        for item in cinfo[6]:
            item = store[item - 1]
            printe("You find {} and take it.".format(item[2]))
            if item[3] != 0:
                print("You got {} lives.".format(item[3]))
                pinfo["lives"] += item[3]
                if pinfo["lives"] > pinfo["maxLives"]:
                    pinfo["lives"] = pinfo["maxLives"]
                printLives()
            if item[4] != pinfo["current_chance"]:
                pinfo["weapon"] = item[7]
                pinfo["current_chance"] = item[4]
                printCurrentChance()
            if item[5] != 0:
                pinfo["attack_chance"] -= item[5]
                printMissingChance()


# HOW EXITS WORK


def exitf(exit):
    print(
        f"You cannot believe that this is an end to the monotony of the dungeon.\nYou see {exit[2]}."
    )
    go_exit = tinput("Would you like to go there? y/n")
    if go_exit == "y":
        print(f"When you enter, you find yourself {exit[3]}.")
        if exit[3] == "back to the store":
            return "at store"
        else:
            return "escaped"
    return "not going"


# MONSTER FIGHTING FUNCTIONS


def player_attack(multiplier, minfo):
    hit = random.randint(1, 10)
    if hit >= pinfo["attack_chance"]:
        print("You hit! (You rolled a {})".format(hit))
        time.sleep(1)
        print("Rolling to hit...")
        time.sleep(2)
        livtaken = dice(pinfo["current_chance"])
        if multiplier != 1:
            print(
                f"You got {livtaken} for lives taken, but since {minfo[4]} defended, you only take {colors.green}{round(multiplier * livtaken)} lives{colors.endc}."
            )
            livtaken = round(multiplier * livtaken)
        else:
            print(f"You took {colors.green}{livtaken} lives{colors.endc}.")
        minfo[3] = minfo[3] - livtaken
    else:
        print("You missed and rolled a {}.".format(hit))


def monster_attack(multiplier, minfo):
    hit = random.randint(1, 10)
    if hit >= minfo[8]:
        print("Monster hit 🙁(It rolled a {})".format(hit))
        time.sleep(1)
        print("Rolling to hit...")
        time.sleep(2)
        livtaken = dice(minfo[7])
        if multiplier == 0.5:
            print(
                f"{minfo[4]} got {colors.red}{livtaken}{colors.endc} for lives taken, but since you defended, {minfo[4]} only takes {colors.red}{round(multiplier * livtaken)} lives{colors.endc}."
            )
            livtaken = round(multiplier * livtaken)
        else:
            print(f"{minfo[4]} took {colors.red}{livtaken} lives{colors.endc}.")
        pinfo["lives"] = pinfo["lives"] - livtaken
    else:
        print(f"{minfo[4]} missed and rolled a {hit}!")


def fight(minfo):
    global pinfo
    print("You have met " + minfo[4])
    print("The goal is to hit at a place where he is not blocked.")
    print(
        "It can block at 1 place from low, middle, and high. You must try to guess a place where he is not blocked."
    )
    m_lives = minfo[3]
    u_lives = pinfo["lives"]
    places = ["l", "m", "h"]
    attacker = random.choice(["your", minfo[4] + "'s"])
    while m_lives > 0 and u_lives > 0:
        print("\n             ")
        print("It is " + attacker + " turn to attack.")
        if attacker == "your":
            multiplier = 1
            blocked = random.choice(places)
            guess = tinput(
                f"Enter based on the key shown:\n\nl: Attack Down Low With {pinfo['weapon'].title()}\nm: Attack in the Middle With {pinfo['weapon'].title()}\nh: Attack Up High With {pinfo['weapon'].title()}\n"
            )
            if guess not in places:
                guess = tinput(
                    "You entered it wrong! Enter from the options.\nIf you do not enter from the options, this attack will fail!\n"
                )
            if guess in places:
                if guess == blocked:
                    print("It blocked here! Now you will only get to damage half.")
                    multiplier = 0.5
                elif guess != blocked:
                    print("The monster blocked {}. Yay!".format(blocked))
                player_attack(multiplier, minfo)
            attacker = minfo[4] + "'s"
        else:
            multiplier = 1
            blocked = tinput(
                f"Enter based on the key shown:\n\nl: Block Down Low With {pinfo['weapon'].title()}\nm: Block in the Middle With {pinfo['weapon'].title()}\nh: Block Up High With {pinfo['weapon'].title()}\n"
            )
            if blocked not in places:
                blocked = tinput(
                    "That is not a valid input. Please try again.\nYou must block from the options to block successfully.\n-."
                )
            attacked = random.choice(places)
            if attacked == blocked:
                print(
                    "It attacked here! Now the monster will only get to damage half if it attacks."
                )
                multiplier = 0.5
            elif attacked != blocked:
                print("The monster attacked {}. Ugh!".format(attacked))
            monster_attack(multiplier, minfo)
            attacker = "your"
        m_lives = minfo[3]
        u_lives = pinfo["lives"]
        print(
            f"{colors.green}Monster's lives: {m_lives}     {colors.endc + colors.red}Your lives: {u_lives}{colors.endc}"
        )
    if u_lives <= 0:
        return False
    else:
        return True


# STAR WARS END SCENE


def star_wars(color):
    x = 0.9
    if color == "red":
        print("You pick up the red lightsaber.\n")
        time.sleep(x)
        print("A evil glee fills you.\n")
        time.sleep(x)
        print(
            "You find the Darth Amir in a dark dungeon room after breaking a stone wall.\n"
        )
        time.sleep(x)
        print(
            "You learn the ways of the dark side and help him in trapping Fyoda, Amir's sworn nemesis.\n"
        )
        time.sleep(x)
        print("You kill all monsters in the dungeon in anger.\n")
        time.sleep(x)
        print("You slice the storekeeper's head off and own the dungeon.\n")
        time.sleep(x)
        print("The dungeon is your domain now, but you wish to expand it.\n")
        time.sleep(x)
        print("You find the path to Earth and rule the planet.\n")
        time.sleep(x)
        print("Everyone cowers before you.\n")
        time.sleep(x)
        print("You are known as Darth Dungeonis.\n")
        time.sleep(x)
        print(
            "A Jedi suddenly arrives from the depths of the dungeon and challenges you to a duel.\n"
        )
        time.sleep(x)
        print("This Jedi arrogantly calls himself the 'Dungeon Survivor' *Scoff*.\n")
        time.sleep(x)
        print(
            "You accept his duel without a second thought and a fierce battle ensues.\n"
        )
        time.sleep(x)
        print(
            "After many weeks of fighting, you are struck by his green lightsaber and in your dying breaths, you wonder.\n"
        )
        time.sleep(x)
        print(
            "You think back to your innocent past and the choices you made, including the lightsaber color.\n"
        )
        time.sleep(x)
        print("You have lost the game, as you became evil.\n")
    elif color == "green":
        print("You feel wiser, like Master Yoda.")
        time.sleep(x)
        print("You find Yoda in a special room through a pathway of light.")
        time.sleep(x)
        print("He teaches you the ways of the light side.")
        time.sleep(x)
        print("You escape and become a Jedi, known to most as the Dungeon Survivor.")
        time.sleep(x)
        print("An arrogant Sith Lord had escaped the dungeon before you.")
        time.sleep(x)
        print("You decide to duel him and free the Earth from his tyrannous rule.")
        time.sleep(x)
        print(
            "He accepts, and the fierce battle results in a final strike as you strike him."
        )
        time.sleep(x)
        print(
            "He seems to have muttered something about red lightsabers versus green lightsabers, but you think nothing of it."
        )
        time.sleep(x)
        print(
            "You have won! Take a screenshot of the current page and you will be officially added to the Dungeon Hall of Fame."
        )


# HOW DOES RESTING WORK


def rest():
    print(
        "Let's determine how many lives you gain through rest as the total of 2 six sided die."
    )
    healed = random.randint(1, 6) + random.randint(1, 6)
    pinfo["lives"] += healed
    if pinfo["lives"] > pinfo["maxLives"]:
        pinfo["lives"] = pinfo["maxLives"]
    print(f"You regained {colors.red}{healed} lives{colors.endc} after resting.")


# HOW DOES BUYING AN ITEM WORK


def buy(item):
    global play, pinfo
    if item[1] > pinfo["coins"]:
        print(
            f"{colors.yellow}{colors.bold}{colors.itl}You do not have enough coins to buy this item.{colors.endc}"
        )
    elif item[0] == 7:
        star_wars("red")
        play = False
    elif item[0] == 8:
        star_wars("green")
        play = False
    else:
        # Get Things
        print(f"OK -- buying ------------ {colors.bold}{item[2]}{colors.endc}")
        pinfo["coins"] -= item[1]
        printCoins()
        # Say what they got
        if item[3] != 0:
            pinfo["lives"] += item[3]
            if pinfo["lives"] > pinfo["maxLives"]:
                pinfo["lives"] = pinfo["maxLives"]
            print(f"You got {colors.red}{item[3]} lives{colors.endc}.")
            printLives()

        if item[4] != pinfo["current_chance"]:
            pinfo["weapon"] = item[7]
            pinfo["current_chance"] = item[4]
            printCurrentChance()

        if item[5] != 0:
            pinfo["attack_chance"] -= item[5]
            printMissingChance()


# HOW DOES THE STORE WORK?


def storef(recently):
    global store
    if recently > 5:
        rested = False
    else:
        rested = True
    eaten = False
    in_store = True
    while in_store:
        printLine()
        print("\n")
        printCoins()
        time.sleep(0.5)
        print("Here are your options:")
        time.sleep(1)
        dashes = "----------"
        for item in store:
            dashes = "-" * (11 - len(str(item[1])))
            print(
                f"{colors.bold}{item[0]}: 💰{colors.yellow + str(item[1]) + colors.endc} {colors.bold}{dashes} {item[2]}{colors.endc}"
            )
            time.sleep(0.5)
        dashes = "-" * 10
        print(
            f"{colors.bold}r: 💰{colors.yellow}0{colors.endc} {colors.bold}{dashes} Rest{colors.endc}"
        )
        time.sleep(0.5)
        print(
            f"{colors.bold}l: 💰{colors.yellow}0{colors.endc} {colors.bold}{dashes} Leave Store{colors.endc}"
        )
        time.sleep(0.5)
        buy_what = tinput("\n\nEnter the number of the item you want to buy ")
        if buy_what == "r" and rested == False:
            rest()
            rested = True
        elif buy_what == "r":
            print(
                f"\n{colors.red}{colors.bold}{colors.itl}You do not feel tired, as you just rested.{colors.endc}"
            )
        elif buy_what == "l":
            printe(
                f"\n{colors.bold}{colors.cyan}{colors.ul}You leave the store.\nYou are prepared to head out into the dungeon.{colors.endc}\n\n"
            )
            in_store == False
            break
        else:
            itemExists = False
            for item in store:
                if str(item[0]) == (buy_what).strip(" "):
                    itemExists = True
                    if eaten and item[0] == 1:
                        print(
                            f"\n{colors.red}{colors.bold}{colors.itl}You have already eaten and do not feel hungry.{colors.endc}"
                        )
                    elif item[0] == 1:
                        eaten = True
                        buy(item)
                    else:
                        if item[4] != pinfo["current_chance"]:
                            store.remove(item)
                        buy(item)
            if itemExists == False:
                printe(
                    f"\n{colors.red}{colors.bold}Please choose a valid item.{colors.endc}"
                )


# MAIN FUNCTION


def main():
    global storeIter, iterations, play, yPos, xPos, enterStore
    optionsDict = {
        f"{colors.green}up": f"{colors.green}Explore the dungeon area directly to the North.",
        f"{colors.green}down": f"{colors.green}Explore the dungeon area directly to the South.",
        f"{colors.green}left": f"{colors.green}Explore the dungeon area directly to the West.",
        f"{colors.green}right": f"{colors.green}Explore the dungeon area directly to the East.",
        f"{colors.green}stats": f"{colors.green}Marvel at the statistics of your character.",
        f"{colors.green}export": f"{colors.green}Pause the game by saving your current game.",
    }
    initialise()
    if play == False:
        print(
            f"\n\n{colors.cyan}{colors.bold}{colors.ul}Press Run to Play.{colors.endc}"
        )
        return
    for i in room_types:
        if roomMap[yPos][xPos] == str(i[0]):
            print(f"You are in a {colors.orange}{i[1]}{colors.endc}")
    while play:
        if pinfo["lives"] <= 0:
            play = False
            break
        print_hidden()
        printLine()
        if touching("#"):
            optionsDict[f"{colors.yellow}store"] = (
                f"{colors.yellow}Enter the store only found in this special room."
            )
        else:
            optionsDict = {
                key: val
                for key, val in optionsDict.items()
                if key != f"{colors.yellow}store"
            }
        print(f"{colors.bold}\nEnter from the following options:\n\n{colors.endc}")
        printDict(optionsDict)
        direction = (tinput("\n\nType Here ").lower()).strip()
        moved = move(direction, iterations)
        if moved == True:
            iterations += 1
            storeIter += 1
        if play == False:
            break
        for i in room_types:
            if roomMap[yPos][xPos] == str(i[0]):
                print(f"You are in a {colors.orange}{i[1]}{colors.endc}")

        if enterStore:
            storef(storeIter)
            storeIter = 0
            enterStore = False

        for trap in traps:
            if touching(trap[0]):
                trap_state = trapped(trap)
                if trap_state == "dead":
                    play = False
                    break
        for i in mons:
            if touching(i[0]):
                won_fight = fight(i)
                if won_fight:
                    removeFromBoard(i[0])
                    print("You have killed the monster.")
                    if i[5] != 0:
                        pinfo["lives"] += i[5]
                        print(
                            f"You searched the monster and found a pizza that gave you {colors.red}{i[5]} lives{colors.endc} after eating it.\n"
                        )
                        printLives()
                    if i[6] != 0:
                        pinfo["coins"] += i[6]
                        print(f"You got {i[6]} coins after searching the monster.")
                        printCoins()
                else:
                    play = False
                    break
        for chest in chests:
            if touching(chest[0]) and chest[8] == False:
                chest[1] = random.choice(sizes)
                print(f"You notice a {chest[1]} chest.")
                want_open = tinput("Do you want to open it? y/n")
                if want_open == "n":
                    print("Okay")
                elif want_open == "y":
                    chesterling = open_chest(chest)
                    removeFromBoard(chest[0])
                    if chesterling == "dead":
                        play = False
                        break
                else:
                    print(
                        "You did not enter a valid response\n and the chest got angry and disappeared."
                    )
        for exit in exits:
            if touching(exit[0]):
                exited = exitf(exit)
                if exited == "escaped":
                    pinfo["lives"] = 0
                    play = False
                    break
                elif exited == "at store":
                    yPos = 5
                    xPos = 5
                elif exited == "not going":
                    continue
    if pinfo["lives"] <= 0:
        print(
            f"\n\n{colors.red}{colors.bold}You have died and lost the game.{colors.endc}"
        )
    if not exported:
        print(
            f"\n\n{colors.red}{colors.bold}{colors.ul}Game over. Play again by pressing Run.{colors.endc}"
        )
    else:
        print(
            f"\n\n{colors.green}{colors.bold}Thank you for playing Dungeon Adventure! Please come back soon!{colors.endc}"
        )


if __name__ == "__main__":
    main()
