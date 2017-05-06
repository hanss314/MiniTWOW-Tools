import json, sys

path = sys.argv[1]

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
	mapping = keywords[vote[0]]
	order = []
	
	for c in vote[1].upper():
		print(c)
		indexes.append(ord(c)-65)

	print(indexes)
	for index in indexes:
		order.append(mapping[index])
		
	final_votes.append(order)
	
open('./{}/votes.json'.format(path),'w').write(json.dumps(final_votes))