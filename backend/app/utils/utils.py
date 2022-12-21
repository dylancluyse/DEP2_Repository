

def map_result_and_description(result, description):
    column_names = [column_description[0] for column_description in description]
    res = {k: v for k, v in zip(column_names, result[0])}
    return res

