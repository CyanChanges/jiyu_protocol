import ipaddress
import socket
from struct import pack
from typing import Union


class JiyuProtocol:
    jy_cmd_bytes = {
        "message": [0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00, 0x01, 0x00, 0x9e, 0x03, 0x00, 0x00, 0x10, 0x41, 0xaf, 0xfb,
                    0xa0, 0xe7, 0x52,
                    0x40, 0x91, 0xdc, 0x27, 0xa3, 0xb6, 0xf9, 0x29, 0x2e, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x50,
                    0x81, 0x91, 0x03,
                    0x00, 0x00, 0x91, 0x03, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00,
                    0x00, 0x00],
        "command": [0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00, 0x01, 0x00, 0x6e, 0x03, 0x00, 0x00, 0x5b, 0x68, 0x2b, 0x25,
                    0x6f, 0x61, 0x64,
                    0x4d, 0xa7, 0x92, 0xf0, 0x47, 0x00, 0xc5, 0xa4, 0x0e, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x64,
                    0x86, 0x61, 0x03,
                    0x00, 0x00, 0x61, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00,
                    0x00, 0x00, 0x01,
                    0x00, 0x00, 0x00, 0x43, 0x00, 0x3a, 0x00, 0x5c, 0x00, 0x57, 0x00, 0x69, 0x00, 0x6e, 0x00, 0x64,
                    0x00, 0x6f, 0x00,
                    0x77, 0x00, 0x73, 0x00, 0x5c, 0x00, 0x73, 0x00, 0x79, 0x00, 0x73, 0x00, 0x74, 0x00, 0x65, 0x00,
                    0x6d, 0x00, 0x33,
                    0x00, 0x32, 0x00, 0x5c, 0x00, 0x63, 0x00, 0x6d, 0x00, 0x64, 0x00, 0x2e, 0x00, 0x65, 0x00, 0x78,
                    0x00, 0x65, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00,
                    0x00, 0x00, 0x2f, 0x00, 0x63, 0x00, 0x20, 0x00],
        "reboot": [0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00, 0x01, 0x00, 0x2a, 0x02, 0x00, 0x00, 0xbf, 0x40, 0x22, 0x4e, 0x57,
                   0x2d, 0x3e,
                   0x4f, 0x9b, 0x6f, 0xc1, 0x8d, 0xe1, 0xeb, 0x4f, 0x62, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x50, 0x81,
                   0x1d, 0x02,
                   0x00, 0x00, 0x1d, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x13, 0x00, 0x00,
                   0x10, 0x0f,
                   0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x59, 0x65, 0x08, 0x5e, 0x06, 0x5c,
                   0xcd, 0x91,
                   0x2f, 0x54, 0xa8, 0x60, 0x84, 0x76, 0xa1, 0x8b, 0x97, 0x7b, 0x3a, 0x67, 0x02, 0x30, 0x00, 0x00, 0x00,
                   0x00, 0x00],
        "shutdown": [0x44, 0x4d, 0x4f, 0x43, 0x00, 0x00, 0x01, 0x00, 0x2a, 0x02, 0x00, 0x00, 0xc8, 0xe3, 0x97, 0xfd,
                     0xc0, 0xb5, 0x9f,
                     0x45, 0x87, 0x72, 0x05, 0xbd, 0x4e, 0x46, 0xa8, 0x96, 0x20, 0x4e, 0x00, 0x00, 0xc0, 0xa8, 0x50,
                     0x81, 0x1d, 0x02,
                     0x00, 0x00, 0x1d, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14, 0x00,
                     0x00, 0x10, 0x0f,
                     0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x59, 0x65, 0x08, 0x5e, 0x06,
                     0x5c, 0x73, 0x51,
                     0xed, 0x95, 0xa8, 0x60, 0x84, 0x76, 0xa1, 0x8b, 0x97, 0x7b, 0x3a, 0x67, 0x02, 0x30, 0x00, 0x00,
                     0x00, 0x00, 0x00]}

    @classmethod
    def _decrypt_bytes(cls, key):
        return u''.join(map(chr, cls.jy_cmd_bytes[key]))

    @classmethod
    def send_content(cls, content: str, is_cmd=False, port=4705,
                     ip_network: Union[ipaddress.IPv4Network, ipaddress.IPv6Network] | None = None,
                     ip_addresses: Union[tuple[ipaddress.IPv4Network | ipaddress.IPv6Network],
                                         list[ipaddress.IPv4Address | ipaddress.IPv4Address]] = []):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if is_cmd:
            send_data = cls.jy_cmd_bytes['command'] + cls._hl_build(content)
        else:
            send_data = cls.jy_cmd_bytes['message'] + cls._hl_build(content)
        length = 0
        if ip_network:
            length += sock.sendto(
                pack("%dB\0" % (len(send_data)), *send_data),
                (str(ip_network.broadcast_address), port)
            )
        if ip_addresses:
            for ip_addr in ip_addresses:
                length += sock.sendto(pack("%dB\0" % (len(send_data)), *send_data), (str(ip_addr), port))
        sock.close()
        return length

    @classmethod
    def send_shutdown(cls, is_reboot: bool = False, port=4705,
                      ip_network: Union[ipaddress.IPv4Network, ipaddress.IPv6Network] | None = None,
                      ip_addresses: Union[tuple[ipaddress.IPv4Network | ipaddress.IPv6Network],
                                          list[ipaddress.IPv6Address | ipaddress.IPv6Address]] = []):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        snd_lst = set(ip_addresses)
        snd_data = cls.jy_cmd_bytes['reboot' if is_reboot else 'shutdown']
        snd_bytes = pack("%dB\0" % (len(snd_data)), *snd_data)
        if ip_network:
            snd_lst.update((ip_network.broadcast_address,))
        length = 0
        for ip_addr in snd_lst:
            length += sock.sendto(snd_bytes, (str(ip_addr), port))
        return length

    @staticmethod
    def _hl_split_once(char):
        if ord(char) > 0xff:
            return int(bin(ord(char) << 8)[2:][8:], 2) >> 8, int(bin(ord(char) >> 8)[2:], 2)
        else:
            return ord(char), 0

    @classmethod
    def _hl_build(cls, string: str):
        hl_lst = []
        for char in string:
            hl_lst += cls._hl_split_once(char)
        return hl_lst