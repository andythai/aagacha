import json

# This loads in the OC data from a json file and returns it as a dictionary.
# Navigate the dictionary using oc_data[ID]
def load_json(file_path='data/oc_data.json'):
    # Load in data from the .json file
    with open(file_path) as json_file:
        oc_data = json.load(json_file)    
    return oc_data['ocs']

# This function creates a set of strings for the discord bot to send as a message to display OC stats.
# oc_entry is the dictionary from the ID of an OC.
# Example: oc_entry = oc_data[0]
def create_text(oc_entry):    
    # Append star rating to string form
    num_stars = int(oc_entry['baseStars'])
    stars_string = ''
    for i in range(5):
        if i < num_stars:
            stars_string += ':star2:'
        else:
            stars_string += ':eight_pointed_black_star:'
    
    # Load then write lore / description to quote
    lore_text = '> '
    with open(oc_entry['lorePath']) as f:
        lore_text += f.read()
    
    # Show stats
    stats_text = '**BASE STATS**\n' + '```CSS\n'
    stats_text += 'HP: ' + oc_entry['baseHP'] + '\n'
    stats_text += 'Attack: ' + oc_entry['baseAttack'] + '\n'
    stats_text += 'Defense: ' + oc_entry['baseDefense'] + '\n'
    stats_text += 'Speed: ' + oc_entry['baseSpeed'] + '\n'
    stats_text += 'Luck: ' + oc_entry['baseLuck'] + '\n'
    stats_text += '```'
        
    text_output = '**' + oc_entry['ocName'] + '**\n' + stars_string
    text_output += '\n' + lore_text + '\n' + stats_text
    return oc_entry['artPath'], text_output