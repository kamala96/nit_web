def get_short_description(obj, field_name='description', max_length=60):
    """
    Truncates the specified field of the given object to a specified length.
    """
    field_value = getattr(
        obj, field_name, '')  # Get the value of the specified field
    if len(field_value) > max_length:
        return field_value[:max_length] + '...'
    return field_value
