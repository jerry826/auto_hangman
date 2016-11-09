# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: model2.py
@time: 2016/11/9 23:07
"""

import time
import collections
import re
import pandas as pd
from hangman import hangman

def match(words_set,word_show,correct):
    '''
    Make a match based on the information avaiable i.e. find the word in the form of _ _ a _ _ n in the word set
    :param words_set: the old word set
    :param word_show: the pattern we have known from the game
    :param correct:   the character we can see in the pattern
    :return:
    '''
    word_set1 = '  '.join(words_set)
    pattern = word_show.replace('_', '[^' + correct + ' ]')
    re_pattern = re.compile(pattern)
    word_set2 = re_pattern.findall(word_set1)
    return word_set2





def get_dict_freq(data, k=7):
    '''
    Calculate the k characters with the highest frequency
    :param data: dict data
    :param k: number of characters we want
    :return: word frequency result
    '''
    data.columns = ['word']
    data['length'] = list(map(lambda x: len(x), data['word']))
    word_groups = data.groupby('length')
    # frequency dict
    freq_set = {}
    #
    word_set = {}
    # calculate the character frequency
    for id, word_group in word_groups:
        data0 = ([x for x in ''.join(list(word_group['word']))])
        c = collections.Counter(data0)
        common = (c.most_common(k))
        chars = [x[0] for x in common]
        freq_set[id] = ''.join(chars)
        word_set[id] = list(word_group['word'])

    return freq_set, word_set


def play_hangman2(game,n,freq_set,word_set,k):
    '''
    Auto hangman player
    :param game: hangman game class
    :param n:    the word length
    :param freq_set: the character frequency data
    :param word_set: the word set
    :param k:  guessing parameter
    :return:  the guess result
    '''
    guessed = ''
    correct = ''
    word_show = '_' * n
    state = 1
    #####################################################
    # Step1: fast guessing for the first k characters   #
    #####################################################
    i = 0
    while state == 1 and i < k:
        ch = freq_set[n][i]
        # make a guess
        (word_show1, state) = game.guess(ch)
        # update the result and make record
        if word_show != word_show1:
            # we are right
            correct += ch
            word_show = word_show1
        guessed += ch
        i += 1
    #####################################################
    #      Step2: Guess with Pattern recognition        #
    #####################################################
    # check whether the game has stopped
    if state == 1:
        # build a new word set based on our new information
        word_set2 = match(word_set[n], word_show, correct)
        # print(word_set2)
        chs = [x for x in ''.join(word_set2)]
        # find the most frequent character in the new word set
        common2 = collections.Counter(chs).most_common(20)
        # start guess
        guess_count = 0
        while state == 1:
            # find a character has not been used with the highest frequency
            j = 0
            w = common2[j]
            while w[0] in guessed:
                j += 1
                w = common2[j]
            # make a guess
            (word_show1, state) = game.guess(w[0])
            # update the result and make record
            guessed += w[0]
            if word_show != word_show1:
                # we are right
                correct += w[0]
                word_show = word_show1
                # make a pattern recognition again
                word_set2 = match(word_set2, word_show, correct)
                chs = [x for x in ''.join(word_set2)]
                common2 = (collections.Counter(chs)).most_common(20)
            guess_count += 1

    return guessed, state, correct


def test2(k=4,path='C:\\Users\\Jerry\\Desktop\\words_50000.txt',display=False):
	print('Start testing: ')
	# preparing work
	data = pd.read_table(path, header=None)
	freq_set, word_set = get_dict_freq(data,k=k)
	# test client
	guess_recorder = []   # record every guess in our game
	result_recorder = []  # record the game result  2: win 3:lose
	correct_recorder = [] # record the correct guess in every game


	for word in list(data['word']):
		if display:
			print('-------------------------')
		game = hangman(word,display)

		[guessed, state, correct ] = play_hangman2(game,len(word),freq_set,word_set,k)

		guess_recorder += [guessed]
		result_recorder += [state]
		correct_recorder += [correct]
	print('-----------------------------------------------------------')
	print('Correct Guesses: %0.3f' % (sum([3 - x for x in  result_recorder])/50000.0))
	return list(data['word']), guess_recorder,result_recorder,correct_recorder



if __name__ == '__main__':
	t0 = time.time()
	raw_result = test2(k=4, path='C:\\Users\\Jerry\\Desktop\\words_50000.txt', display=False)  # turn off screen display
	t1 = time.time()
	print('Time spent: %0.1f s' % (t1 - t0))
	# Save the result
	result = pd.DataFrame([x for x in raw_result], index=['word', 'guess', 'result', 'correct']).T
	result['wrong_guess'] = list(map(lambda x, y: len(x) - len(y), result['guess'], result['correct']))
	print(result.head())