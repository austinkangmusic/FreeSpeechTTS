def extract_values(obj, keys_to_find):
    extracted = {}
    if isinstance(obj, dict):
        for key in keys_to_find:
            if key in obj:
                extracted[key] = obj[key]
    elif hasattr(obj, "__dict__"):
        for key in keys_to_find:
            if hasattr(obj, key):
                extracted[key] = getattr(obj, key)
    
    # Return the values in the order of keys_to_find if they exist
    return tuple(extracted.get(key, None) for key in keys_to_find)
