
class TreeNode:
	def __init__(self, label, position) :
		self.label = label														## Label on the edge leading to this node	
		self.children = {}														## Dictionary containing the node's branches
		self.position = position 												## Invalid(-1) for non leaf nodes; Suffix Index for leaf nodes  

class SuffixTree:
	def __init__(self, text) :
		textLength = len(text)
		text += "$"
		self.root = TreeNode(None, -1)
		self.root.children[text[0]] = TreeNode(text,0)							## Adding longest suffix edge
		for i in range(1, textLength) :											
			j = i
			current = self.root
			while j < textLength:
				if text[j] in current.children:
					child = current.children[text[j]]
					childLabel = child.label
					k = 1
					labelLength = len(childLabel) 
					while k < labelLength and j+k < textLength and text[j+k] == childLabel[k]:
						k += 1
					if k == labelLength:										## Successfully traversed the edge
						current = child
						j += k
					else:														## Falls off the edge
						oldChild = childLabel[k]
						newChild = text[j+k]
						child.label = childLabel[k:]
						middleChild = TreeNode(childLabel[:k], -1)				## Adding a new inner node	
						middleChild.children[oldChild] = child					## Modifying the existing node's label
						middleChild.children[newChild] = TreeNode(text[j+k:], i)		## Adding new leaf node 
						current.children[childLabel[0]] = middleChild
						j = textLength
				else:
					current.children[text[j]] = TreeNode(text[j:], i)			## Adding a new leaf node
					j = textLength
					
					
	def exactMatchOnly(self, substring, text, title):							## Walk down till query string match is found
		textLength = len(text)
		current = self.root
		subLength = len(substring)
		i = 0
		matchedLength = 0														
		while i < subLength:													
			if substring[i] in current.children:
				child = current.children[substring[i]]
				childLabel = child.label
				labelLength = len(childLabel)
				j = 1
				while j < labelLength and i+j < subLength and substring[i+j] == childLabel[j]:
					j += 1
				matchedLength += j	
				if matchedLength == subLength:								## Match Found
					matchedQueryPositions = self.dfsForLeaves(current.children[substring[i]])
					for k in matchedQueryPositions:
						print(title)
						print("Exact Match Found at: ",k)
						count = 10										## To print surrounding text
						startIndex = k
						while startIndex > 0 and count:
							if(text[startIndex-1] == ' '):
								count -= 1
							startIndex -= 1
						count = 10
						endIndex = k+subLength
						while endIndex < textLength and count:
							if(text[endIndex] == ' '):
								count -= 1
							endIndex += 1
						print(text[startIndex:endIndex])
						print()									 
					return  
				else:
					i += j
					if j == labelLength:								## Edge label matched and exhausted
						current = current.children[childLabel[0]]
			else:
				return None		
	
	
	def firstMatchOccurence(self, substring, text, title):	
		textLength = len(text)
		subLength = len(substring)	
		for m in range(0, subLength):										##	Removing one character from the left in each iteration
			i = m
			current = self.root
			matchedLength = 0
			while i < subLength:						
				if substring[i] in current.children:
					child = current.children[substring[i]]
					childLabel = child.label
					labelLength = len(childLabel)
					j = 1
					while j < labelLength and i+j < subLength and substring[i+j] == childLabel[j]:
						j += 1
					matchedLength += j	
					if matchedLength == subLength-m:						## Match Found
						matchedQueryPositions = self.dfsForLeaves(current.children[substring[i]])
						k = min(matchedQueryPositions)
						return  (k, title, text, matchedLength)
					else:
						i += j												## Updating number of characters matched
					if j == labelLength:									## Exhausted the edge label
						current = current.children[childLabel[0]]
				else:														## to exit the while loop
					i = subLength		
		return (None,title, text, 0)
					
	def firstOccurenceOnly(self, substring, text, title):					## To print the first occurence
		(k, title, text, matchedLength) = self.firstMatchOccurence(substring, text, title)
		subLength = len(substring)
		textLength = len(text)
		if k is not None: 
			print(title)
			print("First Exact/Partial Match Found at: ",k)
			count = 10
			startIndex = k
			while startIndex > 0 and count:
				if(text[startIndex-1] == ' '):
					count -= 1
				startIndex -= 1
			count = 10
			endIndex = k+subLength
			while endIndex < textLength and count:
				if(text[endIndex] == ' '):
					count -= 1
				endIndex += 1
			print(text[startIndex:endIndex])
			print()
					
	def documentRanking(self, substring, text,title, i, rankScore, rankWiseTitles):					
			words = substring.split()											## Considering each word individually 
			numberOfWords = len(words)
			rankScore[i] = 0													
			for j in range(numberOfWords):		
				wordLength = len(words[j])
				found, title, text, matchedLength = self.firstMatchOccurence(words[j],text, title)		## Finding first match
				if found is not None:																
					rankScore[i] += (matchedLength/wordLength)*100								## Updating RankScore of the document			
			currentvalue = rankScore[i]															## Insertion sort 
			position = i
			while position > 0 and rankScore[position-1] < currentvalue:
				rankScore[position] = rankScore[position-1]
				rankWiseTitles[position] = rankWiseTitles[position-1]
				position = position-1
			rankScore[position] = currentvalue
			rankWiseTitles[position] = title 
										  
	
	def dfsForLeaves(self, current) :									## Finding leaf nodes of a subtree
		stack = []
		matchedSuffixIndex = []
		stack.append(current)
		while stack:
			node = stack.pop()														
			if node.position != -1:										## Leaf node detected 
				matchedSuffixIndex.append(node.position)
			for i in node.children.keys():						
				stack.append(node.children[i])
		return matchedSuffixIndex					
	
	
	
						
def main():
	query = input("What is your query? ")
	f = open("/data/AesopTales.txt", "r")
	titles = list()
	texts = list()
	texts = [[] for i in range(312)]
	titles = [[] for i in range(312)]
	roots = list()
	roots = [[] for i in range(312)]
	rankScore = list()
	rankScore = [[0] for i in range(312)]
	rankWiseTitles = list()
	rankWiseTitles = [[] for i in range(312)]	
	for i in range(312):
		title = ""
		currentText = ""
		title += f.readline()
		f.readline()
		count = 2
		while count:
			newline = f.readline()
			if newline.strip():
				currentText += newline
				count = 2
			else:
				count -= 1
		titles[i] = title
		texts[i] = currentText	
		roots[i] = SuffixTree(currentText)						
		roots[i].exactMatchOnly(query, currentText, title)
		roots[i].firstOccurenceOnly(query,currentText, title)
		roots[i].documentRanking(query,currentText,title, i, rankScore, rankWiseTitles)
	print('Ordering documents based on Rank: ')
	[print(i+1, rankWiseTitles[i]) for i in range(311)]
	f.close()	
	
if __name__ == "__main__":
	main()	
