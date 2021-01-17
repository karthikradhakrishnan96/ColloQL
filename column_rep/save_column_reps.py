import argparse
import json
import os
import random
import zipfile
from tqdm import tqdm
from column_rep.column_encoders import ColumnEncoderSampler
from sqlova.utils.utils_wikisql import load_wikisql


def construct_args(parser):
    parser.add_argument("--data_root", default="./data/WikiSQL-1.1/data")
    parser.add_argument("--num_rows", type=int, default=99999999999)
    parser.add_argument("--out_root", default="./column_rep/outs_all_repeat")
    args = parser.parse_args()
    return args



def get_column_reps(tables):
    global num_sample # TODO: Fix this
    column_vectors = {}
    # batch
    samples_to_be_encoded = []
    sample_index = 0
    for idx in tqdm(tables):
        column_vectors[idx] = {}
        table = tables[idx]
        rows = table["rows"]
        for col_idx, header_name in enumerate((table["header"])):
            col = [x[col_idx] for x in rows]
            col = (col)
            sample = col if len(col) < num_sample else random.sample(col, num_sample)
            sample = [str(x) for x in sample]
            samples_to_be_encoded.append(sample)
            # vector = column_encoder.encode_sample([str(x) for x in sample])
            column_vectors[idx][header_name] = sample_index
            sample_index += 1
    encoded_samples = column_encoder.encode_batch(samples_to_be_encoded)
    for table_idx in column_vectors:
        table = column_vectors[table_idx]
        for header_name in table:
            sample_idx = table[header_name]
            table[header_name] = encoded_samples[sample_idx]
    return column_vectors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = construct_args(parser)
    path_main = args.data_root
    num_sample = args.num_rows
    # column_encoder = ColumnEncoder(batch_size=64)
    column_encoder = ColumnEncoderSampler(batch_size=64)
    # column_encoder = DummyColumnEncoder(batch_size=64)


    if not os.path.exists(path_main+os.path.sep+"train.tables.jsonl"):
        print("tables not found, extracting, hopefully zip will be found")
        with zipfile.ZipFile(path_main+os.path.sep+"train.tables.jsonl.zip", 'r') as zip_ref:
            zip_ref.extractall(path_main+os.path.sep)

    _, train_tables, _, dev_tables, _, _ = load_wikisql(path_main, toy_model=False, toy_size=-1,
                                                                      no_w2i=True, no_hs_tok=True)
    train_column_reps = get_column_reps(train_tables)
    dev_column_reps = get_column_reps(dev_tables)

    output_dir = args.out_root

    with open(output_dir+ "/" + "train_vecs.json", "w") as f:
        json.dump(train_column_reps, f)

    with open(output_dir+ "/" + "dev_vecs.json", "w") as f:
        json.dump(dev_column_reps, f)

    print("Written to files. Have a good day")