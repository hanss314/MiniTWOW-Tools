import random, argparse, os, textwrap, json, csv
from PIL import Image, ImageDraw, ImageFont
from textTools import wrap_text

#font change if needed
font = ImageFont.truetype('./resources/arial.ttf',30)

def parse_args(keylist):
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument("-i", "--iterations", nargs='?', const=10, default=10)
    args = parser.parse_args()
    path = args.input
    its=int(args.iterations)
    
    submissions = []
    with open('./twows/{}/responses.csv'.format(path),'r') as csvfile:#read responses
        reader = csv.reader(csvfile,delimiter=',', quotechar='"')
        for row in reader:
            submissions.append(row[1])
            
    keyorder = random.sample(range(len(keylist)),its)
    submissionCount = len(submissions)
    
    return (path,its,submissions,keyorder,submissionCount)
    
def create_random_order(submissions,its,submissionCount):
    voteList = []
    for randomListNumber in range(int(10*its/len(submissions))+1):
    
        randomSubmissionOrder = list(range(submissionCount))
        random.shuffle(randomSubmissionOrder)
        voteList.append(randomSubmissionOrder)
        
    return voteList

        
'''def wrap_text(text,width):
    lines = textwrap.wrap(text,width)
    new_text='\n'.join(lines)
    return new_text'''
    
def count_words(text):
    
    return text.strip().count(' ')+1
            

def draw_screens(keylist,path,its,keyorder,voteList,submissionCount,submissions):
    screenDict = {}
    voteNumber = 0
    text_writer = open('./twows/{}/ballots.txt'.format(path),'w')
    for iteration in range(its):

        base = Image.open('./resources/base.png').convert('RGB')
        drawer = ImageDraw.Draw(base)
        existingEntries = []
        
        word = keylist[keyorder[iteration]].upper()
        w = drawer.textsize(word,font)[0]
        drawer.text((1360-int(w/2), 30), word, font=font, fill="black")
        
        text_writer.write(word+'\n\n')
        
        for i in range(10):
            
            #ensures all submissions are displayed
            submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount] 
            while submissionNumber in existingEntries:
                voteList[int(voteNumber/submissionCount)].remove(submissionNumber)
                voteList[int(voteNumber/submissionCount)].append(submissionNumber)
                submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount]
                
            response = wrap_text(submissions[submissionNumber],1100,font,drawer)
            drawer.text((100,70.875*i+60-drawer.textsize(response,font)[1]/2), response, font=font, fill=(0,0,0))
            distance = 130+drawer.textsize(response,font)[0]
            
            wordCount = count_words(response)
                    
            if wordCount >10:
                drawer.text((distance,int(71.5*i)+42), str(wordCount), font=font, fill=(255,0,0))#blue
            else:
                drawer.text((distance,int(71.5*i)+42), str(wordCount), font=font, fill=(30,30,255))#red
            
            existingEntries.append(submissionNumber)
            ballot_line = ':regional_indicator_{}: {} ({})\n'.format(chr(i+97),submissions[submissionNumber],wordCount)
            text_writer.write(ballot_line)
            
            voteNumber+=1
            
        screenDict[word]=list(existingEntries)
        base.save('./twows/{}/voteScreens/{}.png'.format(path,iteration))
        text_writer.write('\n\n\n\n\n')
        
    open('./twows/{}/dict.json'.format(path),'w').write(json.dumps(screenDict))
    
    
def main():
    keylist = open('./resources/words.txt','r').read().split('\n')
    path,its,submissions,keyorder,submissionCount = parse_args(keylist)
    voteList = create_random_order(submissions,its,submissionCount)

    os.makedirs('./twows/{}/voteScreens'.format(path), exist_ok=True)

    draw_screens(keylist,path,its,keyorder,voteList,submissionCount,submissions)
    
    
if __name__ == '__main__':
    main()
