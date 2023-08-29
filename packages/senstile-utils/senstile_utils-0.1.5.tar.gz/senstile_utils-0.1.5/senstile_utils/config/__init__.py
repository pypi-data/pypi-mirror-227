import os
import toml
import logging

class Config:
    """
    The Config class provides a way to load and access application configurations.

    Attributes:
        - DEFAULT_ENV (str): The default environment if none is specified.
        - cache (dict): A cache to store previously accessed configuration values.

    Usage:
        config = Config()
        db_host = config.get("database.host")

    Note:
        The class uses the Singleton pattern ensuring that only one configuration instance exists.
        It uses the `PYTHON_ENV` environment variable to determine which configuration to load.
    """
    _instance = None
    _initialized = False
    DEFAULT_ENV = 'local'
    cache = dict()

    def __new__(cls, *args, **kwargs):
        """Returns the single instance of Config, creating it if necessary."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self, config_path_dir=None):
        if Config._initialized:
            return
        env = os.environ.get('PYTHON_ENV', Config.DEFAULT_ENV)
        config_path = None
        if config_path_dir is None:
            config_path_dir = os.getcwd()

        if env == Config.DEFAULT_ENV:
            config_path = os.path.join(config_path_dir, f'config.toml')
        else:
            config_path = os.path.join(config_path_dir,  f'config.{env}.toml')

        logging.info(f"CONFIG PATH: {config_path}")
        print(f"CONFIG PATH: {config_path}")
        schema_path = os.path.join(config_path_dir, "config.schema.toml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file '{config_path}' not found.")

        if not os.path.exists(schema_path):
            self.schema = dict()
        else:
            with open(schema_path, 'r') as s:
                self.schema = toml.load(s)

        with open(config_path, 'r') as f:
            self.data = toml.load(f)

        self._validate_schema()

        Config._initialized = True

    def _validate_schema(self):
        """
        Validates the loaded configuration data against the provided schema.

        Raises:
            ValueError: If the configuration data does not match the schema.
        """
        def validate(node, schema, key_path=[]):
            if isinstance(schema, dict):
                if not isinstance(node, dict):
                    return False
                for key, value in schema.items():
                    key_path.append(key)
                    if key not in node:
                        key_path_str = ".".join(key_path)
                        raise ValueError(
                            f"Configuration does not match the provided schema. The key = \"{key_path_str}\" is not present in the config file")
                    if not validate(node[key], value, key_path):
                        return False
                    key_path.pop(-1)
            elif isinstance(schema, list):
                if len(schema) == 0:
                    raise ValueError(
                        f"The schema= {schema} must contains at least one data validator")
                if not isinstance(node, list):
                    return False
                for i in range(len(node)):
                    data = node[i]
                    key_path.append(i)
                    if not validate(data, schema[0], key_path):
                        return False
                    key_path.pop(-1)
            else:
                type_mapping = {
                    'int': int,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'bool': bool
                }
                expected_type = type_mapping.get(schema, None)
                if not expected_type:
                    raise ValueError(f"Unknown schema type: {schema}")
                if not isinstance(node, expected_type):
                    key_path_str = ".".join(key_path)
                    raise ValueError(
                        f"The type of \"{key_path_str}\" is not of type {expected_type}")
            return True

        if not validate(self.data, self.schema):
            raise ValueError(
                "Configuration does not match the provided schema.")

    def get(self, initial_key: str, default=None):
        """
        Retrieves a value from the configuration using a dot-separated key.

        Args:
            - initial_key (str): The dot-separated key, e.g., "database.host".
            - default: The default value to return if the key is not found.

        Returns:
            The configuration value corresponding to the provided key, or the default value.

        Raises:
            RuntimeError: If the key is not found in the configuration and no default value is provided.
        """
        if initial_key in Config.cache:
            return Config.cache.get(initial_key)
        sub_keys = [key.strip() for key in initial_key.split(".")
                    if key.strip() is not None]
        data_value = self.data
        for key in sub_keys:
            if not (key in data_value):
                if default is None:
                    raise RuntimeError(
                        f"The key \"{initial_key}\" is not present in config data")
                else:
                    return default
            data_value = data_value[key]
        Config.cache[initial_key] = data_value
        return data_value

    @staticmethod
    def clear_instance():
        Config._instance = None
        Config._initialized = False
        Config.cache = dict()
