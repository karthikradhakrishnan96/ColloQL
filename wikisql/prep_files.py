#!/usr/bin/env python
import json
from argparse import ArgumentParser
from tqdm import tqdm
from lib.dbengine import DBEngine
from lib.query import Query
from lib.common import count_lines


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('pred_file', help='predictions by the model')
    parser.add_argument('mode', help='dev or test')
    args = parser.parse_args()

    all_meta = {}
    fm = open("./" + args.mode + ".tables.jsonl")
    for line in fm:
        meta = json.loads(line)
        all_meta[meta["id"]] = meta
    fm.close()

    lines = []

    with open(args.pred_file) as fp:
        for lp in tqdm(fp, total=count_lines(args.pred_file)):
            ep = json.loads(lp)
            if "query" in ep and ep["query"]["agg"] in [1, 2, 4, 5] and all_meta[ep["table_id"]]["types"][ep["query"]["sel"]] == "text":
                ep["query"]["agg"] = 0
            lines.append(ep)
    with open(args.pred_file, "w") as fp:
        for line in lines:
            fp.write(json.dumps(line)+"\n")

