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
    suits: list = ["Spades", "Hearts", "Clubs", "Diamonds"]
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
    playerCards = [Card("", 0)]
    numPlayerCards = 0

    dealerCards = [Card("", 0)]
    numDealerCards = 0

    def __init__(self, playerCards: Type[Card], numPlayerCards: int, dealerCards: Type[Card], numDealerCards: int, playerType: str) -> None:
        if playerType == "p":
            self.playerCards = playerCards
            self.numPlayerCards = numPlayerCards
        else:
            self.dealerCards = dealerCards
            self.numDealerCards = numDealerCards

    def getCards(self, playerType: str) -> str:
        cardsString = ""
        if playerType == "p":
            for card in self.playerCards:
                if card.getRank() != 0:
                    cardsString += card.printCard() + "\n"
        else:
            for card in self.dealerCards:
                if card.getRank() != 0:
                    cardsString += card.printCard() + "\n"

        return cardsString

    def clear(self, playerType: str) -> None:
        if playerType == "p":
            self.playerCards.clear()
            self.numPlayerCards = 0
        else:
            self.dealerCards.clear()
            self.numDealerCards = 0

    def addCard(self, card: Type[Card], playerType: str) -> None:
        if playerType == "p":
            if self.numPlayerCards <= MAX_CARDS:
                self.playerCards.append(card)
                self.numPlayerCards += 1
        else:
            if self.numDealerCards <= MAX_CARDS:
                self.dealerCards.append(card)
                self.numDealerCards += 1

    def total(self, playerType: str) -> int:
        scores = {}
        rankList = []
        if playerType == "p":
            rankList = [card.getRank() for card in self.playerCards]
        else:
            rankList = [card.getRank() for card in self.dealerCards]

        for i in range(len(rankList)):
            for combination in combinations(rankList, i + 1):
                if sum(combination) <= 21:
                    scores[sum(combination)] = combination

        scoresList = list(scores[max(scores.keys())])

        return sum(scoresList)


class Player:
    __hand = Hand([Card("", 0)], 0, None, 0, "p")
    __score = 0

    def __init__(self, hand: Type[Hand], score: int) -> None:
        self.__hand = hand
        self.__score = score

    def getScore(self) -> int:
        return self.__score

    def hit(self, card: Type[Card], playerType: str) -> None:
        self.__hand.addCard(card, playerType)

    def total(self, playerType: str) -> int:
        return self.__hand.total(playerType)

    def getHand(self, playerType: str) -> str:
        return self.__hand.getCards(playerType)

    def addPoints(self, points: int) -> None:
        self.__score += points

    def handClear(self, playerType: str) -> None:
        self.__hand.clear(playerType)


class Dealer(Player):
    def __init__(self, hand: Type[Hand], score: int) -> None:
        super().__init__(hand, score)

    def autoPlay(self, d: Type[Deck]) -> None:
        handPointValue = 0
        while handPointValue < 16:
            self.hit(d.deal(), "d")
            handPointValue += d.deal().getRank()


class BlackJackGame:
    deck = None
    dealer = Dealer(None, 0)
    player = Player(None, 0)

    def __init__(self, deck: Type[Deck]) -> None:
        self.deck = deck

        playerCard = Card("", 0)
        dealerCard = Card("", 0)

        playerHand = Hand([playerCard], 0, None, 0, "p")
        dealerHand = Hand(None, 0, [dealerCard], 0, "d")

        self.dealer: Type[Dealer] = Dealer(playerHand, 0)
        self.player: Type[Player] = Player(dealerHand, 0)

        self.numOfRounds = 1

    def createInitialHand(self, playerType: str) -> None:
        if playerType == "p":
            self.player.hit(self.deck.deal(), playerType)
            self.player.hit(self.deck.deal(), playerType)
        else:
            self.dealer.hit(self.deck.deal(), playerType)
            self.dealer.hit(self.deck.deal(), playerType)

    def resetHand(self, p: Type[Player], playerType: str) -> None:
        p.handClear(playerType)

    def play(self) -> None:

        print("\nInitial Player Score:", self.player.getScore())
        print("Initial Dealer Score:", self.dealer.getScore())

        while not self.deck.closeToEmpty():
            print("\nROUND " + str(self.numOfRounds))
            print("=========")

            # Dealing two cards to player
            print("\nCreating initial hand for player")
            self.createInitialHand("p")
            print(self.player.getHand("p"))
            print("Total points for player:", self.player.total("p"))

            # Dealing two cards to dealer
            print("\nCreating initial hand for dealer")
            self.createInitialHand("d")
            print(self.dealer.getHand("d"))
            print("Total points for dealer:", self.dealer.total("d"))

            print("\n")

            # Continuously ask for input from player until either HIT or STAY is entered
            inputStr = ""
            while inputStr != "HIT" and inputStr != "STAY":
                inputStr = input("Enter HIT or STAY: ")

            # DEALER WIN CASE

            # If player inputs HIT then deal a card to player and check if points for player are
            # more than 21 then dealer wins the round
            if inputStr == "HIT":
                self.player.hit(self.deck.deal(), "p")
                print("\nPlayer hand at round " + str(self.numOfRounds))
                print(self.player.getHand("p"))
                print("Total points for player:", self.player.total("p"))
                if self.player.total("p") >= 21:
                    self.dealer.addPoints(1)
                    print("\nDealer wins round " + str(self.numOfRounds) + "!")
                    # round is over, reset for next round
                    self.resetHand(self.player, "p")
                    self.resetHand(self.dealer, "d")
                    # display score after each round ends
                    print("\nPlayer Score after round " +
                          str(self.numOfRounds) + ":", self.player.getScore())
                    print("Dealer Score after round " +
                          str(self.numOfRounds) + ":", self.dealer.getScore())
                    # goto next round
                    self.numOfRounds += 1
                    continue

            # If player inputs STAY then continuously deal cards to dealer until it's score is
            # less than 16
            if inputStr == "STAY":
                self.dealer.autoPlay(self.deck)
                print("\nDealer hand at round " + str(self.numOfRounds))
                print(self.dealer.getHand("d"))
                print("Total points for dealer:", self.dealer.total("d"))

            # PLAYER WIN CASE

            # If the player has a greater total than the dealer or the dealer total crosses above
            # 21 then player wins the round
            if self.player.total("p") > self.dealer.total("d") or self.dealer.total("d") >= 21:
                self.player.addPoints(1)
                print("\nPlayer wins round " + str(self.numOfRounds) + "!")
                # round is over, reset for next round
                self.resetHand(self.player, "p")
                self.resetHand(self.dealer, "d")
                # display score after each round ends
                print("\nPlayer Score after round " +
                      str(self.numOfRounds) + ":", self.player.getScore())
                print("Dealer Score after round " +
                      str(self.numOfRounds) + ":", self.dealer.getScore())
                # goto next round
                self.numOfRounds += 1
                continue

            # DRAW CASE
            print("\nDraw! for round " + str(self.numOfRounds))

            # display score after each round ends
            print("\nPlayer Score after round " +
                  str(self.numOfRounds) + ":", self.player.getScore())
            print("Dealer Score after round " +
                  str(self.numOfRounds) + ":", self.dealer.getScore())

            self.numOfRounds += 1

            # reset hands after each round
            self.resetHand(self.player, "p")
            self.resetHand(self.dealer, "d")

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
