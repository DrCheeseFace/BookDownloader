import requests
from bs4 import BeautifulSoup as bs

def getsearch():
	global searchQuery
	searchQuery = input('Enter Search term for book / author: ')
	search = "https://libgen.is/search.php?req="
	addOn = ""
	words = searchQuery.split()
	for i in words:
		i=i.capitalize()
		addOn = addOn + ('+'+ i )

	search = search + addOn	
	print(search)
	return search

def printhtml(r):
	soup = bs(r.text)
	print(soup.prettify())


def findBooks(r):

	soup = bs(r.text, 'html.parser')
	links_with_text = []
	for a in soup.find_all('a', href=True): 
		if a.text and "93.174.95.29" in a['href']: 
			links_with_text.append(a['href'])

	return links_with_text

def findTitles(r):
	soup = bs(r.text,'html.parser')
	bookTitles = []
	for a in soup.find_all('a'):
		if a.text and 'book/index.php?md5' in a['href']:
			bookTitles.append(a.text)		
	return bookTitles


	
def findDownload(r):
	soup = bs(r.text,'html.parser')
	for a in soup.find_all('a',href = True):
		if a.text and "/main/" in a['href']:
			downloadLinks.append(a['href'])


search = getsearch()
r = requests.get(search)
#printhtml(r)
links = findBooks(r)
titles = findTitles(r)

downloadLinks = []
for i in links:
	try:
		r = requests.get(i,verify = False)
		findDownload(r)
	except:
		pass

count = 0
for i in downloadLinks:
	if ('.epub'  in i) and ('.pdf'  in i):
		downloadLinks.pop(count)
		titles.pop(count)
	count+=1



if len(downloadLinks) == 0:
	print('no Download links available\n 1) check for typos \n 2) try replacing a number with a word and vice versa eg:five instead of 5')	
	exit()



count = 1
print('\n')
for i in downloadLinks:
	title = titles[count-1]
	string = str(count)+')'+title
	if 'epub' in i:
		print(string+'epub')
	else:
		print(string+'pdf')
	print('\n')
	

	
	count+=1

downloadIndex = int(input('index of which download? : '))




request = 'https://93.174.95.29' + str(downloadLinks[downloadIndex-1])
print(request)
r = requests.get(request,allow_redirects =True,verify = False)
if '.epub' in downloadLinks[downloadIndex-1]:
	open(titles[downloadIndex-1]+'.epub','wb').write(r.content)
else:
	open(titles[downloadIndex-1]+'.pdf','wb').write(r.content)

print('DONE') 






