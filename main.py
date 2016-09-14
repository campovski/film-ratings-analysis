import tools
import sys

jaz = "ur33974390"

print("Redownload data?")
decision = input()
if int(decision):
	tools.prenesi_user(jaz, True)
	tools.uredi_csv(jaz)
	csv, film_dict = tools.csv_reader(jaz)
	film_arr = tools.get_filmpages(csv, True)
else:
	csv, film_dict = tools.csv_reader(jaz)
	film_arr = tools.get_filmpages(csv)
	
for film in film_arr:
	film_id = film[0]
	try:
		film_dict[film_id].append(film[1])
		film_dict[film_id].append(film[2])
		film_dict[film_id].append(film[3])
	except IndexError:
		print("Index error occured while {0}: {1}, quitting...".format(film[0], film_dict[film_id][0]))
		sys.exit()
	except:
		print("Unknown error occured while {0}: {1}, quitting...".format(film[0], film_dict[film_id][0]))
		sys.exit()
		
i = tools.write_actors_directors(film_dict)
print("Succesfully parsed actors, directors and genre: {0}/{1}".format(i, len(film_dict)))
