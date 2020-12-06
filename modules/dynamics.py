from typing import List, Set, Dict, Tuple, Optional
import numpy as np
import cv2
import os


def create_party_image(party: Tuple['oc.OC', 'oc.OC', 'oc.OC'], save_path: str = 'cache/party_cache.png'):
    """This function dynamically generates the party lineup image based on the current status of the party.
    
    :param party: The list containing the OC card lineup to generate for.
    :save_path: The temporary cache to save this image to. The image is replaced with each iteration. 
    :return: The path that the image is saved to.
    """
    party_imgs = []
    
    # Go through each OC card in the party list and create an image from there.
    for card in party:
        card_img = cv2.imread(card.art_path, cv2.IMREAD_UNCHANGED)
        
        # Take on the resolution of the first image. (Probably should change this to a different metric)
        if party_imgs:  
            card_img = cv2.resize(card_img, (party_imgs[0].shape[1], party_imgs[0].shape[0]))
            
        # Tint red if OC card is defeated.
        if not card.enabled:
            card_img[:, :, 0] = 0
            card_img[:, :, 1] = 0
            
        party_imgs.append(card_img)
    party_imgs = np.hstack(party_imgs)
    
    # Make a directory if the directory doesn't exist.
    try:
        os.mkdir('cache/')
    except OSError:
        pass
    cv2.imwrite(save_path, party_imgs)
    return save_path