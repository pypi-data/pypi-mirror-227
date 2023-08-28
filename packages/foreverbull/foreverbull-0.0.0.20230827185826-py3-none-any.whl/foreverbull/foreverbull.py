import logging
import socket
import threading
from inspect import signature

from foreverbull import data, models
from foreverbull.broker.socket.client import SocketClient, SocketConfig
from foreverbull.broker.socket.exceptions import SocketClosed, SocketTimeout
from foreverbull.broker.socket.router import MessageRouter
from foreverbull.broker.storage.storage import Storage
from foreverbull.worker import WorkerPool


class Foreverbull(threading.Thread):
    # By keeping the _algo in a dict we save it from being pickled into the thread
    # If the thread ends up owning this it wont work in the workers later "RLOCK pickle failure.."
    # TODO: Maybe a better way to this? Python magic
    _algo = {}
    _parameters = []

    def __init__(
        self,
        local_host=socket.gethostbyname(socket.gethostname()),
        local_port=5555,
        storage_endpoint="localhost:9000",
        storage_access_key="minioadmin",
        storage_secret_key="minioadmin",
    ):
        self.storage: Storage = Storage(storage_endpoint, storage_access_key, storage_secret_key, secure=False)
        self.socket_config: SocketConfig = SocketConfig(host=local_host, port=local_port)
        self.running = False
        self._worker_pool: WorkerPool = None
        self._socket: SocketClient = None
        self.logger = logging.getLogger(__name__)
        self._routes = MessageRouter()
        self._routes.add_route(self.info, "info")
        self._routes.add_route(self.stop, "stop")
        self._routes.add_route(self.configure_execution, "configure_execution", models.backtest.Execution)
        self._routes.add_route(self.run_execution, "run_execution")
        self._routes.add_route(self.stop_execution, "stop_execution")
        threading.Thread.__init__(self)

    @staticmethod
    def _eval_param(type: str) -> str:
        if type == int:
            return "int"
        elif type == float:
            return "float"
        elif type == bool:
            return "bool"
        elif type == str:
            return "str"
        else:
            raise Exception("Unknown parameter type: {}".format(type))

    @staticmethod
    def set_algo(func):
        for key, value in signature(func).parameters.items():
            if value.annotation == data.Asset or value.annotation == data.Portfolio:
                continue
            default = None if value.default == value.empty else str(value.default)
            parameter = models.service.Parameter(
                key=key, default=default, type=Foreverbull._eval_param(value.annotation)
            )
            Foreverbull._parameters.append(parameter)
        Foreverbull._algo["func"] = func

    @staticmethod
    def algo():
        def decorator(func):
            Foreverbull.set_algo(func)
            return func

        return decorator

    def info(self):
        return models.service.Info(type="worker", version="0.0.1", parameters=self._parameters)

    def run(self):
        self.running = True
        self.logger.info("Starting instance")
        self._socket = SocketClient(self.socket_config)
        context_socket = None
        self.logger.info("Listening on {}:{}".format(self.socket_config.host, self.socket_config.port))
        while self.running:
            try:
                context_socket = self._socket.new_context()
                request = context_socket.recv()
                response = self._routes(request)
                context_socket.send(response)
                context_socket.close()
            except SocketTimeout:
                context_socket.close()
            except SocketClosed:
                return
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
        self._socket = None
        self.logger.info("exiting")

    def setup(self):
        if "func" not in self._algo:
            raise Exception("No algorithm defined")
        self._worker_pool = WorkerPool(self._algo["func"])
        self._worker_pool.setup()

    def configure_execution(self, execution: models.backtest.Execution) -> None:
        self.logger.info("Configuring instance")
        self._worker_pool.configure_execution(execution)
        return None

    def run_execution(self):
        self.logger.info("Running backtest")
        self._worker_pool.run_execution()

    def stop_execution(self):
        self.logger.info("Stopping backtest")
        self._worker_pool.stop_execution()

    def stop(self):
        self.logger.info("Stopping instance")
        self.running = False
        if self._worker_pool:
            self._worker_pool.stop()

    def get_backtest_result(self, backtest: str):
        return self.storage.backtest.download_backtest_results(backtest)
