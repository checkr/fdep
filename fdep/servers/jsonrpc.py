"""Implement a simple JSONRPC server."""
from __future__ import absolute_import

from base64 import b64decode

from fdep.servers import RPCServer
from jsonrpc import JSONRPCResponseManager, dispatcher

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class JSONRPCRequestHandler(BaseHTTPRequestHandler):
    """Implement JSON RPC request handler."""
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

    def is_authenticated(self):
        if not JSONRPCRequestHandler.should_authenticate():
            return True

        if self.authenticate(self.headers):
            return True
        else:
            self.send_response(401, 'Authentication failed')
            self.send_header('WWW-Authenticate', 'Basic realm="Fdep JSONRPC Server"')
            self.end_headers()

    def do_POST(self):
        if not self.is_authenticated():
            return

        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len)
        response = JSONRPCResponseManager.handle(body, dispatcher)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.json.encode('utf-8'))


class JSONRPCServer(RPCServer):
    """Implement a JSONRPC server."""

    def register_functions(self, func_pairs):
        for name, func in func_pairs:
            dispatcher[name] = self.wrap_function(name, func)

    def serve_forever(self, **kwargs):

        if kwargs.get('username') and kwargs.get('password'):
            JSONRPCRequestHandler.set_account(kwargs['username'], kwargs['password'], kwargs.get('temp_password'))

        self.server = HTTPServer(('0.0.0.0', kwargs['port']), JSONRPCRequestHandler)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

    def shutdown(self):
        if not getattr(self, 'server', None):
            raise Exception("The server has never been started.")
        self.server.shutdown()
        self.server.server_close()
