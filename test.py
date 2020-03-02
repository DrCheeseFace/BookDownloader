import requests
from bs4 import BeautifulSoup as bs


def getsearch():
	global searchQuery
	searchQuery = input('Enter book name and author (author is optional): ')
	search = "https://libgen.is/search.php?req="
	addOn = ""
	words = searchQuery.split()
	for i in words:
		i=i.capitalize()
		addOn = addOn + ('+'+ i )

	search = search + addOn	
	print(search)
	return search

def printHTML(request):
	data = request.text
	soup = bs(data)
	prettyHTML = soup.prettify()
	print(prettyHTML)

def findBooks(r):

	soup = bs(r.text, 'html.parser')
	links_with_text = []
	for a in soup.find_all('a', href=True): 
		if a.text and "93.174.95.29" in a['href']: 
			links_with_text.append(a['href'])

	return links_with_text

def findDownload(r):
	soup = bs(r.text,'html.parser')
	for a in soup.find_all('a',href = True):
		if a.text and "/main/" in a['href']:
			downloadLinks.append(a['href'])


search = getsearch()
r = requests.get(search)
links = findBooks(r)



downloadLinks = []
for i in links:
	try:
		r = requests.get(i)
		findDownload(r)
	except:
		pass
count = 0
for i in downloadLinks:
	if '.epub' not in i and '.pdf' not in i:
		downloadLinks.pop(count)
	count+=1



if len(downloadLinks) == 0:
	print('no Download try a different search')	
	exit()



count = 1
for i in downloadLinks:
	link = '\n' + str(count) + ') ' + 'http://93.174.95.29' + i
	count+=1
	print(link)
downloadIndex = int(input('index of which download? : '))

print('\n http://93.174.95.29'+downloadLinks[downloadIndex-1])
r = requests.get('http://93.174.95.29'+downloadLinks[downloadIndex-1],allow_redirects =True)
if '.epub' in downloadLinks[downloadIndex-1]:
	open(searchQuery+'.epub','wb').write(r.content)
else:
	open(searchQuery+'.pdf','wb').write(r.content)

print('DONE') 






