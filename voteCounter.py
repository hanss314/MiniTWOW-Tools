import ast, argparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument('key')
	args = parser.parse_args()
	
	keys = ast.literal_eval(open(args.key,'r').read())

	print(str(keys))


if __name__=='__main__':
	main()
