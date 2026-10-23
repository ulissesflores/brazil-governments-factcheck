# Cliente minimo (stdlib) do Qlik Engine JSON-RPC sobre WebSocket, para o Painel Estatistico de Pessoal (acesso publico, anonimo).
# Uso de rede: SO na aquisicao. A resposta bruta de cada chamada e gravada em bruto/pep/ e entra na cadeia de hash.
import base64, json, os, socket, ssl, struct, sys

class WS:
    def __init__(self, host, path, origin, cookie=""):
        raw = socket.create_connection((host, 443), timeout=60)
        self.s = ssl.create_default_context().wrap_socket(raw, server_hostname=host)
        key = base64.b64encode(os.urandom(16)).decode()
        req = ("GET %s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
               "Sec-WebSocket-Version: 13\r\nOrigin: %s\r\nUser-Agent: Mozilla/5.0\r\n%s\r\n") % (path, host, key, origin, ("Cookie: %s\r\n" % cookie) if cookie else "")
        self.s.sendall(req.encode())
        hdr = b""
        while b"\r\n\r\n" not in hdr:
            c = self.s.recv(4096)
            if not c:
                break
            hdr += c
        self.head, _, rest = hdr.partition(b"\r\n\r\n")
        self.buf = rest
        if b" 101 " not in self.head.split(b"\r\n")[0]:
            raise RuntimeError("handshake falhou: " + self.head.decode(errors="replace")[:300])

    def _need(self, n):
        while len(self.buf) < n:
            c = self.s.recv(65536)
            if not c:
                raise EOFError
            self.buf += c

    def send(self, txt):
        d = txt.encode()
        mask = os.urandom(4)
        n = len(d)
        h = b"\x81"
        if n < 126:
            h += bytes([0x80 | n])
        elif n < 65536:
            h += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            h += bytes([0x80 | 127]) + struct.pack(">Q", n)
        self.s.sendall(h + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(d)))

    def recv(self):
        out = b""
        while True:
            self._need(2)
            b1, b2 = self.buf[0], self.buf[1]
            n = b2 & 0x7F
            off = 2
            if n == 126:
                self._need(4); n = struct.unpack(">H", self.buf[2:4])[0]; off = 4
            elif n == 127:
                self._need(10); n = struct.unpack(">Q", self.buf[2:10])[0]; off = 10
            self._need(off + n)
            payload = self.buf[off:off + n]
            self.buf = self.buf[off + n:]
            op = b1 & 0x0F
            if op == 9:
                continue
            if op == 8:
                raise EOFError("close")
            out += payload
            if b1 & 0x80:
                return out.decode()

class Engine:
    def __init__(self, host, appid, prefix="/", cookie="", query=""):
        self.ws = WS(host, "%sapp/%s%s" % (prefix, appid, query), "https://" + host, cookie)
        self.i = 0
        self.log = []

    def call(self, handle, method, params):
        self.i += 1
        msg = {"jsonrpc": "2.0", "id": self.i, "handle": handle, "method": method, "params": params}
        self.ws.send(json.dumps(msg))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.i:
                self.log.append((msg, r))
                return r
