import os
import dataclasses
import ujson, yaml, tomllib
from pathlib import Path

from instances import configData, ConfigData

class DataHandler:
    @staticmethod
    def write_file(file_path: str | Path, data):
        try:
            is_bytes = isinstance(data, bytes)
            mode = 'wb' if is_bytes else 'w'
            with open(file_path, mode) as f:
                f.write(data)
            return True
        except IOError:
            print(f"Failed to write file {file_path}, Check that the file is writable.")
        except Exception as e:
            print(f"An unexpected error ocurred while writing to file. Error: {e}")

    @staticmethod
    def read_file(file_path: str | Path, is_bytes: bool) -> str | bytes:
        try:
            mode = 'rb' if is_bytes else 'r'
            with open(file_path, mode) as f:
                return f.read()
        except FileNotFoundError:
            print(f"Failed to read file {file_path}, Check that the file exists.")
        except PermissionError:
            print(f"Failed to read file {file_path}, Check permissions.")
        except IOError:
            print(f"Failed to read file {file_path}, Check that the file is readable.")
        except Exception as e:
            print(f"An unexpected error ocurred while reading file. Error: {e}")

    @staticmethod
    def _serialize_json(data) -> str | None:
        try:
            return ujson.dumps(data, indent=4)
        except TypeError as e:
            print(f"Failed to serialize data to JSON. Ensure that all data types are serializable. Error: {e}")
        except OverflowError as e:
            print(f"Failed to serialize data to JSON. Data is too large to be serialized. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while serializing data to JSON. Error: {e}")

    @staticmethod
    def _deserialize_json(data: str | bytes):
        try:
            return ujson.loads(data)
        except ValueError as e:
            print(f"Failed to deserialize data from JSON. Ensure that the data is a valid JSON string. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while deserializing data from JSON. Error: {e}")

class BaseJSON:
    """Base class for handling JSON serialization, and optionally encrypt and pickle."""

    def __init__(self, class_obj: object, file_path: str):
        self.class_obj = class_obj
        self.serialize_json = True
        self.class_data = dataclasses.asdict(class_obj) if dataclasses.is_dataclass(class_obj) else class_obj.__dict__
        # Ensure directory exists
        if file_dir := os.path.dirname(file_path):
            os.makedirs(file_dir, exist_ok=True)
        self.file_path = Path(file_path)

    def save_file(self):
        """Serializes data, optionally encrypts and converts to binary, and writes to file."""
        try:
            if self.serialize_json:
                data = DataHandler._serialize_json(self.class_data)
                if data is None: return

            Result = DataHandler.write_file(self.file_path, data)
            if Result:
                self.on_saved_file()
        except Exception as e:
            print(f"Unexpected error saving data: {e}")

    def load_file(self):
        """Reads data from file, optionally decrypts and converts from binary, and deserializes."""
        try:
            data = DataHandler.read_file(self.file_path, is_bytes=False)
            if data is None: return

            if self.serialize_json:
                data = DataHandler._deserialize_json(data)
                if data is None: return

            self.class_data = data
            self.on_loaded_file()
        except Exception as e:
            print(f"Unexpected error loading data: {e}")

    def on_saved_file(self):
        """Subclasses should implement logic to perform actions after data is saved."""
        raise NotImplementedError("Subclasses must implement on_saved_file()")

    def on_loaded_file(self):
        """Subclasses should implement logic to perform actions after data is loaded."""
        raise NotImplementedError("Subclasses must implement on_loaded_file()")

    def update_global(self):
        """Updates global variables based on loaded data. Implementation varies by subclass."""
        raise NotImplementedError("Subclasses must implement update_global()")

class ConfigJSON(BaseJSON):
    """Handles JSON operations for configuration data."""

    def __init__(self, file_path: str, config_obj: ConfigData = configData, **kwargs):
        super().__init__(config_obj, file_path, **kwargs)

    def on_saved_file(self):
        ...

    def on_loaded_file(self):
        self.update_global()

    def update_global(self):
        """Updates the global Config object with loaded data."""
        global configData
        configData.__dict__.update(**self.class_data)