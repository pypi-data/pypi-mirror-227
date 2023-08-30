import logging, signal, grpc
from concurrent import futures
from profiles_rudderstack.utils import RefManager
from profiles_rudderstack.service import ProfilesRpcService, ClientTokenAuthInterceptor
from profiles_rudderstack.tunnel.tunnel_pb2 import PingRequest
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import PythonServiceStub, add_PythonServiceServicer_to_server

logging.basicConfig(level=logging.INFO)

class ProfilesRPCServer:
    def __init__(self, token: str, PythonRpcAddress: str, GoRpcAddress: str, currentSupportedSchemaVersion: int):
        self.logger = logging.getLogger("PythonRPCServer")

        self.PythonRpcAddress = PythonRpcAddress
        self.GoRpcAddress = GoRpcAddress
        self.currentSupportedSchemaVersion = currentSupportedSchemaVersion
        
        isRunning = self.__is_server_running(token)
        if not isRunning:
            self.__server_init(token)

    def __is_server_running(self, token: str):
        try:
            interceptors = [ClientTokenAuthInterceptor(token)]
            with grpc.secure_channel(self.PythonRpcAddress) as channel:
                grpc.intercept_channel(channel, *interceptors)
                pythonService = PythonServiceStub(channel)
                response = pythonService.Ping(PingRequest())
                return response.message == "ready"
        except:
            return False
        
    def __server_init(self, secret: str):
        refManager = RefManager()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ServerTokenAuthInterceptor(secret)])
        service = ProfilesRpcService(
            token=secret, 
            refManager=refManager,
            GoRpcAddress=self.GoRpcAddress,
            currentSupportedSchemaVersion=self.currentSupportedSchemaVersion
        )
        add_PythonServiceServicer_to_server(service, server)
        server.add_insecure_port(self.PythonRpcAddress)
        server.start()

        self.logger.info("Initialized Python RPC Server")
        self.server = server

        def signal_handler(sig, frame):
            self.logger.info("Stopping Python RPC Server")
            service.channel.close()
            server.stop(0)
            exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        server.wait_for_termination()

    def stop(self):
        self.logger.info("Stopping Python RPC Server")
        self.server.stop(0)


class ServerTokenAuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, token: str):
        self.token = token

    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get('authorization', '')

        if token != self.token:
            context = handler_call_details.invocation_context
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")
        else:
            return continuation(handler_call_details)
