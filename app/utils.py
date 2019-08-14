"""Utils module."""

def parse_with_type(value):
    """Take text value and return tuple (type, parsed value)"""
    if value is None: return None, None
    try:
        return int, int(value) 
    except ValueError as ex:
        try:
            return float, float(value)
        except ValueError as ex:
            return str, str(value) 
