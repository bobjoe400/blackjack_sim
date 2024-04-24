import csv
from bj_util import *
from bj_plays import get_hand_info, PLAYS

def load_strategy(filename: str) -> list[list[str]]:
	datafile = open(filename, 'r')
	return list(csv.reader(datafile))

def get_suggest_play(player_cards: list[str], 
					 num_splits: int, 
					 dealer_card: str, 
					 strategy_matrix: list[list[str]]) -> int:
	player_hand_number = get_hand_info(player_cards)

	if player_cards in const.BLACKJACKS and num_splits == 0:
		return const.STRATEGY_BLACKJACK

	if player_hand_number[const.HAND_SUM_INDEX] == 21:
		return const.STRATEGY_STAND

	soft = player_hand_number[const.HAND_SOFT_INDEX]
	split = False

	if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
		split = True
		player_hand_number = (const.POSSIBLE_CARDS[player_cards[0]], player_hand_number[const.HAND_SOFT_INDEX])

	dealer_card_index = strategy_matrix[const.STRATEGY_DEALER_CARD_INDEX].index(str(const.POSSIBLE_CARDS[dealer_card]))

	search_start_index = const.STRATEGY_HARD_START_INDEX
	search_size = const.STRATEGY_HARD_SEARCH_SIZE

	if soft:
		search_start_index = const.STRATEGY_SOFT_START_INDEX
		search_size = const.STRATEGY_SOFT_SEARCH_SIZE

	if split:
		search_start_index = const.STRATEGY_SPLITS_START_INDEX
		search_size = const.STRATEGY_SPLIT_SEARCH_SIZE
	
	rows_to_search = ['0']*search_size
	
	for i in range(search_start_index, search_start_index + search_size):
		rows_to_search[i - search_start_index] = strategy_matrix[i][0]

	strategy_row_index = rows_to_search.index(str(player_hand_number[const.HAND_SUM_INDEX])) + search_start_index 
	
	selected_row = strategy_matrix[strategy_row_index]
 
	return int(selected_row[dealer_card_index])


