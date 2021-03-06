from unittest import TestCase
from nexchange.rpc.ethash import EthashRpcApiClient
from core.tests.base import TransactionImportBaseTestCase
from ticker.tests.base import TickerBaseTestCase
from core.tests.utils import data_provider
from unittest.mock import patch
from core.tests.base import ETH_ROOT
from accounts.task_summary import import_transaction_deposit_crypto_invoke,\
    update_pending_transactions_invoke
from orders.task_summary import exchange_order_release_periodic
from risk_management.task_summary import reserves_balance_checker_periodic
from orders.models import Order
from core.models import Transaction, Currency, Pair
import os
from rest_framework.test import APIClient
from accounts import task_summary as account_tasks
from decimal import Decimal
from collections import namedtuple
from risk_management.models import Reserve
from orders.utils import release_order
import requests_mock
from django.conf import settings


ETHERSCAN_API_KEY = 'ether_scan_api_key'

ethash_check_tx_params = namedtuple(
    'eth_check_tx_params',
    ['case_name', 'tx_block', 'current_block', 'tx_status', 'min_confs',
     'expected_return']
)


class EthashClientTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(EthashClientTestCase, self).__init__(*args, **kwargs)
        self.client = EthashRpcApiClient()

    def test_data_hash(self):
        address = '0x74f6fcffac8cbf168684892837f27877e20c9e66'
        value = int(100 * 1e18)
        data_expected = \
            '0xa9059cbb' \
            '00000000000000000000000074f6fcffac8cbf168684892837f27877e20c9e66'\
            '0000000000000000000000000000000000000000000000056bc75e2d63100000'
        data = self.client.get_data_hash(
            'transfer(address,uint256)',
            *[address, hex(value)]
        )
        self.assertEqual(data_expected, data)


class EthashRawE2ETestCase(TransactionImportBaseTestCase,
                           TickerBaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ENABLED_TICKER_PAIRS = \
            ['BTCETH', 'BTCBDG', 'BTCEOS', 'BTCOMG',
             'ETHBTC', 'BDGBTC', 'EOSBTC', 'OMGBTC',
             'KCSBTC', 'BNBBTC', 'KNCBTC', 'BTCBIX',
             'BTCKCS', 'BTCBNB', 'BTCKNC', 'BIXBTC',
             'BTCHT', 'BTCCOSS', 'BTCBNT', 'BTCCOB',
             'HTBTC', 'COSSBTC', 'BNTBTC', 'COBBTC',
             'BTCBMH', 'BMHBTC']
        super(EthashRawE2ETestCase, cls).setUpClass()
        cls.import_txs_task = import_transaction_deposit_crypto_invoke
        cls.update_confirmation_task = update_pending_transactions_invoke
        cls.api_client = APIClient()
        cls.api = EthashRpcApiClient()

        cls.reserves = Reserve.objects.all()
        for r in cls.reserves:
            for account in r.account_set.filter(disabled=False):
                if account.wallet != 'rpc7':
                    account.disabled = True
                    account.save()

    @classmethod
    def tearDownClass(cls):
        for r in cls.reserves:
            for account in r.account_set.filter(disabled=True):
                account.disabled = False
                account.save()

    def _create_paid_order_api(self, pair_name, amount_base, address):
        order_data = {
            "amount_base": amount_base,
            "is_default_rule": False,
            "pair": {
                "name": pair_name
            },
            "withdraw_address": {
                "address": address
            }
        }
        order_api_url = '/en/api/v1/orders/'
        response = self.api_client.post(
            order_api_url, order_data, format='json')
        order = Order.objects.get(
            unique_reference=response.json()['unique_reference']
        )
        tx_data = {
            'amount': order.amount_quote,
            'tx_id': self.generate_txn_id(),
            'order': order,
            'address_to': order.deposit_address,
            'type': Transaction.DEPOSIT,
            'currency': order.pair.quote
        }
        res = order.register_deposit(tx_data)
        tx = res.get('tx')
        order.confirm_deposit(tx)
        return order

    @data_provider(
        lambda: (
            ('BTCETH',),
            ('BTCBDG',),
            ('BTCEOS',),
            ('BTCOMG',),
            ('BTCKCS',),
            ('BTCBNB',),
            ('BTCKNC',),
            ('BTCHT',),
            ('BTCBIX',),
            ('BTCBNT',),
            ('BTCCOSS',),
            ('BTCCOB',),
            ('BTCBMH',),
        )
    )
    @patch.dict(os.environ, {'RPC7_PUBLIC_KEY_C1': '0xmain_card'})
    @patch.dict(os.environ, {'RPC_RPC7_K': 'password'})
    @patch.dict(os.environ, {'RPC_RPC7_HOST': '0.0.0.0'})
    @patch.dict(os.environ, {'RPC_RPC7_PORT': '0000'})
    @patch('core.models.Currency.is_quote_of_enabled_pair')
    @patch('accounts.tasks.monitor_wallets.app.send_task')
    @patch(ETH_ROOT + 'get_accounts')
    @patch('web3.eth.Eth.getTransactionReceipt')
    @patch('web3.eth.Eth.blockNumber')
    @patch('web3.eth.Eth.getTransaction')
    @patch('web3.eth.Eth.getBlock')
    def test_pay_ethash_order(self, pair_name,
                              get_txs_eth_raw, get_tx_eth,
                              get_block_eth, get_tx_eth_receipt, get_accounts,
                              send_task, is_quote):
        is_quote.return_value = True
        amount_base = 0.5

        self._create_order(pair_name=pair_name, amount_base=amount_base)
        mock_currency = self.order.pair.quote
        mock_amount = self.order.amount_quote

        card = self.order.deposit_address.reserve
        get_accounts.return_value = [card.address.upper()]

        get_txs_eth_raw.return_value = self.get_ethash_block_raw(
            mock_currency, mock_amount, card.address
        )
        confs = mock_currency.min_confirmations + 1
        get_tx_eth.return_value = self.get_ethash_tx_raw(
            mock_currency, mock_amount, card.address, block_number=0
        )
        get_block_eth.return_value = confs
        self.import_txs_task.apply()

        self.order.refresh_from_db()
        self.assertEquals(self.order.status, Order.PAID_UNCONFIRMED, pair_name)
        # Failed status
        get_tx_eth_receipt.return_value = self.get_ethash_tx_receipt_raw(
            mock_currency, mock_amount, status=0, _to=card.address
        )
        self.update_confirmation_task.apply()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.PAID_UNCONFIRMED, pair_name)
        # Success status
        get_tx_eth_receipt.return_value = self.get_ethash_tx_receipt_raw(
            mock_currency, mock_amount, status=1, _to=card.address
        )
        self.update_confirmation_task.apply()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.PAID, pair_name)
        # Check Send Gas
        task, tx_id = send_task.call_args[0]
        with patch(ETH_ROOT + 'release_coins') as release_coins:
            getattr(
                account_tasks,
                task.split('accounts.task_summary.')[1]
            ).apply_async(tx_id)
            if mock_currency.is_token:
                self.assertEqual(release_coins.call_count, 1, pair_name)
                release_coins.assert_called_with(
                    Currency.objects.get(code='ETH'),
                    card.address,
                    Decimal(
                        str(mock_currency.tx_price.limit * mock_currency.tx_price.amount_wei / (10**18))  # noqa
                    )
                )
            else:
                self.assertEqual(release_coins.call_count, 0, pair_name)

    @data_provider(
        lambda: (
            ('ETHBTC',),
            ('BDGBTC',),
            ('EOSBTC',),
            ('OMGBTC',),
            ('KCSBTC',),
            ('BNBBTC',),
            ('KNCBTC',),
            ('HTBTC',),
            ('BIXBTC',),
            ('BNTBTC',),
            ('COSSBTC',),
            ('COBBTC',),
            ('BMHBTC',),
        )
    )
    @patch.dict(os.environ, {'RPC7_PUBLIC_KEY_C1': '0xmain_card'})
    @patch.dict(os.environ, {'RPC_RPC7_K': 'password'})
    @patch.dict(os.environ, {'RPC_RPC7_HOST': '0.0.0.0'})
    @patch.dict(os.environ, {'RPC_RPC7_PORT': '0000'})
    @patch(ETH_ROOT + '_list_txs')
    @patch(ETH_ROOT + 'net_listening')
    @patch('web3.eth.Eth.getTransactionReceipt')
    @patch('web3.eth.Eth.blockNumber')
    @patch('web3.eth.Eth.getTransaction')
    @patch('web3.eth.Eth.sendTransaction')
    @patch('web3.personal.Personal.lockAccount')
    @patch('web3.personal.Personal.unlockAccount')
    @patch(ETH_ROOT + 'get_balance')
    def test_release_ethash_order(self, pair_name, get_balance, unlock, lock,
                                  send_tx, get_tx_eth, get_block_eth,
                                  get_tx_eth_receipt, eth_listen,
                                  eth_list_txs):
        eth_list_txs.return_value = []
        eth_listen.return_value = True
        amount_base = 50
        pair = Pair.objects.get(name=pair_name)
        base = pair.base
        if base.minimal_amount >= Decimal(amount_base):
            base.minimal_amount = Decimal(amount_base) / Decimal('2')
            base.save()
        order = self._create_paid_order_api(
            pair_name, amount_base,
            '0x77454e832261aeed81422348efee52d5bd3a3684'
        )
        get_balance.return_value = amount_base * 2
        reserves_balance_checker_periodic.apply()
        send_tx.return_value = self.generate_txn_id()
        exchange_order_release_periodic.apply()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.RELEASED, pair_name)
        get_tx_eth_receipt.return_value = self.get_ethash_tx_receipt_raw(
            order.pair.base, order.amount_base, status=1,
            _to=order.withdraw_address.address
        )
        confs = order.pair.base.min_confirmations + 1
        get_tx_eth.return_value = self.get_ethash_tx_raw(
            order.pair.base, order.amount_base,
            order.withdraw_address.address,
            block_number=0
        )
        get_block_eth.return_value = confs
        self.update_confirmation_task.apply()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.COMPLETED, pair_name)

    @data_provider(lambda: (
        ethash_check_tx_params(
            case_name='Min Confirmation, confirmed',
            tx_block=0, current_block=12, tx_status=1, min_confs=12,
            expected_return=(True, 12)
        ),
        ethash_check_tx_params(
            case_name='1 Confirmation, not confirmed',
            tx_block=0, current_block=1, tx_status=1, min_confs=12,
            expected_return=(False, 1)
        ),
        ethash_check_tx_params(
            case_name='Min confirmations 0, not confirmed',
            tx_block=0, current_block=0, tx_status=1, min_confs=0,
            expected_return=(False, 0)
        ),
        ethash_check_tx_params(
            case_name='Min confirmations with bad status, not confirmed',
            tx_block=0, current_block=12, tx_status=0, min_confs=12,
            expected_return=(False, 12)
        ),
    ))
    @patch(ETH_ROOT + '_get_current_block')
    @patch(ETH_ROOT + '_get_tx_receipt')
    @patch(ETH_ROOT + '_get_tx')
    def test_check_tx_ethash(self, get_tx, get_tx_receipt, get_current_block,
                             **kwargs):
        tx_id = '123'
        self.ETH.min_confirmations = kwargs['min_confs']
        self.ETH.save()
        get_tx.return_value = self.get_ethash_tx_raw(
            self.ETH, Decimal('1'), '0x', block_number=kwargs['tx_block']
        )
        get_tx_receipt.return_value = self.get_ethash_tx_receipt_raw(
            self.ETH, Decimal('1'), status=kwargs['tx_status']
        )
        get_current_block.return_value = kwargs['current_block']
        res = self.api.check_tx(tx_id, self.ETH)
        self.assertEqual(res, kwargs['expected_return'], kwargs['case_name'])

    @data_provider(
        lambda: (
            ('ETHBTC',),
        )
    )
    @patch.dict(os.environ, {'RPC7_PUBLIC_KEY_C1': '0xmain_card'})
    @patch.dict(os.environ, {'RPC_RPC7_K': 'password'})
    @patch.dict(os.environ, {'RPC_RPC7_HOST': '0.0.0.0'})
    @patch.dict(os.environ, {'RPC_RPC7_PORT': '0000'})
    @patch(ETH_ROOT + '_list_txs')
    @patch(ETH_ROOT + 'net_listening')
    @patch('web3.eth.Eth.sendTransaction')
    @patch('web3.personal.Personal.lockAccount')
    @patch('web3.personal.Personal.unlockAccount')
    @patch(ETH_ROOT + 'get_balance')
    def test_release_ethash_order_with_util(self, pair_name, get_balance,
                                            unlock, lock,
                                            send_tx, eth_listen, eth_list_txs):
        eth_list_txs.return_value = []
        eth_listen.return_value = True
        amount_base = 50
        pair = Pair.objects.get(name=pair_name)
        base = pair.base
        if base.minimal_amount >= Decimal(amount_base):
            base.minimal_amount = Decimal(amount_base) / Decimal('2')
            base.save()
        order = self._create_paid_order_api(
            pair_name, amount_base,
            '0x77454e832261aeed81422348efee52d5bd3a3684'
        )
        get_balance.return_value = amount_base * 2
        reserves_balance_checker_periodic.apply()
        send_tx.return_value = None
        exchange_order_release_periodic.apply()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.PRE_RELEASE, pair_name)
        self.assertEqual(send_tx.call_count, 1)
        pre_called_with = send_tx.call_args[0][0]
        send_tx.return_value = tx_id = self.generate_txn_id()
        release_order(order)
        self.assertEqual(send_tx.call_count, 2)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.RELEASED, pair_name)
        called_with = send_tx.call_args[0][0]
        self.assertEqual(called_with, pre_called_with)
        tx = order.transactions.get(type='W')
        self.assertEqual(tx.tx_id, tx_id)
        self.assertEqual(tx.address_to, order.withdraw_address)
        self.assertEqual(called_with['to'], order.withdraw_address.address)
        self.assertEqual(tx.amount, order.amount_base)
        self.assertEqual(
            Decimal(called_with['value']) * Decimal('1e-18'), order.amount_base
        )

    @requests_mock.mock()
    @patch('orders.models.base.BaseUserOrder.coverable')
    @patch(ETH_ROOT + 'get_main_address')
    @patch(ETH_ROOT + 'health_check')
    @patch(ETH_ROOT + 'release_coins')
    def test_do_not_release_if_transaction_is_not_unique(
            self, request_mock, mock_release_coins, eth_health_check,
            mock_get_main_address, mock_coverable
    ):
        mock_get_main_address.return_value = settings.ETHERSCAN_API_KEY
        withdraw_address = '0x77454e832261aeed81422348efee52d5bd3a3684'
        order = self._create_paid_order_api(
            'ETHBTC', 0.5,
            withdraw_address
        )
        mock_coverable.return_value = True
        eth_health_check.return_value = True
        ETH = Currency.objects.get(code='ETH')
        value = int(
            Decimal(order.amount_base) * Decimal('1E{}'.format(ETH.decimals))
        )
        etherscan_txs_from_api = {"status": "1", "result": [
            {"to": "0x12313213", "value": "785471956517588563", 'input': '0x'},
            {"to": withdraw_address.lower(), "value": str(value),
             'input': '0x'}
        ]}
        tx_count = settings.RPC_IMPORT_TRANSACTIONS_VALIDATION_COUNT
        url = 'https://api.etherscan.io/api?module=account&action={action}&' \
              'address={address}&sort=desc&page=1&offset={tx_count}&apikey=' \
              '{etherscan_api_key}'. \
            format(action='txlist', address=settings.ETHERSCAN_API_KEY,
                   tx_count=tx_count,
                   etherscan_api_key=settings.ETHERSCAN_API_KEY)
        request_mock.get(url, json=etherscan_txs_from_api)
        exchange_order_release_periodic()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.PRE_RELEASE)
        self.assertTrue(order.flagged, True)
        self.assertEqual(mock_release_coins.call_count, 0)

    @requests_mock.mock()
    @patch('orders.models.base.BaseUserOrder.coverable')
    @patch(ETH_ROOT + 'get_main_address')
    @patch(ETH_ROOT + 'health_check')
    @patch(ETH_ROOT + 'release_coins')
    def test_do_not_release_if_transaction_is_not_unique_token(
            self, request_mock, mock_release_coins, eth_health_check,
            mock_get_main_address, mock_coverable
    ):
        mock_get_main_address.return_value = settings.ETHERSCAN_API_KEY
        withdraw_address = '0xB8c77482e45F1F44dE1745F52C74426C631bDD52'
        order = self._create_paid_order_api(
            'BNBBTC', 0.5,
            withdraw_address
        )
        mock_coverable.return_value = True
        eth_health_check.return_value = True
        ETH = Currency.objects.get(code='BNB')
        value = int(
            Decimal(order.amount_base) * Decimal('1E{}'.format(ETH.decimals))
        )
        etherscan_txs_from_api = {"status": "1", "result": [
            {"to": "0x12313213", "value": "785471956517588563", 'input': '0x',
             'tokenSymbol': 'BNB'},
            {"to": ETH.contract_address.lower(), "value": str(value),
             'input': '0x', 'tokenSymbol': 'BNB'}
        ]}
        tx_count = settings.RPC_IMPORT_TRANSACTIONS_VALIDATION_COUNT
        url = 'https://api.etherscan.io/api?module=account&action={action}&' \
              'address={address}&sort=desc&page=1&offset={tx_count}&apikey=' \
              '{etherscan_api_key}'. \
            format(action='tokentx', address=settings.ETHERSCAN_API_KEY,
                   tx_count=tx_count,
                   etherscan_api_key=settings.ETHERSCAN_API_KEY)
        request_mock.get(url, json=etherscan_txs_from_api)
        exchange_order_release_periodic()
        order.refresh_from_db()
        self.assertEqual(order.status, Order.PRE_RELEASE)
        self.assertTrue(order.flagged, True)
        self.assertEqual(mock_release_coins.call_count, 0)
