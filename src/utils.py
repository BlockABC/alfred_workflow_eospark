# -*- coding:utf-8 -*-
import json, sys, time 
import config
from workflow import Workflow3, web
from datetime import datetime
import _strptime

reload(sys)
sys.setdefaultencoding('utf-8')

def get_data_from_api(url, method='get', params=None):
	try:
		r = {}
		if method == 'get':
			r = web.get(url = url)
		else:
			r = web.post(url = url, data = params)
		r.raise_for_status()
		resp = r.text
		data = json.loads(resp)
		search_data = data['data']
		return search_data
	except:
		return None

def get_data_from_rpc(url, method='get', params=None):
	try:
		r = {}
		if method == 'get':
			r = web.get(url = url)
		else:
			r = web.post(url = url, data = json.dumps(params))
		r.raise_for_status()
		resp = r.text
		data = json.loads(resp)
		return data
	except:
		return None

def utc2local(str_utc):
	now_stamp = time.time()
	local_time = datetime.fromtimestamp(now_stamp)
	utc_time = datetime.utcfromtimestamp(now_stamp)
	offset = local_time - utc_time

	st_utc = datetime.strptime(str_utc, '%Y-%m-%dT%H:%M:%S.%f')
	local_st = st_utc + offset
	return local_st.strftime('%Y-%m-%d %H:%M:%S.%f')
