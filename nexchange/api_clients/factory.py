from .uphold import UpholdApiClient
from .rpc import ScryptRpcApiClient, EthashRpcApiClient
from .bittrex import BittrexApiClient
from .kraken import KrakenApiClient


class ApiClientFactory:
    UPHOLD = UpholdApiClient()
    SCRYPT = ScryptRpcApiClient()
    ETHASH = EthashRpcApiClient()
    BITTREX = BittrexApiClient()
    KRAKEN = KrakenApiClient()

    @classmethod
    def get_api_client(cls, node):
        if node in cls.UPHOLD.related_nodes:
            return cls.UPHOLD
        elif node in cls.SCRYPT.related_nodes:
            return cls.SCRYPT
        elif node in cls.BITTREX.related_nodes:
            return cls.BITTREX
        elif node in cls.KRAKEN.related_nodes:
            return cls.KRAKEN
        elif node in cls.ETHASH.related_nodes:
            return cls.ETHASH
