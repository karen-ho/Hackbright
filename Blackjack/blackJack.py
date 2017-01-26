# Hackbright game for Winter 2017 
import random

# definition of a deck of cards
suits_name = {
    "Heart": u'\u2764', 
    "Diamond": u'\u2666', 
    "Spade": u'\u2660', 
    "Club": u'\u2663'
    }

card_values = {
    "Ace": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

class Card(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.points = card_values[value]
        self.symbol = suits_name[suit]

    def is_ace(self):
        return self.value.lower() == "ace"

    def name(self):
        return self.value + "-" + self.suit

# returns a list of cards
def create_deck():
    deck = []
    for card_value in card_values:
        for suit in suits_name:
            deck.append(Card(suit, card_value))

    return deck

# determines value of cards on hand
# will determine with to use ace as 11 or 1 points
def get_points(cards):
    points = 0 #when ace = 11
    num_aces = 0

    for card in cards:
        if card.is_ace():
            num_aces = num_aces + 1

        points = points + card.points

    if points <= 21:
        return points

    for num in xrange(num_aces):
        if points <= 21:
            return points

        points = points - 10

    return points

# prints out an intro
def print_intro():
    print_line()
    with open('intro.txt', 'r') as f:
        data = f.read()
        print data
    print "Welcome to BlackJack!"

# prints a new line of starts
def print_line():
    print "*" * 80

# prints your hand with ascii art
def print_cards(cards, is_dealer_first_hand=False):
    num = len(cards)
    border_top = ("_" * 11 + " ") * num
    border_bottom = ("-" * 11 + " ") * num

    if is_dealer_first_hand:
        side_border = "|" + " " * 9 + "| |" +  u'\u26C6' * 9 + "|"
        card_top = "|" + cards[0].value + " " * (9 - len(cards[0].value)) + "| |" + u'\u26C6' * 9 + "|"
        card_bottom = "|" +  " " * (9 - len(cards[0].value)) + cards[0].value + "| |" + u'\u26C6' * 9 + "|"
        card_face = "|" + " " * 4 + cards[0].symbol + " " * 4 + "| |" + u'\u26C6' * 9 + "|"

    else:
        side_border = ("|" + " " * 9 + "| ") * num

        card_top = ""
        card_face = ""
        card_bottom = ""
        for card in cards:
            card_top = card_top + "|" + card.value + " " * (9 - len(card.value)) + "| "
            card_face = card_face + "|" + " " * 4 + card.symbol + " " * 4 + "| "
            card_bottom = card_bottom + "|" +  " " * (9 - len(card.value)) + card.value + "| "

    print border_top
    print card_top
    print side_border
    print side_border
    print card_face
    print side_border
    print side_border
    print card_bottom
    print border_bottom

# checks to see if you have won
def is_game_over(my_cards, dealer_cards, is_first_draw):
    current_points = get_points(my_cards)
    dealer_points = get_points(dealer_cards)
    # check for black jack
    if  is_first_draw and (current_points == 21 or dealer_points == 21):
        return True
    elif current_points > 21:
        return True
    
    return False

# shuffle the discard cards into the deck
def deal_card_or_shuffle(deck, discard):
    if len(deck) == 0:
        random.shuffle(discard)
        deck = discard[:]
        discard = []
        print "Deck has been shuffled"
    card =  deck.pop(0)
    return card, deck, discard

# check win conditions after no more actions
def check_winner(my_cards, dealer_cards, is_first_draw):
    current_points = get_points(my_cards)
    dealer_points = get_points(dealer_cards)
    if is_first_draw:
        if current_points == 21:
            print "BlackJack!! Congratulations"
        elif dealer_points == 21:
            print "Dealer has " + print_hand(dealer_cards)
            print "Dealer got BlackJack"
    else:
        if current_points > 21:
           print "Busted :("
        elif dealer_points > 21:
            print "Dealer busted. You win!"
        elif dealer_points > current_points:
            print "Dealer wins"
        elif dealer_points < current_points:
            print "You win!"
        else:
            print "It's a tie"

def print_hand(cards):
    return ", ".join(map(lambda x: x.name(), cards))

def play_black_jack():
    deck = create_deck()
    random.shuffle(deck)

    discard = []
    starting = raw_input("What would you like to do? Deal (d), Quit (q) ")
    print_line()

    while not starting.lower() == "q":
        if starting.lower() == "d":
            is_first_draw = True
            first_card, deck, discard = deal_card_or_shuffle(deck, discard)
            second_card, deck, discard = deal_card_or_shuffle(deck, discard)
            my_cards = [first_card, second_card]

            dealer_first_card, deck, discard = deal_card_or_shuffle(deck, discard)
            dealer_second_card, deck, discard = deal_card_or_shuffle(deck, discard)
            dealer_cards = [dealer_first_card, dealer_second_card]

            print_cards(dealer_cards, True)
            print "Dealer has " + dealer_first_card.name() + ", hidden"

            print_cards(my_cards)
            print "You have " + print_hand(my_cards)

            print_line()

            while not is_game_over(my_cards, dealer_cards, is_first_draw):
                action = raw_input("Do you want to Hit (h) or Stay (s)? ")
                is_first_draw = False

                if action.lower() == "h":
                    next_card, deck, discard = deal_card_or_shuffle(deck, discard)
                    my_cards.append(next_card)

                    print_cards(dealer_cards, True)
                    print "Dealer has " + dealer_first_card.name() + ", hidden"

                    print_cards(my_cards)
                    print "You have " + print_hand(my_cards)

                    print "You have drawn a " + next_card.name()
                    print_line()
                elif action.lower() == "s":
                    dealer_points = get_points(dealer_cards)

                    print_cards(dealer_cards)
                    print "Dealer has " + print_hand(dealer_cards)

                    print_cards(my_cards)
                    print "You have " + print_hand(my_cards)
                    print_line()

                    while dealer_points < 17:
                        dealer_next_card, deck, discard = deal_card_or_shuffle(deck, discard)
                        dealer_cards.append(dealer_next_card)
                        dealer_points = get_points(dealer_cards)

                        print_cards(dealer_cards)
                        print "Dealer has " + print_hand(dealer_cards)

                        print_cards(my_cards)
                        print "You have " + print_hand(my_cards)

                        print "Dealer has drawn a " + dealer_next_card.name()
                        print_line()

                    break
                else: 
                    print "Invalid command. "

            check_winner(my_cards, dealer_cards, is_first_draw)
            discard = discard + my_cards + dealer_cards

        else:
            print "Invalid command. "

        starting = raw_input("What would you like to do? Deal (d), Quit (q) ")

    print "Thanks for playing!"

print_intro()
play_black_jack()