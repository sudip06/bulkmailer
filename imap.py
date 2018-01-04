import ssl

from socks import create_connection
from socks import PROXY_TYPE_SOCKS4
from socks import PROXY_TYPE_SOCKS5
from socks import PROXY_TYPE_HTTP

from imaplib import IMAP4
from imaplib import IMAP4_PORT
from imaplib import IMAP4_SSL_PORT

class SocksIMAP4(IMAP4):
    """
    IMAP service trough SOCKS proxy. PySocks module required.
    """

    PROXY_TYPES = {"socks4": PROXY_TYPE_SOCKS4,
                   "socks5": PROXY_TYPE_SOCKS5,
                   "http": PROXY_TYPE_HTTP}

    def __init__(self, host, port=IMAP4_PORT, proxy_addr=None, proxy_port=None,
                 rdns=True, username=None, password=None, proxy_type="socks5"):

        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.rdns = rdns
        self.username = username
        self.password = password
        self.proxy_type = SocksIMAP4.PROXY_TYPES[proxy_type.lower()]

        IMAP4.__init__(self, host, port)

    def _create_socket(self):
        return create_connection((self.host, self.port), proxy_type=self.proxy_type, proxy_addr=self.proxy_addr,
                                 proxy_port=self.proxy_port, proxy_rdns=self.rdns, proxy_username=self.username,
                                 proxy_password=self.password)


class socksIMAP4SSL(SocksIMAP4):

    def __init__(self, host='', port=IMAP4_SSL_PORT, keyfile=None, certfile=None, ssl_context=None, proxy_addr=None,
                 proxy_port=None, rdns=True, username=None, password=None, proxy_type="socks5"):

        if ssl_context is not None and keyfile is not None:
                raise ValueError("ssl_context and keyfile arguments are mutually "
                                 "exclusive")
        if ssl_context is not None and certfile is not None:
            raise ValueError("ssl_context and certfile arguments are mutually "
                             "exclusive")

        self.keyfile = keyfile
        self.certfile = certfile
        if ssl_context is None:
            ssl_context = ssl._create_stdlib_context(certfile=certfile,
                                                     keyfile=keyfile)
        self.ssl_context = ssl_context

        SocksIMAP4.__init__(self, host, port, proxy_addr=proxy_addr, proxy_port=proxy_port,
                            rdns=rdns, username=username, password=password, proxy_type=proxy_type)

    def _create_socket(self):
        sock = SocksIMAP4._create_socket(self)
        server_hostname = self.host if ssl.HAS_SNI else None
        return self.ssl_context.wrap_socket(sock, server_hostname=server_hostname)

    def open(self, host='', port=IMAP4_PORT):
        SocksIMAP4.open(self, host, port)


if __name__ == "__main__":

    email = "test@esp.com"
    password = "secret_password"
    imap_server = "imap.esp.com"
    imap_port = 993

    proxy_addr = "100.42.161.8"
    proxy_port = 45554
    proxy_type = "socks5"

    mailbox = socksIMAP4SSL(host=imap_server, port=imap_port,
                            proxy_addr=proxy_addr, proxy_port=proxy_port, proxy_type=proxy_type)
    mailbox.login(email, password)

    typ, data = mailbox.list()
    print(typ)
    print(data)
