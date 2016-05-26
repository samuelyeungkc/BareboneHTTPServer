# To establish connection
import socket

# To access file
import os

# return the path of resource in URI from HTTP header
# example : return abc/cde in http://localhost/abc/cde
def URIResourcePath(str):

        newStr = str
        index = newStr.index("/") + 1
        newStr = newStr[index:]
        endIndex = newStr.index(" ")
        newStr = newStr[:endIndex]

	'''
	print "From Header"
	print str
	print "Leaving Resource......" + newStr
	'''

        return newStr

def serve_file(fileName, contentType):

	# tmp for developement
	if not os.path.exists(fileName):
		return ""


	allFile = open(fileName, "r")
	size = os.fstat(allFile.fileno()).st_size
	contentTypeHeader = getContentTypeHeader(contentType)
	httpResponse = composeHeader(size, contentTypeHeader)
	httpResponse += allFile.read()
	return httpResponse

# return a list of dirs from path 
# ex : return ['dir1', 'dir2'] from dir1/dir2/file
def getDirList(path):
        list = []

        # empty case
        if len(path) == 0:
                return list

        # case : no '/'
        elif path.find("/") == -1:
		#list.append(path)
                return list

        # case : 1 or more '/'
        else:
                list = path.split("/")
		print "path...." + path
		print "list...." + str(list)

		# remove last element  
		list.pop()

	print "get result : " + str(list)
        return list


# return file name from path, "" if it does not contain one
# example : return "file1" in "dirA/dirB/file1", "" in "dirA/dirB/", "" in "" or "/"
def getFileName(path):
        fileName = ""

        length = len(path)
        index = path.rfind("/")

        # case : empty string
        if length == 0:
                fileName = ""
        # case : non-empty string with no "/"
        elif index == -1:
                fileName = path
        # case : non-empty string ends with "/"
        elif index == length:
                fileName = ""
        # case : non-empty string with "/", not ending with /
        else:
                fileName = path[index+1:]
        
        return fileName

def getContentTypeHeader(type):
	typeHeader = ""

	if type.endswith(".htm") or type.endswith("html"):
		typeHeader = "text/html"
	else:
		typeHeader = "application/octet-stream"

	return typeHeader

def composeHeader(length, contentType):
	header = ""
	header += "HTTP/1.1 200 OK\n"
	header += "Content-Type: %s\n" % (contentType)
	header += "Content-Length: %d\n" % (length)
	header += "Connection: close\n"
	header += "\r\n"

	return header

def listCurDirAsHTTPResponse(fileName):
        contentType = "html"

	if len(fileName) != 0:
		fileName += "/"


        # fetch list of files
        fileList = ""
        filesInDir = os.listdir(".")
        for f in filesInDir:
                if not f.startswith("."):
                        fileList += "<a href=\"" + fileName  +  f + "\">" + f + "</a>" + "<br/>"

        # html code, used to calculate length of html code
        htmlCode = "<html><body></body></html>"
        htmlCodeLen = len(htmlCode) + len(fileList)

        # compose HTTP header
        httpResponse = composeHeader(htmlCodeLen, contentType)

        # add in content from folder
        httpResponse += "<html><body>" + fileList + "</body></html>"

        return httpResponse



# main start

host = "localhost"
port = 8000

# create socket object
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind( (host, port) )

# displaying status msg
print "Listening for connection....................."

while (1):
	soc.listen(1)
	connev, addr = soc.accept()

	httpResponse = ""

	# output connection client info
	#print "connected by " + str(addr[0]) + " using port " + str(addr[1])

	# recive data from client
	data = connev.recv(1024)

	# determine what to servre according to request
	resource = URIResourcePath(data)
	#print "The client is looking for: " + resource
	
	# determine file name
	fileName = getFileName(resource)
	#print "File name : " + fileName

	# determine what to serve according to request
	# serve root
	if resource == "":

		httpResponse = listCurDirAsHTTPResponse("")

	# debug
	elif resource.find("favicon.ico") != -1:
		print "favicon.ico"

	# serve sub dirs welcome page
	else:


		print "Resource......" + resource
		dirList = getDirList(resource)
		
		print "....................................."


		# save original dir to go back after the request
		originDir = os.getcwd()

		#print "the target...." + fileName + "..."

		# change dir to target
		for dir in dirList:
			os.chdir(dir)	

		print "at dir....." + str(os.getcwd())
		print "dir list..." + str(dirList)

		# go to target dir
		# serve dir content list
		#print "dir List : " + str(dirList)
		#print "file name : " + fileName
		if os.path.isdir(fileName):
			os.chdir(fileName)
			print "inside..."
			httpResponse = listCurDirAsHTTPResponse(fileName)
			
		# serve html files
		elif fileName.endswith(".html") or fileName.endswith(".htm"):
			contentType = "html"
			#print "here!"
			httpResponse = serve_file(fileName, contentType)

		# serve other files
		else:
			contentType = "regularFiles"
			httpResponse = serve_file(fileName, contentType)


		# clean up back to origin dir
		os.chdir(originDir)

	# error : invalid path, file not found

        # Debug : output HTTP request header
        #print "####################################################"
        #print data
        #print "####################################################"

	# send back data
	connev.sendall(httpResponse)
	connev.close()


# prompt exit
print "Connection closed. Program exiting now..."
