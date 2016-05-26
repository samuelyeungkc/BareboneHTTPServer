def URIResource(str):

	str = str[:str.index("\n")]

	newStr = str
	index = newStr.index("/") + 1
	newStr = newStr[index:]
	endIndex = newStr.index(" ") 
	newStr = newStr[:endIndex]

	return newStr

str2 = """GET /ooo!123l3 HTTP/1.1
Host: localhost:8000
Accept-Encoding: gzip, deflate
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.2 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.2
Accept-Language: en-us
Cache-Control: max-age=0
Connection: keep-alive
"""
str3 = URIResource(str2)
print str3
