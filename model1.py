# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: model1.py
@time: 2016/11/9 23:04
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


def play_hangman1(game,n,word_set):
    '''
    Auto hangman player
    :param game: hangman game class
    :param n:    the word length
    :param word_set: the word set
    :param k:  guessing parameter
    :return:  the guess result
    '''
    guessed = ''
    correct = ''
    word_show = '_' * n
    state = 1

    chs = [x for x in ''.join(word_set)]
    # find the most frequent character in the  word set
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
            word_set = match(word_set, word_show, correct)
            chs = [x for x in ''.join(word_set)]
            common2 = (collections.Counter(chs)).most_common(20)
        guess_count += 1
    return guessed, state, correct

def split_data(data):
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
    word_set = {}
    # calculate the character frequency
    for id, word_group in word_groups:
        word_set[id] = list(word_group['word'])

    return word_set

def test1(path='C:\\Users\\Jerry\\Desktop\\words_50000.txt',display=False):
    print('Start testing: ')
    # preparing work
    data = pd.read_table(path, header=None)
    word_set = split_data(data)
    # test client
    guess_recorder = []   # record every guess in our game
    result_recorder = []  # record the game result  2: win 3:lose
    correct_recorder = [] # record the correct guess in every game

    for word in list(data['word']):
        if display:
            print('-------------------------')
        game = hangman(word,display)

        [guessed, state, correct ] = play_hangman1(game,len(word),word_set[len(word)])

        guess_recorder += [guessed]
        result_recorder += [state]
        correct_recorder += [correct]
    print('-----------------------------------------------------------')
    print('Correct Guesses: %0.3f' % (sum([3 - x for x in  result_recorder])/50000.0))
    return list(data['word']), guess_recorder,result_recorder,correct_recorder



if __name__ == '__main__':
	t0 = time.time()
	raw_result = test1(path='C:\\Users\\Jerry\\Desktop\\words_50000.txt', display=False)  # turn off screen display
	t1 = time.time()
	print('Time spent: %0.1f s' % (t1 - t0))
	# Save the result
	result = pd.DataFrame([x for x in raw_result], index=['word', 'guess', 'result', 'correct']).T
	result['wrong_guess'] = list(map(lambda x, y: len(x) - len(y), result['guess'], result['correct']))
	print(result.head())