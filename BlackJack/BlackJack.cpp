#include <iostream>

#define MAX_CARDS 11

using std::string;

class Card
{
public:
    Card()
    {
        suit = "";
        rank = 0;
    }

    Card(string SUIT, int RANK) : suit(SUIT), rank(RANK) {}

    string getSuit() const
    {
        return suit;
    }

    int getRank() const
    {
        return rank;
    }

    string printCard() const
    {
        return std::to_string(rank) + " of " + suit;
    }

private:
    string suit;
    int rank;
};

class Deck
{
public:
    Deck()
    {
        Card card;
        for (int i = 0; i < 52; i++)
        {
            deck[i] = card;
        }

        currCard = 0;
    }

    Deck(Card *DECK, int CURRCARD) : currCard(CURRCARD)
    {
        for (int i = 0; i < 52; i++)
        {
            deck[i] = DECK[i];
        }
    }

    Card *getDeck()
    {
        return deck;
    }

    Card *shuffle()
    {
        // shuffle logic
        return deck;
    }

    Card deal()
    {
        Card cardDealt = deck[currCard];
        // pop the card at index currCard
        return cardDealt;
    }

    bool closeToEmpty()
    {
        return (sizeof(deck) / sizeof(deck[0])) < 10;
    }

private:
    Card deck[52];
    int currCard;
};

class Hand
{
public:
    Hand()
    {
        Card card;
        for (int i = 0; i < MAX_CARDS; i++)
        {
            cards[i] = card;
        }

        numCards = 0;
    }

    Hand(Card *CARDS, int NUMCARDS) : numCards(NUMCARDS)
    {
        for (int i = 0; i < sizeof(CARDS) / sizeof(CARDS[0]); i++)
        {
            cards[i] = CARDS[i];
        }
    }

    string getCards()
    {
        string cardsString = "";
        for (int i = 0; i < sizeof(cards) / sizeof(cards[0]); i++)
        {
            if (cards[i].getRank() != 0)
            {
                cardsString += cards[i].printCard() + "\n";
            }
        }

        return cardsString;
    }

    void clear()
    {
        Card card;
        for (int i = 0; i < sizeof(cards) / sizeof(cards[0]); i++)
        {
            cards[i] = card;
        }
    }

    void addCard(Card card)
    {
        std::cout << "Here in addCard()" << std::endl;
        std::cout << card.printCard() << std::endl;
        if (numCards < MAX_CARDS)
        {
            int currSize = sizeof(cards) / sizeof(cards[0]);
            std::cout << currSize << std::endl;
            cards[currSize] = card;
            numCards++;
        }

        for (int i = 0; i < sizeof(cards) / sizeof(cards[0]); i++)
        {
            std::cout << cards[i].printCard() << std::endl;
        }
    }

    int total()
    {
        int totalPoints = 0;
        for (int i = 0; i < sizeof(cards) / sizeof(cards[0]); i++)
        {
            totalPoints += cards[i].getRank();
        }

        return totalPoints;
    }

private:
    Card cards[MAX_CARDS];
    int numCards;
};

class Player
{
public:
    Player()
    {
        Hand h;
        hand = h;
        score = 0;
    }

    Player(Hand HAND, int SCORE) : hand(HAND), score(SCORE) {}

    int getScore() const
    {
        return score;
    }

    void hit(Card card)
    {
        std::cout << "Here in hit()" << std::endl;
        hand.addCard(card);
    }

    int total()
    {
        return hand.total();
    }

    string getHand()
    {
        return hand.getCards();
    }

    void addPoints(int points)
    {
        score += points;
    }

    void handClear()
    {
        hand.clear();
    }

private:
    Hand hand;
    int score;
};

class Dealer : public Player
{
public:
    Dealer() : Player() {}

    Dealer(Hand HAND, int SCORE) : Player(HAND, SCORE) {}

    void autoPlay(Deck d)
    {
        int handPointValue = 0;
        while (handPointValue < 16)
        {
            hit(d.deal());
            handPointValue += d.deal().getRank();
        }
    }
};

class BlackJackGame
{
public:
    BlackJackGame()
    {
        Deck d;
        deck = d;

        numOfRounds = 0;
    }

    BlackJackGame(Deck DECK) : deck(DECK)
    {
        Player p;
        player = p;

        Dealer d;
        dealer = d;

        std::cout << "Here in BlackJackGame()" << std::endl;
    }

    void createInitialHand(string playerType)
    {
        if (playerType == "p")
        {
            player.hit(deck.deal());
            player.hit(deck.deal());
        }
        else
        {
            dealer.hit(deck.deal());
            dealer.hit(deck.deal());
        }
    }

    void resetHand(Player p)
    {
        p.handClear();
    }

    void play()
    {
        std::cout << "Creating initial hand for player" << std::endl;
        createInitialHand("p");
        std::cout << player.getHand() << std::endl;
        std::cout << "Total points for player: " << player.total() << std::endl;

        std::cout << "Creating initial hand for dealer" << std::endl;
        createInitialHand("d");
        std::cout << dealer.getHand() << std::endl;
        std::cout << "Total points for dealer: " << dealer  .total() << std::endl;

        std::cout << "Initial player score: " << player.getScore() << std::endl;
        std::cout << "Initial dealer score: " << dealer.getScore() << std::endl;

        while (!deck.closeToEmpty())
        {
            string inputStr;
            std::cout << "Enter HIT or STAY: ";
            std::cin >> inputStr;
            while (inputStr != "HIT" || inputStr != "STAY")
            {
                std::cout << "Enter HIT or STAY: ";
                std::cin >> inputStr;
            }

            if (inputStr == "HIT")
            {
                player.hit(deck.deal());
                std::cout << player.getHand() << std::endl;
                std::cout << "Total points for player: " << player.total() << std::endl;
                if (player.total() > 21)
                {
                    dealer.addPoints(1);
                }
            }

            if (inputStr == "STAY")
            {
                dealer.autoPlay(deck);
                std::cout << dealer.getHand() << std::endl;
                std::cout << "Total points for dealer: " << dealer.total() << std::endl;
            }

            if (player.total() > dealer.total() || dealer.total() > 21)
            {
                player.addPoints(1);
            }

            numOfRounds++;

            std::cout << "Player score for round " << numOfRounds << ": " << player.getScore() << std::endl;
            std::cout << "Dealer score for round " << numOfRounds << ": " << dealer.getScore() << std::endl;
        }
    }

private:
    Deck deck;
    Player player;
    Dealer dealer;
    int numOfRounds;
};

int main()
{
    std::cout << "Welcome to BlackJack!" << std::endl;

    // Create the deck
    std::cout << "Creating Deck" << std::endl;
    Card deck[52];
    string suits[4] = {"Spades", "Hearts", "Clubs", "Diamonds"};
    int suitIndex = 0;

    for (int i = 0; i < 52; i++)
    {
        int rank = i % 13 + 1;
        int cardRank = rank;

        if (rank > 12)
        {
            suitIndex++;
        }

        if (suitIndex > 3)
        {
            suitIndex = 3;
        }

        // Ace has rank of 11
        if (rank == 1)
        {
            cardRank = 11;
        }

        // Jack, Queen and King all have rank of 10
        if (rank == 11 || rank == 12 || rank == 13)
        {
            cardRank = 10;
        }

        deck[i] = Card(suits[suitIndex], cardRank);
    }

    Deck newDeck = Deck(deck, 0);

    // Shuffle the Deck
    std::cout << "Shuffling Deck" << std::endl;
    newDeck.shuffle();

    // Play the BlackJack Game
    std::cout << "Staring the BlackJack game" << std::endl;
    BlackJackGame bjg = BlackJackGame(newDeck);
    bjg.play();

    return 0;
}