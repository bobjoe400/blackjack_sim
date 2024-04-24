from bj_util import *
from typing import Callable, Union

def deal_card(deck: list[str], curr_hand: list[str]):
    curr_hand.append(deck.pop(0))

def make_bet(player_info, player_num, curr_hand_index):
    print_message("Player ", player_num, " bets ", const.MIN_BET, " on hand ", curr_hand_index, "!", end=' ', sep='')
    player_info[const.PLAYER_CURRENT_CHIPS_INDEX] -= const.MIN_BET
    player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index] += const.MIN_BET
    print_message("Player", player_num, "now has", player_info[const.PLAYER_CURRENT_CHIPS_INDEX],"chips left.", end = ' ')
    print_message("Their current bet amount is ", player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index]," chips on hand ", curr_hand_index, ".", sep = '')

def player_can_double(player_info, player_num, split: bool = False):
    if player_info[const.PLAYER_CURRENT_CHIPS_INDEX] - (const.DOUBLE_BET_NUM, const.SPLIT_DOUBLE_BET_NUM)[split] * const.MIN_BET < const.PLAYER_MIN_CHIPS:
        if split:
            print_message("Player", player_num, "cannot afford to split then double.")
            return False
        print_message("Player", player_num, "cannot afford to double.")
        return False
    return True

def get_hand_info(player_cards: list[str]) -> list[Union[int, bool]]:
    sum = 0
    soft = False
    aces_in_hand = 0
    subracted = False

    for card in player_cards:
        if card == 'A':
            aces_in_hand += 1
            soft = True

            if aces_in_hand > 1:
                sum += 1
                continue

        if (sum := sum + const.POSSIBLE_CARDS[card]) > const.BUST_NUMBER and soft and not subracted:
            soft = False
            subracted = True
            sum -= 10

    return [sum, soft]

def print_player_action(player_num, action):
    if(player_num == -1):
        print_message("Dealer ", end='')

    else:
        print_message("Player " + str(player_num) + " ", end='')

    print_message(action)

def execute_current_strategy(strategy: int, 
                             curr_hand: list[str], 
                             deck: list[str], 
                             player_info: PLAYER_INFO_TYPE, 
                             player_num: int, 
                             curr_hand_index: int, 
                             player_cards: list[list[str]], 
                             num_hands: int) -> tuple[tuple[list[int | bool], bool, list[list[str]], bool], int]:
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
    
    return (current_play, num_hands)

def blackjack(player_cards: list, 
              deck: list, 
              player_info: PLAYER_INFO_TYPE, 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'blackjack!')

    return (get_hand_info(player_cards), False, [], True)

def hit(player_cards: list, 
        deck: list, 
        player_info: PLAYER_INFO_TYPE, 
        player_num: int = -1,
        curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'hits!')

    deal_card(deck, player_cards)

    return (get_hand_info(player_cards), True, [], True)

def stand(player_cards: list, 
          deck: list, 
          player_info: PLAYER_INFO_TYPE, 
          player_num: int = -1,
          curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'stands!')

    return (get_hand_info(player_cards), False, [], True)

def double(player_cards: list, 
           deck: list, 
           player_info: PLAYER_INFO_TYPE, 
           player_num: int = -1,
           curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if not player_can_double(player_info, player_num):
        print_message("Player", player_num, "cannot afford to double.")
        return (get_hand_info(player_cards), True, [], False)

    print_player_action(player_num, 'doubles! Only one card dealt.')

    deal_card(deck, player_cards)

    make_bet(player_info, player_num, curr_hand_index)

    return (get_hand_info(player_cards), False, [], False)

def double_hit(player_cards: list, 
               deck: list, 
               player_info: PLAYER_INFO_TYPE, 
               player_num: int = -1,
               curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_ALLOWED:
        current_play = double(player_cards, deck, player_info, player_num, curr_hand_index)
        if current_play[const.CURRENT_PLAY_SUCCESS_INDEX]:
            return current_play
    
    print_message("Doubling not allowed.")

    return hit(player_cards, deck, player_info, player_num)

def double_stand(player_cards: list, 
                 deck: list, 
                 player_info: PLAYER_INFO_TYPE, 
                 player_num: int = -1,
                 curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_ALLOWED:
        current_play = double(player_cards, deck, player_info, player_num, curr_hand_index)
        if current_play[const.CURRENT_PLAY_SUCCESS_INDEX]:
            return current_play
    
    print_message("Doubling not allowed.")

    return stand(player_cards, deck, player_info, player_num)

def split(player_cards: list, 
          deck: list, 
          player_info: PLAYER_INFO_TYPE, 
          player_num: int = -1,
          curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if player_info[const.PLAYER_CURRENT_CHIPS_INDEX] - const.SPLIT_BET_NUM * const.MIN_BET < 0:
        print_message("Player", player_num, "cannot afford to split")
        return (get_hand_info(player_cards), True, [], False)
    
    print_player_action(player_num, "splits!")

    split_1 = [player_cards[0]]
    split_2 = [player_cards[1]]

    deal_card(deck, split_1)
    deal_card(deck, split_2)

    player_info[const.PLAYER_BET_LIST_INDEX].insert(curr_hand_index, player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index])
    player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index + 1] = 0
    
    make_bet(player_info, player_num, curr_hand_index + 1)

    return (get_hand_info(split_1), True, [split_1, split_2], True)

def split_double_hit(player_cards: list, 
              deck: list, 
              player_info: PLAYER_INFO_TYPE, 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_AFTER_SPLIT_ALLOWED:
        if not player_can_double(player_info, player_num, True):
            print_message("Player", player_num, "cannot afford to split then double.")
            return (get_hand_info(player_cards), True, [], False)

        split_cards = split(player_cards, deck, player_info, player_num, curr_hand_index)
        
        double(split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX][0], deck, player_info, player_num, curr_hand_index)
        double(split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX][1], deck, player_info, player_num, curr_hand_index)
        
        return (split_cards[const.CURRENT_PLAY_HAND_NUM_INDEX], False, split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX], split_cards[const.CURRENT_PLAY_SUCCESS_INDEX])
    
    return hit(player_cards, deck, player_info, player_num)

def surrender(player_cards: list, 
              deck: list, 
              player_info: PLAYER_INFO_TYPE, 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, "surrenders!")

    return (get_hand_info(player_cards), False, [], True)

def surrender_hit(player_cards: list, 
                  deck: list, 
                  player_info: PLAYER_INFO_TYPE, 
                  player_num: int = -1,
                  curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print_message("Surrender not allowed.")

    return hit(player_cards, deck, player_info, player_num, curr_hand_index)

def surrender_stand(player_cards: list, 
                    deck: list, 
                    player_info: PLAYER_INFO_TYPE, 
                    player_num: int = -1,
                    curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print_message("Surrender not allowed.")

    return stand(player_cards, deck, player_info, player_num)

def surrender_split(player_cards: list, 
                    deck: list, 
                    player_info: PLAYER_INFO_TYPE, 
                    player_num: int = -1,
                    curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print_message("Surrender not allowed.")

    return split(player_cards, deck, player_info, player_num, curr_hand_index)

PLAYS: list[tuple[Callable[[list[str], 
                            list[str], 
                            PLAYER_INFO_TYPE, 
                            int,
                            int], 
                           tuple[list[Union[int, bool]], 
                                 bool, 
                                 list[list[str]],
                                 bool]], 
                  int, 
                  str]] = \
    [(blackjack, 0, "plays_blackjack"),
    (hit, 1, "plays_hit"), 
    (stand, 0, "plays_stand"), 
    (double_hit, 1, "plays_double_hit"), 
    (double_stand, (0,1)[const.DOUBLE_ALLOWED], "plays_double_stand"), 
    (split, 2,"plays_split"), 
    (split_double_hit, (1,4)[const.DOUBLE_AFTER_SPLIT_ALLOWED],"plays_split_double_hit"), 
    (surrender_hit, (1,0)[const.SURRENDER_ALLOWED],"plays_surrender_hit"), 
    (surrender_stand, 0,"plays_surrender_stand"), 
    (surrender_split, (2,0)[const.SURRENDER_ALLOWED],"plays_surrender_stand")]