"""Read and write fdep configuration."""
import os

import yaml


class FdepEntryDictionary(object):

    def __init__(self, _dict):
        self._dict = _dict

    def __getitem__(self, key):
        """Get the item in a coherent manner.

        We have two types of entries: just a string type, and a dictionary type.
        We convert anything into the new dictionary type.
        e.g. "http://foo.bar" => {"source": "http://foo.bar"}
        """
        obj = self._dict[key]
        if isinstance(obj, str):
            obj = dict(source=obj)
        return obj

    def __setitem__(self, key, value):
        """Set the item in order to make the config file prettier.

        If the object only has the key "source", we convert it into a string.
        """
        if set(value.keys()) == {'source'}:
            value = value['source']
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def items(self):
        return [(k, self[k]) for k in self._dict.keys()]

    def get(self, key):
        if key not in self._dict:
            return None
        return self[key]


class FdepConfig(object):
    """Serialize and unserialize fdep configuration file."""

    def __init__(self, root_path, config_dict):
        """Initialize a fdep configuration object with a dictionary."""
        self.root_path = root_path
        self._config = config_dict

    def save(self, path=None):
        """Save a fdep configuration object into a YAML file."""
        if path is None:
            path = os.path.join(self.root_path, 'fdep.yml')
        with open(path, 'w') as f:
            f.write(yaml.dump(self._config, default_flow_style=False))

    def __getitem__(self, key):
        """Get the item in a coherent manner.

        We have two types of entries: just a string type, and a dictionary type.
        We convert anything into the new dictionary type.
        e.g. "http://foo.bar" => {"source": "http://foo.bar"}
        """
        return FdepEntryDictionary(self._config[key])

    def __setitem__(self, key, value):
        """Set the item in order to make the config file prettier.

        If the object only has the key "source", we convert it into a string.
        """
        if not isinstance(value, FdepEntryDictionary):
            raise Exception("An FdepEntryDictionary object is expected.")
        self._config[key] = value._dict

    def __delitem__(self, key):
        del self._config[key]

    def get(self, key):
        """Implement an exception-free getter."""
        if key not in self._config:
            return None
        return self[key]

    @classmethod
    def load(cls, path):
        """Load a fdep configuration from a YAML file."""
        if not os.path.exists(path):
            return None

        with open(path) as f:
            root_path = os.path.dirname(path)
            return FdepConfig(root_path, yaml.load(f.read()))

    @classmethod
    def find_root_path(cls, current_path='.'):
        """Find a relative path that has the configuration."""
        paths_to_search = set()
        current_path = [current_path]

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

        # Search going down the tree
        for path in sorted_paths:
            config_path = os.path.join(path, 'fdep.yml')
            if os.path.exists(config_path):
                return path
        return None
