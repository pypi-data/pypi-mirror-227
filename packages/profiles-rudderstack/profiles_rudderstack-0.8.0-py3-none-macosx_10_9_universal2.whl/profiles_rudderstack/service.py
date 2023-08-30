import json, grpc, importlib.util, importlib.metadata, logging, pkg_resources
from packaging.requirements import Requirement
from typing import Callable, Tuple, List
from google.protobuf import struct_pb2, json_format
from grpc_interceptor import ClientCallDetails, ClientInterceptor

from profiles_rudderstack.model import BaseModel, BaseModelType
from profiles_rudderstack.utils import RefManager
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import PythonServiceServicer, WhtServiceStub

logging.basicConfig(level=logging.INFO)

class ProfilesRpcService(PythonServiceServicer):
    def __init__(self, token: str, refManager: RefManager, GoRpcAddress: str, currentSupportedSchemaVersion: int):
        self.logger = logging.getLogger("PythonRPCService")

        self.GoRpcAddress = GoRpcAddress
        self.currentSupportedSchemaVersion = currentSupportedSchemaVersion
        self.__refManager = refManager
        if not self.__is_go_rpc_up():
            raise Exception("WHT RPC server is not up")

        interceptors = [ClientTokenAuthInterceptor(token)]
        self.channel = grpc.insecure_channel(GoRpcAddress)
        intercept_channel = grpc.intercept_channel(self.channel, *interceptors)
        self.whtService = WhtServiceStub(intercept_channel)
    
    def __is_go_rpc_up(self):
        try:
            with grpc.insecure_channel(self.GoRpcAddress) as channel:
                is_up = grpc.channel_ready_future(channel)
                is_up.result(timeout=5)
                return True
        except:
            return False
        
    def __createFactoryFunc(self, modelClass: BaseModel, modelType: str):
        def factory(baseProjRef:int, modelName: str, buildSpec: dict):
            newPyModelResponse: tunnel_pb2.NewPythonModelResponse = self.whtService.NewPythonModel(tunnel_pb2.NewPythonModelRequest(
                name=modelName,
                model_type=modelType, 
                build_spec=json.dumps(buildSpec),
                base_proj_ref=baseProjRef,
            ))

            whtModelRef = newPyModelResponse.model_ref
            model = modelClass(modelName, buildSpec, whtModelRef, self.whtService, self.currentSupportedSchemaVersion)
            pyModelRef = self.__refManager.createRef(model)

            return whtModelRef, pyModelRef
        
        return factory
        
    def __registerModelType(self, package: str, project_ref: int):
        requirement = Requirement(package)
        module = importlib.import_module(requirement.name)
        if module is None:
            return f"{requirement.name} not found" 

        registerFunc: Callable[[],Tuple[BaseModelType, BaseModel]] = getattr(module, "RegisterModelType")
        if registerFunc is None:
            return f"RegisterModelType not found in {requirement.name}"

        modelTypeClass, modelClass = registerFunc()
        modelType = modelTypeClass.ModelType
        
        schema = struct_pb2.Struct()
        json_format.ParseDict(modelTypeClass.BuildSpecSchema, schema)
        
        self.whtService.RegisterModelType(tunnel_pb2.RegisterModelTypeRequest(
            model_type=modelType, 
            model_args=modelTypeClass.ModelArgs,
            build_spec_schema=schema,
            project_ref=project_ref,
        ))

        factory = self.__createFactoryFunc(modelClass, modelType)
        self.__refManager.createRefWithKey(modelType, {
            "package": requirement.name,
            "factoryFunc": factory,
        })
        
        return None
    
    def RegisterPackages(self, request: tunnel_pb2.RegisterPackagesRequest, context):
        not_installed: List[str] = []
        for package in request.packages:
            try:
                pkg_resources.require(package)
            except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                not_installed.append(package)
        
        if not_installed:
            error_message = "The following package(s) are not installed or their version is not correct: {}.".format(", ".join(not_installed))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(error_message)
            return tunnel_pb2.RegisterPackagesResponse()

        for package in request.packages:
            err = self.__registerModelType(package, request.project_ref)
            if err is not None:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(err)
                return tunnel_pb2.RegisterPackagesResponse()
        
        return tunnel_pb2.RegisterPackagesResponse()
    
    def ModelFactory(self, request: tunnel_pb2.ModelFactoryRequest, context):
        modelTypeRef = self.__refManager.getRef(request.model_type)
        if modelTypeRef is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model type not found")
            return tunnel_pb2.ModelFactoryResponse()
        
        buildSpec = json.loads(request.build_spec)
        whtModelRef, pyModelRef = modelTypeRef["factoryFunc"](request.base_proj_ref, request.model_name, buildSpec)
        
        return tunnel_pb2.ModelFactoryResponse(wht_model_ref=whtModelRef, python_model_ref=pyModelRef)
    
    def GetModelCreatorRecipe(self, request: tunnel_pb2.GetModelCreatorRecipeRequest, context):
        model: BaseModel | None = self.__refManager.getRef(request.model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model not found")
            return tunnel_pb2.GetModelCreatorRecipeResponse()

        recipe = model.get_model_creator_recipe()
        return tunnel_pb2.GetModelCreatorRecipeResponse(recipe=recipe)
    
    def Validate(self, request: tunnel_pb2.ValidateRequest, context):
        model: BaseModel | None = self.__refManager.getRef(request.model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model not found")
            return tunnel_pb2.ValidateResponse()

        isValid, err = model.validate()
        return tunnel_pb2.ValidateResponse(valid=isValid, error=err)
    
    def GetPackageVersion(self, request: tunnel_pb2.GetPackageVersionRequest, context):
        modelTypeRef = self.__refManager.getRef(request.model_type)
        if modelTypeRef is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model type not found")
            return tunnel_pb2.GetPackageVersionResponse()

        package = modelTypeRef["package"]
        version = importlib.metadata.version(package)
        return tunnel_pb2.GetPackageVersionResponse(version=version)

    def Ping(self, request, context):
        return tunnel_pb2.PingResponse(message="ready")


class ClientTokenAuthInterceptor(ClientInterceptor):
    def __init__(self, token):
        self.token = token

    def intercept(self, method, request_or_iterator, call_details: grpc.ClientCallDetails):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("authorization", self.token)],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)