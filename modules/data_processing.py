from typing import List, Set, Dict, Tuple, Optional
import json


def load_json(file_path: str = 'data/oc_data.json') -> Dict:
    """This loads in the OC data from a json file and returns it as a dictionary.
    You can navigate the dictionary using oc_data[ID]
    
    :param file_path: Where to load in the OC JSON file.
    :return: A dictionary with all of the OC data in a usable format.
    """
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