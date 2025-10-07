from .storage import Storage
from .json_storage import JsonStorage
from .pickle_storage import PickleStorage

class StorageFactory:

    def get_storage(filepath: str) -> Storage:

        filepath_lower = filepath.lower()

        if filepath_lower.endswith('.json'):
            return JsonStorage(filepath)
        
        elif filepath_lower.endswith('.pkl') or filepath_lower.endswith('.pickle'):
            return PickleStorage(filepath)
            
        # elif filepath_lower.endswith('.db') or filepath_lower.endswith('.sqlite') or filepath_lower.endswith('.sqlite3'):
        #     return SQLiteStorage(filepath)
            
        else:
            raise ValueError(f"Unsupported filetype: {filepath}.\nSupported extensions: .json, .pkl, .db, .sqlite.")