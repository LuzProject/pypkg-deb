# module imports
from argparse import ArgumentParser
from os import path
from pydeb import Deb, Pack

# local imports
from . import logger
from .utils import get_version

def main(argv=None) -> None:
	parser = ArgumentParser()
	
	parser.add_argument('path', action='store', help='path to operate on')
	parser.add_argument('-b', '--build', action='store_true', help='build a .deb file from a directory')
	parser.add_argument('-x', '--extract', action='store_true', help='extracts the deb file')
	parser.add_argument('-c', '--contents', action='store_true', help='list the contents of the deb file')
	parser.add_argument('-v', '--version', action='version', version=f'pypkg-deb v{get_version()}',
	help='show current version and exit')
	parser.add_argument(
     	'-Z', help='specify a compression algorithm (gzip, xz, bzip). ignored unless using "-b"')
	parser.add_argument(
		'-z', help='specify a compression level (1-9); defaults to 9. ignored unless using "-b"', type=int)
 
	args = parser.parse_args()
	
	if not path.exists(args.path):
		logger.error('Specified path does not exist.')
		exit(1)
	
	if not args.extract and not args.contents and not args.build:
		logger.error('Please specify an operation.')
		exit(1)
	
	if args.extract:
		deb = Deb(file=args.path, remove_file=False)
		logger.log(f'Successfully extracted "{deb.control.package}"')
	if args.contents:
		deb = Deb(file=args.path, remove_file=True)
		logger.log('Contents:')
		for f in deb.filepaths.get('root'):
			print(f)
	if args.build:
		if not args.Z:
			args.Z = 'xz'
		if not args.z:
			args.z = 9
		packed = Pack(args.path, algorithm=args.Z, compression_level=args.z)
		deb = Deb(file=packed.debpath, remove_file=True)
		logger.log(f'Successfully built "{deb.control.package}"')
	
	
if __name__ == '__main__':
	main()