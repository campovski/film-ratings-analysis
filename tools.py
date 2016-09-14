import re
import requests
import os

jaz = "ur33974390"

def prenesi_user(user, force_overwrite=False):
	if not os.path.isfile("ratings.html") or force_overwrite:
		try:
			print("Saving {}".format(user))
			website = requests.get("http://www.imdb.com/user/"+user+"/ratings?start=1&view=compact&sort=ratings_date:desc&defaults=1&my_ratings=restrict&scb=0.14288297295570374")
			print("Website downloaded!")
			with open("ratings.html", 'w') as dat:
				dat.write(website.text)
				print('Saved!')
		except requests.exceptions.ConnectionError:
			print("Error 404")		
	else: print("Already saved!")
	naredi_csv(user, force_overwrite)
	
def naredi_csv(user, force_overwrite=False):
	if not os.path.isfile("{}.csv".format(user)) or force_overwrite:
		html_file = open("ratings.html")
		text = html_file.read()
		poizvedba = re.compile("""<td class="title"><a href="/title/tt(?P<id>.*?)/">(?P<naslov>.*?)</a></td>.*?
<td class="year">(?P<leto>\d+)</td>.*?
<td class="title_type">.*?</td>.*?
<td class="your_ratings">.*?
    <a>(?P<ocena>\d+?)</a>.*?
</td>""", re.MULTILINE)
		html_file.close()

		print("Creating CSV...")
		csv_file = open("{}.csv".format(user),'w')
		csv_file.write("imdb_id|title|year|grade")
		for match in poizvedba.finditer(text):
			csv_file.write("{0}|{1}|{2}|{3}\n".format(match.group("id"), match.group("naslov"), match.group("leto"), match.group("ocena")))
		csv_file.close()
		print("CSV created!")
	else: print("CSV already created!")
	
def uredi_csv(user):
	csv_file = "{}.csv".format(user)
	text_arr = []
	with open(csv_file, 'r') as dat:
		for line in dat:
			text_arr.append(line)
	
	print("Sorting CSV...")
	merge_sort(text_arr)

	with open(csv_file, 'w') as dat:
		for line in text_arr:
			dat.write(line)
		print("CSV saved!")
		
def csv_reader(user):
	csv_dict = {}
	csv = []
	with open("{}.csv".format(user)) as dat:
		for line in dat:
			film_id, naslov, leto, ocena = line.split('|')
			csv_dict[film_id] = [naslov, leto, ocena.strip()]
			csv.append([film_id, naslov, leto, ocena.strip()])
	print("CSV file has been read!")
	return csv, csv_dict
	
def get_filmpages(filmi, force_overwrite=False):
	regex_genre = re.compile('<span class="itemprop" itemprop="genre">(?P<genre>.+?)</span>')
	regex_actor = re.compile('<meta name="description" content=.*?With (?P<actor>.+?)[.]')
	regex_director = re.compile('<meta name="description" content="Directed by (?P<director>.+?)[.]')
	
	print("Creating film_arr...")
	#film_arr = [film_id, [genres], [directors], [actors]]
	film_arr = []
	current_film_index = 0
	if not os.path.isdir("filmi"):
		os.mkdir("filmi")
	for film in filmi:
		if not os.path.isfile("filmi/{}.html".format(film[0])) or force_overwrite:
			get_filmpage(film[0])
			
		html_file = open("filmi/{}.html".format(film[0]))
		text = html_file.read()
		html_file.close()
		
		film_arr.append([film[0]])
		tmp = []
		for match in regex_genre.finditer(text):
			tmp.append(match.group('genre'))
		film_arr[current_film_index].append(tmp)
		
		if regex_director.search(text) == None:
			film_arr[current_film_index].append([])
		else:
			for match in regex_director.finditer(text):
				film_arr[current_film_index].append(match.group('director').split(", "))
		if regex_actor.search(text) == None:
			film_arr[current_film_index].append([])
		else:
			for match in regex_actor.finditer(text):
				film_arr[current_film_index].append(match.group('actor').split(", "))
		
		current_film_index += 1
	print("film_arr created!")
	#print(film_arr)
	return film_arr
	
def get_filmpage(film_id):
	try:
		print("Saving {}.html...".format(film_id))
		website = requests.get("http://www.imdb.com/title/tt{}/".format(film_id))
		with open("filmi/{}.html".format(film_id), 'w') as dat:
			dat.write(website.text)
		print("Saved!")
	except:
		print("Failed!")
		
def write_actors_directors(film_dict):
	actors = open("actors.csv", 'w')
	directors = open("directors.csv", 'w')
	genres = open("genres.csv", 'w')
	
	actors.write("imdb_id|actor\n")
	directors.write("imdb_id|director\n")
	genres.write("imdb_id|genre\n")
	
	i = 0;
	for f_id in film_dict.keys():
		try:
			film_actors = film_dict[f_id][5]
			film_director = film_dict[f_id][4]
			film_genre = film_dict[f_id][3]
			
			for actor in film_actors:
				actors.write("{0}|{1}\n".format(f_id, actor))
				
			for director in film_director:
				directors.write("{0}|{1}\n".format(f_id, director))
			
			for genre in film_genre:
				genres.write("{0}|{1}\n".format(f_id, genre))
			
			i += 1
		except: 
			print("F*** this s***!!")
			
	actors.close()
	directors.close()
	genres.close()
	return i
		
				
def merge_sort(alist):
	if len(alist)>1:
		mid = len(alist)//2
		lefthalf = alist[:mid]
		righthalf = alist[mid:]

		merge_sort(lefthalf)
		merge_sort(righthalf)
		
		i=0
		j=0
		k=0
		while i < len(lefthalf) and j < len(righthalf):
			if lefthalf[i] < righthalf[j]:
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
