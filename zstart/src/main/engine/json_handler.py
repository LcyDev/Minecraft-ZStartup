import yaml, tomllib

from utils import useful

class BaseJSON:
    """Base class for handling JSON serialization, encryption, and optional binary conversion."""

    def __init__(self, class_obj: object, file_path: str):
        self.class_obj = class_obj
        self.class_data = dataclasses.asdict(class_obj) if dataclasses.is_dataclass(class_obj) else None
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.file = io.open(file_path, "w+")  # Open file for reading and writing

    def __enter__(self):  # For context manager usage
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_file()

    def close_file(self):
        """Closes the file handle if it's open."""
        if self.file:
            self.file.close()
            self.file = None

    def load_file(self):
        """Reads data from file."""
        try:
            raw_data: dict
            if self.file.endswith('.toml'):
                raw_data = tomllib.load(self.file)
            elif self.file.endwith('.yml') or self.file.endswith('.yaml'):
                raw_data = yaml.safe_load(self.file)
            else:
                return
            useful.normalize_keys(raw_data)
            useful.update_dict(self.class_data, raw_data)
            self.on_loaded_file()
        except (ValueError, EOFError, NameError) as e:
            print(f"Error loading file: {e}")

    def on_loaded_file(self):
        """Subclasses should implement logic to perform actions after data is loaded."""
        raise NotImplementedError("Subclasses must implement on_loaded_file()")

    def update_global(self):
        """Updates global variables based on loaded data. Implementation varies by subclass."""
        raise NotImplementedError("Subclasses must implement update_global()")