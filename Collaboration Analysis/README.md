# Collaboration Analysis

Analysis of human-AI collaboration patterns across global regions based on raw usage data.

## 📊 Active Files

### **Data Files**
- `regional_collaboration_analysis.csv` - ✅ **Accurate collaboration data with counts and percentages**

## 🔄 Data Processing

**Source**: Raw country-level data from `../claude.csv` (NOT regionanalysis.csv)
**Aggregation**: Summed by region, calculated proper percentages
**Exclusion**: "not_classified" excluded from percentage calculations

## 📈 Collaboration Patterns

### **Pattern Types**
- **Directive** (30-50%) - Direct task completion requests
- **Task Iteration** (20-27%) - Iterative refinement processes
- **Learning** (13-24%) - Educational and tutorial requests
- **Feedback Loop** (8-12%) - Review and improvement cycles
- **Validation** (3-5%) - Verification and checking requests
- **None** (2-7%) - No specific collaboration pattern

### **Regional Insights**
- **Latin America**: Highest directive usage (47.5%)
- **Europe**: Balanced approach with high learning (24.0%)
- **APAC**: Strong directive + task iteration combination
- **North America**: Most diverse collaboration mix
- **Middle East & Africa**: Growing collaboration adoption

## ✅ Data Quality

- **Percentages sum to 100%** for each region (excluding not_classified)
- **Raw counts verified** against source data
- **No inflated weighted values** (unlike archived regionanalysis.csv)

## 🎯 Key Finding

**Directive pattern dominates globally**, suggesting users primarily seek direct task completion rather than collaborative learning or iterative refinement.