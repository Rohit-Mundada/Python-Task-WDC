from itertools import combinations
import random
from typing import Type


MAX_CARDS = 11


class Card:
    suit = ""
    rank = 0

    def __init__(self, suit: str, rank: int) -> None:
        self.suit = suit
        self.rank = rank

    def getSuit(self) -> str:
        return self.suit

    def getRank(self) -> int:
        return self.rank

    def printCard(self) -> str:
        return "%s" % self.rank + " of " + self.suit


class Deck:
    deck = [Card("", 0)]
    currCard = 0

    def __init__(self, deck: Type[Card], currCard: int) -> None:
        self.deck = deck
        self.currCard = currCard

    def getDeck(self) -> Card:
        return self.deck

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def deal(self) -> Card:
        cardDealt = self.deck[self.currCard]
        self.deck.pop(self.currCard)
        return cardDealt

    def closeToEmpty(self) -> bool:
        if len(self.deck) < 10:
            return True
        else:
            return False


class Hand:
    cards = [Card("", 0)]
    numCards = 0

    def __init__(self, cards: Type[Card], numCards: int) -> None:
        self.cards = cards
        self.numCards = numCards

    def getCards(self) -> str:
        cardsString = ""
        for card in self.cards:
            if card.getRank() != 0:
                cardsString += card.printCard() + "\n"

        return cardsString

    def clear(self) -> None:
        self.cards.clear()
        self.numCards = 0

    def addCard(self, card: Type[Card]) -> None:
        if self.numCards < MAX_CARDS:
            self.cards.append(card)
            self.numCards += 1

    def total(self) -> int:
        scores = {}
        rankList = [card.getRank() for card in self.cards]

        for i in range(len(rankList)):
            for combination in combinations(rankList, i + 1):
                if sum(combination) <= 21:
                    scores[sum(combination)] = combination

        scoresList = list(scores[max(scores.keys())])

        return sum(scoresList)


class Player:
    __hand = Hand([Card("", 0)], 0)
    __score = 0

    def __init__(self, hand: Type[Hand], score: int) -> None:
        self.__hand = hand
        self.__score = score

    def getScore(self) -> int:
        return self.__score

    def hit(self, card: Type[Card]) -> None:
        self.__hand.addCard(card)

    def total(self) -> int:
        return self.__hand.total()

    def getHand(self) -> str:
        return self.__hand.getCards()

    def addPoints(self, points: int) -> None:
        self.__score += points

    def handClear(self) -> None:
        self.__hand.clear()


class Dealer(Player):
    def __init__(self, hand: Type[Hand], score: int) -> None:
        super().__init__(hand, score)

    def autoPlay(self, d: Type[Deck]) -> None:
        handPointValue = 0
        while handPointValue < 16:
            self.hit(d.deal())
            handPointValue += d.deal().getRank()


class BlackJackGame:
    deck = [Card("", 0)]
    dealer = Dealer(Hand([Card("", 0)], 0), 0)
    player = Player(Hand([Card("", 0)], 0), 0)
    numOfRounds = 1

    def __init__(self, deck: Type[Deck]) -> None:
        self.deck = deck

    def createInitialHand(self, playerType: str) -> None:
        if playerType == "p":
            self.player.hit(self.deck.deal())
            self.player.hit(self.deck.deal())
        else:
            self.dealer.hit(self.deck.deal())
            self.dealer.hit(self.deck.deal())

    def resetHand(self, p: Type[Player]) -> None:
        p.handClear()

    def play(self) -> None:
        # Initial condition
        print("\nInitial Player Score:", self.player.getScore())
        print("Initial Dealer Score:", self.dealer.getScore())
        # Number of cards in deck at the start
        print("\nNumber of cards in the deck initially:",
              len(self.deck.getDeck()))

        while not self.deck.closeToEmpty():
            print("\n#=========#")
            print("# ROUND " + str(self.numOfRounds) + " #")
            print("#=========#")

            # Dealing two cards to player
            print("\nCreating initial hand for player")
            self.createInitialHand("p")
            print(self.player.getHand())
            print("Total points for player:", self.player.total())

            # Dealing two cards to dealer
            print("\nCreating initial hand for dealer")
            self.createInitialHand("d")
            print(self.dealer.getHand())
            print("Total points for dealer:", self.dealer.total())

            print("\n")

            # Continuously ask for input from player until either HIT or STAY is entered
            inputStr = ""
            while inputStr != "HIT" and inputStr != "STAY":
                inputStr = input("Enter HIT or STAY: ")

            #=================#
            # DEALER WIN CASE #
            #=================#

            # If player inputs HIT then deal a card to player and check if points for player are
            # more than 21 then dealer wins the round
            if inputStr == "HIT":
                self.player.hit(self.deck.deal())
                print("\nPlayer hand at round " + str(self.numOfRounds))
                print(self.player.getHand())
                print("Total points for player:", self.player.total())
                if self.player.total() >= 21:
                    self.dealer.addPoints(1)
                    print("\nDealer wins round " + str(self.numOfRounds) + "!")
                    # Round is over, reset for next round
                    self.resetHand(self.player)
                    self.resetHand(self.dealer)
                    # Display score after each round ends
                    print("\nPlayer Score after round " +
                          str(self.numOfRounds) + ":", self.player.getScore())
                    print("Dealer Score after round " +
                          str(self.numOfRounds) + ":", self.dealer.getScore())
                    # Display number of cards left in deck after each round ends
                    print("\nNumber of cards left in deck after round " +
                          str(self.numOfRounds) + ":", len(self.deck.getDeck()))
                    # Goto next round
                    self.numOfRounds += 1
                    continue

            # If player inputs STAY then continuously deal cards to dealer until it's score is
            # less than 16
            if inputStr == "STAY":
                self.dealer.autoPlay(self.deck)
                print("\nDealer hand at round " + str(self.numOfRounds))
                print(self.dealer.getHand())
                print("Total points for dealer:", self.dealer.total())

            #=================#
            # PLAYER WIN CASE #
            #=================#

            # If the player has a greater total than the dealer or the dealer total crosses above
            # 21 then player wins the round
            if self.player.total() > self.dealer.total() or self.dealer.total() >= 21:
                self.player.addPoints(1)
                print("\nPlayer wins round " + str(self.numOfRounds) + "!")
                # Round is over, reset for next round
                self.resetHand(self.player)
                self.resetHand(self.dealer)
                # Display score after each round ends
                print("\nPlayer Score after round " +
                      str(self.numOfRounds) + ":", self.player.getScore())
                print("Dealer Score after round " +
                      str(self.numOfRounds) + ":", self.dealer.getScore())
                # Display number of cards left in deck after each round ends
                print("\nNumber of cards left in deck after round " +
                      str(self.numOfRounds) + ":", len(self.deck.getDeck()))
                # Goto next round
                self.numOfRounds += 1
                continue

            #===========#
            # DRAW CASE #
            #===========#

            print("\nDraw for round " + str(self.numOfRounds) + "!")
            # Round is over,  reset for next round
            self.resetHand(self.player)
            self.resetHand(self.dealer)
            # Display score after each round ends
            print("\nPlayer Score after round " +
                  str(self.numOfRounds) + ":", self.player.getScore())
            print("Dealer Score after round " +
                  str(self.numOfRounds) + ":", self.dealer.getScore())
            # Display number of cards left in deck after each round ends
            print("\nNumber of cards left in deck after round " +
                  str(self.numOfRounds) + ":", len(self.deck.getDeck()))
            # Goto next round
            self.numOfRounds += 1

        # Declare winner
        if self.player.getScore() > self.dealer.getScore():
            print("\n->You win by " + str(self.player.getScore() -
                  self.dealer.getScore()) + " rounds!<-")
        elif self.dealer.getScore() > self.player.getScore():
            print("\n->Dealer wins by " + str(self.dealer.getScore() -
                  self.player.getScore()) + " rounds!<-")
        else:
            print("\n->It's a draw!<-")

        # Game over
        print("\n-=-=-=-=-")
        print("Game over")
        print("-=-=-=-=-")


print("-=-=-=-=-=-=-=-=-=-=-")
print("Welcome to BlackJack!")
print("-=-=-=-=-=-=-=-=-=-=-")

# Create the Deck
print("\nCreating Deck")
deck: list = []
suits: list = ["Spades", "Hearts", "Clubs", "Diamonds"]
suitIndex: int = 0
for cardIndex in range(52):
    rank: int = cardIndex % 13 + 1
    cardRank: int = rank

    if rank > 12:
        suitIndex += 1

    if suitIndex > 3:
        suitIndex = 3

    # Ace has rank of 11
    if rank == 1:
        cardRank = 11

    # Jack, Queen and King all have rank of 10
    if rank == 11 or rank == 12 or rank == 13:
        cardRank = 10

    deck.append(Card(suits[suitIndex], cardRank))

newDeck = Deck(deck, 0)

# Shuffle the Deck
print("Shuffling Deck")
newDeck.shuffle()

# Play the BlackJack Game
print("Starting the BlackJack game")
bjg = BlackJackGame(newDeck)
bjg.play()
