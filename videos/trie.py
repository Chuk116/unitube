# Python program for insert and search 
# operation in a Trie 

class TrieNode: 
	
	# Trie node class 
	def __init__(self): 
		self.children = [None]*93

		# isEndOfWord is True if node represent the end of the word 
		self.isEndOfWord = False
		
		self.freq = 0

class Trie: 
	
	# Trie data structure class 
	def __init__(self): 
		self.root = self.getNode() 

	def getNode(self): 
	
		# Returns new trie node (initialized to NULLs) 
		return TrieNode() 

	def _charToIndex(self,ch): 
		
		# private helper function 
		# Converts key current character into index 
		# use only 'a' through 'z' and lower case 
		# print(ch + ":" + str(ord(ch)) + "  " + str(ord(ch)-ord('!')))
		return ord(ch)-ord('!') 


	def insert(self,key): 
		# If not present, inserts key into trie 
		# If the key is prefix of trie node, 
		# just marks leaf node 
		pCrawl = self.root 
		length = len(key) 
		for level in range(length): 
			index = self._charToIndex(key[level]) 
			# print(index)
			# if current character is not present 
			if not pCrawl.children[index]: 
				pCrawl.children[index] = self.getNode() 
			pCrawl = pCrawl.children[index] 

		# mark last node as leaf 
		pCrawl.isEndOfWord = True 
		pCrawl.freq += 1

	def search(self, key): 
		
		# Search key in the trie 
		# Returns true if key presents 
		# in trie, else false 
		pCrawl = self.root 
		length = len(key)
		numSimilarWords = 0
		for level in range(length): 
			index = self._charToIndex(key[level]) 
			if not pCrawl.children[index]: 
				return False, numSimilarWords
			pCrawl = pCrawl.children[index]
			
			if pCrawl.isEndOfWord: 
				numSimilarWords += pCrawl.freq * 0.5

		numSimilarWords += 1.0
		if pCrawl != None and pCrawl.isEndOfWord: 
			return True, numSimilarWords * 2
		else: 
			return False, numSimilarWords


# This code is adapted from Atul Kumar (www.facebook.com/atul.kr.007) 

