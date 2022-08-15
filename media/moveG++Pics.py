# -*- coding: utf-8 -*-
"""
Created on Sat Mar 09 17:31:47 2013

@author: HaysParents
"""

import os
import shutil
import exifread
import datetime
#import fnmatch
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def moveFile(obj, day):
	dest = obj.DestDir + obj.delim + day

	try: 
		os.makedirs(dest)
	except OSError:
		if not os.path.isdir(dest):
			raise
	if os.path.isdir(dest):
		shutil.move(obj.CurrDir + obj.delim + obj.filename, dest + obj.delim + obj.filename) # move the files from rigin to destination
		print("moved: " + obj.CurrDir + obj.delim + obj.filename + " --> " + dest + obj.delim + obj.filename)


def movePics(obj):
	with open("%s\\%s" % (obj.CurrDir, obj.filename), 'rb') as image: # file path and name
		exif = exifread.process_file(image)
		image.close()
		#print(exif)
		try:
			dt = str(exif['EXIF DateTimeOriginal'])  # might be different
			# segment string dt into date and time
			day, dtime = dt.split(" ", 1)
			day = day.replace(":", "-")
			#print(day)

			moveFile(obj, day)
		except:
			#print("FAILED: " + obj.CurrDir + obj.delim + obj.filename)
			# file creation timestamp in float
			c_time = os.path.getctime(obj.filename)
			# convert creation timestamp into DateTime object
			dt_c = datetime.datetime.fromtimestamp(c_time)
			#print('Created on:', dt_c)
			moveFile(obj, str(dt_c.date()))
	return

def creation_date(filename):
	parser = createParser(filename)
	metadata = extractMetadata(parser)
	creationDate = metadata.get('creation_date')
	#metadata.close()
	parser.close()
	return creationDate

def moveVids(obj):
	DateTimeCreated = str(creation_date(obj.filename))
	day = DateTimeCreated.split(" ")[0]
	#print(day)

	moveFile(obj, day)
	return


def main(): 
	class MoveMediaPaths:
		def __init__(self):
			self.delim = "\\"
			self.picTypes = ['.jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF', 'webp', 'WEBP']
			self.vidTypes = ['.mp4', '.MP4']
			self.CurrDir = os.path.dirname(os.path.abspath(__file__)) # Get directory of the script
			self.DestDir = self.CurrDir
			self.filename = ""
	m = MoveMediaPaths()

	#PicDest = m.CurrDir + m.delim + 'pics'
	#VidDest = m.CurrDir + m.delim + 'vids'
	year = "2021"
	PicDest = m.CurrDir + m.delim + 'Pictures' + m.delim + year 
	VidDest = m.CurrDir + m.delim + 'Videos' + m.delim + year 

	dirList=os.listdir(m.CurrDir)
	for filename in os.listdir(m.CurrDir):
		print("Processing: " + m.CurrDir + m.delim + filename)
		if filename.endswith(tuple(m.picTypes)):
			m.DestDir = PicDest
			m.filename = filename
			movePics(m)
		elif filename.endswith(tuple(m.vidTypes)):
			m.DestDir = VidDest
			m.filename = filename
			moveVids(m)

if __name__ == "__main__":
    main()

