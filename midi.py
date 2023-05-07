import os, sys


def cls():  # Clear screen
    os.system("cls" if os.name == "nt" else "clear")


try:
    filename = sys.argv[1]
    error = f"Opened {os.path.basename(filename)}"  # Not an error, just to be displayed on first run
except IndexError:
    print(
        "Please specify a MIDI file by dragging it onto this script or by passing the file in a terminal"
    )
    input("\nPress enter to close")
    cls()
    sys.exit()

with open(filename, "rb") as f:  # Open file as global
    sig = f.read(4)
    if sig != b"MThd":  # Validate that the file is a MIDI file
        print("This is not a valid MIDI file")
        input("\nPress enter to close")
        cls()
        sys.exit()

with open(filename, "rb") as f:
    all = f.read()
    file = list(all)


def getInstruments() -> dict:
    offsets = []
    offset = 0
    for byte in file:
        if 192 <= byte <= 207:
            offsets.append(offset)
        offset += 1

    instruments = {}
    for offset in offsets:
        channel = file[offset] % 192
        instrument = file[offset + 1]
        instruments[offset] = [channel, instrument]
    return instruments


def save() -> None:
    cls()
    byte = bytes(file)

    with open(filename, "wb") as f:
        f.write(byte)
    print("Save Successful")


def change(id, newInstrument):
    file[int(id) + 1] = newInstrument


def displayMenu(instruments) -> None:
    global error
    cls()
    message = f"\n{error}\n"
    message += """Please input the byte of the change event that you'd like to edit.
Type 'S' to save.
----------------------------------------
 BYTE | CHANNEL | INSTRUMENT | LOCATION
----------------------------------------
"""

    for byte, data in instruments.items():
        location = round(byte / len(file) * 100)
        message += (
            str(byte).ljust(6)
            + " "
            + str(data[0]).ljust(9)
            + " "
            + str(data[1]).ljust(12)
            + " "
            + (str(location) + "%").ljust(10)
            + "\n"
        )
    print(message)
    error = ""


def valID(id, instruments) -> bool:
    global error
    cls()
    if id.isdigit():
        if int(id) in list(instruments.keys()):
            return True
        else:
            error = "That isn't a valid byte"
    else:
        error = "Please only enter digits"

    return False


def changeEvent(id, instruments) -> bool:
    global error
    cls()
    message = f"\n{error}\n"
    message += """ BYTE | CHANNEL | INSTRUMENT | LOCATION
----------------------------------------
"""
    data = instruments[int(id)]
    location = round(int(id) / len(file) * 100)
    message += (
        id.ljust(6)
        + " "
        + str(data[0]).ljust(9)
        + " "
        + str(data[1]).ljust(12)
        + " "
        + (str(location) + "%").ljust(10)
        + "\n"
    )
    print(message)
    error = ""

    newInstrument = input("Change instrument to: ")
    if not newInstrument.isdigit():
        error = "Please only enter digits"
        return False

    newInstrument = int(newInstrument)
    if 0 <= newInstrument < 128:
        change(id, newInstrument)
        error = ""
        return True
    error = "Please input a number between 0 and 127 (incl.)"
    return False


if __name__ == "__main__":
    while True:
        instruments = (
            getInstruments()
        )  # Gets dictionary containing the channel number instrument and for each channel change byte
        displayMenu(instruments)
        id = input()
        if id.lower() == "s":
            save()
            break  # Quit when saved
        elif valID(id, instruments):  # Validate number input
            while True:
                if changeEvent(id, instruments):  # Loop until input is valid
                    break
    input("\nPress enter to close")  # Wait for enter before exiting
    cls()
    sys.exit()
