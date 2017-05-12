import ast, argparse, statistics, textwrap, csv, json, os
from PIL import Image, ImageDraw, ImageFont
from voteConverter import convert
from booksonaGen import make_book
from textTools import wrap_text


#fonts, change if needed
font = ImageFont.truetype('./resources/arial.ttf',20)
bigfont =  ImageFont.truetype('./resources/arial.ttf',30)
smallfont = ImageFont.truetype('./resources/arial.ttf',13)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-e", "--perc_elim", nargs='?', const=5, default=5)
	parser.add_argument("-t", "--num_gold", nargs='?', const=5, default=5)
	args = parser.parse_args()
	path = args.input
	
	votes = convert(path)
	prompt = open('./{}/prompt.txt'.format(path),'r').read().split('\n')[0]
	scores = []
	twowers=set()
	
	with open('./{}/responses.csv'.format(path),'r') as csvfile:#read responses
		reader = csv.reader(csvfile)
		for row in reader:
			#scoredata format [twower, response, votes/mean, count, boost, final, stdev]
			twowers.add(row[0])
			try:
				scores.append([row[0],row[1],[],0,int(row[2]),0,0,0])
			except:
				scores.append([row[0],row[1],[],0,0,0,0,0])
	
	twowers = list(twowers)
	twower_count = len(twowers)
	
	top_number = int(args.num_gold) #chart coloring ranges
	elim_number=0
	
	if int(args.perc_elim) < 0:
		elim_number = -int(args.perc_elim)
	else:
		elim_number = round(int(args.perc_elim)*len(twowers)/100)
	
	return (path, prompt, scores, votes, twowers, twower_count, top_number, elim_number)
		
	
def draw_header(prompt, base, drawer,scores):
	prompt = wrap_text(prompt,1000,bigfont,drawer)
	header_height = drawer.textsize(prompt,bigfont)[1]+35
	base = Image.new('RGBA',(1368,header_height+int(67/2*len(scores))),color=(255,255,255,255))
	drawer = ImageDraw.Draw(base)
	base.paste(Image.open('./resources/header.png'),(0,header_height-40))
	drawer.text((15,0),prompt,font=bigfont, fill=(0,0,0,255))
	
	return (prompt, base, drawer, header_height)
	

def process_votes(votes, scores, path):	

	for user_vote in votes:#maps votes to responses
		count = 1/len(user_vote)
		
		for vote in user_vote:
			percentage = 100.0
			for resp_num in vote[:-1]:
				scores[resp_num][2].append(percentage*count)
				scores[resp_num][3] += count
				percentage -= 100/9
				if percentage < 0:
					percentage = 0
				
				
			try:			
				
				unvtd = len(vote[-1])-1
				percentage_left = 50*unvtd/9
			
				for unvoted in vote[-1]:
					scores[unvoted][2].append(-percentage_left)#negative as a flag so it doesn't count as a vote
					scores[unvoted][3] += count
								
			except Exception:
				pass
			

	for scoredata in scores:
		scoredata = calc_stats(scoredata)
		
		
	mergeSort(scores)#sorts from best to worst. Mergesort for best worst case	
	return scores
	
def write_csv(scores, path):
	with open('./{}/results.csv'.format(path), 'w') as result_file:
	
		writer = csv.writer(result_file,lineterminator='\n')
		writer.writerow(['Twower','Response','Subtotal','Boost','Total','Standard Deviation','Votes'])
		writer.writerow([])
		for scoredata in scores:
			writer.writerow(scoredata[0:3]+scoredata[4:8])
	
def calc_stats(scoredata):#calculate stats, dm if you want more
	
	scoredata[7]=len([vote for vote in scoredata[2] if vote >=0])
	#print(scoredata[2])
	votes = list(abs(vote) for vote in scoredata[2])
	try:
		scoredata[2] = sum(votes)/scoredata[3]
		'''
		if scoredata[0].startswith('hanss314'):
			scoredata[2]=1000
		'''
	except:
		print('\"{}\" by {} was not voted for'.format(scoredata[1],scoredata[0]))
		scoredata[2] =0
		
	scoredata[5] = scoredata[2]	+ scoredata[4]
		
	try:
		scoredata[6] = statistics.stdev(votes)
	except:
		scoredata[6] = 0
		
	votegraph = [0 for i in range(10)]
	for vote in votes:
		vote_dev = 0
		if vote % (100/9) > 0.01:
			vote_dev = 0.5
			
		ind = 9-int(9*(vote+0.000001)/100)
		votegraph[ind]+= 1-vote_dev
		try:
			votegraph[ind+1]+= vote_dev
		except:
			pass
			
	scoredata.append(votegraph)	
	return scoredata
		
def draw_rankings(scores, top_number, elim_number,twower_count,base,drawer,header_height,twowers):#this one is a bit of a mess
	backgroundCol=0
	addBackground=0
	ranking=1
	twower_responses_count = {}
	
	for i in range(len(scores)):	
		twower, response, subt, boost, standev, vote_count = scores[i][0], scores[i][1], scores[i][2], scores[i][4], scores[i][6], scores[i][7]
		
		if ranking == (top_number+1):#change background depending on ranking
			backgroundCol = 1
			addBackground = 0
		elif ranking == (twower_count-elim_number+1) and twower in twowers:
			backgroundCol = 2
			addBackground = 0
			
		if (addBackground % 2) ==0:#only needs extra stuff added every two twowers
			if backgroundCol==0:
				base.paste(Image.open('./resources/top.png'),(0,int(67/2*i)+header_height))
			elif backgroundCol==1:
				base.paste(Image.open('./resources/normal.png'),(0,int(67/2*i)+header_height))
			elif backgroundCol==2:
				base.paste(Image.open('./resources/eliminated.png'),(0,int(67/2*i)+header_height))
		
		if not os.path.isfile('./booksonas/'+twower+'.png'):
			make_book(twower,'./booksonas/')
		
		try:#attempt to add booksona
			booksona = Image.open('./booksonas/'+twower+'.png')
			booksona.thumbnail((32,32),Image.BICUBIC)
			base.paste(booksona,(333,int(67/2*i)+header_height),booksona)
		except:
			pass
			
			
		
		if twower in twowers:#handles multiple submissions
			twowers.remove(twower)
			twower_responses_count[twower]=1
			if ranking % 10 == 1:
				rankingString = str(ranking)+'st'
			elif ranking % 10 == 2:
				rankingString = str(ranking)+'nd'
			elif ranking % 10 == 3:
				rankingString = str(ranking)+'rd'
			else:
				rankingString = str(ranking)+'th'
				
			drawer.text((15,int(67/2*i+7)+header_height),rankingString,font=font,fill=(0,0,0,255))
			ranking += 1
			
		else:
			twower_responses_count[twower]+=1
			scores[i][0] += '[{}]'.format(twower_responses_count[twower]) 
			twower = scores[i][0]
				
			
			
		if drawer.textsize(twower,font)[0] > 255: #draws twower name
			drawer.text((60,int(67/2*i+7)+header_height),
				twower,font=smallfont,fill=(0,0,0,255))
				
		else:
			drawer.text((60,int(67/2*i+7)+header_height),
				twower,font=font,fill=(0,0,0,255))
				
		if drawer.textsize(response,font)[0] > 600: #draws responses
			response = wrap_text(response,600,smallfont,drawer)
			
			if response.count('\n') == 0:
				drawer.text((378,int(67/2*i+8)+header_height),
					response,font=smallfont,fill=(0,0,0,255))
			else:
				drawer.text((378,int(67/2*i)+header_height),
					response,font=smallfont,fill=(0,0,0,255))
		else:
			drawer.text((378,int(67/2*i+7)+header_height),
				response,font=font,fill=(0,0,0,255))
		
		draw_stats(drawer,twower,subt,standev,boost,vote_count,header_height,i)
		
				
		addBackground += 1
		
	return scores
	
def draw_stats(drawer,twower,subt,standev,boost,vote_count,header_height,rank):
	if boost == 0:
		drawer.text((998,int(67/2*rank+7)+header_height),
			"%.2f" % round(subt,2)+'%',font=font,fill=(0,0,0,255))
		
	else:
		mean_str = "%.2f" % round(subt,2)
		mean_str += '(+{})'.format(boost)
		mean_str += '%'		
		
		drawer.text((998,int(67/2*rank+7)+header_height),
			mean_str,font=font,fill=(0,0,0,255))
		
	drawer.text((1164,int(67/2*rank+7)+header_height),
		"%.2f" % round(standev,2)+'%',font=font,fill=(0,0,0,255))
		
	drawer.text((1309-drawer.textsize(str(vote_count),font)[0]/2,
		int(67/2*rank+7)+header_height),str(vote_count),
		font=font,fill=(0,0,0,255))
		
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][5] > righthalf[j][5]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
	
def main():
	path, prompt, scores, votes, twowers, twower_count, top_number, elim_number = parse_args()
	
	
	base = Image.new('RGBA',(1368,1368),color=(255,255,255))
	drawer = ImageDraw.Draw(base)

	prompt, base, drawer, header_height = draw_header(prompt, base, drawer,scores)
	scores = process_votes(votes, scores, path)
	scores = draw_rankings(scores,top_number,elim_number,twower_count,base,drawer,header_height,twowers)
	write_csv(scores,path)
	
	base.save('./{}/results.png'.format(path))


if __name__=='__main__':
	main()
