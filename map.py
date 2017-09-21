import gmplot
import googlemaps
import csv
import pickle

# Requires Google API key
gmaps = googlemaps.Client('GOOGLE API KEY')

# load_address()
# Pulls location addresses from a csv file into a list and geocodes each address
# Saves the list of geocoded addresses as a pickle file
# Returns a list of geocoded addresses
def load_address():
	# Open csv file
	with open('address.csv') as file:
		data = csv.reader(file)
		addresses = []
		geocodes = []
		next(data, None)  # skip the headers
		# Add each address into the list of addresses
		for row in data:
			addresses.append(str(row[0]))

	# Geocode each address using the Google Maps Geocoding API
	for address in addresses:
		result = gmaps.geocode(address)
		geocodes.append(result)

	pickle.dump(geocodes, open("locations.pickle", "wb"))
	return(geocodes)

# map_geocodes()
# Opens geocode file and plots locations onto a Google Maps page
def map_geocodes():
	lats = []
	lngs = []
	geocodes = pickle.load(open("locations.pickle", "rb"))

	# Extract longitude and latitude from each Geocode location
	for code in geocodes:
		if code: #not an empty geocode
			print(code[0]['geometry']['location']['lat'], code[0]['geometry']['location']['lng'])
			lats.append(code[0]['geometry']['location']['lat'])
			lngs.append(code[0]['geometry']['location']['lng'])

	# Using the gmplot library plot all longitude and latitude points
	mapper = gmplot.GoogleMapPlotter.from_geocode("Toronto")
	mapper.scatter(lats,lngs, '#3B0B39', size=40, marker=False)
	mapper.draw("locations.html")

def main():
	load_address()
	map_geocodes()

if __name__ == '__main__':
	main()
