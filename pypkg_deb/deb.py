# module imports
from argparse import Namespace
from os import getcwd, listdir, mkdir, path, remove, system, walk
from pathlib import Path
from shutil import rmtree

# local imports
from . import logger
from .utils import cmd_in_path


def get_filepaths(directory):
	file_paths = []
	
	for root, directories, files in walk(directory):
		for filename in files:
			filepath = path.join(root.replace(directory, '') + '/' + filename)
			file_paths.append(filepath)
	
	return file_paths

class Control:
	def __init__(self, control: str):
		# bundle id
		self.package: str
		
		# name
		self.name: str
		
		# version
		self.version: str
		
		# author
		self.author: str
		
		# maintainer
		self.maintainer: str
		
		# desc
		self.description: str
		
		# arch
		self.architecture: str
		
		# depends
		self.depends: str
		
		# section
		self.section: str
		
		# icon
		self.icon: str
		
		# depiction
		self.depiction: str
		
		# sileo depiction
		self.sileodepiction: str
		
		# assign
		self.__assign(control)
	
	def __assign(self, control: str):
		last = ''
		# split control by line
		for line in control.splitlines():
			# split by value and key
			key = ''
			value = ''
			# check and make sure no multiline funny business is going on
			if len(line.split(': ')) == 1:
				key = last
				value = line
			else:
				key = line.split(': ')[0]
				value = line.split(': ')[1]
				last = key
			# match statement
			match key:
				case 'Package':
					self.package = value
				case 'Name':
					self.name = value
				case 'Version':
					self.version = value
				case 'Author':
					self.author = value
				case 'Maintainer':
					self.maintainer = value
				case 'Description':
					self.description = value
				case 'Architecture':
					self.architecture = value
				case 'Depends':
					self.depends = value
				case 'Section':
					self.section = value
				case 'Icon':
					self.icon = value
				case 'Depiction':
					self.depiction = value
				case 'SileoDepiction':
					self.sileodepiction = value


class Deb:
	def __init__(self, file: str, remove_file: bool = True):
		# xpath
		self.__xpath = ''
		
		# rmfile
		self.rmfile = remove_file
		
		# file path
		self.file = file
		
		# extract
		tmp = self.__extract()
		
		# control
		self.control = Control(open(f'{tmp}/control/control').read())
		
		# filepaths
		self.filepaths = {'root': [], 'control': []}
		
		# assign filepaths
		for file in get_filepaths(tmp):
			# if file starts with /data, add it to 'root'
			if file.startswith('/data'): self.filepaths['root'].append(file.replace('/data', ''))
			# if file starts with /control, add it to 'control'
			if file.startswith('/control'): self.filepaths['control'].append(file.replace('/control/', ''))
		
		# get contents of scripts
		self.scripts = {}
		
		for f in self.filepaths.get('control'):
			if f == '': continue
			self.scripts[f.replace('/', '')] = open(f'{tmp}/control/{f}').read()
		
		if remove_file: rmtree(tmp)

	def __extract(self) -> str:
		# set file var
		file = self.file
		# filename
		filename = Path(file).name
		# set path
		if self.rmfile:
			self.__xpath = f'./.{filename}.tmp'
		else:
			self.__xpath = f'./{filename.replace(".deb", "")}'
		# get full path
		path = f'{file if file.startswith("/") else getcwd() + "/" + file}'
		# get ar command
		ar = cmd_in_path('ar')
		# ensure file exists
		if ar == None:
			logger.error('Command "ar" is not installed. Please install it in order to use this script.')
			exit(1)
		# get tar command
		tar = cmd_in_path('tar')
		# ensure file exists
		if tar == None:
			logger.error('Command "tar" is not installed. Please install it in order to use this script.')
			exit(1)
		# make tmp dir
		mkdir(self.__xpath)
		# extract deb
		system(f'cd {self.__xpath} && ar x {path}')
		# remove all files except control and data
		for file in listdir(self.__xpath):
			if not file.startswith('control.') and not file.startswith('data.'):
				remove(f'{self.__xpath}/{file}')
			else:
				filename_0 = file.split('.')[0]
				system(f'cd {self.__xpath} && mkdir {filename_0}')
				match file.replace('control.', '').replace('data.', ''):
					case 'tar.xz':
						system(f'cd {self.__xpath} && {tar} xf {file} -C {filename_0}')
						remove(f'{self.__xpath}/{file}')
					case 'tar.gz':
						system(f'cd {self.__xpath} && {tar} xf {file} -C {filename_0}')
						remove(f'{self.__xpath}/{file}')
					case 'tar.lzma':
						system(f'cd {self.__xpath} && {tar} xf {file} -C {filename_0}')
						remove(f'{self.__xpath}/{file}')
					case 'tar.zst':
						system(f'cd {self.__xpath} && {tar} xf {file} -C {filename_0}')
						remove(f'{self.__xpath}/{file}')
					case _:
						logger.error(f'Unknown archive format. ({file.replace("control.", "").replace("data.", "")})')
						exit(1)

		# return path that we extracted to
		return self.__xpath