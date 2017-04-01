import ast, argparse, random

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--votes", nargs='?', const=10, default=10)
	args = parser.parse_args()
	keys = list(ast.literal_eval(open('./dict.txt','r').read()).keys())
	writer = open('votes.txt','w')
	options = ['a','b','c','d','e','f','g','h','i','j']	
	
	for i in range(int(args.votes)):
		random.shuffle(options)
		voteString = '['+random.choice(keys)+' '
		for c in options:
			voteString += c
		writer.write(voteString+']\n')
	
	
	
	
	
if __name__ == '__main__':
	main()