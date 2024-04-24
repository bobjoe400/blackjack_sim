from constants import *
from typing import Callable, Union

def deal_card(deck, curr_hand):
    curr_hand.append(deck.pop(0))

def make_bet(player_info, player_num, curr_hand_index):
    print("Player ", player_num, " bets ", const.MIN_BET, " on hand ", curr_hand_index, "!", end=' ', sep='')
    player_info[const.PLAYER_CURRENT_CHIPS_INDEX] -= const.MIN_BET
    player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index] += const.MIN_BET
    print("Player", player_num, "now has", player_info[const.PLAYER_CURRENT_CHIPS_INDEX],"chips left.", end = ' ')
    print("Their current bet amount is ", player_info[const.PLAYER_BET_LIST_INDEX][curr_hand_index]," chips on hand ", curr_hand_index, ".", sep = '')

def player_can_double(player_info, player_num, split: bool = False):
    if player_info[const.PLAYER_CURRENT_CHIPS_INDEX] - (const.DOUBLE_BET_NUM, const.SPLIT_DOUBLE_BET_NUM)[split] * const.MIN_BET < const.PLAYER_MIN_CHIPS:
        if split:
            print("Player", player_num, "cannot afford to split then double.")
            return False
        print("Player", player_num, "cannot afford to double.")
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
        print("Dealer ", end='')

    else:
        print("Player " + str(player_num) + " ", end='')

    print(action)

def blackjack(player_cards: list, 
              deck: list, 
              player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'blackjack!')

    return (get_hand_info(player_cards), False, [], True)

def hit(player_cards: list, 
        deck: list, 
        player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
        player_num: int = -1,
        curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'hits!')

    deal_card(deck, player_cards)

    return (get_hand_info(player_cards), True, [], True)

def stand(player_cards: list, 
          deck: list, 
          player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
          player_num: int = -1,
          curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, 'stands!')

    return (get_hand_info(player_cards), False, [], True)

def double(player_cards: list, 
           deck: list, 
           player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
           player_num: int = -1,
           curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if not player_can_double(player_info, player_num):
        print("Player", player_num, "cannot afford to double.")
        return (get_hand_info(player_cards), True, [], False)

    print_player_action(player_num, 'doubles! Only one card dealt.')

    deal_card(deck, player_cards)

    make_bet(player_info, player_num, curr_hand_index)

    return (get_hand_info(player_cards), False, [], False)

def double_hit(player_cards: list, 
               deck: list, 
               player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
               player_num: int = -1,
               curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_ALLOWED:
        current_play = double(player_cards, deck, player_info, player_num, curr_hand_index)
        if current_play[const.CURRENT_PLAY_SUCCESS_INDEX]:
            return current_play
    
    print("Doubling not allowed.")

    return hit(player_cards, deck, player_info, player_num)

def double_stand(player_cards: list, 
                 deck: list, 
                 player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
                 player_num: int = -1,
                 curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_ALLOWED:
        current_play = double(player_cards, deck, player_info, player_num, curr_hand_index)
        if current_play[const.CURRENT_PLAY_SUCCESS_INDEX]:
            return current_play
    
    print("Doubling not allowed.")

    return stand(player_cards, deck, player_info, player_num)

def split(player_cards: list, 
          deck: list, 
          player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
          player_num: int = -1,
          curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if player_info[const.PLAYER_CURRENT_CHIPS_INDEX] - const.SPLIT_BET_NUM * const.MIN_BET < 0:
        print("Player", player_num, "cannot afford to split")
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
              player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.DOUBLE_AFTER_SPLIT_ALLOWED:
        if not player_can_double(player_info, player_num, True):
            print("Player", player_num, "cannot afford to split then double.")
            return (get_hand_info(player_cards), True, [], False)

        split_cards = split(player_cards, deck, player_info, player_num, curr_hand_index)
        
        double(split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX][0], deck, player_info, player_num, curr_hand_index)
        double(split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX][1], deck, player_info, player_num, curr_hand_index)
        
        return (split_cards[const.CURRENT_PLAY_HAND_NUM_INDEX], False, split_cards[const.CURRENT_PLAY_SPLIT_CARDS_INDEX], split_cards[const.CURRENT_PLAY_SUCCESS_INDEX])
    
    return hit(player_cards, deck, player_info, player_num)

def surrender(player_cards: list, 
              deck: list, 
              player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
              player_num: int = -1,
              curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    print_player_action(player_num, "surrenders!")

    return (get_hand_info(player_cards), False, [], True)

def surrender_hit(player_cards: list, 
                  deck: list, 
                  player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
                  player_num: int = -1,
                  curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print("Surrender not allowed.")

    return hit(player_cards, deck, player_info, player_num, curr_hand_index)

def surrender_stand(player_cards: list, 
                    deck: list, 
                    player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
                    player_num: int = -1,
                    curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print("Surrender not allowed.")

    return stand(player_cards, deck, player_info, player_num)

def surrender_split(player_cards: list, 
                    deck: list, 
                    player_info: list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
                    player_num: int = -1,
                    curr_hand_index: int = -1) -> tuple[list[Union[int, bool]], bool, list[list[str]], bool]:
    if const.SURRENDER_ALLOWED:
        return surrender(player_cards, deck, player_info, player_num)
    
    print("Surrender not allowed.")

    return split(player_cards, deck, player_info, player_num, curr_hand_index)

PLAYS: list[tuple[Callable[[list[str], 
                            list[str], 
                            list[Union[int, list[list[str]] , list[list[Union[int, bool]]], int, int, list[bool], list[bool]]], 
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