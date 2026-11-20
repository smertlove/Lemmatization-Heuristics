```bash
uv run -m scripts.make_lemmatization_rules --data-path "/mnt/data_storage/datasets/generative_lemmatization_datasets/csvs/train.csv" --out-dir ./data
```

```bash
uv run -m scripts.count_lemmatization_stats --data_dir ./data
```
