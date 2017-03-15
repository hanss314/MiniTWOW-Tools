from PIL import Image, ImageDraw, ImageFont
import random, argparse
import re


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-i", "--iterations", nargs='?', const=10, default=10)
	args = parser.parse_args()
	its=int(args.iterations)
	
	submissions = open(args.input,'r').read().split('\n')
	keys = random.sample(
		open('./resources/words.txt','r').read().split('\n'),
		its)
	arial = ImageFont.truetype('arial.ttf',30)
	
	for iteration in range(its):

		base = Image.open('./resources/base.png').convert('RGB')
		drawer = ImageDraw.Draw(base)
		submissionOrder = random.sample(submissions,10)
		
		for i in range(10):
			phrase = submissionOrder[i]
			drawer.text((100,71*i+45), phrase, font=arial, fill=(0,0,0))
			distance = 130+drawer.textsize(phrase,arial)[0]
			indivWords = re.sub('/[^a-zA-Z0-9 ]/','',phrase).split(' ')
			wordCount = 0
			for string in indivWords:
				if re.search('[a-zA-Z0-9]',string):
					wordCount +=1
			
			if wordCount >10:
				drawer.text((distance,71*i+45), str(wordCount), font=arial, fill=(255,0,0))
			else:
				drawer.text((distance,71*i+45), str(wordCount), font=arial, fill=(30,30,255))
			
			
		word = keys[iteration].upper()
		w = drawer.textsize(word,arial)[0]
		drawer.text((1360-int(w/2), 30), word, font=arial, fill="black")
		
		base.save('./screens/'+str(iteration)+'.png')
	
	
	
if __name__ == '__main__':
	main()