from PIL import Image, ImageDraw, ImageFont
import random, argparse, re, os, textwrap


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-i", "--iterations", nargs='?', const=10, default=10)
	args = parser.parse_args()
	its=int(args.iterations)
	
	keylist = open('./resources/words.txt','r').read().split('\n')
	keyorder = random.sample(range(len(keylist)),its)
	
	submissions = open('./'+args.input+'/responses.txt','r').read().split('\n')
	submissionCount = len(submissions)
	voteList = []
	voteNumber = 0
	screenDict = {}
	
	for randomListNumber in range(int(10*its/len(submissions))+1):
		randomSubmissionOrder = list(range(submissionCount))
		random.shuffle(randomSubmissionOrder)
		voteList.append(randomSubmissionOrder)
		
	print(str(voteList))
	
	arial = ImageFont.truetype('./resources/arial.ttf',30)
	os.makedirs('./'+args.input+'/voteScreens', exist_ok=True)
	
	for iteration in range(its):

		base = Image.open('./resources/base.png').convert('RGB')
		drawer = ImageDraw.Draw(base)
		existingEntries = []
		
		for i in range(10):
			
			submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount]
			
			while submissionNumber in existingEntries:
				voteList[int(voteNumber/submissionCount)].remove(submissionNumber)
				voteList[int(voteNumber/submissionCount)].append(submissionNumber)
				submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount]
				
			lines = textwrap.wrap(submissions[submissionNumber],width=85)
			phrase = ''
			for line in lines:
				phrase += (line+'\n')
			
			
			drawer.text((100,71*i+78-drawer.textsize(phrase,arial)[1]/2), phrase, font=arial, fill=(0,0,0))
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
			
			existingEntries.append(submissionNumber)
			voteNumber+=1
			
		word = keylist[keyorder[iteration]].upper()
		w = drawer.textsize(word,arial)[0]
		drawer.text((1360-int(w/2), 30), word, font=arial, fill="black")
		screenDict[word]=list(existingEntries)
		
		base.save('./'+args.input+'/voteScreens/'+str(iteration)+'.png')
	open('./'+args.input+'/dict.txt','w').write(str(screenDict))
	
	
if __name__ == '__main__':
	main()
