from fdep.servers import RPCServer

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    from xmlrpc.server import SimpleXMLRPCServer


class XMLRPCServer(RPCServer):
    """Implement a XMLRPC server."""

    def register_functions(self, func_pairs):
        self.func_pairs = func_pairs

    def serve_forever(self, **kwargs):
        server = SimpleXMLRPCServer(('0.0.0.0', kwargs['port']))

        for name, func in self.func_pairs:
            server.register_function(func, name=name)
        server.serve_forever()
