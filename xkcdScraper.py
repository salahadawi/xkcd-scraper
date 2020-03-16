#! /usr/bin/python3

import requests, sys, bs4, os, re

i = 1
try:
	os.mkdir("xkcd")
except:
	pass

res = requests.get("http://xkcd.com/1")
res.raise_for_status()
while(1):
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	try:
		imageLink = "http:" + soup.select_one("#comic > img[src]")["src"]
	except:
		imageLink = "http:" + soup.select_one("#comic > a > img[src]")["src"]
	imageResponse = requests.get(imageLink)
	file = open("xkcd/" + str(i)+ "-" + re.search("[^\/]+$", imageLink)[0], "wb")
	for chunk in imageResponse.iter_content(1024):
		file.write(chunk)
	file.close()
	print("Image number " + str(i) + " named " + re.search("[^\/]+$", imageLink)[0] + " downloaded.")
	linkNext = "http://xkcd.com" + soup.select_one("#middleContainer > ul > li:nth-of-type(4) > a")["href"]
	try:
		res = requests.get(linkNext)
		res.raise_for_status()
	except:
		print("Download finished.\n" + str(i) + " images downloaded.\n")
		sys.exit()
	i = int(soup.select_one("#middleContainer > ul > li:nth-of-type(4) > a")["href"].strip("/"))