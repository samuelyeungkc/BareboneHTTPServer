import os

# return a list of dirs from path
# ex : return ['dir1', 'dir2'] from dir1/dir2/file
def getPath(path):
	list = []

	# empty case
	if len(path) == 0:
		return list

	# case : no '/'
	elif path.find("/") == -1:
		return list

	# case : 1 or more '/'
	else:
		list = path.split("/")
		list.pop()

	return list

print "Starting ........."
print "case : abc/cde/efg/ghi/ijk ... " + str(getPath("abc/cde/efg/ghi/ijk"))
list = getPath("abc/cde/efg/ghi/ijk")
for element in list:
	print element
print "Completed."
