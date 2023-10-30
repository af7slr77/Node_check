import requests
import json
from config.zilliqa import MAIN_NODE, MAX_NODE_TIMEOUT_SECOND
from time import time
import logging
from typing import Union, Dict, List, Any

get_blocks_logger = logging.getLogger('block.block_worker.get_blocks')


def get_blocks() -> Dict[str, Union[float, int, None]]:
    params: str = json.dumps(
        {
            "id": "1",
            "jsonrpc": "2.0",
            "method": "GetBlockchainInfo",
            "params": [""]
        }
    )
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    try:
        start: float = time()
        result: Dict[str, Any] = requests.post(
            MAIN_NODE, 
            data=params, 
            headers=headers,
            timeout=MAX_NODE_TIMEOUT_SECOND
        ).json()
        stop: float = time()
        responce_time: float = stop - start
        current_ds_epoch: int = int(result['result']['CurrentDSEpoch'])
        current_mini_epoch: int = int(result['result']['CurrentMiniEpoch'])
        blocks_with_data: Dict[str, Union[float, int, None]] = {
            'current_ds_epoch': current_ds_epoch,
            'current_mini_epoch': current_mini_epoch,
            'response_time': responce_time
        }
        return blocks_with_data
    except Exception as ex:
        get_blocks_logger.warning(ex, extra={'line': 40})
        blocks_with_none: Dict[str, Union[float, int, None]] = {
            'current_ds_epoch': None,
            'current_mini_epoch': None,
            'response_time': None
        }
        return blocks_with_none
