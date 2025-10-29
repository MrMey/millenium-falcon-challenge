### Universe data
The SQLite file contains one table `routes`.

Example (taken from example1):
```
('Tatooine', 'Dagobah', 6),
('Dagobah', 'Endor', 4),
('Dagobah', 'Hoth', 1),
('Hoth', 'Endor', 1),
('Tatooine', 'Hoth', 6)
```

### How to compile deps
`uv pip compile requirements.in -o requirements.txt`

### How to install deps 
`uv pip install -r requirements.txt`
