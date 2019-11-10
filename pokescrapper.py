##########################################################################################

__author__ = "Roger Truchero Visa"
__copyright__ = ""
__credits__ = ["Roger Truchero Visa"]
__license__ = "GPL"
__version__ = ""
__maintainer__ = "Roger Truchero Visa"
__email__ = "rtruchero@lleida.net"
__status__ = "development"

##########################################################################################

from urllib.request import Request, urlopen
import bs4 # Beatiful soup
import re # Regexp
import random # Shuffling

##########################################################################################

# Structure: <font color="red">This is some text!</font>
html_colors = {
	'Grass' : '7AC74C', 
	'Poison' : 'A33EA1', 
	'Fire' : 'EE8130', 
	'Flying' : 'A98FF3', 
	'Water' : '6390F0', 
	'Bug' : 'A6B91A', 
	'Normal' : 'A8A77A', 
	'Electric' : 'F7D02C', 
	'Ground' : 'E2BF65', 
	'Fairy' : 'D685AD', 
	'Fighting' : 'C22E28', 
	'Psychic' : 'F95587', 
	'Rock' : 'B6A136', 
	'Steel' : 'B7B7CE', 
	'Ice' : '96D9D6', 
	'Ghost' : '735797', 
	'Dragon' : '6F35FC', 
	'Dark' : '705746'
}

# Function to get data from "https://pokemondb.net/pokedex/national"
def get_data(url = "https://pokemondb.net/pokedex/national"):

	#url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
	req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req).read()

	return html 

# Function to parse data
def parse_data(data):
	soup = bs4.BeautifulSoup(data, "lxml")

	generations = soup.find_all("div", "infocard-list infocard-list-pkmn-lg")

	pokedex = []

	count = 1
	for generation in generations:
		#print("Generation {0}".format(count))		
		pokemons = generation.find_all("div", "infocard");

		for pokemon in pokemons:

			poke_name = pokemon.find_all("a", "ent-name")			
			poke_id = pokemon.find_all("small")
			poke_types = pokemon.select('a[class*="itype "]')
			poke_img = re.search('(.+?)data-src=\"(.+?)\"(.+?)', str(pokemon))

			if poke_img: poke_img = poke_img.group(2)

			types = []
			for poke_type in poke_types:
				types.append(poke_type.text)

			pokedex.append([poke_id[0].text, poke_name[0].text, types, poke_img])

		count += 1

	return pokedex

# Function to choose the 6 pokemon team
def choose_random_team(pokedex):
	team = []
	random.shuffle(pokedex) # Randomize the selected team

	for pokemon in pokedex:
		if len(pokemon[2]) == 2 and is_repeated_type(team, pokemon[2]) == False:
			team.append(pokemon)
			if(len(team) == 6): break
	
	return team

# Check if the pokemon type is yet in the team
def is_repeated_type(team, types):
	for pokemon in team:
		if (types[0] in pokemon[2]) and (types[1] in pokemon[2]): return True
	return False

# Function to generate the html template with the poke team
def generate_html(team):
	file = open("template.html", "r");	
	write_file = open("poketeam.html", "w+")

	template = file.read()

	for i in range(0, 6):
		template = template.replace("%%image" + str(i+1) + "%%", team[i][3])
		template = template.replace("%%pokeid" + str(i+1) + "%%", team[i][0])
		template = template.replace("%%pokemon" + str(i+1) + "%%", team[i][1])		
		types = "<font color=\""+ html_colors[team[i][2][0]] + "\">" + team[i][2][0] + "</font>  ·  " + "<font color=\""+ html_colors[team[i][2][1]] + "\">" + team[i][2][1] + "</font>"		  
		template = template.replace("%%types" + str(i+1) + "%%", types)

	write_file.write(template)

	file.close()
	write_file.close()

# Main function
def main():
	data = get_data()
	pokedex = parse_data(data)	
	team = choose_random_team(pokedex)
	generate_html(team)

# Main call
if __name__ == "__main__":
	main()