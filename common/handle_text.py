import os
import sys
import argparse
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from common import general_utils as utils
from common import data_utils
from common import df_utils
from common import konlpy_utils


_this_folder_ = os.path.dirname(os.path.abspath(__file__))
_this_basename_ = os.path.splitext(os.path.basename(__file__))[0]


def main(args):
    ini = utils.get_ini_parameters(args.ini_fname)

    if args.op_mode == 'REFINE_TEXTLINE':
        ini = ini['REFINE_TEXTLINE']
        utils.folder_exists(ini['in_path'], create_=True)
        utils.folder_exists(ini['out_path'], create_=True)

        csv_fnames = sorted(utils.get_filenames(ini['in_path'], extensions=utils.CSV_EXTENSIONS))
        for idx, csv_fname in enumerate(csv_fnames):
            print(" [REFINE_TEXTLINE] # Processing {} ({:d}/{:d})".format(csv_fname, (idx + 1), len(csv_fnames)))
            dir_name, core_name, ext = utils.split_fname(csv_fname)
            rst_fname = 'refine_' + core_name + ext

            text_list = data_utils.read_csv_file(csv_fname)
            print("Text list size : {}".format(len(text_list)))

            uniq_texts = data_utils.extract_unique_list(text_list)
            print("Unique text list size : {}".format(len(uniq_texts)))

            # Save refined csv file.
            data_utils.write_list_to_csv(uniq_texts, os.path.join(ini['out_path'], rst_fname))
            pass

    elif args.op_mode == 'EXTRACT_WORD':
        ini = ini['EXTRACT_WORD']
        utils.folder_exists(ini['in_path'], create_=True)
        utils.folder_exists(ini['out_path'], create_=True)

        csv_fnames = sorted(utils.get_filenames(ini['in_path'], extensions=utils.CSV_EXTENSIONS))
        for idx, csv_fname in enumerate(csv_fnames):
            print(" [EXTRACT_WORD] # Processing {} ({:d}/{:d})".format(csv_fname, (idx + 1), len(csv_fnames)))
            dir_name, core_name, ext = utils.split_fname(csv_fname)
            rst_fname = 'extract_' + core_name + '.txt'
            rst_fpath = os.path.join(ini['out_path'], rst_fname)

            # Tokenize by OKT.
            text_df = pd.read_csv(csv_fname, names=['TEXTS'])
            token_modes = konlpy_utils.TokenMode
            text_df['nouns'] = text_df['TEXTS'].apply(konlpy_utils.tokeniz_nouns, mode=token_modes.komoran)

            # Merge to one series.
            merge_nouns = df_utils.merge_values_in_series(text_df['nouns'])

            # Remove duplicates.
            uniq_nouns = merge_nouns.drop_duplicates().reset_index(drop=True)

            # remove len(value) == 1
            remove_nouns = uniq_nouns[uniq_nouns.apply(lambda x: len(x) > 1)].reset_index(drop=True)

            # Save word dict.
            print(" [EXTRACT_WORD] # Saving at {}".format(rst_fpath))
            remove_nouns.to_csv(rst_fpath, index=False, header=None)

        pass

    return True

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--op_mode", required=True, choices=['REFINE_TEXTLINE', 'EXTRACT_WORD'], help="operation mode")
    parser.add_argument("--ini_fname", required=True, help="System code ini filename")

    args = parser.parse_args(argv)

    return args

SELF_TEST_ = True
OP_MODE = 'EXTRACT_WORD' # REFINE_TEXTLINE / EXTRACT_WORD / ...
INI_FNAME = _this_basename_ + ".ini"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        if SELF_TEST_:
            sys.argv.extend(["--op_mode", OP_MODE])
            sys.argv.extend(["--ini_fname", INI_FNAME])
        else:
            sys.argv.extend(["--help"])

    main(parse_arguments(sys.argv[1:]))