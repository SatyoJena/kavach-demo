import requests
import re
from datetime import datetime
# Socks listener connection
proxy  = {
	"https" : "socks5h://127.0.0.1:9050",
	"http"  : "socks5h://127.0.0.1:9050"
}

'''def httpOrHttps(url) :
	try :
		requests.get("http://" + url, proxies = proxy)
	except :
		pass
''' #TODO : im tired -highest priority




def parseOnions(url : str) -> list : # maybe convert 'set' back to list for better functionality
	result = requests.get(url, proxies = proxy)
	regexquery = "\w+\.onion"
	data = re.findall(regexquery, str(result.content))
	if (len(data) == 0) :
		print("No files in current database :(")
		exit() # TODO : write a try except block
	data = list(set(data))
	data = [i+"\n" for i in data ]
	# write to a file
	with open("link_database.txt","a") as file: #TODO : write to a csv file instead with the search term
		file.write("======================= " + datetime.now().isoformat() + " ====================\n")
		file.writelines(data)
	return data

# better than hidden wiki - httpsite is ahmia.fi
_MASTER_URL   = "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"
def searchInAhmia() :
	query = "search/?q=" 
	terms = input("Enter a query: ")
	terms = terms.replace(" ", "+")
	url   = _MASTER_URL + query + terms
	return parseOnions(url)

# entry point TODO: implement __name__ == "__main__"
data  = searchInAhmia()
for index, url in enumerate(data) :
	print(index, '. ', url, sep = "")

msg = """
=============== MENU ===============
1. Check status of all urls
2. Choose a url as root and repeat
3. Try with another search term
Choose an option..
"""
while True :
	choice = int(input(msg))
	if choice == 1 :
		for index, url in enumerate(data) :
			checkRequest  = requests.get("http://" + url, proxies = proxy)
			print (url, "\t status = ", checkRequest.status_code)
			# TODO : use colorama to print red and green

	elif choice == 2 :
		index = int(input("Enter the index of the url: "))
		data = parseOnions("http://" +  url)
		for index, url in enumerate(data) :
			print(index, '. ', url, sep = "")
	elif choice == 3 :
		searchInAhmia()
