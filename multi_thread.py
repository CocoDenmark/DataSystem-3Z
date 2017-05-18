#coding=utf-8
import os
import time
import urllib
import datetime
import httplib
import socket
import threading


mylock = threading.Lock()
shared_list = []




def write_read():
	today2 = datetime.datetime.now().strftime('%Y-%m-%d')
	des_dir = 'E:\\data_file_20150916\\stock\\htf_data\\raw_sina\\'
	wf = open(des_dir+today2+'.txt','a')
	ept_time = 0
	time.sleep(5)
	while ept_time < 10:
		try:
			mylock.acquire()
			ll = len(shared_list)
			if ll == 0:
				ept_time += 1
				print 'emt:',ept_time
				mylock.release()
				time.sleep(3)
				continue
			w_content = shared_list[0]
			del shared_list[0]
			mylock.release()
			if len(w_content) == 0:
				continue
			wf.write(w_content)
			print 'w'
			ept_time = 0
		except:
			continue
	wf.close()


	
def download(order):        
	try:
		today2 = datetime.datetime.now().strftime('%Y-%m-%d')
	except:
		today2 = '2015-07-22'              
	read_code_dir = 'G:\\Filesys\\stock_set\\'
	cf = open(read_code_dir+today2+'.txt', 'rb')
	line = cf.readline().strip()
	code_list1 = line.split(',')
	code_list = []
	for c in code_list1[:-1]:
		code = c[0:6]
		if code[0] == '6':
			code = 'sh' + code
		else:
			code = 'sz' + code
		code_list.append(code)
	str_l = []
	length = len(code_list)
	fix_l = 800
	pre = -1
	i = 1
	while i*fix_l<length:
		code = ''
		for c in code_list[(i-1)*fix_l:i*fix_l]:
			code = code + ',' + c
		str_l.append(code[1:])
		i += 1
	code = ''
	for c in code_list[(i-1)*fix_l:]:
		code = code + ',' + c
	str_l.append(code[1:])
   
	host = 'hq.sinajs.cn'
	results=socket.gethostbyname(host)
	conn = httplib.HTTPConnection(results)     
	i = 0
	len_str = len(str_l)
	if order == 0:
		start = 0
		end = int(len_str/2)
	else:
		start = int(len_str/2)
		end = len_str
	i = start
	h = time.localtime().tm_hour
	m = time.localtime().tm_min
	while not (h>=15 and m >=6):
		while i < end:
			time1 = int(round(time.time() * 1000)) 
			conn.request('get', '/list='+str_l[i])
			content = conn.getresponse().read()
		#conn.close()
			mylock.acquire()
			shared_list.append(content)
		#print content[:500]
			mylock.release()
			time2 = int(round(time.time() * 1000))
			print order,i,'time:',time2-time1
			i += 1
		i = start
		h = time.localtime().tm_hour
		m = time.localtime().tm_min
	conn.close()

def test():
	thread.start_new_thread(download,())
	thread.join()
	#thread.start_new_thread(write_read,())
	
if __name__=='__main__':
	threads = []
	t=threading.Thread(target=download,args=(0,))  #code_list3
	threads.append(t)
	threads[-1].start()
	t=threading.Thread(target=download,args=(1,))  #code_list3
	threads.append(t)
	threads[-1].start()
	t=threading.Thread(target=write_read,args=())  #code_list3
	threads.append(t)
	threads[-1].start()
	threads[-3].join()
	threads[-2].join()
	threads[-1].join()
