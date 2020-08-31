import numpy as np
import cv2
import os

# Generate a party line-up based on the provided cards
def create_party_image(party, save_path='cache/party_cache.png'):
	party_imgs = []
	for card in party:
		card_img = cv2.imread(card.art_path, cv2.IMREAD_UNCHANGED)
		if party_imgs:  # Take on the resolution of the first image. (Probably should change this to a different metric)
			card_img = cv2.resize(card_img, (party_imgs[0].shape[1], party_imgs[0].shape[0]))
		party_imgs.append(card_img)
	party_imgs = np.hstack(party_imgs)
	try:
		os.mkdir('cache/')
	except OSError:
		pass
	cv2.imwrite(save_path, party_imgs)
	return save_path