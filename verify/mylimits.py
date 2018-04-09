from verify import verify_data_str

col_A = {
    'max':10,
    'min':2,
}

col_B = {
    "length_max":13,
}

col_C ={
    "length_max":6,
    "length_min":2,
}

col_D = {
    'choices':['A','B','C'],
}

limits = [col_A,col_B,col_C,col_D,col_D,col_D,col_D,col_D]
filters = [verify_data_str,] * 8
cols_sum = 8
verify_dir = '.'
headline_row_num = 1