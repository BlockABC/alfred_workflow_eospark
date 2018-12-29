# -*- coding:utf-8 -*-
import json,sys
import config
from datetime import datetime
from workflow import Workflow3, web
from workflow.background import is_running, run_in_background
from threading import Thread
from utils import get_data_from_api, get_data_from_rpc, utc2local


def get_bp_info(item):
	bp_info = get_data_from_api(config.API_BP_INFO + item)
	if len(bp_info['bp_list']) > 0:
		#print bp_info
		data = bp_info['bp_list'][0]
		str_claim = str(data['rewards_to_claimed'])
		str_prefix = '节点 | '
		subtitle = str_prefix + '当前排名: ' + str(data['rank']) + ' # 待申领 EOS 数量: ' + str_claim[:str_claim.find('.')] + ' # 已生产区块数: ' + str(data['produced_block_num']) + ' # 地区: ' + data['area']
		title = item
		link = config.BP_URL + item
		uid = 'bp_list_' + item
		icon = config.ICON_BP_PATH
		return title, subtitle, link, uid, icon, {}
	return '', '', '', '', '', {}

def get_account_info(item):
	balance = get_data_from_api(config.API_ACCOUNT_BALANCE + item)
	if balance:
		liquid = ('0' if balance['balance'] == '' else balance['balance'])
		stake_to_others = ('0' if balance['stake_to_others'] == '0.0000' else balance['stake_to_others'])
		stake_to_self = ('0' if balance['stake_to_self'] == '0.0000' else balance['stake_to_self'])
		unstake = ('0' if balance['unstake'] == '0.0000' else balance['unstake'])
		total_balance = float(liquid) + float(stake_to_others) + float(stake_to_self) + float(unstake)

		subtitle = '账户 | '
		str_cmd = subtitle + '流动资金: ' + liquid + ' # 抵押给他人: ' + stake_to_others + ' # 抵押给自己: ' + stake_to_self + ' # 正在赎回: ' + unstake
		subtitle = subtitle + 'EOS 总资产：' + str(total_balance)

		modifier_subtitles = {'cmd': str_cmd, 'cmd_paste': str_cmd}

		title = item
		link = config.ACCOUNT_URL + item
		uid = 'account_list_' + item
		icon = config.ICON_ACCOUNT_PATH
		return title, subtitle, link, uid, icon, modifier_subtitles
	return '', '', '', '', '', {}


def get_contract_info(item):
	contract_states = get_data_from_api(config.API_CONTRACT_INFO + item)
	if contract_states:
		state = '审计状态: '
		state = state + '已审计' if contract_states['audit_status'] != 'neverAudit' else '未审计'
		state = state + ' # 开源状态: '
		if contract_states['consistency_status'] == 'Inconsistent':
			state = state + '开源代码不一致'
		elif contract_states['consistency_status'] == 'Unverified':
			state = state + '未开源'
		elif contract_states['consistency_status'] == 'Verify Passed':
			state = state + '已开源'

		subtitle = '合约 | '
		str_local_time = utc2local(contract_states['code_deploy_time'])
		str_cmd = subtitle + '最近一次部署时间: ' + str_local_time
		modifier_subtitles = {'cmd': str_cmd, 'cmd_paste': str_local_time}

		subtitle = subtitle + state
		title = item
		link = config.CONTRACT_URL + item
		uid = 'contract_list_' + item
		icon = config.ICON_CONTRACT_PATH
		return title, subtitle, link, uid, icon, modifier_subtitles
	return '', '', '', '', '', {}

def get_token_info(item):
	symbol, creator = item.split(':')
	token_info = get_data_from_rpc(config.RPC_GET_TOKEN_INFO, 'post', {'code':creator, 'json':True, 'symbol':symbol})
	if token_info :
		str_prefix = '代币 | '
		supply = token_info[symbol]['supply']
		max_supply = token_info[symbol]['max_supply']
		subtitle = str_prefix + '当前发行量: ' + supply.split(' ')[0] + ' # 最大发行量: ' + max_supply.split(' ')[0]
		title = item
		link = config.TOKEN_URL + item
		uid = 'token_list_' + item
		icon = config.ICON_TOKEN_PATH
		str_cmd = str_prefix + '发行方: ' + item.split(':')[1]
		modifier_subtitles = {'cmd': str_cmd, 'cmd_paste':item.split(':')[1]}
		return title, subtitle, link, uid, icon, modifier_subtitles
	return '', '', '', '', '', {}


result_list = []


def set_result_list(cate, item):
	title, subtitle, link, uid, icon = 'title', 'subtitle', 'link', 'uid', 'icon'
	modifier_subtitles = {}

	if cate == 'account_list':
		title, subtitle, link, uid, icon, modifier_subtitles = get_account_info(item)
	elif cate == 'bp_list':
		title, subtitle, link, uid, icon, modifier_subtitles = get_bp_info(item)
	elif cate == 'contract_list':
		title, subtitle, link, uid, icon, modifier_subtitles = get_contract_info(item)
	elif cate == 'token_list':
		title, subtitle, link, uid, icon, modifier_subtitles = get_token_info(item)

	if title != '':
		result_list.append((title, subtitle, link, None, True, uid, icon, None, None, None, None, link, modifier_subtitles,))
	return

def get_search_result_from_svr(q):
	url = config.API_URL_KEY_SEARCH + q
	search_data = get_data_from_api(url)
	if not search_data:
		return
	threads = []
	item_limit = config.ITEM_LIMIT
	item_cates = ['account_list', 'bp_list', 'contract_list', 'token_list']
	for itr in item_cates:
		if itr in search_data:
			for item in search_data[itr][:item_limit]:
				t = Thread(target = set_result_list, args = [itr, item])
				t.start()
				threads.append(t)

	for t in threads:
		t.join()
	return 

def main(wf):
	get_search_result_from_svr(sys.argv[1])
	wf.cache_data('results_from_svr', result_list)
	return 0

if __name__ == '__main__':
	wf = Workflow3()
	log = wf.logger
	sys.exit(wf.run(main))

