#coding:utf-8
"""
"""
__author__ = "Roger Liu(liuwenbin_2011@163.com)"
__version__ = "$v1.0"
__date__ = "$Date: 2013/2/21"
__copyright__ = "Copyright (c) 2013 Roger Liu"
__license__ = "Python"

import sys
import time
import os
import urllib
from optparse import OptionParser
from sgmllib import SGMLParser

class LinkProcessor(SGMLParser):
	def __init__(self, path):
		self.path = path
		self.counter_img = 0
		self.counter_js = 0
		self.counter_css = 0
		self.img_name_list = {}
		self.css_name_list = {}
		self.js_name_list = {}
		SGMLParser.__init__(self)

	def reset(self):
		SGMLParser.reset(self)

	def start_img(self, attrs):
		for element in attrs:
			if element[0] == "src":
				temp = element[1].split(".")
				extension = '.' + temp[-1]
				filepath = self.path+'/images/'+str(self.counter_img)+extension
				fsock = open(filepath,'wb')
				
				try:
					urllib.urlretrieve(element[1], filepath)
				except Exception:
					pass
				newlink = "images/"+str(self.counter_img)+extension
				self.counter_img += 1
				self.img_name_list[element[1]] = newlink

	def start_link(self, attrs):
		for element in attrs:
			if element[0] == "href":
				temp = element[1].split(".")
				extension = '.' + temp[-1]
				filepath = self.path+'/css/'+str(self.counter_css)+extension
				try:
					urllib.urlretrieve(element[1], filepath)
				except Exception:
					pass
	
				newlink = "css/"+str(self.counter_css)+extension
				self.css_name_list[element[1]] = newlink
				self.counter_css += 1
		
	
	def start_script(self, attrs):
		for element in attrs:
			if element[0] == "src":
				temp = element[1].split(".")
				temp1 = temp[-1]
				extension = '.' + temp1[:2]
				
				filepath = self.path+'/js/'+str(self.counter_js)+extension
				try:
					urllib.urlretrieve(element[1], filepath)
				except Exception:
					pass
				newlink = "js/"+str(self.counter_js)+extension
				self.counter_js += 1
				self.js_name_list[element[1]] = newlink

def parse():
	"""
	parse the args
	"""
	parser = OptionParser(description="The script is used to add certain arguments to the all the links in the specified page")
	parser.add_option("-u", "--url", dest="urlpth", action="store", help="Path you want to fetch")
	parser.add_option("-d", "--backup_time", dest="backup_time", action="store", help="auto backup time")
	parser.add_option("-o", "--output", dest="outputpth", action="store", help="Output path")
	(options, args) = parser.parse_args()
	return options

def generate_dir(outputpth):
	"""
		generate dirs with time stamp and return it 
	"""
	timestamp = time.strftime("%Y%m%d%X",time.localtime())
	path = outputpth + '/' + str(timestamp)
	os.mkdir(path)	
	f = open(path+'/'+'index.html','wb')
	f.close()
	os.mkdir(path+'/'+'images')
	os.mkdir(path+'/'+'js')
	os.mkdir(path+'/'+'css')
	
	return path

def download_resources(url, path):
	sock = urllib.urlopen(url)
	htmlSource = sock.read()
	sock.close()
	linkProc = LinkProcessor(path)
	linkProc.feed(htmlSource)
	

	sock = urllib.urlopen(url)
	fsock = open(path+'/index.html','wb')
	fsock.write(sock.read())
	fsock.close()
	fsock = open(path+'/index.html','r')
	html = fsock.read()
		
	html = str(html)
	fsock.close()

	for k, v in linkProc.img_name_list.items():
		html = html.replace(k,v)
	for k, v in linkProc.css_name_list.items():
		html = html.replace(k, v)
	for k, v in linkProc.js_name_list.items():
		html = html.replace(k,v)
	
	fsock = open(path+'/index.html','w')
	
	fsock.write(html)
	fsock.close()	


def main():
	"""main function"""
	options = parse()
	if not options.urlpth or not options.backup_time or not options.outputpth:
		print 'Need to specify the parameters option "-u" or "-d" or " -o"!'
	if '-h' in sys.argv or '--help' in sys.argv:#print help info
		print __doc__
	
	while True:
		time.sleep(int(options.backup_time))
		path = generate_dir(options.outputpth)	
		download_resources(options.urlpth, path)	

if __name__ == '__main__':
	main()
