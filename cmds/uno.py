import random

class uno():
    def __init__(self):
        self.deck = [{
            "type": "numbered",
            "order": 0,
            "number": 0,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 1,
            "number": 0,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 2,
            "number": 0,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 3,
            "number": 0,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 4,
            "number": 1,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 5,
            "number": 1,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 6,
            "number": 1,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 7,
            "number": 1,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 8,
            "number": 2,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 9,
            "number": 2,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 10,
            "number": 2,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 11,
            "number": 2,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 12,
            "number": 3,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 13,
            "number": 3,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 14,
            "number": 3,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 15,
            "number": 3,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 16,
            "number": 4,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 17,
            "number": 4,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 18,
            "number": 4,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 19,
            "number": 4,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 20,
            "number": 5,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 21,
            "number": 5,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 22,
            "number": 5,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 23,
            "number": 5,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 24,
            "number": 6,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 25,
            "number": 6,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 26,
            "number": 6,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 27,
            "number": 6,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 28,
            "number": 7,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 29,
            "number": 7,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 30,
            "number": 7,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 31,
            "number": 7,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 32,
            "number": 8,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 33,
            "number": 8,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 34,
            "number": 8,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 35,
            "number": 8,
            "color": "blue"
        }, {
            "type": "numbered",
            "order": 36,
            "number": 9,
            "color": "red"
        }, {
            "type": "numbered",
            "order": 37,
            "number": 9,
            "color": "yellow"
        }, {
            "type": "numbered",
            "order": 38,
            "number": 9,
            "color": "green"
        }, {
            "type": "numbered",
            "order": 39,
            "number": 9,
            "color": "blue"
        }, {
            "type": "wild",
            "order": 40,
            "name": "+4"
        }, {
            "type": "wild",
            "order": 41,
            "name": "+4"
        }, {
            "type": "wild",
            "order": 42,
            "name": "+4"
        }, {
            "type": "wild",
            "order": 43,
            "name": "+4"
        }, {
            "type": "wild",
            "order": 44,
            "name": "wild"
        }, {
            "type": "wild",
            "order": 45,
            "name": "wild"
        }, {
            "type": "wild",
            "order": 46,
            "name": "wild"
        }, {
            "type": "wild",
            "order": 47,
            "name": "wild"
        }, {
            "type": "special",
            "order": 48,
            "name": "+2",
            "color": "red"
        }, {
            "type": "special",
            "order": 49,
            "name": "+2",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 50,
            "name": "+2",
            "color": "green"
        }, {
            "type": "special",
            "order": 51,
            "name": "+2",
            "color": "blue"
        }, {
            "type": "special",
            "order": 52,
            "name": "+2",
            "color": "red"
        }, {
            "type": "special",
            "order": 53,
            "name": "+2",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 54,
            "name": "+2",
            "color": "green"
        }, {
            "type": "special",
            "order": 55,
            "name": "+2",
            "color": "blue"
        }, {
            "type": "special",
            "order": 56,
            "name": "reverse",
            "color": "red"
        }, {
            "type": "special",
            "order": 57,
            "name": "reverse",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 58,
            "name": "reverse",
            "color": "green"
        }, {
            "type": "special",
            "order": 59,
            "name": "reverse",
            "color": "blue"
        }, {
            "type": "special",
            "order": 60,
            "name": "reverse",
            "color": "red"
        }, {
            "type": "special",
            "order": 61,
            "name": "reverse",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 62,
            "name": "reverse",
            "color": "green"
        }, {
            "type": "special",
            "order": 63,
            "name": "reverse",
            "color": "blue"
        }, {
            "type": "special",
            "order": 64,
            "name": "skip",
            "color": "red"
        }, {
            "type": "special",
            "order": 65,
            "name": "skip",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 66,
            "name": "skip",
            "color": "green"
        }, {
            "type": "special",
            "order": 67,
            "name": "skip",
            "color": "blue"
        }, {
            "type": "special",
            "order": 68,
            "name": "skip",
            "color": "red"
        }, {
            "type": "special",
            "order": 69,
            "name": "skip",
            "color": "yellow"
        }, {
            "type": "special",
            "order": 70,
            "name": "skip",
            "color": "green"
        }, {
            "type": "special",
            "order": 71,
            "name": "skip",
            "color": "blue"
        }]

        self.deck_ = self.deck
    
        self.discard_pile = {}

        self.hand1 = []
        self.hand2 = []
    
    def deal_cards(self):
        for i in range(7):
            random_card_index = random.randrange(len(self.deck))
            self.hand1.append(self.deck[random_card_index])
            self.deck.pop(random_card_index)
        for i in range(7):
            random_card_index = random.randrange(len(self.deck))
            self.hand2.append(self.deck[random_card_index])
            self.deck.pop(random_card_index)

    def humanize_hand(self, hand):
        cards = []
        for i in range(len(hand)):
            if i['type'] == "numbered":
                cards.append(f"{i['color']}, {i['number']}")
            elif i['type'] == "wild":
                cards.append(f"{i['name']}")
            else:
                cards.append(f"{i['color']}, {i['name']}")
        return cards

    def show_cards(self, user, hand):
        if hand == 1:
            statement = f"{user}, you have {len(self.hand1)} cards."
            cards = []
            for i in self.hand1:
                if i['type'] == "numbered":
                    cards.append(f"{i['color']}, {i['number']}")
                elif i['type'] == "wild":
                    cards.append(f"{i['name']}")
                else:
                    cards.append(f"{i['color']}, {i['name']}")
            body = ""
            for i in cards:
                body += f"{i}\n"
            return [statement, body]
        else:
            statement = f"{user}, you have {len(self.hand2)} cards."
            cards = []
            for i in self.hand2:
                if i['type'] == "numbered":
                    cards.append(f"{i['color']}, {i['number']}")
                elif i['type'] == "wild":
                    cards.append(f"{i['name']}")
                else:
                    cards.append(f"{i['color']}, {i['name']}")
            body = ""
            for i in cards:
                body += f"{i}\n"
            return [statement, body]
