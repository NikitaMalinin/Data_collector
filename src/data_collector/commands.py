import decimal

dict_result_dfs = {
    'Frame': {
        'Basis': None,
        'Stress': None,
        'Adjustment factors': None
    },
    'Stringer': {
        'Basis': None,
        'Stress': None,
        'Adjustment factors': None
    },
    'Skin': {
        'Basis': None,
        'Stress': None,
        'Adjustment factors': None
    }
}


def round_down(value):
    try:
        with decimal.localcontext() as ctx:
            d = decimal.Decimal(str(value))
            ctx.rounding = decimal.ROUND_DOWN
            return float(round(d, 4))
    except:
        return value


def get_key(dict, value):
    for k, v in dict.items():
        if v[1] == value:
            return k


def get_basis():
    return


def get_fatigue_stress():
    return


def get_adjustment_factors():
    return


def get_maintenance_tasks():
    return
