# -*- coding:utf-8 -*-
import config, data_from_svr
import json, sys, re
from datetime import datetime
from workflow import Workflow3, web
from workflow.background import is_running, run_in_background
from utils import get_data_from_api, utc2local


def add_default_item(item):
	link = config.SEARCH_URL + item
	itr = wf.add_item(uid = 'default', icon = config.ICON_SEARCH_PATH, title = '跳转 EOSPark 网页搜索', subtitle = '打开默认浏览器', valid=True, arg = link, quicklookurl = link)
	cmd_subtitle = 'Let\'s go'
	itr.add_modifier('cmd', cmd_subtitle)

def add_num_account_item(item):
	title, subtitle, link, uid, icon, modifier_subtitles = data_from_svr.get_account_info(item)
	if title == '':
		return
	itr = wf.add_item(uid = uid, icon = icon,  title = item, subtitle = subtitle, valid=True, arg = link, quicklookurl = link)
	if modifier_subtitles != {}:
		itr.add_modifier('cmd', modifier_subtitles['cmd'], modifier_subtitles['cmd_paste'])

def add_block_item(item):
	block_data = get_data_from_api(config.API_BLOCK_INFO + item)
	if block_data:
		str_prefix = '区块 | '
		trx_int = len(block_data['transactions'])
		subtitle = str_prefix + '内含交易数：' + str(trx_int) + ' # 出块节点：' + block_data['producer']
		uid = 'block_' + item
		link = config.BLOCK_URL + item
		icon = config.ICON_BLOCK_PATH
		itr = wf.add_item(uid = uid, icon = icon,  title = item, subtitle = subtitle, valid=True, arg = link, quicklookurl = link)
		block_hash = block_data['id']
		cmd_subtitle = str_prefix + 'id: ' + block_hash
		itr.add_modifier('cmd', cmd_subtitle, block_hash)

def add_tx_item(item):
	tx_data = get_data_from_api(config.API_TX_INFO + item)
	if tx_data:
		str_prefix = '交易 | '
		tx_type, tx_hash, tx_time = '', '', tx_data['timestamp']
		if tx_data['eospark_trx_type'] == 'ordinary':
			tx_type = '普通'
			tx_hash = tx_data['trx']['id']
		else:
			tx_type = '内联'
			tx_hash = tx_data['id']

		subtitle = str_prefix + '类型：' + tx_type + ' # 所在区块：' + str(tx_data['block_num']) + ' # 时间: ' + utc2local(tx_time)
		uid = 'tx_' + item
		link = config.TX_URL + item
		icon = config.ICON_TX_PATH
		itr = wf.add_item(uid = uid, icon = icon,  title = item, subtitle = subtitle, valid=True, arg = link, quicklookurl = link)

def main(wf):
	item = sys.argv[1]
	
	add_default_item(item)
	has_item = False
	if len(item) == 64 :
		has_item = True
		add_tx_item(item)
	if item.isdigit():
		has_item = True
		add_block_item(item)

	pattern = re.compile(r'^[1-5.]{1,12}$')
	m = pattern.match(item)
	if m:
		has_item = True
		add_num_account_item(item)

	if not wf.cached_data_fresh('results_from_svr', max_age = 1):
		run_in_background('from_svr', ['/usr/bin/python', wf.workflowfile('data_from_svr.py'), item])

	if is_running('from_svr'):
		wf.rerun = config.REFRESH
		link = config.SEARCH_URL + item
		title = '更多内容正在搜索中🔍' if has_item else  '正在搜索中🔍'
		has_item = False
		wf.add_item(uid = 'more', icon = config.ICON_SEARCH_PATH, title = title, subtitle = '', valid=True, arg = link, quicklookurl = link)
		wf.send_feedback()
		return 0
	
	results_from_svr = wf.cached_data('results_from_svr', max_age = 0)
	for item in results_from_svr:
		itr = wf.add_item(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11])
		if item[12] != {}:
			itr.add_modifier('cmd', item[12]['cmd'], item[12]['cmd_paste'])

	wf.send_feedback()


if __name__ == '__main__':
    
	wf = Workflow3()
	log = wf.logger
	sys.exit(wf.run(main))
