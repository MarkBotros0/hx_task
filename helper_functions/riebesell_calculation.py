import math

def riebesell(riebesell_base_limit, riebesell_z, x):
    ratio = x / riebesell_base_limit
    log_value = math.log(1 + riebesell_z, 2)
    return ratio ** log_value