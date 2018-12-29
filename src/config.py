# -*- coding:utf-8 -*-

API_KEY = 'a9564ebc3289b7a14551baf8ad5ec60a' # 你的 APIKEY，建议自己申请一个免费的 KEY，不然都用公共的，会有频率限制，体验不太好,申请地址：https://eospark.com/openapi/apply
ITEM_LIMIT = 3 # 检索候选词个数: 1~5
REFRESH = 1 # Alfred 候选列表刷新间隔，单位：秒

LOGO = 'images/logo.png'
ACCOUNT_URL = 'https://eospark.com/account/'
ICON_ACCOUNT_PATH = 'images/account.png'
CONTRACT_URL = 'https://eospark.com/contract/'
ICON_CONTRACT_PATH = 'images/contract.png'
BP_URL = 'https://eospark.com/bp/'
ICON_BP_PATH = 'images/bp.png'
TOKEN_URL = 'https://eospark.com/contract/'
ICON_TOKEN_PATH = 'images/token.png'

BLOCK_URL = 'https://eospark.com/block/'
ICON_BLOCK_PATH = 'images/block.png'
TX_URL = 'https://eospark.com/tx/'
ICON_TX_PATH = 'images/tx.png'
ICON_SEARCH_PATH = 'images/search.png'
SEARCH_URL = 'https://eospark.com/search?query='

API_HOST = 'https://api.eospark.com/api'
API_ACCOUNT_BALANCE = API_HOST + '?module=account&action=get_account_balance&apikey=' + API_KEY + '&account='
API_CONTRACT_INFO = API_HOST + '?module=contract&action=get_contract_info&apikey=' + API_KEY + '&account='
API_BLOCK_INFO = API_HOST + '?module=block&action=get_block_detail&apikey=' + API_KEY + '&block_num='
API_TX_INFO = API_HOST + '?module=transaction&action=get_transaction_detail_info&apikey=' + API_KEY + '&trx_id='
API_URL_KEY_SEARCH = API_HOST + '?module=home&action=search_by_key&apikey=' + API_KEY + '&key='
API_BATCH_ACCOUNT_BALANCE = API_HOST + '?module=account&action=get_currency_balance_by_accounts&apikey=' + API_KEY + '&code=eosio.token&accounts='
API_BP_INFO = API_HOST + '?module=account&action=get_bp_info&apikey=' + API_KEY + '&account='

RPC_HOST = 'https://mainnet.meet.one/v1/chain'
RPC_GET_TOKEN_INFO = RPC_HOST + '/get_currency_stats'
RPC_BP_INFO = RPC_HOST + '/get_producers'

