class Integration(object):
    """Implement hooks for third party integrations."""

    def capture_exception(self, exc):
        pass

    def before_function(self, func_name, args):
        pass

    def after_function(self, func_name, args, result):
        pass
