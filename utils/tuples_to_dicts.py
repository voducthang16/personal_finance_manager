def tuples_to_dicts(tuples, columns):
    return [dict(zip(columns, row)) for row in tuples]
