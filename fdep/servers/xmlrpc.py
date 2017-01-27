from fdep.servers import RPCServer


class XMLRPCServer(RPCServer):
    """Implement a XMLRPC server."""

    def register_functions(self, func_pairs):
        pass

    def serve_forever(self, **kwargs):
        pass
