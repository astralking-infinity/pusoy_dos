import sys
from functools import partial
from pprint import pprint

from pusoy_dos import *
from player_nodes import ActivePlayer

# Pusoy dos (Filipino Poker)
# Rules:
#   -> Suits ranking (from highest to lowest): 'Diamonds', 'Hearts', 'Spades', 'Clubs'
#   -> Cards ranking: highest is '2 of Diamonds', Lowest card is '3 of Clubs'
# Combinations:
#   Pair: 2 cards with equal value
#   Three of a kind: 3 cards with equal value
#   Straight: 5 cards with consecutive value with different suits (Rank by highest single in each straight)
#   Flush: 5 cards with same suit (Ranked by suits of each Flush)
#   Full house: Combination of Three of a kind and a Pair (Ranked by Three of a kind used)
#   Four of a kind: 4 cards with equal value plus a single card of any value (Ranked by four cards used)
#   Straight flush: 5 cards with consecutive values and same suit

# Initialize deck
deck = Deck()
deck.shuffle()

# Prepare players
john = Player('John')
jane = Player('Jane')
jess = Player('Jess')
june = Player('June')

# players = [john, jane, jess, june]
players = ActivePlayer(john, jane, jess, june)

# Deal cards for each player in rotation until there are no cards left in deck.
while deck.not_empty():
    players.next_turn().draw(deck)

print('Number of players:', players.get_size())
print(players)

player_in_control = None

# Determine the first turn by the player with the lowest card on hand
for player in players:
    if Card('Clubs', '3') in player.hand:
        player_in_control = players.assign_control(player)
        break


####### Implementing 'lock' system???????????????? #########
# The idea is an instance will be locked until a 'key' has
# been passed to another player.

winners = []
loser = None

previous_move = None

first_turn = True
next_turn = False
pass_ = False
pass_count = 0
while players.get_size() > 1:
    print('\nPass count:', pass_count)
    print('Player size:', players.get_size(), 'Pass count:', pass_count)
    try:
        if pass_count == (players.get_size() - 1) or first_turn:
            if player_in_control not in players:
                player = players.assign_control(players.get_first())
            else:
                player = players.assign_control(player_in_control)
            print(f"""{f" {player.name}'s turn and control ":#^50}""")
            pass_count = 0
        elif next_turn:
            player = players.next_turn()
            print(f"""{f" {player.name}'s turn ":#^50}""")
            next_turn = False
        else:
            print('Something went wrong')
    except Exception as e:
        print(e)

    print('Cards on hand:', player.card_count())
    player.sort_hand()
    player.show_hand()

    picked_cards = []

    # Choose cards to form valid combination
    print('Choose card(s) to form a combination:(<suit> <value>):')
    while True:

        try:
            picked_card = input('> ').title()
            if not picked_card:
                continue

            if picked_card == 'Quit' or picked_card == 'Q':
                # Optional exit status for faster bug fixing.
                sys.exit()
            elif picked_card == 'Done' or picked_card == 'D':
                if first_turn and Card('Clubs', '3') not in picked_cards:
                    print('Please include 3 of clubs in play as a first turn. Try again.')
                    picked_cards = []
                    continue
                group_cards = group_value(picked_cards)
                picked_cards.sort(key=partial(frequency_counter,
                                              group_cards=group_cards,
                                              func=card_func_key,
                                              valueby='rank'))
                valid, combotype = verify_combination(picked_cards)
                if valid:
                    card_play = CardPlay(combotype, picked_cards)
                    if not previous_move or player_in_control == player:
                        previous_move = player.play(card_play)
                        next_turn = True
                        player_in_control = player
                        if player.has_empty_hand():
                            print('Player', player.name, 'done')
                            winners.append(player)
                            players.remove(player)
                    else:
                        if is_higher(card_play, previous_move):
                            previous_move = player.play(card_play)
                            next_turn = True
                            player_in_control = player
                            if player.has_empty_hand():
                                print('Player', player.name, 'done')
                                winners.append(player)
                                players.remove(player)
                        else:
                            print('Wrong card(s). Choose another card(s) to play.')
                            picked_cards = []
                            continue
                else:
                    pprint(picked_cards)
                    print('Not a valid combination. Try again.')
                    picked_cards = []
                    continue
                break

            elif picked_card == 'Pass':
                if first_turn or player_in_control == player:
                    print('Player in control of the game cannot pass.')
                else:
                    pass_ = True
                    break
            else:
                suit, value = picked_card.split()

                if suit not in SUIT.keys() or value not in CARD_RANKS:
                    print(f"Wrong input.")
                    continue

                card = Card(suit, value)
                if card not in player.hand:
                    print(f"You don't have the card, {card}.")
                elif card in picked_cards:
                    print(f'{card} is already picked. Choose another one.')
                else:
                    picked_cards.append(card)
        except ValueError:
            print('Invalid input format.')

    print('Card played: ', previous_move)

    if pass_:
        next_turn = True
        pass_ = False
        pass_count += 1
    else:
        pass_count = 0
    first_turn = False

print('Game over. Loser:', players.get_last().name)
