import codecs
import csv
import json
import os
import random
import re
import statistics
import sys
import operator


DIV_0_ERR = "#DIV/0!"
INFINITY = 999999.0


def read_csv_file(csv_file, delimiter=','):
    """ Read csv file
    :param csv_file:
    :param delimiter:
    :return:
    """
    mtx = []
    with open(csv_file, "r", encoding='utf-8-sig') as f:
        for row in csv.reader(f, delimiter=delimiter):
            row = [x.strip() if x != DIV_0_ERR else "" for x in row]
            mtx.append(row)
    return mtx


def read_csv_file_as_dict(file_path):
    data_list = read_csv_file(file_path)
    trans_data_list = transpose_list(data_list)
    d = {}
    for line in trans_data_list:
        d[line[0]] = line[1:]
    return d


def list_to_dict(data_list, top_key=True):
    if top_key:
        data_list = transpose_list(data_list)
    d = {}
    for row in data_list:
        d[row[0]] = row[1:]
    return d


def dict_to_list_list(data_dict):
    l = []
    for key, val in data_dict.items():
        l.append([key] + val)
    return l


def dict_to_list(data_dict, key=True, val=True):
    key_li = []
    val_li = []
    for dict_key, dict_val in data_dict.items():
        key_li.append(dict_key)
        val_li.append(dict_val)

    if key and val:
        return key_li, val_li
    elif key:
        return key_li
    elif val:
        return val_li


def dict_to_val_tuple(data_dict):
    t = ()
    for key, val in data_dict.items():
        t += (val,)
    return t


def convert_char_to_num(char):
    """Convert one-digit alphabet character to number.
    :param char:
    :return:
    """
    base = 26  # 26 letters from A to Z
    digit = 0
    pos = 0
    for c in reversed(char):
        val = ord(c) - ord('A') + 1
        pos += pow(base, digit) * val
        digit += 1

    return pos - 1


def crop_mtx(csv_mtx, start_pos, end_pos):
    """Crop the rectangle shaped cells from  csv format list
    :param csv_mtx:
    :param start_pos:
    :param end_pos:
    :return:
    """
    roi_mtx = []
    for yi in range(end_pos[0], end_pos[1] + 1):
        roi_mtx.append(csv_mtx[yi][start_pos[0]:start_pos[1] + 1])
    return roi_mtx


def transpose_list(in_list):
    try:
        return list(map(list, zip(*in_list)))
    except TypeError:
        return in_list


def get_col_list(list_obj, n):
    return list(map(operator.itemgetter(n), list_obj))


def write_list_to_csv(dataset, filepath, overwrite=False):
    if not filepath:
        return
    if not overwrite:
        post_fix = '-1'
        while os.path.exists(filepath):
            filepath = filepath.rsplit('.', 1)[0] + '-' + post_fix + '.' + filepath.rsplit('.', 1)[-1]
    with codecs.open(filepath, 'w', 'utf-8-sig') as f:
        for row_dat in dataset:
            f.write(','.join([str(x).replace(',', ' / ') for x in row_dat]) + '\n')


def write_list_to_separate_csv(dataset, var, filename, overwrite=False):
    dataset_dict = split_dataset_by_var(dataset, var)
    for dataset_key, dataset_val in dataset_dict.items():
        save_filename = filename.rsplit('.', 1)[0] + '-' + dataset_key + '.' + filename.rsplit('.', 1)[-1]
        write_list_to_csv(dataset_val, save_filename, overwrite=overwrite)


def is_json(my_json):
    try:
        json.loads(my_json)
    except ValueError:
        return False
    return True


def get_range_list(num_range, separator=',', range_separator='~'):

    enum_list = [val.strip() for val in num_range.split(separator)]
    try:
        while True:
            pos = enum_list.index(range_separator)
            if 0 < pos < len(enum_list):
                del enum_list[pos]
                enum_list = (enum_list[0:pos]
                             + [x for x in range(int(enum_list[pos - 1]) + 1, int(enum_list[pos]), 1)]
                             + enum_list[pos:])
    except ValueError:
        pass
    return [int(x) for x in enum_list]


def gen_db_row_dat(table_info, handler, server_mode='', quote=True):
    row_dat = {}
    var_name_list = [key for key, val in handler.vars.items()]
    # if server_mode == 'EST':
    #     first_removed_str = 'EVAL'
    #     second_removed_str = 'OUT'
    # elif server_mode == 'EVAL':
    #     first_removed_str = 'EST'
    #     second_removed_str = 'OUT_AI'
    # refined_var_name_list = [var_name for var_name in var_name_list if not first_removed_str + '_' in var_name
    #                                                                     if not second_removed_str + '_' in var_name]

    for info in table_info[1:]:
        key = info[0]
        if key not in var_name_list:
            continue
        try:
            if 'INT' in info[1].upper():
                row_dat[key] = str(int(handler.vars[key].val))
            elif 'FLOAT' in info[1].upper():
                row_dat[key] = str(float(handler.vars[key].val))
            else:
                if quote:
                    try: ##
                        row_dat[key] = str("'" + handler.vars[key].val + "'")
                    except AttributeError as e:
                        print("Attribute Error: data_lib - gen_db_row_dat: ", e)
                else:
                    row_dat[key] = str(handler.vars[key].val)
        except ValueError:
            row_dat[key] = 'NULL'
            pass
    return row_dat


def gen_row_dat(table_info, handler):
    row_dat = {}
    for info in table_info[1:]:
        key = info[0]
        # print(key)
        if 'int' in info[1]:
            row_dat[key] = str(int(handler.vars[key].val))
        elif 'float' in info[1]:
            row_dat[key] = str(float(handler.vars[key].val))
        else:
            row_dat[key] = str(handler.vars[key].val)
    return row_dat

def extract_unique_list(in_list):
    return [list(t) for t in set(tuple(element) for element in in_list)]

def extract_rows_from_table(dataset, col_names, fill_null=False):
    """ Extract rows from DB table.
    :param dataset:
    :param col_names:
    :return:
    """
    trans_dataset = transpose_list(dataset)
    rows = []
    if type(col_names).__name__ == 'str':
        col_names = [col_names]
    for col_name in col_names:
        if col_name in dataset[0]:
            idx = dataset[0].index(col_name)
            rows.append(trans_dataset[idx])
        else:
            if fill_null:
                null_list = [''] * (len(trans_dataset[0])-1)
                null_list = [col_name] + null_list
                rows.append(null_list)
            else:
                pass
    if len(col_names) == 1:
        return rows[0]
    else:
        return transpose_list(rows)


def extract_cols_from_table(dataset, col_names):
    """ Extract columns from DB table.
    :param dataset:
    :param col_names:
    :return:
    """
    trans_dataset = transpose_list(dataset)
    rows = []
    if type(col_names).__name__ == 'str':
        col_names = [col_names]
    for col_name in col_names:
        idx = dataset[0].index(col_name)
        rows.append(trans_dataset[idx])
    if len(col_names) == 1:
        return rows[0]
    else:
        return transpose_list(rows)


def get_col_from_table(dataset, ref_name, idx_array, tar_name):
    ref_idx = dataset[0].index(ref_name)
    tar_idx = dataset[0].index(tar_name)
    trans_dataset = transpose_list(dataset)
    arr = []
    for i in idx_array:
        # print(i)
        pos = trans_dataset[ref_idx].index(str(i))
        arr.append(trans_dataset[tar_idx][pos])

    return arr


def convert_db_to_dict(values, keys):
    db_dict = {}
    for idx in range(len(keys)):
        db_dict[keys[idx][0]] = values[idx]
    return db_dict


def parse_string_domain(str_domain):
    if not str_domain:
        return ''
    domain = [val.strip() for val in str_domain.split(',')]
    try:
        idx = domain.index('~')
        if len(domain[0]) >= 8:
            return "YYYYMMDD"
        if 0 < idx < len(domain):
            del domain[idx]
            non_numeric = re.sub("[0-9]", "", domain[0])
            #domain = [re.sub("[^0-9]", "", val) for val in domain]
            first_item = re.sub("[^0-9]", "", domain[0])
            last_item = re.sub("[^0-9]", "", domain[-1])
            for val in range(int(last_item)-1, int(first_item), -1):
                domain.insert(idx, non_numeric + str(val))
        return domain
    except ValueError:
        return domain


def is_class_name(obj, class_name):
    if obj.__class__.__name__ == class_name:
        return True
    return False


def get_average(val_list):
    try:
        return sum(val_list) / float(len(val_list))
    except TypeError:
        return -1


def get_stdev(val_list):
    try:
        return statistics.stdev(val_list)
    except TypeError:
        return -1


def get_variance(val_list):
    try:
        return statistics.variance(val_list)
    except TypeError:
        return -1


def separate_dataset_var_dict(dataset_dict, separator_var, domains):

    # dataset_dict = {'a':[1,2,3,4,5], 'b':[6,7,8,9,10]}
    # separator_var = 'a'
    # domains = [[1, 3], [2, 4, 5]]

    idx_list = []

    for domain in domains:
        idx_list.append([])
        for item in domain:
            indices = [i for i, val in enumerate(dataset_dict[separator_var]) if item == val]
            idx_list[len(idx_list)-1].extend(indices)

    separated_dataset_dict = {}

    for key, val_list in dataset_dict.items():
        separated_dataset_dict[key] = []
        for indices in idx_list:
            separated_dataset_dict[key].append([val_list[i] for i in indices])

    return separated_dataset_dict


def convert_var_dict_to_list(separated_dataset_dict):
    num = len(separated_dataset_dict[(list(separated_dataset_dict.keys())[0])])
    separated_dataset_list = [{} for i in range(num)]
    for key, val_list in separated_dataset_dict.items():
        for idx in range(num):
            separated_dataset_list[idx][key] = val_list[idx]

    return separated_dataset_list


def string_list_to_float_list(string_list):
    for i in range(len(string_list)):
        string_list[i] = float(string_list[i])


def remove_row(mtx, idx, val):
    some_list = []
    for row in mtx:
        if row[idx] != val:
            some_list.append(row)
    return some_list


def split_dataset_by_var(dataset, var):

    var_names = dataset[0]
    dataset = dataset[1:]

    dataset_dict = {}
    idx = var_names.index(var)
    for row_data in dataset:
        val = row_data[idx]
        val_num = pattern_op_num_dict[val]
        if val_num not in dataset_dict:
            dataset_dict[val_num] = [var_names]
        dataset_dict[val_num].append(row_data)

    # dataset_list = []
    # for _, new_dataset in dataset_dict.items():
    #     dataset_list.append(new_dataset)

    return dataset_dict


def replace_dataset_by_dict(dataset, key, replacement_dict, logger=None): # 2, 3, 4

    dim = [len(dataset), len(dataset[0])]

    del_list = []
    try:
        col_idx = dataset[0].index(key)
    except ValueError:
        return dataset

    for row_idx in range(1, len(dataset)):
        val = dataset[row_idx][col_idx]
        if val == '':
            continue

        dataset[row_idx][col_idx] = replacement_dict[val] if val in replacement_dict else del_list.append(row_idx)

    del_list = sorted(del_list, reverse=True)
    for idx in del_list:
        del dataset[idx]

    msg = "\n Processing replace dataset by dictionary : "
    msg += "{:d} x {:d} -> {:d} x {:d}".format(dim[0], dim[1], len(dataset), len(dataset[0]))
    if logger:
        logger.info(msg)

    return dataset


def get_columns_added_list(list_a, list_b, column_list, key_var):

    b_key_idx = list_b[0].index(key_var)
    idx_list = [list_b[0].index(column_name) for column_name in column_list]

    add_dict = {}
    for row_dat in list_b[1:]:
        add_dict[row_dat[b_key_idx]] = [row_dat[idx] for idx in idx_list]

    new_list = [list_a[0].extend(column_list)]
    a_key_idx = list_a[0].index(key_var)
    for row_dat in list_a[1:]:
        key = row_dat[a_key_idx]
        try:
            new_list.append(row_dat.extend(add_dict[key]))
        except KeyError:
            new_list.append(row_dat)

    return new_list