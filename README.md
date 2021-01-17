# ColloQL
Contains code and data from our upcoming EMNLP workshop paper "ColloQL: Robust Cross-Domain Text-to-SQL Over Search Queries"


Largely adapted from SQLova : https://github.com/naver/sqlova


Place Stanford CoreNLP 2018-02-27 (3.9.1) in the models folder:  http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip


Some required dependencies:

```console
python -m pip install records
python -m pip install transformers
python -m pip install flashtext
```


To run the training:

```console
export PYTHONHASHSEED=420 && cd ColloQL/ && python train.py --seed 420 --bS 16 --accumulate_gradients 2 --bert_type_abb uS --fine_tune --lr 0.001 --lr_bert 0.00001 --max_seq_length 510 --do_train --data_path "/content/wikisql_noise/data/WikiSQL-1.1/data" --key "run_key" --shelf_bert_path "<Path to off-the-shelf BERT model>" --column_vector_path "./column_rep/outs" --lS 2
```

The best test and dev results are in the wikisql folder
```console
cd ColloQL/wikisql && python evaluate.py test.jsonl test.db test_results_colloql.jsonl
```


