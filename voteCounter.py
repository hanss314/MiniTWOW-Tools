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
	
	twowers = []
	responses = []
	boosts = {}
	
	with open('./{}/responses.csv'.format(path),'r') as csvfile:#read responses
		reader = csv.reader(csvfile)
		for row in reader:
			twowers.append(row[0])
			responses.append(row[1])
			
			try:
				boosts[row[0]] = int(row[2])
			except:
				pass
			
	scores = [[response,[],0.0]for response in responses]		
	#votes = json.load(open('./{}/votes.json'.format(path),'r'))
	
	indiv_twowers = list(set(twowers))#data about the data (metadata?)
	twower_count = len(indiv_twowers)
	
	top_number = int(args.num_gold) #chart coloring ranges
	elim_number=0
	if int(args.perc_elim) < 0:
		elim_number = -int(args.perc_elim)
	else:
		elim_number = round(int(args.perc_elim)*len(indiv_twowers)/100)
	
	return (path, prompt, twowers, responses, scores, votes, indiv_twowers, twower_count, top_number, elim_number, boosts)
		
	
def draw_header(prompt, base, drawer, responses):
	prompt = wrap_text(prompt,1000,bigfont,drawer)
	header_height = drawer.textsize(prompt,bigfont)[1]+35
	base = Image.new('RGBA',(1368,header_height+int(67/2*len(responses))),color=(255,255,255,255))
	drawer = ImageDraw.Draw(base)
	base.paste(Image.open('./resources/header.png'),(0,header_height-40))
	drawer.text((15,0),prompt,font=bigfont, fill=(0,0,0,255))
	
	return (prompt, base, drawer, header_height)
	
def remove_dups(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def process_votes(votes, scores, twowers, boosts):	

	for user_vote in votes:#maps votes to responses
		count = 1/len(user_vote)
		for vote in user_vote:
			vote = remove_dups(vote)
			try:
				percentage = 100.0
				for resp_num in vote:
						
					scores[resp_num][1].append(percentage*count)
					scores[resp_num][2] += count
					percentage -= 100/9
			except Exception:
				pass
			

	for scoredata in scores:
		scoredata = calc_stats(scoredata,scores.index(scoredata),twowers,boosts)
		
		
	mergeSort(scores)#sorts from best to worst. Mergesort for best worst case
	return scores
	
def calc_stats(scoredata,resp_ind,twowers,boosts):#calculate stats, dm if you want more
	try:
		scoredata[2] = sum(scoredata[1])/scoredata[2]
		'''
		if twowers[resp_ind].startswith('hanss314'):
			scoredata[2]=1000
		'''
	except Exception:
		print('\"{}\" by {} was not voted for'.format(scoredata[0],twowers[resp_ind]))
		scoredata[2] =0
	try:	
		scoredata[2] += boosts[twowers[resp_ind]]
		if scoredata[2]>100:
			scoredata[2]=100
	except:
		pass
		
	try:
		scoredata.append(statistics.stdev(scoredata[1]))
	except Exception:
		scoredata.append(0)
	
	scoredata.append(len(scoredata[1]))#number of votes
	scoredata[1]= twowers[resp_ind]#twower name
	scoredata[0],scoredata[1]=scoredata[1],scoredata[0]#rearranges list in order on chart
	return scoredata
		
def draw_rankings(scores, top_number, elim_number,twower_count,base,drawer,header_height,indiv_twowers,boosts):#this one is a bit of a mess
	backgroundCol=0
	addBackground=0
	ranking=1
	
	for i in range(len(scores)):	
		twower, response, mean, standev, voteCount = scores[i][0], scores[i][1], scores[i][2], scores[i][3], scores[i][4]
		
		if ranking == (top_number+1):#change background depending on ranking
			backgroundCol = 1
			addBackground = 0
		elif ranking == (twower_count-elim_number+1) and twower in indiv_twowers:
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
			
			
		
		if twower in indiv_twowers:#handles multiple submissions
			indiv_twowers.remove(twower)
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
			
		if drawer.textsize(twower,font)[0] > 255: #draws twower name
			drawer.text((320-drawer.textsize(twower,smallfont)[0],int(67/2*i+7)+header_height),
				twower,font=smallfont,fill=(0,0,0,255))
				
		else:
			drawer.text((320-drawer.textsize(twower,font)[0],int(67/2*i+7)+header_height),
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
		
		draw_stats(drawer,twower,mean,standev,boosts,voteCount,header_height,i)
		
				
		addBackground += 1
		
	return base
	
def draw_stats(drawer,twower,mean,standev,boosts,voteCount,header_height,rank):
	try:
		mean_str = str(mean-boosts[twower])[:4]
		mean_str += '(+{})'.format(boosts[twower])
		mean_str += '%'
		
		
		drawer.text((998,int(67/2*rank+7)+header_height),
			mean_str,font=font,fill=(0,0,0,255))
	except:
		drawer.text((998,int(67/2*rank+7)+header_height),
			str(mean)[:5]+'%',font=font,fill=(0,0,0,255))
		
	drawer.text((1164,int(67/2*rank+7)+header_height),
		str(standev)[:5]+'%',font=font,fill=(0,0,0,255))
		
	drawer.text((1309-drawer.textsize(str(voteCount),font)[0]/2,
		int(67/2*rank+7)+header_height),str(voteCount),
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
            if lefthalf[i][2] > righthalf[j][2]:
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
	path, prompt, twowers, responses, scores, votes, indiv_twowers, twower_count, top_number, elim_number, boosts = parse_args()
	
	
	base = Image.new('RGBA',(1368,1368),color=(255,255,255))
	drawer = ImageDraw.Draw(base)

	
	prompt, base, drawer, header_height = draw_header(prompt, base, drawer, responses)
	scores = process_votes(votes, scores, twowers, boosts)
	draw_rankings(scores,top_number,elim_number,twower_count,base,drawer,header_height,indiv_twowers, boosts)
	
	base.save('./'+path+'/results.png')


if __name__=='__main__':
	main()
