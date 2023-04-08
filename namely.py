#!/usr/bin/python3

from string import Template
import itertools
import re
import argparse
import pathlib
import sys

from namelyParser import parseArguments

"""
Replace instances of $(first) or $(last) accounting for length arguements as well

This is a seperate function because our names have a slightly different format then
custom values since they are seperated by a space ie:
	Tyler Kranig
would be a value in a name file
"""
def replaceNames(templates: list, names: list) -> list:
	ret = []

	for template in templates:
		temp = Template(template)
		search = re.findall('\${(first|last)(\d+)*}', template)

		if len(search) != 0 and len(names) > 0:
			for name in names:
				first, last = name

				substitution_dictionary = {
						'first': first,
						'last': last,
				}
				
				for pattern in search:
					if pattern[1] != '':
						key = ''.join(pattern)
						length = int(pattern[1])
						name = first if pattern[0] == 'first' else last

						substitution_dictionary[key] = name[:length]

				ret.append(temp.safe_substitute(substitution_dictionary))
		else:
			ret.append(template)

	return ret

"""
Replace custom keys with whatever string is specified inside a file
Also handles domain replacement
"""
def replaceValues(templates: list, key: str, values: list) -> list:
	ret = []

	for template in templates:
		temp = Template(template)
		search = re.findall('\${(%s)(\d)*}' % (key), template)

		if len(search) != 0 and len(values) > 0:
			for value in values:
				substitution_dictionary = {
						key: value,
				}
				
				for pattern in search:
					if pattern[1] != '':
						numKey = ''.join(pattern)
						length = int(pattern[1])

						substitution_dictionary[numKey] = value[:length]

				ret.append(temp.safe_substitute(substitution_dictionary))
		else:
			ret.append(template)

	return ret

"""
The following load* functions accept a filename, open 
that filename, and return a list consisting of each line, 
stripped of '\n' characters. 

The loadNames function also splits each line at the first
whitespace, expecting each line to be in the format:

		first last 

The loadFile function returns a file opened in write mode
where the file's name is the inputted filename. 

.rstrip() removes the '\n' character.
The if statement checks if the line still exists after
being stripped of all whitespace and that the line 
does not start with a '#' symbol.

"""

def loadNames(parserMetavar):
	if parserMetavar is None: return []
	with open(parserMetavar, "r") as all_names:
		return [name.rstrip().split() for name in all_names.readlines() if name.strip() and not name.startswith("#")]

def loadDomains(parserMetavar):
	if parserMetavar is None: return []
	with open(parserMetavar, "r") as all_domains:
		return [domain.rstrip() for domain in all_domains.readlines() if domain.strip() and not domain.startswith("#")]

def loadTemplates(parserMetavar):
	with open(parserMetavar, "r") as all_templates:
		return [template.rstrip() for template in all_templates.readlines() if template.strip() and not template.startswith("#")]

def loadFile(parserMetavar):
	return open(parserMetavar, "w")


# Creates a list of lists wherein each list contains the 
# contents of a single keyfile. 
def loadKeys(parserMetavar):
	keyDict = {}

	for key,filename in parserMetavar:
		with open(filename, "r") as all_values:
			keyDict[key] = [value.rstrip() for value in all_values.readlines() if value.strip() and not value.startswith("#")]

	return keyDict


"""
The following write* functions are responsible for 
outputting the correctly formatted emails to stdout
or to a specified file.

The writeToFile function is hard coded to write to 
the outfile variable, which is globally instantiated in 
main(). Newline characters '\n' are concatenated to each
email. 

"""

OUTFILE = None

def writeToTerminal(email):
	print(email)

def writeToFile(email):
	OUTFILE.write(email + '\n')


def main():
	parser = parseArguments()  #  Launches the parser.

	# If no CLI arguments are provided, print the argparse help screen. 
	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	# Parses the provided CLI arguments. namelyParser.py
	parser = parser.parse_args()

	# Templates are the only required argument
	if not (parser.template or parser.templatefile):
		raise Exception('No templates provided. Use either -t or -tf')

	# Chooses between a single paramter provided in the CLI or a specified file containing multiple lines of parameters. 
	names = [parser.name] if parser.name else loadNames(parser.namefile)
	domains = [parser.domain] if parser.domain else loadDomains(parser.domainfile)
	templates = [parser.template] if parser.template else loadTemplates(parser.templatefile)

	# Build a key dictionary for custom keys, add in domains
	keyDict = loadKeys(parser.key) if parser.key else {}
	keyDict["domain"] = domains

	# Opens the filename provided by the CLI, or sets itself to None.
	OUTFILE = loadFile(parser.outfile) if parser.outfile else None

	# Chooses which write* function to use based on if an outfile argument was provided.
	write_function = writeToFile if parser.outfile else writeToTerminal

	# Populate initial list with names to fill in
	retList = replaceNames(templates, names)

	# Replace each of the custom keys with values provided in files
	for key, value in keyDict.items():
		retList = replaceValues(retList, key, value)


	# Writes every email in emails_lists to either the terminal or to an outfile
	for string in retList:
		write_function(string)


	# Closes the specified outfile if it exists.
	if OUTFILE:
		OUTFILE.close()


if __name__ == '__main__':
	main()