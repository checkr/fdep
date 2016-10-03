"""Read and write fdep configuration."""
import yaml
import os


class FdepConfig(object):
    """Serialize and unserialize fdep configuration file."""

    def __init__(self, config_dict):
        self.config = config_dict

    def save(self, path):
        with open(path, 'w') as f:
            f.write(yaml.dump(self.config, default_flow_style=False))

    @classmethod
    def load(cls, path):
        with open(path) as f:
            return FdepConfig(yaml.load(f.read()))

    @classmethod
    def find_local_config(cls):
        paths_to_search = set()
        current_path = ['.']

        while True:
            path = os.path.abspath(
                os.path.join(*current_path)
            )
            if path in paths_to_search:
                break

            paths_to_search.add(path)
            current_path.append('..')

        sorted_paths = sorted(
            list(paths_to_search),
            key=lambda x: -len(x)
        )

        for path in sorted_paths:
            config_path = os.path.join(path, 'fdep.yml')
            if os.path.exists(config_path):
                return config_path
        return None
