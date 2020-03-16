#! /usr/bin/python3

import requests, sys, bs4, os, re

i = 1
try:
	os.mkdir("xkcd")
except:
	pass
while(1):
	if i == 404:
		i+= 1
	try:
		res = requests.get("http://xkcd.com/" + str(i))
		res.raise_for_status()
	except:
		print("Download finished.\n" + str(i) + " images downloaded.\n")
		sys.exit()
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	try:
		imageLink = "http:" + soup.select_one("#comic > img[src]")["src"]
	except:
		imageLink = "http:" + soup.select_one("#comic > a > img[src]")["src"]
	imageResponse = requests.get(imageLink)
	file = open("xkcd/" + str(i) + re.search("\.\w+$", imageLink)[0], "wb")
	for chunk in imageResponse.iter_content(1024):
		file.write(chunk)
	file.close()
	print("Image " + re.search("[^\/]+$", imageLink)[0] + " downloaded.")
	i += 1