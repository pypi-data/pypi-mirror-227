"""
Get the correct addresses for the contracts by testing the deployment addresses using the RPC
Currently using Safe v1.3.0
https://github.com/gnosis/safe-deployments/tree/main/src/assets/v1.3.0
"""
from eth_typing import ChecksumAddress

from gnosis.eth import EthereumClient


def _get_valid_contract(
    ethereum_client: EthereumClient, addresses: ChecksumAddress
) -> ChecksumAddress:
    """
    :param ethereum_client:
    :param addresses:
    :return: First valid contract found in blockchain
    """

    for address in addresses:
        if ethereum_client.is_contract(address):
            return address
    raise ValueError(f"Network ${ethereum_client.get_network()} is not supported")


def get_safe_contract_address(ethereum_client: EthereumClient) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
            "0x69f4D1788e39c87893C980c06EdF4b7f686e2938",
        ],
    )


def get_safe_l2_contract_address(ethereum_client: EthereumClient) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0x3E5c63644E683549055b9Be8653de26E0B4CD36E",
            "0xfb1bffC9d739B8D520DaF37dF666da4C687191EA",
        ],
    )


def get_default_fallback_handler_address(
    ethereum_client: EthereumClient,
) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0xf48f2B2d2a534e402487b3ee7C18c33Aec0Fe5e4",
            "0x017062a1dE2FE6b99BE3d9d37841FeD19F573804",
        ],
    )


def get_proxy_factory_address(ethereum_client: EthereumClient) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2",
            "0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC",
        ],
    )


def get_last_multisend_address(ethereum_client: EthereumClient) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761",
            "0x998739BFdAAdde7C933B942a68053933098f9EDa",
        ],
    )


def get_last_multisend_call_only_address(
    ethereum_client: EthereumClient,
) -> ChecksumAddress:
    return _get_valid_contract(
        ethereum_client,
        [
            "0x40A2aCCbd92BCA938b02010E17A5b8929b49130D"
            "0xA1dabEF33b3B82c7814B6D82A79e50F4AC44102B"
        ],
    )
