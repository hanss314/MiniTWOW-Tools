import json, sys, csv

def convert(path):

	keywords = json.load(open('./{}/dict.json'.format(path),'r'))
	vote_strings={}
	votes = []
	final_votes = []
		
	with open('./{}/votes.csv'.format(path),'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			try:
				vote_strings[row[0]].append(row[1])
			except:
				vote_strings[row[0]] = [row[1]]
			
				
	

	for user_vote_str in vote_strings.values():
		user_vote = []
		
		for vote in user_vote_str:
			current = vote.strip('[')
			current = current.strip('\n')
			current = current.strip(']')
			current = current.split(' ')
			user_vote.append(current)
			
		votes.append(user_vote)
		
		
	for user_vote in votes:
		final_vote = []
		for vote in user_vote:
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
				
			final_vote.append(order)
		final_votes.append(final_vote)
	
	return final_votes
	#open('./{}/votes.json'.format(path),'w').write(json.dumps(final_votes))

if __name__ == '__main__':
	votes = convert(sys.argv[1])
	print(votes)
	open('./{}/votes.json'.format(path),'w').write(json.dumps(votes))