import sys
from enum import Enum


class Fact_Type(Enum):
    APPEARANCE = 1,

    NR_HANDS = 2,
    NR_LEGS  = 3,
    NR_EYES  = 4,

    DISPLACEMENT = 5,
    SKIN = 6,
    COLOR = 7,


# user answered with YES for these facts
known_yes_facts = []
# user answered with NO for these facts
known_no_facts  = []


def get_user_input(question: str) -> bool:
    for i in range(10):
        response_str: str = input(question).lower()
        if response_str == "yes" or response_str == "ye" or response_str == "y":
            return True
        elif response_str == "no" or response_str == "n":
            return False
    print("Come on...")
    sys.exit()


class Fact:
    def __init__(self, name: str, type: Fact_Type = None, question: str = "", affirmation: str = ""):
        self.name = name
        self.type = type
        self.question = question
        self.affirmation = affirmation

    def __eq__(self, other) -> bool:
        if isinstance(other, Fact) is False:
            return False
        return self.name == other.name and self.type == other.type

    def equal_type(self, other) -> bool:
        if isinstance(other, Fact) is False:
            return False
        return self.type == other.type

    def equal_name(self, other) -> bool:
        if isinstance(other, Fact) is False:
            return False
        return self.name == other.name


class Rule:
    def __init__(self, fact: Fact, condition: str = "AND", *rules):
        self.fact = fact
        self.condition = condition
        if len(rules) != 0:
            self.rules = rules
        else:
            self.rules = None

    def forward_chaining(self) -> bool:
        # check if we already know about some facts
        if self.fact in known_no_facts:
            return False
        if self.fact in known_yes_facts:
            return True
        # example: if the user said that the creature has 2 hands we shouldn't ask if it has 4 hands
        for yes_fact in known_yes_facts:
            if self.fact.equal_type(yes_fact) is True:
                if self.fact.equal_name(yes_fact) is False:
                    return False

        if self.rules is None:
            response = get_user_input(self.fact.question + " (yes/no)\n")
            if response is True:
                known_yes_facts.append(self.fact)
            else:
                known_no_facts.append(self.fact)
            return response

        if self.condition == "AND":
            for rule in self.rules:
                response = rule.forward_chaining()
                if response is False:
                    known_no_facts.append(self.fact)
                    return False
        elif self.condition == "OR":
            for rule in self.rules:
                response = rule.forward_chaining()
                if response is False:
                    known_no_facts.append(self.fact)
                    return False
                else:
                    break

        known_yes_facts.append(self.fact)
        return True

    def backward_chaining(self, depth = 0):
        for i in range(depth):
            print("\t", end='')
        print(self.fact.affirmation)
        if self.rules is None:
            return
        for rule in self.rules:
            rule.backward_chaining(depth + 1)


if __name__ == '__main__':
    # creating the knowledge database
    humanoid = Rule(Fact("humanoid", Fact_Type.APPEARANCE, "Does it look like a humanoid?", "A humanoid"),
                    "AND",
                    Rule(Fact("2 hands", Fact_Type.NR_HANDS, "Does it have 2 hands?", "It has 2 hands")),
                    Rule(Fact("2 legs", Fact_Type.NR_LEGS, "Does it have 2 legs?", "It has 2 legs")),
                    Rule(Fact("2 eyes", Fact_Type.NR_EYES, "Does it have 2 eyes?", "It has 2 eyes")))
    alien = Rule(Fact("alien", Fact_Type.APPEARANCE, "Does it look like an alien?", "An alien"),
                 "AND",
                 Rule(Fact("4 hands", Fact_Type.NR_HANDS, "Does it have 4 hands?", "It has 4 hands")),
                 Rule(Fact("2 legs", Fact_Type.NR_LEGS, "Does it have 2 legs?", "It has 2 legs")),
                 Rule(Fact("3 eyes", Fact_Type.NR_EYES, "Does it have 3 eyes", "It has 3 eyes")))
    feline = Rule(Fact("feline", Fact_Type.APPEARANCE, "Does it look like a feline?", "A feline"),
                  "AND",
                  Rule(Fact("0 hands", Fact_Type.NR_HANDS, "Does it have 0 hands?", "It has 0 hands")),
                  Rule(Fact("4 legs", Fact_Type.NR_LEGS, "Does it have 4 legs", "It has 4 legs")),
                  Rule(Fact("fur", Fact_Type.SKIN, "Does it have fur?", "It has fur")))
    centaur = Rule(Fact("centaur", Fact_Type.APPEARANCE, "Does it look like a centaur?", "A centaur"),
                   "AND",
                   Rule(Fact("4 legs", Fact_Type.NR_LEGS, "Does it have 4 legs?", "It has 4 legs")),
                   Rule(Fact("2 hands", Fact_Type.NR_HANDS, "Does it have 2 hands?", "It has 2 hands")),
                   Rule(Fact("fur", Fact_Type.SKIN, "Does it have fur?", "It has fur")))
    bug = Rule(Fact("bug", Fact_Type.APPEARANCE, "Does it look like a bug?", "A bug"),
               "AND",
               Rule(Fact("2 hands", Fact_Type.NR_HANDS, "Does it have 2 hands?", "It has 2 hands")),
               Rule(Fact("2 legs", Fact_Type.NR_LEGS, "Does it have 2 legs?", "It has 2 legs")),
               Rule(Fact("fur", Fact_Type.SKIN, "Does it have fur?", "It has fur")),
               Rule(Fact("4 eyes", Fact_Type.NR_EYES, "Does it have 4 eyes?", "It has 4 eyes")))
    flying = Rule(Fact("flying", Fact_Type.DISPLACEMENT, "Does it fly?", "It flies"))
    swimming = Rule(Fact("swimming", Fact_Type.DISPLACEMENT, "Does it swim?", "It swims"))
    walking = Rule(Fact("walking", Fact_Type.DISPLACEMENT, "Does it walk?", "It walks"))
    white = Rule(Fact("white", Fact_Type.COLOR, "Is it white?", "It's white"))
    green = Rule(Fact("green", Fact_Type.COLOR, "Is it green?", "It's green"))
    blue = Rule(Fact("blue", Fact_Type.COLOR, "Is it blue?", "It's blue"))
    yellow = Rule(Fact("yellow", Fact_Type.COLOR, "Is it yellow?", "It's yellow"))
    red = Rule(Fact("red", Fact_Type.COLOR, "Is it red?", "It's red"))
    gray = Rule(Fact("gray", Fact_Type.COLOR, "Is it gray?", "It's gray"))
    purple = Rule(Fact("purple", Fact_Type.COLOR, "Is it purple?", "It's purple"))

    bird_person = Rule(Fact("Bird Person", affirmation="A Bird Person is:"), "AND", humanoid, flying, white)
    amfiddian = Rule(Fact("Amfiddian", affirmation="An Amfiddian is:"), "AND", alien, swimming, green)
    meeseeks = Rule(Fact("Meeseeks", affirmation="A Meeseeks is:"), "AND", humanoid, walking, blue)
    squanchy = Rule(Fact("Squanchy", affirmation="A Squanchy is:"), "AND", feline, walking, yellow)
    gazorpian = Rule(Fact("Gazorpian", affirmation="A Gazorpian is:"), "AND", alien, walking, red)
    cat_person = Rule(Fact("Cat Person", affirmation="A Cat Person is:"), "AND", feline, walking, gray)
    boobloosian = Rule(Fact("Boobloosian", affirmation="A Boobloosian is:"), "AND", alien, swimming, gray)
    goomby = Rule(Fact("Goomby", affirmation="A Goomby is:"), "OR", centaur, walking, white)
    gromflomit = Rule(Fact("Gromflomit", affirmation="A Gromflomit is:"), "OR", bug, flying, gray)
    daron_person = Rule(Fact("Daron Person", affirmation="A Daron Person is:"), "AND", humanoid, walking, purple)
    flansian = Rule(Fact("Flansian", affirmation="A Flansian is:"), "AND", alien, swimming, yellow)

    database = [bird_person, amfiddian, meeseeks, squanchy, gazorpian, cat_person, boobloosian, goomby, gromflomit, daron_person, flansian]

    while True:
        print("1. For forward-chaining")
        print("2. For backward-chaining")
        print("3. Exit")
        try:
            command = int(input())
        except ValueError:
            continue
        print()

        creature_found = False
        if command == 1:
            for creature in database:
                if creature.forward_chaining() is True:
                    creature_found = True
                    print("It's a " + creature.fact.name + "!\n")

        elif command == 2:
            creature_name = input("Creature type: ")
            for creature in database:
                if creature.fact.name == creature_name:
                    creature_found = True
                    creature.backward_chaining()
            print()

        elif command == 3:
            sys.exit()
        else:
            continue

        if creature_found is False:
            print("There is no such creature in the database!")

        known_yes_facts = []
        known_no_facts = []
        print("**************************")
