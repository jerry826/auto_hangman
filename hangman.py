# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: hangman.py
@time: 2016/11/9 23:03
"""




class hangman():
	def __init__(self, word,display=True):
		'''
		hangman class
		:param word: word for guess
		'''
		self.word = word
		self.length = len(word)
		self.output = ['_']*self.length
		self.error_char = []
		self.state = 1
		self.display = display

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
			if self.display:
				print(' '.join(self.output) + ' missed: ' + ' '.join(self.error_char))
			return ''.join(self.output), self.state
		else:
			if self.display:
				print('Game has already over!')
			return ''.join(self.output), self.state

	def over_check(self):
		'''
		Check whether the game is over
		:return: True if the game is over; False if the game is not over
		'''
		if len(self.error_char) == 6:
			if self.display:
				print('Game over. You lose.')
			self.state = 3
		elif ''.join(self.output) == self.word:
			if self.display:
				print('Game over. You win!')
			self.state = 2


if __name__ == '__main__':
	game = hangman('hangman', display=True)
	game.guess('e')
	game.guess('a')
	game.guess('n')
	game.guess('m')
	game.guess('d')
	game.guess('k')
	game.guess('g')
	game.guess('h')