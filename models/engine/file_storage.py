import json
from models.base_model import BaseModel
from models.engine.custom_exceptions import (GetClassException, GetInstanceException)


class FileStorage:
    """Class for managing file storage and retrieval"""

    __file_path: str = "file.json"  # Path to the json file
    __objects: dict = {}   # Will store all objects by <class name>.id
    models = [
        "BaseModel"
    ]

    def all(self):
        """Returns the dictionary <__objects>"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in <__objects> the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves the dictionary <__objects> to the file <__file_path>"""
        with open(FileStorage.__file_path, "w") as f:
            f.write(
                json.dumps(
                    {
                        key: value.to_dict() for key, value in self.__objects.items()
                    }
                )
            )

    def reload(self):
        """Loads the dictionary <__objects> from the file <__file_path>"""
        # Try opening the file and read it
        # if an error occurred, do nothing
        try:
            with open(FileStorage.__file_path, "r") as f:
                # Get all the objects from the file <__file_path>
                objects = json.loads(f.read())

                FileStorage.__objects = {
                    key: eval(
                        obj["__class__"]
                    )(**obj) for key, obj in objects.items()
                }
        except Exception as e:   # Unable to open the file
            pass
    
    def get(self, model, id):
        """Gets an element by ID"""
        if model not in FileStorage.models:
            raise GetClassException(model)
        
        key = f"{model}.{id}"
        try:
            return FileStorage.__objects[key]
        except KeyError:
            raise GetInstanceException(id, model)