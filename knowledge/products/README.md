# Products

Each subfolder is a product or initiative dossier. Copy `_template/` and rename it to create a new one.

```
products/
├── _template/          # Copy this to start a new product
│   ├── brief.md        # What it is, problem, hypothesis, scope
│   ├── roadmap.md      # Now / Next / Later + milestones
│   ├── metrics.md      # Dated metric snapshots
│   ├── updates.md      # Status updates (newest first)
│   ├── releases/       # Per-release docs
│   └── experiments/    # Experiment write-ups
├── my-product/         # Your first product (created during onboarding)
└── ...
```

## How to use

1. Copy `_template/` → `your-product-name/`
2. Fill in `brief.md` first — it's the entry point agents read
3. Append to `updates.md` and `metrics.md` as the product evolves
4. Create a file in `experiments/` for each experiment
5. Create a file in `releases/` for each release milestone
