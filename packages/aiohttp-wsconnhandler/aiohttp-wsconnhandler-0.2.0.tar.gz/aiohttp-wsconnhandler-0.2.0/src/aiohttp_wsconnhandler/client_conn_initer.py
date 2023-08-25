import asyncio
import logging
import typing as t


import aiohttp


from .ws_conn_handler import WSConnectionHandler


class WSClientConnectionInitializer:
    class SecondaryInitError(Exception):
        pass

    task: asyncio.Task = None
    init_done_event: asyncio.Event
    ws_handler: t.Optional[WSConnectionHandler]
    errors: list

    def initialize(
        self,
        url: str,
        *,
        logger: logging.Logger = None,
        session_kwargs: dict[str, t.Any] = None,
        connection_kwargs: dict[str, t.Any] = None,
        ws_msg_type=aiohttp.WSMsgType.TEXT,
        receive_queue: asyncio.Queue = None,
        send_queue: asyncio.Queue = None,
    ) -> asyncio.Event:
        if self.task is not None:
            raise self.SecondaryInitError()

        self.init_done_event = asyncio.Event()

        self.ws_handler = None
        self.errors = []

        self.task = asyncio.create_task(
            self._connect_and_loop(
                url,
                logger=logger,
                session_kwargs=session_kwargs,
                connection_kwargs=connection_kwargs,
                ws_msg_type=ws_msg_type,
                receive_queue=receive_queue,
                send_queue=send_queue,
                connected_cb=self._on_connected,
                error_cb=self._on_error,
            )
        )

        return self.init_done_event

    def _on_connected(self, handler: WSConnectionHandler) -> None:
        self.ws_handler = handler
        self.init_done_event.set()

    def _on_error(self, errors: list) -> None:
        self.errors.extend(errors)
        self.init_done_event.set()

    @staticmethod
    async def _connect_and_loop(
        url,
        *,
        logger: logging.Logger = None,
        session_kwargs: dict[str, t.Any] = None,
        connection_kwargs: dict[str, t.Any] = None,
        ws_msg_type=aiohttp.WSMsgType.TEXT,
        receive_queue: asyncio.Queue = None,
        send_queue: asyncio.Queue = None,
        connected_cb: t.Callable[[WSConnectionHandler], None] = None,
        error_cb: t.Callable[[list], None] = None,
    ) -> None:
        ws_handler = None
        errors = []

        if session_kwargs is None:
            session_kwargs = {}
        if connection_kwargs is None:
            connection_kwargs = {}
        errors = []
        try:
            async with aiohttp.ClientSession(**session_kwargs) as session:
                async with session.ws_connect(url, **connection_kwargs) as ws:
                    ws_handler = WSConnectionHandler(
                        ws,
                        logger=logger,
                        ws_msg_type=ws_msg_type,
                        receive_queue=receive_queue,
                        send_queue=send_queue,
                    )
                    if connected_cb is not None:
                        connected_cb(ws_handler)
                    await ws_handler.run_loop()
        except aiohttp.ClientError as e:
            errors.append(e)
            if error_cb is not None:
                error_cb(errors)
