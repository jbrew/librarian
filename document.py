from __future__ import division
import os
import re
import math
import operator
from collections import Counter

class Document(object):
	def __init__(self, name, text, max_ngram_size):
		self.name = name
		self.text = text
		self.max_ngram_size = max_ngram_size
		self.NGRAM_COUNTS = self.ngram_counts(text)
		self.TOTALS = self.totals(self.NGRAM_COUNTS)
	
	def term_count(self, term):
		num_words = len(term.split())
		if term in self.NGRAM_COUNTS[num_words-1]:
			return self.NGRAM_COUNTS[num_words-1][term]
		else:
			return 0

	def ngram_counts(self, text):
		counters = []
		for ngram_size in range(1, self.max_ngram_size+1):
			regex_string = self.regex_string(ngram_size)
			full_expression = "(?=(%s))(?<!\w)" % regex_string
			counters.append(Counter(re.findall(full_expression, text.lower().replace(".","").replace("\n"," ").replace("'",""))))
		return counters	

	# for each dictionary of ngrams, returns the total number of ngrams of that size in this document
	def totals(self, ngram_counts):
		totals = []
		for c in ngram_counts:
			total = sum([val for val in c.values()])
			totals.append(total)
		return totals

	# returns the dictionary of ngrams of the specified size, mapped to counts
	def get_ngrams(self, n):
		return self.NGRAM_COUNTS[n-1]

	# returns the appropriate regex string for searching for ngrams of a certain size
	def regex_string(self, ngram_size):
		word = "'?\w[\w']*(?:-\w+)*'?"
		space = "\s"
		str = word + (space+word) *(ngram_size-1)
		return str

	# compute term frequency
	def tf(self, term):
		num_words = len(term.split())
		return self.NGRAM_COUNTS[num_words-1][term] / self.TOTALS[num_words-1]



def best_test():
	text = 'it was the best of times it was the worst of times'
	d = Document('example', text, 4)

#best_test()