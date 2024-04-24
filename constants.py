import types

const = types.SimpleNamespace()

const.POSSIBLE_CARDS = {'A': 11, 
                  '2': 2, 
                  '3': 3, 
                  '4': 4, 
                  '5': 5, 
                  '6': 6, 
                  '7': 7, 
                  '8': 8, 
                  '9': 9, 
                  '10': 10, 
                  'J': 10, 
                  'Q': 10, 
                  'K': 10}

const.BLACKJACKS = [['A', 'K'],
			  ['A', 'Q'],
			  ['A', 'J'],
			  ['A', '10']]

const.NUM_SUITS = 4
const.NUM_CARDS_IN_DECK = len(const.POSSIBLE_CARDS) * const.NUM_SUITS

const.RESERVE_DECKS = 2

const.NUM_DECKS = 8
const.NUM_PLAYERS = 1
const.NUM_HANDS = 30

const.RUN_UNTIL_DONE = -1

const.STARTING_CHIPS = 1000
const.MIN_BET = 10
const.PLAYER_MIN_CHIPS = 100

const.NUM_CARDS_PER_PLAYER = 2

const.DEALER_CARDS_INDEX = 0
const.PLAYER_INFO_INDEX = 1

const.PLAYER_NUM_SPLITS_INDEX = 0
const.PLAYER_CARDS_LIST_INDEX = 1
const.PLAYER_HAND_INFO_LIST_INDEX = 2
const.PLAYER_CURRENT_CHIPS_INDEX = 3
const.PLAYER_BET_LIST_INDEX = 4
const.PLAYER_BLACKJACK_LIST_INDEX = 5
const.PLAYER_SURRENDER_LIST_INDEX = 6

const.HAND_SUM_INDEX = 0
const.HAND_SOFT_INDEX = 1

const.PLAYS_FUNC_INDEX = 0
const.PLAYS_CARDS_DRAWN_INDEX = 1

const.BUST_NUMBER = 21
const.DOUBLE_ALLOWED = True
const.DOUBLE_AFTER_SPLIT_ALLOWED = True
const.SURRENDER_ALLOWED = True

const.STRATEGY_FILENAME = 'strategy.csv'
const.STRATEGY_DEALER_CARD_INDEX = 0
const.STRATEGY_HARD_START_INDEX = 1
const.STRATEGY_HARD_SEARCH_SIZE = 17
const.STRATEGY_SOFT_START_INDEX = 18
const.STRATEGY_SOFT_SEARCH_SIZE = 8
const.STRATEGY_SPLITS_START_INDEX = 26
const.STRATEGY_SPLIT_SEARCH_SIZE = 10

const.STRATEGY_BLACKJACK = 0
const.STRATEGY_HIT = 1
const.STRATEGY_STAND = 2
const.STRATEGY_DOUBLE_HIT = 3
const.STRATEGY_DOUBLE_STAND = 4
const.STRATEGY_SPLIT = 5
const.STRATEGY_SPLIT_DOUBLE_HIT = 6
const.STRATEGY_SURRENDER_HIT = 7
const.STRATEGY_SURRENDER_STAND = 8
const.STRATEGY_SURRENDER_SPLIT = 9

const.PLAYS_FUNCTION_INDEX = 0
const.PLAYS_CARDS_DRAWN_INDEX = 1
const.PLAYS_FUNCTION_NAME_INDEX = 2

const.SPLIT_DOUBLE_BET_NUM = 3
const.DOUBLE_BET_NUM = 1
const.SPLIT_BET_NUM = 1

const.CURRENT_PLAY_HAND_NUM_INDEX = 0
const.CURRENT_PLAY_CONTINUE_HAND_INDEX = 1
const.CURRENT_PLAY_SPLIT_CARDS_INDEX = 2
const.CURRENT_PLAY_SUCCESS_INDEX = 3

const.BLACKJACK_PAYOUT_RATIO = 2.5
const.REGULAR_PAYOUT_RATIO = 2.0
const.STANDOFF_PAYOUT_RATIO = 1.0
const.SURRENDER_PAYOUT_RATIO = 0.5

const.WIN_LOSS_LIST_WINS_INDEX = 0
const.WIN_LOSS_LIST_LOSSES_INDEX = 1