import random
from bj_strategy import *
from bj_plays import *
from constants import *

STRATEGY_LIST = []

DEALER_INFO = [0, [['']], 0, 0, [False], [False], [False]]

def generate_deck(num_decks):
    deck = list(const.POSSIBLE_CARDS.keys()) * const.NUM_SUITS * num_decks
    random.shuffle(deck)

    stop_point = ((const.NUM_DECKS - const.RESERVE_DECKS) * const.NUM_CARDS_IN_DECK) + random.randint(0, const.NUM_CARDS_IN_DECK)
    
    return (deck, stop_point)

def initialize_felt(deck, player_info_list):
    dealer_cards = []

    deal_card(deck, dealer_cards)

    for player_num in range(const.NUM_PLAYERS):

        player_info_list[player_num][const.PLAYER_NUM_SPLITS_INDEX] = 0
        player_info_list[player_num][const.PLAYER_CARDS_LIST_INDEX] = [[]]
        player_info_list[player_num][const.PLAYER_HAND_INFO_LIST_INDEX] = [[]]
        player_info_list[player_num][const.PLAYER_BET_LIST_INDEX] = [0]
        player_info_list[player_num][const.PLAYER_BLACKJACK_LIST_INDEX] = [False]
        player_info_list[player_num][const.PLAYER_SURRENDER_LIST_INDEX] = [False]

        deal_card(deck, player_info_list[player_num][const.PLAYER_CARDS_LIST_INDEX][0])

    deal_card(deck, dealer_cards)

    for player_num in range(const.NUM_PLAYERS):
        deal_card(deck, player_info_list[player_num][const.PLAYER_CARDS_LIST_INDEX][0])

    return (dealer_cards, player_info_list)

def play_hand_dealer(deck: list[str], drawn_cards: list[str]) -> int:
    print("\nPlaying dealer's hand. Starting cards:")
    print(drawn_cards)
    
    num_cards_drawn = 0
    
    hand_info = get_hand_info(drawn_cards)
    
    if(hand_info[const.HAND_SUM_INDEX] > 17):
        print("More than 17. Early Stand")
        return num_cards_drawn
    
    if(hand_info[const.HAND_SUM_INDEX] == 17 and hand_info[const.HAND_SOFT_INDEX] == False):
        print("Hard 17, Standing")
        return num_cards_drawn

    while((hand_info := get_hand_info(drawn_cards))[const.HAND_SUM_INDEX] < const.BUST_NUMBER and (hand_info[const.HAND_SUM_INDEX] <= 17)):
        if(hand_info[const.HAND_SUM_INDEX] == 17 and hand_info[const.HAND_SOFT_INDEX] == False):
            print("Hard 17, Standing")
            break

        elif(hand_info[const.HAND_SUM_INDEX] == 17 and hand_info[const.HAND_SOFT_INDEX] == True):
            print("Soft 17, Hitting")

        hit(drawn_cards, deck, DEALER_INFO)

        print("After that move, the Dealer's hand is now:")
        print(drawn_cards)
        
        num_cards_drawn += 1

    if(hand_info[const.HAND_SUM_INDEX] > const.BUST_NUMBER):
        print("Dealer bust! Valid players win!")
    else:
        stand(drawn_cards, deck, DEALER_INFO)

    return num_cards_drawn

def play_hand_player(deck: list, player_info: list[Union[int, list[list[str]], int, int, list[bool], list[bool], list[bool]]], dealer_card: str, player_num: int) -> int:
    print("\nPlaying Player", str(player_num) + "'s hand. Starting cards:")
    print(player_info[const.PLAYER_CARDS_LIST_INDEX], "with Dealer showing a", dealer_card)
    
    player_cards : list = player_info[const.PLAYER_CARDS_LIST_INDEX]
    
    num_cards_drawn = 0
    num_hands = len(player_cards)
    curr_hand_index = 0
    
    while(curr_hand_index < num_hands):
        while True:
            curr_hand = player_cards[curr_hand_index]
            print("Current hand:")
            print(curr_hand)
            
            hand_info = get_hand_info(curr_hand)
            player_info[const.PLAYER_HAND_INFO_LIST_INDEX][curr_hand_index] = hand_info
            
            if hand_info[const.HAND_SUM_INDEX] > const.BUST_NUMBER:
                print("Player", player_num, "busts!")
                break
            
            strategy = get_suggest_play(curr_hand, player_info, dealer_card, STRATEGY_LIST)
            
            current_play = ()

            current_play = PLAYS[strategy][const.PLAYS_FUNCTION_INDEX](curr_hand, deck, player_info, player_num, curr_hand_index)

            if current_play[const.CURRENT_PLAY_SUCCESS_INDEX]:
                
                match strategy:
                    
                    case const.STRATEGY_SPLIT | const.STRATEGY_SPLIT_DOUBLE_HIT | const.STRATEGY_SURRENDER_SPLIT:
                        
                        if not((strategy == const.STRATEGY_SPLIT_DOUBLE_HIT and not const.DOUBLE_AFTER_SPLIT_ALLOWED) or \
                            (strategy == const.STRATEGY_SURRENDER_SPLIT and not const.SURRENDER_ALLOWED)):
                            temp_cards = current_play[const.CURRENT_PLAY_SPLIT_CARDS_INDEX]
                            
                            player_cards.insert(curr_hand_index, temp_cards[0])
                            player_cards[curr_hand_index + 1] = temp_cards[1]
                            
                            player_info[const.PLAYER_HAND_INFO_LIST_INDEX].insert(curr_hand_index, get_hand_info(temp_cards[0]))
                            player_info[const.PLAYER_HAND_INFO_LIST_INDEX][curr_hand_index + 1] = [0, False]
                            
                            player_info[const.PLAYER_BLACKJACK_LIST_INDEX].insert(curr_hand_index, False)
                            player_info[const.PLAYER_BLACKJACK_LIST_INDEX][curr_hand_index + 1] = False
                            
                            player_info[const.PLAYER_SURRENDER_LIST_INDEX].insert(curr_hand_index, False)
                            player_info[const.PLAYER_SURRENDER_LIST_INDEX][curr_hand_index + 1] = False
                            
                            player_info[const.PLAYER_NUM_SPLITS_INDEX] += 1
                            
                            num_hands += 1
                                
                        if strategy == const.STRATEGY_SURRENDER_SPLIT and not const.SURRENDER_ALLOWED:
                            player_info[const.PLAYER_SURRENDER_LIST_INDEX][curr_hand_index] = True
                            
                    case const.STRATEGY_BLACKJACK:
                        player_info[const.PLAYER_BLACKJACK_LIST_INDEX][curr_hand_index] = True
                        
                    case const.STRATEGY_SURRENDER_HIT | const.STRATEGY_SURRENDER_STAND:
                        if const.SURRENDER_ALLOWED:
                            player_info[const.PLAYER_SURRENDER_LIST_INDEX][curr_hand_index] = True

            hand_info = current_play[const.CURRENT_PLAY_HAND_NUM_INDEX]
            continue_hand = current_play[const.CURRENT_PLAY_CONTINUE_HAND_INDEX]

            num_cards_drawn += (0, PLAYS[strategy][const.PLAYS_CARDS_DRAWN_INDEX])[current_play[const.CURRENT_PLAY_SUCCESS_INDEX]]

            if PLAYS[strategy][const.PLAYS_CARDS_DRAWN_INDEX] != 0:
                print("After that move, the player's full hand is now:")
                print(player_info[const.PLAYER_CARDS_LIST_INDEX])

            if hand_info[const.HAND_SUM_INDEX] > const.BUST_NUMBER:
                print("Player ", player_num, " busts on hand ", curr_hand_index,"!", sep='')
                break

            if not continue_hand:
                break

        curr_hand_index += 1

    return num_cards_drawn

def get_payout_ratio(player_info, player_hand_info_list, hand_num, dealer_hand_info, dealer_blackjack):
    curr_payout_ratio = 0
    
    if player_info[const.PLAYER_BLACKJACK_LIST_INDEX][hand_num] == True:
        if dealer_blackjack:
            curr_payout_ratio = const.STANDOFF_PAYOUT_RATIO
        else:
            curr_payout_ratio = const.BLACKJACK_PAYOUT_RATIO
        
    elif player_info[const.PLAYER_SURRENDER_LIST_INDEX][hand_num] == True:
        curr_payout_ratio = const.SURRENDER_PAYOUT_RATIO
        
    elif dealer_hand_info[const.HAND_SUM_INDEX] > const.BUST_NUMBER and player_hand_info_list[hand_num][const.HAND_SUM_INDEX] <= const.BUST_NUMBER:
        curr_payout_ratio = const.REGULAR_PAYOUT_RATIO
        
    elif player_hand_info_list[hand_num][const.HAND_SUM_INDEX] == dealer_hand_info[const.HAND_SUM_INDEX]:
        curr_payout_ratio = const.STANDOFF_PAYOUT_RATIO
        
    elif player_hand_info_list[hand_num][const.HAND_SUM_INDEX] > dealer_hand_info[const.HAND_SUM_INDEX]:
        curr_payout_ratio = const.REGULAR_PAYOUT_RATIO
        
    return curr_payout_ratio
        
                
def calc_winners(current_felt, active_players_list):
    player_info_list = current_felt[const.PLAYER_INFO_INDEX]
    player_hand_info_list = [player_info[const.PLAYER_HAND_INFO_LIST_INDEX] for player_info in player_info_list]
    
    dealer_hand_info = get_hand_info(current_felt[const.DEALER_CARDS_INDEX])
    dealer_blackjack = current_felt[const.DEALER_CARDS_INDEX] in const.BLACKJACKS
    
    total_won_chips_list = [0] * const.NUM_PLAYERS
    total_lost_chips_list = [0] * const.NUM_PLAYERS
    
    for player_num in range(const.NUM_PLAYERS):
        curr_player_info = player_info_list[player_num]
        curr_hand_info_list = player_hand_info_list[player_num]
        
        if not active_players_list[player_num]:
            continue
        
        for hand_num in range(len(curr_hand_info_list)):
            payout_ratio = get_payout_ratio(curr_player_info, curr_hand_info_list, hand_num, dealer_hand_info, dealer_blackjack)
            
            payout = int(curr_player_info[const.PLAYER_BET_LIST_INDEX][hand_num] * payout_ratio) 
            
            if payout_ratio > 0:
               curr_player_info[const.PLAYER_CURRENT_CHIPS_INDEX] += payout
               total_won_chips_list[player_num] += payout
            
            total_lost_chips_list[player_num] += max(0, curr_player_info[const.PLAYER_BET_LIST_INDEX][hand_num] - payout)
    
    return (total_won_chips_list, total_lost_chips_list)

def print_hand_results(win_and_lost_list: list[list[int]], active_players_list):
    print("\nHand over! Here are the results:")
    
    total_chip_change_list = [0] * const.NUM_PLAYERS 
    
    for wins_or_losses in range(len(win_and_lost_list)):
        if wins_or_losses == const.WIN_LOSS_LIST_WINS_INDEX:
            print("\nHere's the winnings:")
        else:
            print("\nHere's the losses:")
            
        current_numbers_list = win_and_lost_list[wins_or_losses]
        
        for player_num in range(const.NUM_PLAYERS):
            if not active_players_list[player_num]:
                print("\tPlayer", player_num, "did not play")
                continue
            
            current_number = current_numbers_list[player_num]
            
            total_chip_change_list[player_num] += (1, -1)[wins_or_losses] * current_number
            
            print("\tPlayer", player_num, ("won", "lost")[wins_or_losses], current_number, "chips")
    
    print("\nHere's the total chip change:")
        
    for player_num in range(const.NUM_PLAYERS):
        current_chip_change = total_chip_change_list[player_num]
        print("\tPlayer", player_num, "has", ("won", "lost")[current_chip_change < 0], abs(current_chip_change), "chips")
    
    return total_chip_change_list

def run_game(deck, stop_point):
    drawn_cards = 0

    player_info_list: list[list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]]] = \
        [[0, [['']], [[0, False]], const.STARTING_CHIPS, 0, [False], [False]] for i in range(const.NUM_PLAYERS)]

    number_of_hands = 0
    active_players_list = [True for i in range(const.NUM_PLAYERS)]
    while True:
        while(drawn_cards < stop_point):
            print("\n-------------------------")
            print("Starting new hand. Dealing cards to players and dealer. Player making bet.")
            print("-------------------------")

            current_felt = initialize_felt(deck, player_info_list)
            drawn_cards += const.NUM_CARDS_PER_PLAYER * (const.NUM_PLAYERS + 1)
            
            for player_num in range(const.NUM_PLAYERS):
                if player_info_list[player_num][const.PLAYER_CURRENT_CHIPS_INDEX] - const.MIN_BET <= const.PLAYER_MIN_CHIPS:
                    print("Player", player_num, "cannot afford to continue! Skipping turn.")
                    active_players_list[player_num] = False
                    continue
                
                make_bet(current_felt[const.PLAYER_INFO_INDEX][player_num], player_num, 0)
                
                drawn_cards += play_hand_player(deck, current_felt[const.PLAYER_INFO_INDEX][player_num], current_felt[const.DEALER_CARDS_INDEX][0], player_num)
            
            if True not in active_players_list:
                break
            
            drawn_cards += play_hand_dealer(deck, current_felt[const.DEALER_CARDS_INDEX])
            
            win_loss_list = calc_winners(current_felt, active_players_list)
            
            total_chip_change_list = print_hand_results(list(win_loss_list), active_players_list)
            
            number_of_hands += 1
            
            if const.NUM_HANDS != const.RUN_UNTIL_DONE and not (number_of_hands < const.NUM_HANDS):
                break
        
        if const.NUM_HANDS != const.RUN_UNTIL_DONE and not (number_of_hands < const.NUM_HANDS):
            print("\n Reached stop point for number of hands after", const.NUM_HANDS,"hands. Ending game.")
            break
        
        player_chips_list = [player[const.PLAYER_CURRENT_CHIPS_INDEX] - const.MIN_BET > const.PLAYER_MIN_CHIPS for player in player_info_list]
        
        if True not in player_chips_list:
            print("\nAll players have hit their minimum! Ending game after", number_of_hands,"hands.")
            break
        
        print("Reached stop point of deck, shuffling deck")
        
        (deck, stop_point) = generate_deck(const.NUM_DECKS)
        drawn_cards = 0
        
if __name__ == "__main__":
    STRATEGY_LIST = load_strategy(const.STRATEGY_FILENAME)
    (deck, stop_point) = generate_deck(const.NUM_DECKS)
    result = run_game(deck, stop_point)