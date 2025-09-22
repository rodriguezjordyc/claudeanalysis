# Claude Analysis Project

Analysis of Claude AI usage patterns focusing on software development requests and collaboration patterns across global regions.

## 📁 Project Structure

### **Raw Data Files**
- `claude.csv` - ✅ **Primary source data** (country-level usage patterns)
- `api.csv` - Raw 1P API usage data
- `global.csv` - Global geographic data
- `usa.csv` - US-specific usage data
- `regions.csv` - Geographic region mapping

### **Active Analysis Folders**

#### `Software Request Analysis/`
Analysis of software development request patterns by region, SDLC stage, and complexity level.
- **Key Files**: See folder README for details

#### `Collaboration Analysis/`
Analysis of human-AI collaboration patterns across regions.
- **Key Files**: See folder README for details

### **Archive Folder**
- `Archive/scripts/` - One-time processing scripts
- `Archive/intermediate_data/` - Intermediate/problematic data files
- `Archive/backup_files/` - Backup versions of files
- `Archive/orphaned_files/` - Superseded analysis files

## 🔄 Data Flow

1. **Raw Data**: `claude.csv` contains accurate country-level counts
2. **Processing**: Analysis-specific filtering and classification
3. **Output**: Regional aggregations and visualizations

## ⚠️ Important Notes

- **Use `claude.csv` as primary source** - contains accurate raw counts
- **Avoid archived files** - particularly `regionanalysis.csv` (contains inflated weighted values)
- **Keep analysis isolated** - each folder contains domain-specific work

## 📊 Key Insights

- **Software Development**: Implementation & Testing phases dominate globally
- **Collaboration**: Directive pattern most common across all regions
- **Regional Variations**: Significant differences in complexity adoption and collaboration patterns