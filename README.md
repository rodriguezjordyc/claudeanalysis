# Claude AI Usage Analysis Project

*Comprehensive analysis of Claude AI usage patterns across global regions for the Anthropic Economic Index (AEI)*

## 📊 Project Overview

This project analyzes Claude AI usage data to understand global patterns in AI adoption, software development practices, human-AI collaboration, and occupational task distribution. The analysis provides insights into regional variations in AI utilization and development maturity.

**🚀 Ready-to-Run:** All notebooks are self-contained with required data files included locally - no additional data setup needed.

## 📁 Project Structure

```
claudeanalysis/
├── data/
│   ├── raw/                           # Core datasets
│   │   ├── claude.csv                 # Primary usage data (9.2M records)
│   │   ├── api.csv                    # 1P API usage data (6.7M records)
│   │   └── Task Statements.csv        # O*NET occupational task data
│   └── regions.csv                    # Geographic region mappings
├── analysis/                          # Analysis notebooks and scripts
│   ├── ai_maturity/                   # AI Software Maturity Analysis
│   │   ├── AI_Software_Maturity_Analysis.ipynb
│   │   ├── scoring_engine.py & extract_regional_inputs.py
│   │   └── maturity_scores.csv & regional_inputs.csv
│   ├── collaboration/                 # Human-AI Collaboration Patterns
│   │   ├── Regional_Collaboration_Analysis.ipynb
│   │   └── regional_collaboration_analysis.csv
│   ├── onet_analysis/                 # Occupational Task Analysis
│   │   ├── Regional_Domain_Comparisons.ipynb & Regional_Efficiency_Analysis.ipynb
│   │   ├── generate_complexity_dataset.py
│   │   └── domainregional.csv, onetregionalraw*.csv
│   └── software_requests/             # Software Development Request Analysis
│       ├── Regional_Request_Comparisons.ipynb
│       ├── sdlc_classifier.py & strict_software_filter.py
│       └── softwareregionalrequests*.csv
├── visualizations/                    # Interactive dashboards and charts
└── archive/                          # Documentation and legacy files
```

## 🔬 Analysis Domains

### **1. AI Software Maturity Analysis**
**Location:** `analysis/ai_maturity/`

**Methodology:**
- Evaluates regional AI adoption maturity across 5 components: Complexity Adoption, Development Focus, Collaboration Sophistication, Testing Maturity, and Strategic Planning
- Uses weighted scoring system combining complexity metrics, SDLC stage distribution, and collaboration patterns
- Produces regional maturity rankings and component-specific insights

**Key Files:**
- `AI_Software_Maturity_Analysis.ipynb` - Main analysis notebook
- `scoring_engine.py` - Maturity scoring algorithms
- `extract_regional_inputs.py` - Data preparation for scoring

**Output:** Regional maturity scores (0-100 scale), component breakdowns, strategic recommendations

---

### **2. Human-AI Collaboration Analysis**
**Location:** `analysis/collaboration/`

**Methodology:**
- Analyzes 5 collaboration patterns: Directive (task completion), Task Iteration (refinement), Learning (education), Feedback Loop (review cycles), and Validation (verification)
- Calculates regional distribution percentages and specialization indices
- Identifies automation vs. augmentation preferences by region

**Key Files:**
- `Regional_Collaboration_Analysis.ipynb` - Main analysis notebook

**Output:** Regional collaboration pattern distributions, automation/augmentation preferences, behavioral insights

---

### **3. O*NET Occupational Analysis**
**Location:** `analysis/onet_analysis/`

**Methodology:**
- Maps Claude usage to O*NET occupational task categories
- Analyzes task complexity using efficiency metrics and regional specialization
- Examines domain distribution across major SOC occupation groups

**Key Files:**
- `Regional_Domain_Comparisons.ipynb` - Domain distribution analysis
- `Regional_Efficiency_Analysis.ipynb` - Task efficiency and complexity analysis
- `generate_complexity_dataset.py` - Complexity metric calculation

**Output:** Regional task specializations, complexity adoption patterns, occupational domain preferences

---

### **4. Software Development Request Analysis**
**Location:** `analysis/software_requests/`

**Methodology:**
- Classifies software development requests into 5 SDLC stages: Requirements & Planning, Design & Architecture, Implementation & Coding, Testing & QA, Deployment & Maintenance
- Applies strict filtering to identify genuine software development requests
- Analyzes regional distribution and development maturity patterns

**Key Files:**
- `Regional_Request_Comparisons.ipynb` - Main analysis notebook
- `sdlc_classifier.py` - SDLC stage classification logic
- `strict_software_filter.py` - Software request identification

**Output:** Regional SDLC stage distributions, development focus areas, maturity indicators

## 📈 Interactive Visualizations

**Location:** `visualizations/`

The project includes 5 interactive HTML dashboards:
- `collaboration-dashboard.html` - Collaboration pattern analysis
- `efficiency-dashboard.html` - Task efficiency metrics
- `maturity-components.html` - Maturity component breakdowns
- `maturity-dashboard.html` - Overall maturity rankings
- `request-dashboard.html` - Software development patterns

## 🔍 Key Findings

### **Global Patterns:**
- **Software Development:** Implementation & Testing phases dominate globally (65-80% of requests)
- **Collaboration:** Directive pattern most common (30-50%), indicating task completion focus
- **Regional Leadership:** North America and Europe show highest AI maturity scores
- **Occupational Focus:** Computer/Mathematical and Management tasks heavily represented

### **Regional Variations:**
- **Latin America:** Highest directive collaboration usage (47.5%)
- **Europe:** Most balanced collaboration approach, high learning pattern adoption (24.0%)
- **APAC:** Strong directive + task iteration combination
- **Middle East & Africa:** Growing collaboration adoption, development-focused usage

## 📊 Data Quality & Methodology

**Data Sources:**
- Claude.ai usage data (country-level aggregation)
- First-party API usage patterns
- O*NET occupational task database
- External: Population, GDP, geographic mapping data

**Quality Assurance:**
- Minimum observation thresholds (200 conversations/country, 100/US state)
- Privacy protection through aggregation and filtering
- Validation against external economic indicators
- Comprehensive data documentation in `archive/documentation/`

**Processing Pipeline:**
1. Raw data filtering and classification
2. Geographic aggregation and regional mapping
3. Metric calculation and normalization
4. Statistical analysis and visualization generation

## 🛠 Usage Requirements

**Environment:**
- Python 3.13+
- Jupyter Notebook environment
- Required packages: pandas, numpy, matplotlib, seaborn

**Getting Started:**
1. Clone repository
2. Install dependencies: `pip install pandas numpy matplotlib seaborn jupyter`
3. Navigate to desired analysis folder in `analysis/`
4. Open relevant Jupyter notebook
5. Run cells sequentially - all required data files are included locally

## 📚 Additional Resources

- **Original Documentation:** `archive/README_original.md`
- **Data Schema:** `archive/documentation/data_documentation.md`
- **Validation Reports:** `archive/documentation/validation_reports/`
- **Legacy Files:** `archive/legacy/`

---

*This analysis contributes to the Anthropic Economic Index (AEI) research on global AI adoption patterns and economic impacts.*