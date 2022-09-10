import numpy as np
import requests
import string
from PIL import Image

OCR_API_URL = "https://api.ocr.space"
OCR_API_KEY = "K81260059888957" # Throw-away key

def main ():
	print('\033[92mYou have requested help from the cauldron of Wunderwarts:')
	print('the magical cauldron that extracts spells from empty parchments!\033[0m')
	
	image = Image.open('./parchment.png')
	pixels = np.asarray(image).copy()

	# As the head cauldronist I looked into the pixels
	# with pandas and noticed something strange with the blue channel

	for i, row in enumerate(pixels):
		for ii, pixel in enumerate(row):
			if (pixel[2] != 229): # If the blue value is not the usual value, then
				pixels[i][ii] = [0, 0, 0] # convert pixel to black

	# Save image with black text
	clear_image = Image.fromarray(pixels, 'RGB')
	clear_image.save('magic.jpg')

	# Send image to an OCR API
	clear_file = open('magic.jpg', 'rb')
	res = requests.post(
		f'{OCR_API_URL}/parse/image',
		headers={
			'apikey': OCR_API_KEY
		},
		data={ 'OCREngine': 2 },
		files={
			'file': clear_file
		}
	)
	
	parsed_text = res.json()['ParsedResults'][0]['ParsedText']
	parsed_text = parsed_text.replace(' ', '').replace('\n', '')

	# Decrypt text with an ancient rotation spell
	decrypted = rotate_text(parsed_text)

	print('\033[93mYour spells have been extracted and decrypted:\033[0m')
	print(decrypted)

def rotate_text (text, n = 5):
	alphabet = string.ascii_uppercase
	message = ''

	for letter in text.upper():
		if alphabet.find(letter) == -1:
			message += letter
		else:
			rotated_letter = alphabet[(alphabet.find(letter) + n) % len(alphabet)]
			message += rotated_letter

	return message

if __name__ == "__main__":
	main()