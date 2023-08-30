from typing import Dict, Tuple
from abc import ABC, abstractmethod
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import WhtServiceStub
from profiles_rudderstack.tunnel.tunnel_pb2 import ModelArg

# type aliases
ModelArg = ModelArg
WhtService = WhtServiceStub

class BaseModelType(ABC):
    ModelType = "base_model_type"
    ModelArgs : Dict[str, ModelArg] = {}
    # Json Schema
    BuildSpecSchema = {}


class BaseModel(ABC):
    def __init__(self, modelName: str, buildSpec: dict, whtModelRef: int, service: WhtService, schemaVersion: int) -> None:
        pass

    @abstractmethod
    def get_model_creator_recipe(self)-> str:
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self) -> Tuple[bool, str]:
        raise NotImplementedError()
