# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: hangman.py
@time: 2016/11/8 11:35
"""

import pandas as pd
import collections
import re


def match(words_set,word_show,correct):

	word_set1 = '  '.join(words_set)
	pattern = word_show.replace('_', '[^' + correct + ' ]')
	re_pattern = re.compile(pattern)
	word_set2 = re_pattern.findall(word_set1)
	return word_set2

def get_dict_freq(data, k=7):

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

class hangman1():
	def __init__(self, word):
		'''
		hangman class
		:param word: word for guess
		'''
		self.word = word
		self.length = len(word)
		self.output = ['_']*self.length
		self.error_char = []
		self.state = 1

	def guess(self,ch):
		'''
		Take a guess character
		:param ch: guess character
		:return: the result
		'''
		loc = []
		if self.state ==1 :
			# The game can continue
			error = True
			for i in range(self.length):
				if self.word[i] == ch:
					error = False
					self.output[i] = ch
					loc += [i]
			if error:
				self.error_char += [ch]
			# check whether the game has stop
			self.over_check()
			print(' '.join(self.output) + ' missed: ' + ' '.join(self.error_char))

			return ''.join(self.output), self.state
		else:
			print('Game has already over!')
			return ''.join(self.output), self.state


	def over_check(self):
		'''
		Check whether the game is over
		:return: True if the game is over; False if the game is not over
		'''
		if len(self.error_char) == 6:
			print('Game over. You lose.')
			self.state = 3
		elif ''.join(self.output) == self.word:
			print('Game over. You win!')
			self.state = 2




def test():

	# preparing work
	k = 7
	path = 'C:\\Users\\Jerry\\Desktop\\words_50000.txt'
	data = pd.read_table(path, header=None)
	freq_set, word_set = get_dict_freq(data,k=k)

	# test client
	correct_num = 0       # record the game we won
	guess_recorder = []   # record every guess in our game
	result_recorder = []  # record the game result  2: win 3:lose
	correct_recorder = [] # record the correct guess in every game

	for word in list(data['word']):
		print('-------------------------')
		print(word)
		test = hangman1(word)
		n = len(word)
		guessed = ''
		correct = ''
		word_show = '_' * n
		state = 1
		# Step1: fast guessing for the first k characters
		i = 0
		while state == 1 and i<k:
			ch = freq_set[n][i]
			# make a guess
			(word_show1, state) = test.guess(ch)
			# update the result and make record
			if word_show != word_show1:
				# we are right
				correct += ch
				word_show = word_show1
			guessed += ch
			i += 1

		if state == 1: # check whether the game has stopped
			# Step2:  Pattern recognition
			word_set2 = match(word_set[n],word_show,correct)
			# Step3: add more guess
			chs = [x for x in ''.join(word_set2)]
			common2 = collections.Counter(chs).most_common(20) # find the most frequent character in the new word set
			guess_count = 0
			while state == 1:
				j = 0
				# find a character has not been used with highest frequency
				w = common2[j]
				while w[0] in guessed:
					j += 1
					w = common2[j]

				# make a guess
				(word_show1, state) = test.guess(w[0])

				# update the result and make record
				guessed += w[0]
				guess_count += 1
				if word_show != word_show1:
					# we are right
					correct += w[0]
					word_show = word_show1
					# make a pattern recognition
					if guess_count%2==0:
						word_set2 = match(word_set2, word_show, correct)
						chs = [x for x in ''.join(word_set2)]
						common2 = collections.Counter(chs).most_common(20)

		if state == 2:
			correct_num += 1

		guess_recorder += [guessed]
		result_recorder += [state]
		correct_recorder += [correct]

	print('Correct Guesses %0.3f' % (correct_num/50000.0))
	return list(data['word']), guess_recorder,result_recorder,correct_recorder

if __name__ == '__main__':
	% time raw_result = test()
	result = pd.DataFrame([x for x in raw_result],index=['word','guess','result','correct']).T
	result['wrong_guess'] = list(map(lambda x,y: len(x)-len(y),result['guess'],result['correct']))

