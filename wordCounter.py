import sys, csv, re
from collections import OrderedDict

encoding = "ISO-8859-15" 

def main():
    path = sys.argv[1]
    responses = []
    words = []
    counts = {}
    with open('./twows/{}/responses.csv'.format(path),'r',encoding=encoding) as csvfile:#read responses
        reader = csv.reader(csvfile)
        for row in reader:
            responses.append(row[1])

    for response in responses:
        for word in response.split(' '):
            words.append(simplify(word))
            
    for word in words:
        try:
            counts[word] +=1
        except:
            counts[word] = 1
            
    counts = OrderedDict(sorted(counts.items()))
    
    with open('./twows/{}/wordcount.csv'.format(path), 'w',encoding=encoding) as result_file:
    
        writer = csv.writer(result_file,lineterminator='\n')
        writer.writerow(['Word','Count'])
        writer.writerow([])
        for word, count in counts.items():
            print([word,count])
            writer.writerow([word,count])
            
def simplify(text):
    text = text.strip()
    text = re.sub('[^a-zA-Z0-9\']','',text)
    return text.lower()

main()