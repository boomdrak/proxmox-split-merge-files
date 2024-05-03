from typing import Any

def get_object_from_array_by_value(array, obj_key_value: dict) -> Any:
    obj_key = list(obj_key_value.keys())[0]
    obj_value = list(obj_key_value.values())[0]
    for item in array:
        class_attr = getattr(item, obj_key)
        if class_attr == obj_value:
            return item
    return None
