import random

#Todo have cards be drawn from an actual deck
#todo optional money system
#.pop

def main():
    print("Welcome to Blackjack!")
#todo jack queen king
    card_dic={
    }
    player_card=[]
    for i in range(2):
        player_card.append(random.randint(1,13))

    dealer_cards = [random.randint(1, 13),random.randint(1,13)]
    if sum(dealer_cards) > 21:
        print("You won! Dealer went over 21.")
        return
    # Handle dealer drawing the cards
    print(f"Dealer has a visible card: {dealer_cards[0]}")

    # f' or f" will allow variables within strings
    while 1:
        print(f'Your cards {player_card} with a sum of {sum(player_card)}')
        if sum(player_card) > 21:
            print("You lost!")
            return

        user_input = input("Do you want to hit (y), stay (n), or quit (q)?")

        # Makes input case-insensitive
        user_input = user_input.lower()
        if user_input == 'y':
            new_card=random.randint(1,13)
            print(f'New card {new_card}')
            player_card.append(new_card)
        elif user_input == 'n':
            print("Stay")
            break
        elif user_input == 'q':
            return
        else:
                print("Invalid input")

    print(f"Your final cards: {player_card} with a sum of {sum(player_card)}")

    #Algorithm for dealer hit
    while sum(dealer_cards) <= 17-5:
        dealer_cards.append(random.randint(1,13))
        if sum(dealer_cards) > 21:
            print("You won! Dealer went over 21.")
            return



    #Now we have the dealer and player cards
    print(f"Revealing dealer cards: {dealer_cards}, with a sum of {sum(dealer_cards)}")
    if sum(player_card) > sum(dealer_cards):
        print("You won!")
    else:
        print("You lost!")


if __name__ == '__main__':
    main()