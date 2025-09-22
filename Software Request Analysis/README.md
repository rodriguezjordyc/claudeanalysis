# Software Request Analysis

Analysis of software development request patterns across regions, focusing on SDLC stages and complexity levels.

## 📊 Active Files

### **Data Files**
- `softwareregionalrequests_clean.csv` - ✅ **Clean software request data by region/complexity**
- `softwareregionalrequests_with_sdlc.csv` - ✅ **SDLC-classified request data**

### **Analysis Notebooks**
- `Regional Request Comparisons.ipynb` - ✅ **Main analysis notebook**
  - Regional SDLC stage distribution
  - Complexity level comparisons
  - Visualizations and insights

### **Processing Scripts**
- `sdlc_classifier.py` - ✅ **SDLC stage classification logic**
- `strict_software_filter.py` - ✅ **Software request filtering logic**

## 🔄 Analysis Pipeline

1. **Filtering**: `strict_software_filter.py` identifies genuine software development requests
2. **Classification**: `sdlc_classifier.py` categorizes requests into 5 SDLC stages
3. **Analysis**: Main notebook produces regional comparisons and insights

## 📈 Key Findings

- **Implementation & Coding**: Dominates all regions (30-45%)
- **Testing & QA**: Second priority globally (20-35%)
- **Requirements Planning**: Consistently underutilized (5-15%)
- **Regional Variations**: Different development maturity levels

## 🎯 SDLC Stages

1. **Requirements & Planning** - Strategy, guidance, consultation
2. **Design & Architecture** - System design, UI/UX, data modeling
3. **Implementation & Coding** - Development, programming, feature building
4. **Testing & QA** - Debugging, testing, optimization, security
5. **Deployment & Maintenance** - DevOps, infrastructure, monitoring