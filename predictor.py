import random, sys, csv, statistics, re

def strip_drp(name):
	return re.sub('\[.*?\]', '', name)

def collect_data(latest):
	data = []
	means = {}
	stdvs = {}
	to_collect = []
	start_collecting = False

	for twow in open('history.txt','r').read().split('\n'):
		if twow == latest:
			start_collecting = True
		if start_collecting:
			to_collect.append('./twows/'+twow)

	latest_twow = to_collect[0]

	with open('./{}/results.csv'.format(latest_twow),'r') as csvfile:#read responses
		reader = csv.reader(csvfile)
		next(reader, None)
		next(reader, None)
		for row in reader:
			name = strip_drp(row[0])
			try:
				means[name].append(float(row[2]))
				stdvs[name].append(float(row[5]))
			except:
				means[name] = [float(row[2])]
				stdvs[name] = [float(row[5])]

	for twow in to_collect[1:]:
		with open('./{}/results.csv'.format(twow),'r') as csvfile:#read responses
			reader = csv.reader(csvfile)
			next(reader, None)
			next(reader, None)
			for row in reader:
				name = strip_drp(row[0])
				try:
					means[name].append(float(row[2]))
					stdvs[name].append(float(row[5]))
				except:
					pass

	for twower in means.keys():
		mean = statistics.mean(means[twower])
		stdv = statistics.mean(stdvs[twower])
		data.append([twower,mean,stdv])

	return data

def calculate_results(data,death_rate):
	count = len(data)
	results = [[0,0,0] for i in range(count)]

	live = [count]
	while not live[-1] == 1:
		to_append = 0
		if death_rate > 0:
			to_append = max(1,int(live[-1]*(100-death_rate)/100))
		elif death_rate < 0:
			to_append = max(1,int(live[-1]+death_rate))

		live.append(to_append)
	#each array value corresponds to the amount of survivors after each round

	for length in range(100):
		dead = [False for i in range(count)]
		top = 0
		for round in range(len(live)):
			scores = [0.0 for i in range(count)]
			for sim in range(count):
				if dead[sim]:
					scores[sim] = 0
				else:
					scores[sim] = random.gauss(data[sim][1],data[sim][2])


			for i in range(count):
				rank = 1
				for j in range(count):
					if scores[i] < scores[j]:
						rank += 1

				if rank>live[round]:
					dead[i] = True


			#the values for round are simply the values for which 10, 3, and 1 people would stay alive
			
			if(live[round]<=10 and top == 0):
				top = 1
				for ten in range(count)	:
					if not dead[ten]:
						results[ten][0]+=1

			elif(live[round]<=3 and top == 1):
				top = 2
				
				for three in range(count):
					if not dead[three]:
						results[three][1]+=1

			elif(live[round]==1):
				for win in range(count):
					if not dead[win]:
						results[win][2]+=1


	for prin in range(count):
		print('{}\t{}\t{}\t{}'.format(data[prin][0], results[prin][0], results[prin][1], results[prin][2]))

if __name__ == '__main__':
	death_rate = 0
	try:
		death_rate = sys.argv[2]
	except:
		death_rate = -1

	if death_rate == 0:
		print('death rate can\'t be 0!')
	elif death_rate >100:
		print('death rate can\'t be greater than 100!')
	else:
		data = collect_data(sys.argv[1])
		calculate_results(data,death_rate)