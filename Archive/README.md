# Archive Folder

This folder contains files that are no longer actively used in the current analysis but are preserved for reference.

## 📁 Contents

### `scripts/`
One-time processing scripts used during data preparation:
- Region addition and matching scripts
- Data filtering and normalization tools
- Percentage calculation utilities
- Processing validation scripts

### `intermediate_data/`
⚠️ **Problematic data files** - contains inflated weighted values:
- `regionanalysis.csv` - **DO NOT USE** (values ~33,000x inflated)
- `regionanalysis_normalized.csv` - Also contains inflated values
- `regionalrequests.csv` - Intermediate processing file
- `regionalrequests_clean.csv` - Intermediate processing file

### `backup_files/`
Backup versions of files:
- `claude_backup_20250918_100530.csv` - Backup of main data file
- `regions_backup.csv` - Backup of region mapping

### `orphaned_files/`
Files superseded by current analysis:
- Previous analysis notebooks
- Outdated data processing scripts
- Superseded CSV files

## ⚠️ Important Warning

**DO NOT use files from `intermediate_data/`** for analysis. The regionanalysis.csv files contain weighted aggregation that inflates values by ~33,000x compared to raw counts. Always use `../claude.csv` as the primary data source.

## 🗂️ Why These Files Are Archived

- **Scripts**: Single-use processing tools no longer needed
- **Intermediate Data**: Contains problematic weighted values
- **Orphaned Files**: Superseded by current analysis approach
- **Backups**: Safety copies of important files