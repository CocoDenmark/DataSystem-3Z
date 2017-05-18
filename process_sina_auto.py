# -*- coding:utf-8 -*-
# This python script deals with the error file, in which the download-failed codes are recorded.
# 2015-05-29
# created by Miao Zhou at 3zcapital

# import package
import sys
import time
import os
import datetime

 
dir1 = 'E:\\data_file_20150916\\stock\\htf_data\\raw_sina\\'
#dir1 = 'G:\\data_backup\\s\\'
des_dir = 'E:\\data_file_20150916\\stock\\htf_data\\quote_sina'
today = datetime.datetime.now()
today = today.strftime('%Y%m%d')


try:
	os.mkdir(des_dir+os.sep+today)
except:
	pass
c = ['0','6','3']

close1 = datetime.time(hour=11,minute=31,second=0)
open2 = datetime.time(hour=12,minute=59,second=0)
close2 = datetime.time(hour=15,minute=1,second=0)



time1 = time.time()
today1 = datetime.datetime.now()
today1 = today1.strftime('%Y-%m-%d')
if 1:
	r_f = open(dir1+today1+'.txt', 'rb')	
	time_stamp = ''
	end = 0
	while end == 0:
		count = 0
		data_block = {}
		while count < 50000:
			try:
				line = r_f.readline()
				line = line.strip()
				#print line
				if len(line)==1 or len(line)==0:
					end = 1
					break	
				if len(line)<24:
					continue
				ctime=line[-13:-5]
				code = line[13:19]
				if  code[0] not in c:
					print line
					continue
				if code not in data_block.keys():
					data_block[code] = []
				if len(data_block[code]) > 0 and data_block[code][-1][0:8]== ctime:
					continue
				xx=line.find(',')
				main=line[xx:-25]
				data_block[code].append(ctime+main)
				count += 1
			except:
				continue
		print count
		for code in data_block.keys():	
			try:
				ff = open(des_dir+os.sep+today+os.sep+code+'.txt', 'a')	
				for line in data_block[code]:
					ff.write(line+'\r\n')
				ff.close()
			except:
				continue
	r_f.close()
time2 = time.time()
l = 'Run Time: ' + str(time2-time1) + ' seconds'
print l
