# Onet Analysis

Regional analysis of O*NET occupational task demand based on Claude AI usage patterns.

## 📊 Active Files

### **Data Files**
- `domainregional.csv` - ✅ **Regional domain aggregation with percentages (analysis-ready)**
- `domainregional_counts_only.csv` - Regional domain counts without percentages
- `onetregionalraw.csv` - Raw O*NET task data with domain classifications
- `onetregionalraw_with_complexity.csv` - ✅ **Extended dataset with API complexity volumes**

### **Analysis Notebooks**
- `Regional Domain Comparisons.ipynb` - ✅ **Main analysis notebook**
  - Regional domain distribution comparison
  - Occupational specialization profiles
  - Strategic insights framework
- `Regional Efficiency Analysis.ipynb` - ✅ **AI utilization efficiency analysis**
  - Volume-weighted efficiency indices by region
  - Prompt/completion/cost efficiency patterns
  - Domain-specific efficiency profiles

### **Processing Scripts**
- `generate_complexity_dataset.py` - ✅ **Complexity volume dataset generator**
  - Applies 1P API complexity benchmarks to regional data
  - Creates expanded dataset with complexity metrics
  - 94.7% volume coverage with API benchmarks

## 🎯 Domain Classification

### **10 Occupational Domains** (Refined Context-Aware Classification)
1. **Administrative_Support** (30.8%) - Office administration, employment processing, clerical work
2. **Research_Analysis** (15.2%) - Scientific research, field analysis, data interpretation
3. **Software_Development** (10.3%) - Programming, coding, technical systems (context-aware)
4. **Education_Training** (10.1%) - Teaching, instruction, curriculum development
5. **Creative_Communications** (7.7%) - Design, marketing, content creation
6. **Customer_Service** (7.6%) - Customer support, client assistance
7. **Business_Management** (5.9%) - Operations, strategy, consulting
8. **Healthcare_Medical** (5.2%) - Patient care, medical programs, wellness (includes exercise programs)
9. **Financial_Services** (4.6%) - Banking, investment, financial planning
10. **Professional_Services** (2.2%) - Legal, engineering, specialized consulting

## 🔄 Data Processing

**Source**: Raw country-level O*NET task data from `../claude.csv`
**Filter**: `facet='onet_task'` AND `variable='onet_task_count'`
**Aggregation**: Sum of task counts by region + task
**Coverage**: Exhaustive - all unique tasks appearing in any country within each region

## 📈 Dataset Overview

### **Data Quality**
- **Total records**: 2,447 (regional task combinations)
- **Unique O*NET tasks**: 1,212
- **Total task volume**: 394,429
- **Complete regional coverage**: All 5 regions included

### **Regional Task Distribution**
- **North America**: 1,189 unique tasks
- **APAC**: 507 unique tasks
- **Europe**: 350 unique tasks
- **Latin America**: 260 unique tasks
- **Middle East & Africa**: 141 unique tasks

## 🎯 Key Insights

### **Top Occupational Tasks Globally**
1. **Programming & Development**: Error correction, software requirements analysis
2. **Education & Training**: Student assistance, instructional material development
3. **Language & Communication**: Foreign language instruction, content creation

### **Regional Patterns**
- **North America**: Highest task diversity (1,189 unique tasks)
- **APAC**: Strong software development and educational task focus
- **Europe**: Balanced technical and educational demand
- **Latin America**: Concentrated task demand patterns
- **MEA**: Emerging market with focused occupational needs

## 📋 Data Schema

```csv
region,facet,variable,domain,value,percentage
APAC,domain,domain_count,Software_Development,21436,20.5
```

**Fields**:
- `region`: Geographic region
- `facet`: Always "domain"
- `variable`: Always "domain_count"
- `domain`: Classified occupational domain (10 categories)
- `value`: Aggregated count across all countries in region
- `percentage`: Regional percentage (excludes 'none', sums to 100% per region)

## ✅ Validation

- **Source data**: 7,251 country-task records processed
- **Aggregation accuracy**: Regional totals verified
- **Task coverage**: Complete exhaustive coverage confirmed
- **Data integrity**: No missing regions or malformed records

## 🧠 Efficiency Analysis Framework

### **Methodology**
- **Global API Benchmarks**: 1P API efficiency indices (1.0 = global average)
- **Volume Weighting**: Regional efficiency = Σ(Task Volume × Task Efficiency) / Total Volume
- **Coverage**: 365 overlapping tasks representing 94.7% of regional volume

### **Efficiency Dimensions**
1. **Prompt Efficiency**: Input optimization (prompt length, detail, specificity)
2. **Completion Efficiency**: Output optimization (response length, detail, efficiency)
3. **Cost Efficiency**: Computational optimization (processing requirements)

### **Key Findings**
**Regional Efficiency Rankings** (Volume-weighted prompt efficiency):
1. **North America**: 1.41 - Highest efficiency utilization
2. **Latin America**: 1.78 - Moderate efficiency
3. **Europe**: 1.87 - Moderate efficiency patterns
4. **APAC**: 1.92 - Lower efficiency with software focus
5. **Middle East & Africa**: 2.18 - Lowest efficiency utilization

### **Strategic Implications**
- **Counter-intuitive patterns**: Traditional "AI maturity" assumptions challenged
- **Efficiency vs. Volume**: Different regional strategies revealed
- **Domain Specialization**: Software development drives efficiency across regions
- **Utilization Optimization**: Regional best practices for AI interaction patterns

## 🚀 Next Phase Opportunities

1. **Skills Gap Analysis**: Compare regional task demand vs. supply
2. **Occupational Clustering**: Group similar tasks into career pathways
3. **Economic Development**: Correlate task demand with regional GDP/development
4. **Workforce Planning**: Identify high-demand vs. underserved occupational areas
5. **Cross-Regional Analysis**: Task demand flow and migration patterns
6. **Efficiency Optimization**: Regional prompt engineering efficiency programs
7. **Best Practice Transfer**: Cross-regional AI utilization strategy sharing