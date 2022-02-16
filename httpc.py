import socket
import argparse
import sys
from urllib.parse import urlparse

#######################################HELP MESSAGES##################################################
help_get = """httpc help get
usage: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
	-v Prints the detail of the response such as protocol, status, and headers.
	-h key:value Associates headers to HTTP Request with the format 'key:value'."""

help_post = """httpc help post
usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or from file.
	-v	Prints the detail of the response such as protocol, status, and headers.
	-h key:value	Associates headers to HTTP Request with the format 'key:value'.
	-d string	Associates an inline data to the body HTTP POST request.
	-f file	Associates the content of a file to the body HTTP POST request.
	Either [-d] or [-f] can be used but not both."""

general_help = """httpc help
httpc is a curl-like application but supports HTTP protocol only.
Usage:
	httpc command [arguments]
The commands are:
	get	executes a HTTP GET request and prints the response.
	post executes a HTTP POST request and prints the response.
	help prints this screen.

Use "httpc help [command]" for more information about a command."""
#####################################################################################################

def main():
	commandline_args = sys.argv[1:]
	num_commandline_args = len(commandline_args)

	error = check_for_dupplicates(commandline_args)
	if error:
		print(f"Syntax Error: {error}")
		return

	if len(commandline_args) < 1:
		print("Command Line arguments are missing! Please run 'httpc help' for detailed usage")
		return

	if (commandline_args[0] == 'help'):
		if (num_commandline_args >= 2 and commandline_args[1] == 'get'):
			print(help_get)
		elif (num_commandline_args >= 2 and commandline_args[1] == 'post'):
			print(help_post)
		else:
			print(general_help)
		return

	parser = argparse.ArgumentParser(add_help=False, usage='httpc (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL [-o output-file]')
	parser.add_argument("request", help="request", choices=["get", "post"])
	parser.add_argument("-v", help="Prints the status, headers and contents of the response.", default=False, required=False, action="store_true")
	parser.add_argument("-h", metavar='"k:v"', help="setting the header of the request in the format 'key: value.' you can have multiple headers by having the -h option before each header parameter.", default=[], required=False, action="append")
	parser.add_argument("url", help="url")
	action = parser.add_mutually_exclusive_group(required=False)
	action.add_argument("-d", metavar="inline-data", help="Associate the body of the HTTP Request with the inline data", required=False)
	action.add_argument("-f", metavar="file", help="Associate the body of the HTTP Request with the data from a given file", required=False)
	parser.add_argument("-o", metavar="output file", help="Write the body of the response to the specified file instead of the console", required=False)
	args = parser.parse_args()

	url = args.url
	port = 80
	request = args.request.upper()
	if request == "GET":
		if args.d or args.f:
			parser.error("get request should not be used with the options -d or -f.")
		# get_request(args.v, args.h, args.o, url, port, request)
	elif request == "POST":
		if not (args.d or args.f):
			parser.error("post request should be used with the options -d or -f (but not both).")
		# post_request(args.v, args.h, args.d, args.f, args.o, url, port, request)

if __name__ == "__main__":
    main()