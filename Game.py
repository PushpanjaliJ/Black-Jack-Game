import random

# creating global variables for 52 cards of deck suits, ranks and values.
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True

# Card class --> each card object has a suit and a rank.
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # to print a card in form of 'Two of Hearts'
    def __str__(self):
        return self.rank + ' of ' + self.suit

# Deck class --> To hold all 52 card objects and to get shuffled.
class Deck:
    def __init__(self):
        self.deck = []     # to hold all the possible cards in a deck
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    # this print all the cards in deck
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    # for shuffling of cards to play
    def shuffle(self):
        random.shuffle(self.deck)

    # grabbing a card from the deck
    def deal(self):
        return self.deck.pop()

# Hand class --> to hold those cards that have been dealt to each player from the Deck.
class Hand:
    def __init__(self):
        self.cards = []     # this list holds all the cards the player is having
        self.value = 0      # storing the total of the values on the cards the player holds
        self.aces = 0       # count of number of ace cards the player got.

    # adding the value and card after hitting a card from the deck
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        # if the grabbed card is Ace, increase the count of aces by 1
        if card.rank == 'Ace':
            self.aces += 1

    # this game holds 1 and 11 values for the card Ace
    # if the values goes over 21 and there are ace cards with the player
    # the player adjusts the value by reducing it to 10, so that the value given for ace is 1
    # and decrease the number of ace cards count by 1
    def adjust_for_aces(self):
        while self.value > 21 and self.aces != 0:
            self.value -= 10
            self.aces -= 1

# Chips class --> to keep track of player's starting bankroll total, bet amount and ongoing winning or loosings.
class Chips:

    # by default the bankroll can be 100 in amount
    # or else the player can give the amount he want to have
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    # if the player wins, the bet amount adds to his bankroll
    def win_bet(self):
        self.total += self.bet

    # if the player looses, the bet amount deducts from his bankroll
    def loose_bet(self):
        self.total -= self.bet

# taking an input value of bet the player wants to play with.
def take_bet(chip):
    while True:
        try:
            chip.bet = int(input('How many chips bet? '))
        except ValueError:
            print('Sorry, it is not an integer.')
        else:
            if chip.bet > chip.total:
                print('Sorry, you can not exceed', chip.total)
            else:
                break

# it is called whenever the player requests for a hit
# or Dealer's hand having the total value less than 17
# either player can take hits until the bust(value exceeding 21)
# dealing a card off the deck and adding it to the hand
# also adjusting the aces if player exceeds 21.
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()

# asking player whether he/she wants to hit or stand
# hit --> grab a card from deck and play
# stand --> let the dealer play
def hit_or_stand(deck, hand):
    global playing    # to control the while loop ahead
    while True:
        x = input("Would you like to hit or stand: 'h' or 's': ")
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print('Dealer plays.')
            playing = False
        else:
            print('Sorry, please try again.')
            continue
        break

# To display cards after the player hitting a card.
def show_some(player, dealer):

    # show only one of the dealer's cards
    print("Dealer's hand: ")
    print('First card is hidden!')
    print(dealer.cards[1])

    # show all (2 cards) of the player's hand
    print("\n Player's hand:")
    for card in player.cards:
        print(card)

# At the end of the game, all cards are shown with the hand's total values.
def show_all(player, dealer):

    # show all dealer's cards
    print('\n Dealers cards: ')
    for card in dealer.cards:
        print(card)
    print('Value of Dealers hand: {}'.format(dealer.value))

    #show all the players cards
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)
    print("Value of Player's hand: {}".format(player.value))

# The end scenarios of the game:
# 1. Player busts --> The value of player goes over 21.
# 2. Player wins --> Player goes near to 21 than the dealer.
# 3. Dealer busts --> The value of dealer goes over 21.
# 4. Dealer wins --> Dealer goes near to 21 than the player.
# 5. Push --> When the game goes tie with same values with dealer and player.

def player_bust(player, dealer, chips):
    print('Player busts!')
    chips.loose_bet()

def player_wins(player, dealer, chips):
    print('Player wins!')
    chips.win_bet()

def dealer_bust(player, dealer, chips):
    print('Dealer Busts!')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('Dealer wins!')
    chips.loose_bet()

def push(player, dealer):
    print('Tie!')


# STARTING THE GAME
while True:
    print('WELCOME TO BLACK JACK GAME!')

    # create and shuffle the deck, deal two cards to each one
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # create chips and take bet
    player_chips = Chips()
    take_bet(player_chips)

    # now show the cards in between the game
    show_some(player_hand, dealer_hand)

    # playing the game until the player busts
    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            break

    # dealer plays
    if player_hand.value <= 21:

        # until the dealer value is greater than 17.
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_bust(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    print("\n Player's winnings stand at ", player_chips.total)

    # ask the player if he want to replay
    new_game = input('Do you want to play again? Y or N: ')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing!')
        break
