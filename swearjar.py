import json
import random
from dataclasses import dataclass, field

database = 'res/swearjar.json'

class BannedWordData:
    name = "None"
    triggers = []
    value = 0

    def __init__(self, name, triggers, value):
        self.name = name
        self.triggers = triggers
        self.value = value


class BannedWordMessage:
    message = ""
    author = ""
    word_data = []

class Swearjar:
    banned_word_list = {
        BannedWordData("Skrillex", [
            "skrill",
            "skrillex",
        ],
        10)
    }
    def update(self, json_object):
        with open(database, 'r+') as file:
            file_data = json.load(file)
            word = list(json_object.keys())[0]
            name = list(json_object[word].keys())[0]

            if file_data[word].get(name):
                # name exists, update json
                file_data[word][name].update({"Sum": file_data[word][name]["Sum"] + json_object[word][name]["Sum"]})
                file_data[word][name].update({"Forints": file_data[word][name]["Forints"] + json_object[word][name]["Forints"]})
                breakdown_keys = json_object[word][name]["Breakdown"].keys()

                for bdk in breakdown_keys:
                    file_data[word][name]["Breakdown"][bdk] = file_data[word][name]["Breakdown"][bdk] + json_object[word][name]["Breakdown"][bdk]

            else:
                print("don't exist, adding...")
                file_data[word].update(
                    {
                        name: json_object[word][name]
                    }
                )

            print(file_data[word][name])

            file.seek(0)
            json.dump(file_data, file, indent=4)

    def query(self, person="everyone"):
        ret_message = ""

        with open(database, 'r') as file:
            file_data = json.load(file)
            if person == "everyone":
                return self.query_everyone(file_data)
            else:
                return self.query_person(file_data, person)
    
    def query_everyone(self, file_data={}):
        ret_message = "Swearjar Stats:\n===\n"

        total_forints_collected = 0

        for sw in file_data.keys():
            ret_message += "Word: " + sw + ".\n\n"
            for name in file_data[sw].keys():
                ret_message += name + ": " + str(file_data[sw][name]["Sum"]) + "\n"
                for bdk in file_data[sw][name]["Breakdown"].keys():
                    ret_message += " - " + bdk + ": " + str(file_data[sw][name]["Breakdown"][bdk]) + "\n"
                
                forints = file_data[sw][name]["Forints"]
                ret_message += "This sums for " + str(forints) + " forints in the swearjar\n\n"

                total_forints_collected = total_forints_collected + forints
        
        encourage_quips = [
            "Way to go!",
            "Keep on skrillin'!",
            "Put your häăånds up!"
        ]

        ret_message += "All in all, we have collected " + str(total_forints_collected) + " forints. " + random.choice(encourage_quips)

        return ret_message

    def query_person(self, file_data, person):
        ret_message = "Swearjar Stats for " + person + "\n===\n"
        for sw in file_data.keys():
            ret_message += "Word: " + sw + ".\n\n"
            ret_message += "Total: " + str(file_data[sw][person]["Sum"]) + "\n"
            for bdk in file_data[sw][person]["Breakdown"].keys():
                ret_message += " - " + bdk + ": " + str(file_data[sw][person]["Breakdown"][bdk]) + "\n"
            ret_message += "This sums for " + str(file_data[sw][person]["Forints"]) + " forints in the swearjar\n\n"

        return ret_message
