# module imports
from argparse import ArgumentParser
from os import path
from pydeb import Deb

# local imports
from . import logger
from .utils import get_version

def main(argv=None) -> None:
	parser = ArgumentParser()
	
	parser.add_argument('deb', action='store', help='path of the deb file to operate on')
	parser.add_argument('-x', '--extract', action='store_true', help='extracts the deb file')
	parser.add_argument('-c', '--contents', action='store_true', help='list the contents of the deb file')
	parser.add_argument('-v', '--version', action='version', version=f'pypkg-deb v{get_version()}',
	help='show current version and exit')
	
	args = parser.parse_args()
	
	if not path.exists(args.deb):
		logger.error('Specified path to archive does not exist.')
		exit(1)
	
	if not args.extract and not args.contents:
		logger.error('Please specify an operation.')
		exit(1)
	
	save = (not args.extract)
	
	deb = Deb(file=args.deb, remove_file=save)
	
	if args.extract:
		logger.log(f'Successfully extracted "{deb.control.package}"')
	if args.contents:
		logger.log('Contents:')
		for f in deb.filepaths.get('root'):
			print(f)
	
	
if __name__ == '__main__':
	main()