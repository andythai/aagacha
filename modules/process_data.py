import json

# This loads in the OC data from a json file and returns it as a dictionary.
# Navigate the dictionary using oc_data[ID]
def load_json(file_path='data/oc_data.json'):
	# Load in data from the .json file
	with open(file_path) as json_file:
		oc_data = json.load(json_file)
	oc_data = oc_data['ocs']  # Pull down one level
	
	# Populate the lore strings
	for i in range(len(oc_data)):
		try:
			with open(oc_data[i]['lorePath']) as f: 
				oc_data[i]['lore'] += f.read()
		except:  # Skip populating if invalid path.
			pass
	return oc_data