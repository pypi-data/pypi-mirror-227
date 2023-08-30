import json
import logging
from socket import socket, AF_INET, SOCK_STREAM

from .packet import Packet, PacketHeader, PacketType


class Client:
    _socket: socket
    _address: str
    _port: int

    def __init__(self, address: str, port: int):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._address = address
        self._port = port

    @property
    def address(self) -> str:
        return self._address

    @property
    def port(self) -> int:
        return self._port

    def connect(self):
        self._socket.connect((self.address, self.port))
        self._debug('connected')

    def cmd_getsn(self) -> dict:
        self._send_request({'cmd': 'getsn'})

        return self._recv_response()

    def _send_request(self, cmd: dict, sn: int = 0):
        packet = Packet(bytearray(json.dumps(cmd, ensure_ascii=False).encode('gb2312')))

        if sn != 0:
            packet.header.sn = sn

        self._send_data(packet.bytes())

    def _send_data(self, data: bytearray):
        self._debug(f'send: {data}')
        self._socket.send(data)

    def _recv_response(self) -> dict | None:
        header = self._recv_header()

        if header is None or header.type == PacketType.HEARTBEAT:
            return None

        data = self._recv_data(header.length)

        if data is None:
            return None

        return json.loads(data.decode('gb2312'))

    def _recv_header(self) -> PacketHeader | None:
        data = self._recv_data(8)

        if data is None or data[0] != 0x56 or data[1] != 0x5a:
            return None

        return PacketHeader.parse(data)

    def _recv_data(self, n: int) -> bytearray | None:
        data = bytearray()

        while len(data) < n:
            byte = self._socket.recv(n - len(data))

            if not byte:
                return None

            data.extend(byte)

        self._debug(f'recv: {data}')
        return data

    def _debug(self, msg: str):
        logging.debug('[%s:%d] %s', self.address, self.port, msg)
