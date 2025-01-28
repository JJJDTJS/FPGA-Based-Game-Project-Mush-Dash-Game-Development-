import re

def var_names(filename: str) -> tuple[str, str]:
    # assets/xyz.123!1.png => xyz_123_1(_data)
    var_name = re.sub(r'[^a-zA-Z0-9_]', '_', filename.rsplit('.', 1)[0])
    data_var_name = var_name + '_data'
    return var_name, data_var_name
