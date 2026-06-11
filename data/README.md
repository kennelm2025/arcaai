# data/

DVC-tracked data pointers only - raw data never enters git (.gitignore enforces).
B1 remote is a local directory (.dvcstore/, gitignored); the on-prem MinIO remote
described in Blueprint S8.2 replaces it when infra hardens.
