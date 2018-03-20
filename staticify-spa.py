#!/usr/bin/python

import fileinput, glob, os, re, sys

def showUsage(scriptName):
    print("Usage: %s %s" % (scriptName, "directory"))

def main():
    # Meteor appends hash values to .js and .css files
    # This pattern matches a hash value so we can strip it off
    HASH_PATTERN = '(\?hash=[0-9a-z]+)'

    # Set up pattern matcher for index.html file
    # We look for this file because it has links to other files in it
    INDEX_PATTERN = "index.html"
    INDEX_MATCHER = re.compile(INDEX_PATTERN)

    GIT_PATTERN = "/\.git.*"
    GIT_MATCHER = re.compile(GIT_PATTERN)

    # Remove DDP stuff so client doesn't keep bugging server
    DDP_IMPORT_PATTERN = '(DDP = .*)'
    DDP_IMPORT_FILE = "global-imports.js"
    DDP_IMPORT_MATCHER = re.compile(DDP_IMPORT_FILE)
    DDP_SCRIPT_PATTERN = '<script type=".*" src="/packages/ddp.*.js"></script>'

    # Show usage if we don't get a directory argument
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
    print("Pattern: " + HASH_PATTERN)

    # Starting walking from the dir to find all files that may need to be fixed
    for dirpath, subdirs, files in os.walk(dir):
        print('--\ndirectory = ' + dirpath)

        # Skip .git directories
        if GIT_MATCHER.search(dirpath):
            continue

        for filename in files:
            filepath = os.path.join(dirpath, filename)

            # print('\t- file %s (full path: %s)' % (filename, filepath))

            # Rename files to remove hash
    	    fixed_file = re.sub(HASH_PATTERN, '', filename)
    	    fixed_path = re.sub(HASH_PATTERN, '', filepath)
    	    os.rename(filepath, fixed_path)
    	    print('\t- fixed %s (full path: %s)' % (fixed_file, fixed_path))

            # Fix links in index file
    	    if INDEX_MATCHER.match(fixed_file):
                print("\t- INDEX FILE: editing links and scripts in " + INDEX_PATTERN)
                # Use fileinput to open file and edit in place
                for line in fileinput.input(fixed_path, inplace=1):
                    # Remove HASH_PATTERN wherever we find it
                    # Strip line ending because print puts it back on
                    line = re.sub(HASH_PATTERN, '', line.rstrip())
                    # Remove DDP_SCRIPTs wherever we find them
                    line = re.sub(DDP_SCRIPT_PATTERN, '', line)
                    print(line)

            # Remove DDP import
            if DDP_IMPORT_MATCHER.match(fixed_file):
                print("\t- IMPORT FILE: editing imports in " + DDP_IMPORT_FILE)
                for line in fileinput.input(fixed_path, inplace=1):
                    # Remove lines that match DDP_IMPORT_PATTERN
                    if re.search(DDP_IMPORT_PATTERN, line):
                        line = ''
                    print(line.rstrip())

# When called from command line, run main function
if __name__ == '__main__':
  main()
