import argparse
import pathlib

banner = '''
 __  _  __  __ __ ___ _ __   __
|  \| |/  \|  V  | __| |\ `v' /
| | ' | /\ | \_/ | _|| |_`. .' 
|_|\__|_||_|_| |_|___|___|!_!  

by Oriel & Tyler Kranig

github.com/OrielOrielOriel
github.com/tylerkranig

'''

#  Defines path as the parent directory of the script + the character '/'
PATH = str(pathlib.Path(__file__).parent.absolute()) + '/'

"""
Constructs the CLI argument parser. 

The default path for the *file arguments is equal to 
a certain filename concatenated to the parent directory
of the script file as defined by pathlib and instantiated
at the start of the script.  

"""

def parseArguments():
	parser = argparse.ArgumentParser(description=banner, formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('-n', '--name',
		metavar='name',
		nargs=2,
		type=str, 
		help='A single name.'
	)
	parser.add_argument('-nf', '--namefile',
		metavar='namefile',
		type=str,
		help='A list of names.'
	)

	parser.add_argument('-d', '--domain',
		metavar='domain',
		type=str,
		help='A single domain.'
	)
	parser.add_argument('-df', '--domainfile',
		metavar='domainfile',
		type=str,
		help='A list of domains.'
	)

	parser.add_argument('-t', '--template',
		metavar='template',
		type=str,
		help='A single template, has to be the last argument. Don\'t forget to escape the $ symbols.'
	)
	parser.add_argument('-tf', '--templatefile',
		metavar='templatefile',
		type=str,
		default=PATH+'templatelist.txt',
		help='A list of templates.'
	)

	parser.add_argument('-o', '--outfile',
		metavar='outfile',
		type=str,
		help='The file to output to.'
	)

	parser.add_argument('-k', '--key',
		metavar='key',
		nargs=2,
		type=str,
		action='append',
		help='Custom key. -k [key] [wordlist]'
	)

	return parser