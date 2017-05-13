import ast, argparse, random, json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--votes", nargs='?', const=10, default=10)
	args = parser.parse_args()
	keys = list(json.load(open('./dict.json','r')).keys())
	writer = open('votes.csv','w')
	options = ['a','b','c','d','e','f','g','h','i','j']	
	voters = range(int(int(args.votes)*9/10))
	
	for i in range(int(args.votes)):
	
		random.shuffle(options)
		to_show = random.choice(range(1,11))
		voter = random.choice(voters)
		key = random.choice(keys)
		vote = ''.join(options[:to_show])
		vote_str = '{},[{} {}],\n'.format(voter,key,vote)
		writer.write(vote_str)
	
	
	
	
	
if __name__ == '__main__':
	main()