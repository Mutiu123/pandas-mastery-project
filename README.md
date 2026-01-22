# Pandas Mastery Project

A comprehensive, hands-on learning repository to master pandas DataFrame operations through real-world scenarios and practical exercises.

## Project Structure

```
pandas-mastery-project/
├── notebooks/              # Jupyter notebooks for each topic
│   ├── 01_basic_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_selection.ipynb
│   ├── 04_data_transformation.ipynb
│   ├── 05_aggregation_grouping.ipynb
│   ├── 06_advanced_indexing.ipynb
│   ├── 07_combining_dataframes.ipynb
│   ├── 08_time_series.ipynb
│   ├── 09_performance_optimization.ipynb
│   └── 10_real_world_projects.ipynb
├── datasets/              # Realistic dummy datasets
│   ├── employees.csv
│   ├── sales_data.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── ... (more datasets)
├── solutions/             # Solution notebooks
│   └── (same structure as notebooks/)
├── assets/                # Images and resources
└── README.md             # This file
```

## Learning Objectives

By completing this project, you will master:

1. **Basic Data Inspection** - Understanding your data structure and quality
2. **Data Cleaning** - Handling missing values, duplicates, and inconsistencies
3. **Data Selection & Indexing** - Efficiently accessing and filtering data
4. **Data Transformation** - Reshaping, binning, and creating new features
5. **Aggregation & Grouping** - Summarizing data across categories
6. **Advanced Indexing** - Complex boolean operations and multi-level indexing
7. **Combining DataFrames** - Merging, joining, and concatenating datasets
8. **Time Series Operations** - Working with dates and temporal data
9. **Performance Optimization** - Writing efficient pandas code
10. **Real-World Projects** - End-to-end data analysis workflows

## Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install required packages
pip install pandas numpy jupyter matplotlib seaborn faker
```

### Setup

#### Option 1: Quick Setup (Direct Installation)

1. **Clone and navigate to project**
   ```bash
   cd pandas-mastery-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

4. **Start with notebook 01** and work through sequentially

#### Option 2: Recommended Setup (Virtual Environment) 

Using a virtual environment is recommended to keep dependencies isolated and avoid conflicts.

1. **Clone and navigate to project**
   ```bash
   cd pandas-mastery-project
   ```

2. **Create virtual environment**
   
   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   ```
   
   **On Windows:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate
   ```
   
   **On Windows (PowerShell):**
   ```bash
   venv\Scripts\Activate.ps1
   ```
   
   You should see `(venv)` in your terminal prompt 

      **If you face restricted on windows error like Restricted" or "AllSigned, run and then try Activation again:**
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

6. **Start with notebook 01** (`notebooks/01_basic_inspection.ipynb`)

**To deactivate virtual environment when done:**
```bash
deactivate
```

**Next time you work on the project:**
1. `cd pandas-mastery-project`
2. `source venv/bin/activate` (or appropriate activation command)
3. `jupyter notebook`

## Datasets Overview

All datasets are realistic simulations representing common business scenarios:

| Dataset | Description | Rows | Use Cases |
|---------|-------------|------|-----------|
| `employees.csv` | Company employee records | 1000 | HR analytics, salary analysis |
| `sales_data.csv` | Sales transactions | 5000 | Revenue analysis, trends |
| `customers.csv` | Customer information | 2000 | Segmentation, demographics |
| `products.csv` | Product catalog | 500 | Inventory, pricing |
| `orders.csv` | Order history | 10000 | Purchase patterns, logistics |
| `website_traffic.csv` | Web analytics | 50000 | User behavior, engagement |
| `financial_data.csv` | Company finances | 365 | Budget, forecasting |
| `survey_responses.csv` | Customer surveys | 3000 | Satisfaction, feedback |
| `sensor_data.csv` | IoT sensor readings | 100000 | Time series, anomalies |

## Notebook Guide

### 01 - Basic Data Inspection
- Loading data from various sources
- Understanding DataFrame structure
- Quick data profiling
- Identifying data quality issues
- **Practice**: Analyze employee dataset quality

### 02 - Data Cleaning
- Handling missing values (multiple strategies)
- Removing duplicates
- Fixing data types
- Standardizing formats
- **Practice**: Clean messy sales data

### 03 - Data Selection & Indexing
- Column and row selection
- Boolean indexing and filtering
- .loc, .iloc, .at, .iat
- Query method
- **Practice**: Extract specific customer segments

### 04 - Data Transformation
- Creating new columns
- Binning continuous data
- String operations
- Applying custom functions
- **Practice**: Feature engineering for ML

### 05 - Aggregation & Grouping
- GroupBy operations
- Multiple aggregations
- Pivot tables and crosstabs
- Rolling windows
- **Practice**: Sales performance by region

### 06 - Advanced Indexing
- MultiIndex DataFrames
- Complex boolean operations
- Hierarchical indexing
- Advanced filtering
- **Practice**: Multi-level product analysis

### 07 - Combining DataFrames
- Merge (SQL-like joins)
- Concat (stacking)
- Join operations
- Handling conflicts
- **Practice**: Build customer 360° view

### 08 - Time Series Operations
- DateTime indexing
- Resampling and frequency conversion
- Rolling statistics
- Time-based filtering
- **Practice**: Stock price analysis

### 09 - Performance Optimization
- Vectorization vs loops
- Memory optimization
- Efficient data types
- Chunking large files
- **Practice**: Optimize slow operations

### 10 - Real-World Projects
- **Project 1**: E-commerce Sales Dashboard
- **Project 2**: Customer Churn Prediction Prep
- **Project 3**: Financial Report Automation
- **Project 4**: Web Analytics Insights

## Learning Path

### Beginner Path (Start Here)
1. Basic Inspection → 2. Data Cleaning → 3. Data Selection → 4. Data Transformation

### Intermediate Path
5. Aggregation & Grouping → 6. Advanced Indexing → 7. Combining DataFrames

### Advanced Path
8. Time Series → 9. Performance → 10. Real-World Projects

## Tips for Success

1. **Work through notebooks sequentially** - Each builds on previous concepts
2. **Complete all exercises** - Don't just read, code along!
3. **Experiment freely** - Try variations of the examples
4. **Use the solutions only as reference** - Try solving first
5. **Take notes** - Document your learnings
6. **Practice daily** - Consistency beats intensity
7. **Join the community** - Share your progress!

## Exercise Structure

Each notebook follows this pattern:

```python
# 1. Concept Introduction
# Clear explanation with simple example

# 2. Realistic Scenario
# Apply concept to real-world dataset

# 3. Guided Practice
# Step-by-step exercise with hints

# 4. Challenge Problem
# Test your understanding without guidance

# 5. Solution Discussion
# Multiple approaches and best practices
```

## Additional Resources

- [Official Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Stack Overflow - Pandas Tag](https://stackoverflow.com/questions/tagged/pandas)
- [Kaggle Learn - Pandas](https://www.kaggle.com/learn/pandas)

## Contributing

Found an error or want to add content?
- Open an issue
- Submit a pull request
- Share feedback

## License

This project is licensed under MIT License - free to use for learning and teaching.

## Acknowledgments

Built with for aspiring data analysts and scientists.

---

**Ready to become a Pandas expert?** Start with `notebooks/01_basic_inspection.ipynb` 

**Questions?** Check the solutions folder or revisit earlier notebooks.

**Happy Learning!** 
