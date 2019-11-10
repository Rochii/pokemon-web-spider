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
		print("Generation {0}".format(count))		
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


# Main function
def main():
	data = get_data()
	pokedex = parse_data(data)	
	team = choose_random_team(pokedex)
	generate_html(team)
	print(team)


# Main call
if __name__ == "__main__":
	main()