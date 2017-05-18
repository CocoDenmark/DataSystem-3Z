# -*- coding:utf-8 -*-
# This python script deals with the error file, in which the download-failed codes are recorded.
# 2015-05-29
# created by Miao Zhou at 3zcapital

# import package
import sys
from WindPy import w
import time
import os
 

# reload the system to encode by utf-8 dealling with Chinese characters
reload(sys)
sys.setdefaultencoding('utf8')

# start wind
w.start(waitTime=60)

print 'date: ', sys.argv[1], sys.argv[2]

# this script deal with the following 4 dirs
base_dir = ['G:\\Filesys\\stock\\trade\\Forward_Rehabilitation','G:\\Filesys\\stock\\trade\\No_Rehabilitation','G:\\Filesys\\stock\\trade\\Backward_Rehabilitation','G:\\Filesys\\stock\\hold']


for base in base_dir:
	print base
# read the code that failed to download
	try:
		error_file = open(base+os.sep+'error_file'+os.sep+'fail_'+sys.argv[2]+'_renew_'+sys.argv[1]+'.txt', 'rb')
	except:
		dd = base+os.sep+'fail_'+sys.argv[2]+'_renew_'+sys.argv[1]+'.txt'
		print 'No such file!', dd
		break
	line = error_file.readline()
	line = line.strip()
	code_list = line.split('|')
	error_list = list()
	error_file.close()
# download the according info. for the certain code
	for c in code_list:
		if len(c) == 0:
			print 'all have been done'
			break
		type = base.split('\\')
		if type[-1] == 'No_Rehabilitation':
			d = w.wsd(c, "pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,close2,close3,turn,free_turn,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,maxupordown,trade_status,susp_reason", sys.argv[1], sys.argv[1], "Fill=Previous")
		elif type[-1] == 'Forward_Rehabilitation':
			d = w.wsd(c, "pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,trade_status,susp_reason,maxupordown", sys.argv[1], sys.argv[1], "Fill=Previous;PriceAdj=F")
		elif type[-1] == 'Backward_Rehabilitation':	
			d = w.wsd(c, "pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,trade_status,susp_reason,maxupordown", sys.argv[1], sys.argv[1], "Fill=Previous;PriceAdj=B")
		elif type[-1] == 'hold':
			wind_data = list()
			d = w.wsd(c, "total_shares,free_float_shares,float_a_shares,share_restricteda,share_totala,share_restrictedb,share_totalb,share_h,share_oversea,share_totaltradable,share_totalrestricted,share_nontradable,share_ntrd_prfshare,share_rtd_state,share_rtd_statejur,share_rtd_subotherdomes,share_rtd_domesjur,share_rtd_inst,share_rtd_domesnp,share_rtd_subfrgn,share_rtd_frgnjur,share_rtd_frgnnp,holder_top10pct,holder_top10quantity,holder_top10liqquantity,holder_controller,holder_name", sys.argv[1], sys.argv[1], "order=0;Fill=Previous", "showblank=-1")
			wind_data.append(d)
			d = w.wsd(c, "holder_quantity,holder_pct,holder_sharecategory", sys.argv[1], sys.argv[1], "order=1;Fill=Previous")
			wind_data.append(d)
			d = w.wsd(c, "holder_liqname", sys.argv[1], sys.argv[1], "order=0;Fill=Previous")
			wind_data.append(d)
			d = w.wsd(c, "holder_liqquantity,holder_liqsharecategory,holder_num,holder_avgnum,holder_avgpct,holder_havgpctchange,holder_qavgpctchange,holder_havgchange,holder_qavgchange,holder_avgpctchange", sys.argv[1], sys.argv[1], "order=1;shareType=1;Fill=Previous")
			wind_data.append(d)
		
		write_file = open(base+os.sep+'data'+os.sep+sys.argv[2]+os.sep+'current'+os.sep+sys.argv[1]+'.txt', 'a')
# because hold info. is consist of several dataframe, we have different method to write it into the txt file
		if type[-1] != 'hold':
			if d.ErrorCode != 0:
				print 'error at ', c
				time.sleep(2)
# if the download fails agian, record it in the new error list and then write into the error file
				error_list.append(c)
				continue
			length = len(d.Fields)
			write_file.write(c[0:6]+'|')

			i = 0
			for date in d.Times:
				write_file.write(str(date)+'|')
	
				j = 0
				while j<length:
					try:
				 		d.Data[j][i] = d.Data[j][i].encode('utf-8')
					except:
						None
					write_file.write(str(d.Data[j][i]))
					if j < (length-1):
						write_file.write('|')
					j += 1
				i += 1
			write_file.write('\r\n')
			print c
		else:		
			if d.ErrorCode != 0:
				print 'error at ', c
				time.sleep(2)
				error_list.append(c)
				continue
			write_file.write(c[0:6] + '|')
			i = 0
			for date in wind_data[1].Times:
				write_file.write(str(date) + '|')
				j = 0
				k = 1
				for d in wind_data:
					length = len(d.Fields)
					j = 0
					while j < length:
						try:
							d.Data[j][i] = str(d.Data[j][i])
							d.Data[j][i] = d.Data[j][i].encode('utf-8')
						except:
							None
						write_file.write(d.Data[j][i])
						if k < 4:
							write_file.write('|')
						if k == 4:
							if j < (length-1):
								write_file.write('|')
						j += 1
					k += 1
				i += 1
			write_file.write('\r\n')
			print 'hold: ', c
		write_file.close()
	error_file = open(base+os.sep+'error_file'+os.sep+'fail_'+sys.argv[2]+'_renew_'+sys.argv[1]+'.txt', 'wb')
	for e in error_list:
		if len(e) > 1:
			error_file.write(e+'|')
	error_file.close()
