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

print "Test : abc/cde ..." + getFileName("abc/cde")
print "Test : \"\" ..." + getFileName("")
print "Test : samuel ..." + getFileName("samuel")
print "Test : sam/uel/yeung ..." + getFileName("sam/uel/yeung")
print "Test : sam/ ..." + getFileName("sam/")
