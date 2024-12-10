def filter_none_params(params: dict) -> dict:
    return {key: val for key, val in params.items() if val is not None}
