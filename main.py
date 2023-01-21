import ipaddress

from jiyu_ptl import JiyuProtocol

# 向 192.168.0.0/24 网段广播 发送消息 Hello, World
JiyuProtocol.send_content("Hello, World!", ip_network=ipaddress.ip_network("192.168.0.0/24"))
