import inspect
import logging
import os
from datetime import datetime
from functools import partial
from multiprocessing import Event, Process
from threading import Thread
from typing import List

import pynng
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from foreverbull import data, models
from foreverbull.broker.socket.exceptions import SocketTimeout


class Request(BaseModel):
    execution: str
    timestamp: datetime
    symbol: str


class WorkerException(Exception):
    pass


class Worker:
    def __init__(self, survey_address: str, state_address: str, stop_event: Event, algo: callable):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("setting up worker")
        self._survey_address = survey_address
        self._state_address = state_address
        self._stop_event = stop_event
        self._database = None
        self._algo = algo
        self.parameters = {}
        super(Worker, self).__init__()

    @staticmethod
    def _eval_param(type: str, val):
        if type == "int":
            return int(val)
        elif type == "float":
            return float(val)
        elif type == "bool":
            return bool(val)
        elif type == "str":
            return str(val)
        else:
            raise WorkerException("Unknown parameter type")

    def _setup_algorithm(self, parameters: List[models.service.Parameter]):
        func = partial(self._algo)
        func_parameters = inspect.signature(func).parameters.copy()
        for key in ["asset", "portfolio"]:
            try:
                del func_parameters[key]
            except KeyError:
                pass

        for parameter in parameters:
            if parameter.key not in func_parameters:
                raise WorkerException(f"Parameter {parameter.key} not in function")
            if parameter.type != func_parameters[parameter.key].annotation.__name__:
                expected = func_parameters[parameter.key].annotation.__name__
                raise WorkerException(
                    f"Parameter {parameter.key} has type {parameter.type} but expected type {expected}"
                )
            if parameter.value is None:
                if parameter.default is None:
                    raise WorkerException(f"Parameter {parameter.key} has no default value")
                parameter.value = parameter.default
            parameter.value = self._eval_param(parameter.type, parameter.value)
            func = partial(func, **{parameter.key: parameter.value})
            del func_parameters[parameter.key]

        for parameter in func_parameters:
            if func_parameters[parameter].default is inspect._empty:
                raise WorkerException(f"Parameter {parameter} has no default value and is not configured")
            else:
                func = partial(func, **{parameter: func_parameters[parameter].default})
        return func

    def _process(self, request: Request):
        self.logger.debug("Processing: %s", request)
        with self._database_session() as db_session:
            asset = data.Asset.read(request.symbol, request.timestamp, db_session)
            portfolio = data.Portfolio.read(request.execution, request.timestamp, db_session)
        return self._algo(asset=asset, portfolio=portfolio)

    def configure_execution(self, execution: models.backtest.Execution):
        self.logger.info("configuring worker")
        self.socket = pynng.Rep0(dial=f"tcp://{execution.socket.host}:{execution.socket.port}")
        self.socket.recv_timeout = 500
        self.socket.send_timeout = 500
        self._algo = self._setup_algorithm(execution.parameters or [])
        self._database_session = sessionmaker(bind=create_engine(execution.database.url))
        self.logger.info("worker configured correctly")

    def run(self):
        responder = pynng.Respondent0(dial=self._survey_address)
        responder.send_timeout = 500
        responder.recv_timeout = 500
        state = pynng.Pub0(dial=self._state_address)
        state.send(b"ready")
        self.logger.info("starting worker")
        while True:
            try:
                request = models.service.Request.load(responder.recv())
                self.logger.info("Received request")
                if request.task == "configure_execution":
                    execution = models.backtest.Execution(**request.data)
                    self.configure_execution(execution)
                    responder.send(models.service.Response(task=request.task, error=None).dump())
                elif request.task == "run_execution":
                    responder.send(models.service.Response(task=request.task, error=None).dump())
                    self.run_execution()
                elif request.task == "stop":
                    self.logger.debug("Stopping worker")
                    responder.send(models.service.Response(task=request.task, error=None).dump())
                    responder.close()
                    state.close()
                    break
                else:
                    self.logger.info("Received unknown task")
                    responder.send(models.service.Response(task=request.task, error="Unknown task").dump())
            except pynng.exceptions.Timeout:
                pass
            except KeyboardInterrupt:
                responder.close()
                state.close()
                break
            except Exception as e:
                self.logger.exception(repr(e))
                responder.send(models.service.Response(task=request.task, error=repr(e)).dump())

    def run_execution(self):
        while True:
            try:
                self.logger.debug("Getting context socket")
                context_socket = self.socket.new_context()
                request = models.service.Request.load(context_socket.recv())
                order = self._process(Request(**request.data))
                self.logger.debug(f"Sending response {order}")
                context_socket.send(models.service.Response(task=request.task, data=order).dump())
                context_socket.close()
            except (SocketTimeout, pynng.exceptions.Timeout):
                context_socket.close()
            except Exception as e:
                self.logger.exception(repr(e))
                context_socket.send(models.service.Response(task=request.task, error=repr(e)).dump())
                context_socket.close()
            if self._stop_event.is_set():
                break
        self.socket.close()


class WorkerThread(Worker, Thread):
    pass


class WorkerProcess(Worker, Process):
    pass


class WorkerPool:
    def __init__(self, algo: callable):
        self.logger = logging.getLogger(__name__)
        self._workers = []
        self._algo = algo
        self._executors = 2
        self._stop_workers_event = Event()
        self._survey_address = "ipc:///tmp/worker_pool.ipc"
        self._state_address = "ipc:///tmp/worker_states.ipc"
        self.survey = pynng.Surveyor0(listen=self._survey_address)
        self.worker_states = pynng.Sub0(listen=self._state_address)
        self.worker_states.subscribe(b"")
        self.worker_states.recv_timeout = 10000
        self.survey.send_timeout = 30000
        self.survey.recv_timeout = 30000

    def setup(self):
        self.logger.info("starting workers")
        for i in range(self._executors):
            self.logger.info("starting worker %s", i)
            if os.getenv("THREADED_EXECUTION"):
                worker = WorkerThread(self._survey_address, self._state_address, self._stop_workers_event, self._algo)
            else:
                worker = WorkerProcess(self._survey_address, self._state_address, self._stop_workers_event, self._algo)
            worker.start()
            self._workers.append(worker)
        responders = 0
        while True:
            try:
                self.worker_states.recv()
                responders += 1
                if responders == self._executors:
                    break
            except pynng.exceptions.Timeout:
                raise WorkerException("Workers did not respond in time")
        self.logger.info("workers started")

    def configure_execution(self, execution: models.backtest.Execution):
        self.logger.info("configuring workers")
        self.survey.send(models.service.Request(task="configure_execution", data=execution.model_dump()).dump())
        responders = 0
        while True:
            try:
                models.service.Response.load(self.survey.recv())
                responders += 1
                if responders == self._executors:
                    break
            except pynng.exceptions.Timeout:
                raise WorkerException("Workers did not respond in time")
        self.logger.info("workers configured")

    def run_execution(self):
        self.logger.info("running backtest")
        self._stop_workers_event.clear()
        self.survey.send(models.service.Request(task="run_execution").dump())
        responders = 0
        while True:
            try:
                self.survey.recv()
                responders += 1
                if responders == self._executors:
                    break
            except pynng.exceptions.Timeout:
                raise WorkerException("Workers did not respond in time")
        self.logger.info("backtest running")

    def stop_execution(self):
        if self._stop_workers_event.is_set():
            return
        self.logger.info("stopping workers")
        self._stop_workers_event.set()

    def stop(self):
        if not self._stop_workers_event.is_set():
            self.stop_execution()
        self.survey.send(models.service.Request(task="stop").dump())
        responders = 0
        while True:
            try:
                self.survey.recv()
                responders += 1
                if responders == self._executors:
                    break
            except pynng.exceptions.Timeout:
                raise WorkerException("Workers did not respond in time")
        self.logger.info("workers stopped")
        self.survey.close()
        self.worker_states.close()
