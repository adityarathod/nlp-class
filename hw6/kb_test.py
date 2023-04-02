from kb import *


def termdef_resolver():
    print("\nTerm Definition Resolver")
    print("------------------------")
    print("Enter a term to get its definition")
    term = input("Term: ")
    print("Definition: ")
    print(get_definition(term) if get_definition(term) else "No definition found")
    print("------------------------")


def champdata_resolver():
    print("\nChampion Data Resolver")
    print("------------------------")
    print("Enter a champion ID to get its data")
    champ = input("Champion ID: ")
    print("Data: ")
    print(get_individual_champ_data(champ))
    print("------------------------")


def champskins_resolver():
    print("\nChampion Skins Resolver")
    print("------------------------")
    print("Enter a champion ID to get its skins.")
    champ = input("Champion ID: ")
    if champ == "return":
        return
    print("Skins: ")
    print(get_champ_skins(champ))
    print("------------------------")


START_MENU_STRING = """
LoL Knowledge Base Tester
-------------------------
Pick an option:
[1] Get top 10 term definition
[2] Get champion data
[3] Get champion skins
"""


def main():
    print(START_MENU_STRING)
    option = input("Option [type 'q' to quit]: ")
    while option != "q":
        if option == "1":
            termdef_resolver()
        elif option == "2":
            champdata_resolver()
        elif option == "3":
            champskins_resolver()
        else:
            print("Invalid option")
        option = input("\nOption [type 'q' to quit]: ")


if __name__ == "__main__":
    main()
