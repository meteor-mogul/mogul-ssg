import fileinput, glob, os, re, sys

def showUsage(scriptName):
  print("Usage: %s %s" % (scriptName, "directory"))

def printFileName(filename):
  print filename

def rename(dir, patternFrom, patternTo):
    for pathAndFilename in glob.iglob(os.path.join(dir, patternFrom)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title + ext))

def main():
  if len(sys.argv) < 2:
	showUsage(sys.argv[0])
	print "FATAL: Missing directory argument"
	sys.exit(1)
  dir = sys.argv[1]
  # If your current working directory may change during script execution, it's recommended to
  # immediately convert program arguments to an absolute path. Then the variable root below will
  # be an absolute path as well. Example:
  # dir = os.path.abspath(dir)
  print("Directory: " + dir)
  print("Directory (absolute): " + os.path.abspath(dir))
  pattern = '(\?hash=[0-9a-z]+)'
  print("Pattern: " + pattern)

  # Set up pattern matcher for index.html file
  matcher = re.compile("index.html")

  for root, subdirs, files in os.walk(dir):
    print('--\nroot = ' + root)
    list_file_path = os.path.join(root, 'my-directory-list.txt')
    print('list_file_path = ' + list_file_path)

    with open(list_file_path, 'wb') as list_file:
        for subdir in subdirs:
            print('\t- subdirectory ' + subdir)

        for filename in files:
            file_path = os.path.join(root, filename)

            # print('\t- file %s (full path: %s)' % (filename, file_path))

    	    fixed_file = re.sub(pattern, '', filename)
    	    fixed_path = re.sub(pattern, '', file_path)
    	    print('\t- fixed %s (full path: %s)' % (fixed_file, fixed_path))

    	    os.rename(file_path, fixed_path)

    	    if matcher.match(fixed_file):

        		print "\t- INDEX.HTML: editing links in index.html"
        		for line in fileinput.input(fixed_path, inplace=1):
        			line = re.sub(pattern,'', line.rstrip())
        			print(line)

                  #with open(fixed_path, 'rb') as f:
                    #f_content = f.read()
                    #list_file.write(('The file %s contains:\n' % fixed_file).encode('utf-8'))
                    #list_file.write(f_content)
                    #list_file.write(b'\n')

if __name__ == '__main__':
  main()
