import json, sys

def convert(path):

	keywords = json.load(open('./{}/dict.json'.format(path),'r'))
		
	vote_strings = open('./{}/votes.txt'.format(path)).readlines()
	votes = []
	final_votes = []

	for vote in vote_strings:
		current = vote.strip('[')
		current = current.strip('\n')
		current = current.strip(']')
		current = current.split(' ')
		votes.append(current)
		
	for vote in votes:
		indexes = []
		mapping = []
		try:
			mapping = keywords[vote[0]]
		except:
			continue
		order = []
		
		for c in vote[1].upper():
			indexes.append(ord(c)-65)

		for index in indexes:
			order.append(mapping[index])
			
		final_votes.append(order)
		
	open('./{}/votes.json'.format(path),'w').write(json.dumps(final_votes))

if __name__ == '__main__':
	convert(sys.argv[1])