def remove_keys_from_dict_list(dict_list, keys_to_remove):
    """
    Remove a set of keys from each dictionary in a list, if those keys exist.

    Args:
        dict_list (list of dict): List of dictionaries from which keys should be removed.
        keys_to_remove (iterable): Iterable of keys that should be removed from the dictionaries.

    Returns:
        list of dict: A new list of dictionaries with specified keys removed.
    """
    # Create a new list of dictionaries, where each dictionary has the undesired keys removed
    return [{k: v for k, v in d.items() if k not in keys_to_remove} for d in dict_list]


class APIRequestError(Exception):
    """Custom exception for API request errors."""

    pass
