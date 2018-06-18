"""Implement a simple XMLRPC server."""
from base64 import b64decode

import six
from fdep.servers import RPCServer

from six.moves.xmlrpc_server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


class XMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    """Implement a simple basic auth."""
    username = None
    password = None
    temp_password = None

    def authenticate(self, headers):
        auth = headers.get('Authorization')
        try:
            (basic, _, encoded) = auth.partition(' ')
        except:
            return False

        assert basic == 'Basic', 'Only basic authentication supported'

        encodedByteString = encoded.encode()
        decodedBytes = b64decode(encodedByteString)
        decodedString = decodedBytes.decode()
        (username, _, password) = decodedString.partition(':')
        if username == self.__class__.username and\
                (password == self.__class__.password or\
                    self.__class__.temp_password is not None and password == self.__class__.temp_password):
            return True
        else:
            return False

    @classmethod
    def set_account(cls, username, password, temp_password):
        cls.username = username
        cls.password = password
        cls.temp_password = temp_password

    @classmethod
    def should_authenticate(cls):
        return cls.username and cls.password

    def parse_request(self):
        if SimpleXMLRPCRequestHandler.parse_request(self):
            if not XMLRPCRequestHandler.should_authenticate():
                return True

            if self.authenticate(self.headers):
                return True
            else:
                self.send_response(401, 'Authentication failed')
                self.send_header('WWW-Authenticate', 'Basic realm="Fdep XMLRPC Server"')
                self.end_headers()
        return False


class XMLRPCServer(RPCServer):
    """Implement a XMLRPC server."""

    def register_functions(self, func_pairs):
        self.func_pairs = func_pairs

    def serve_forever(self, **kwargs):

        if kwargs.get('username') and kwargs.get('password'):
            XMLRPCRequestHandler.set_account(kwargs['username'], kwargs['password'], kwargs.get('temp_password'))

        self.server = SimpleXMLRPCServer(('0.0.0.0', kwargs['port']), requestHandler=XMLRPCRequestHandler)

        for name, func in self.func_pairs:
            self.server.register_function(
                self.wrap_function(name, func),
                name=name
            )
        self.server.register_multicall_functions()

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

    def shutdown(self):
        if not getattr(self, 'server', None):
            raise Exception("The server has never been started.")
        self.server.shutdown()
        self.server.server_close()
