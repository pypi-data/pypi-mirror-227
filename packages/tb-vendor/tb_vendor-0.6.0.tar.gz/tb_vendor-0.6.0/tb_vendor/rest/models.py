from typing import Type, Union

from tb_rest_client import RestClientCE, RestClientPE
from tb_rest_client.models.models_ce.device import Device as DeviceCE
from tb_rest_client.models.models_pe.device import Device as DevicePE


RestClientClass = Union[Type[RestClientCE], Type[RestClientPE]]
RestClient = Union[RestClientCE, RestClientPE]
Device = Union[DeviceCE, DevicePE]
