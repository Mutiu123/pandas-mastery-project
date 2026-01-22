#!/usr/bin/env python3
"""
Script to create all Pandas mastery project notebooks
"""
import json
import os

def create_notebook_structure(cells):
    """Create standard Jupyter notebook structure"""
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.split('\n')}

def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.split('\n')}

# Notebook configurations
notebooks_config = {
    "04_data_transformation.ipynb": [
        md("# 🔄 Notebook 04: Data Transformation\n\n## Transform and reshape data\n- Create new features\n- Bin continuous data\n- String operations\n- Apply functions"),
        code("import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv('../datasets/employees.csv')\ndf['hire_date'] = pd.to_datetime(df['hire_date'])"),
        md("## 1. Creating New Columns"),
        code("# Calculated columns\ndf['tenure_years'] = (pd.Timestamp.now() - df['hire_date']).dt.days / 365\ndf['full_name'] = df['first_name'] + ' ' + df['last_name']\ndf['total_comp'] = df['salary'] + df['bonus'].fillna(0)"),
        md("## 2. Binning with pd.cut()"),
        code("# Create age groups\ndf['age_group'] = pd.cut(\n    df['age'],\n    bins=[0, 30, 45, 100],\n    labels=['Young', 'Mid-Career', 'Senior']\n)\nprint(df['age_group'].value_counts())"),
        code("# Salary brackets\ndf['salary_bracket'] = pd.cut(\n    df['salary'],\n    bins=[0, 50000, 75000, 100000, 200000],\n    labels=['Entry', 'Mid', 'Senior', 'Executive']\n)"),
        md("## 3. String Operations"),
        code("# Uppercase, lowercase\ndf['dept_upper'] = df['department'].str.upper()\ndf['name_lower'] = df['first_name'].str.lower()\n\n# Extract parts\ndf['email_domain'] = df['email'].str.split('@').str[1]\n\n# String length\ndf['name_length'] = df['first_name'].str.len()"),
        md("## 4. Apply Custom Functions"),
        code("# Simple apply\ndef categorize_performance(score):\n    if score >= 4:\n        return 'Excellent'\n    elif score >= 3:\n        return 'Good'\n    else:\n        return 'Needs Improvement'\n\ndf['performance_category'] = df['performance_score'].apply(categorize_performance)"),
        md("## Practice\n\n### Exercise 1: Create experience levels based on hire_date"),
        code("# Your code here\n"),
        md("### Exercise 2: Extract first initial from first_name"),
        code("# Create 'initial' column\n"),
        md("**Next**: Notebook 05 - Aggregation & Grouping")
    ],
    
    "05_aggregation_grouping.ipynb": [
        md("# Notebook 05: Aggregation & Grouping\n\n## Master GroupBy operations\n- Group and aggregate\n- Multiple statistics\n- Pivot tables\n- Crosstabs"),
        code("import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv('../datasets/employees.csv')"),
        md("## 1. Basic GroupBy"),
        code("# Group by single column\ndept_avg_salary = df.groupby('department')['salary'].mean()\nprint(dept_avg_salary)\n\n# Multiple aggregations\ndept_stats = df.groupby('department')['salary'].agg(['mean', 'median', 'min', 'max', 'count'])\nprint(dept_stats)"),
        md("## 2. Multiple Columns and Functions"),
        code("# Group by multiple columns\nresult = df.groupby(['department', 'position'])['salary'].mean()\nprint(result.head(10))"),
        code("# Different aggregations for different columns\nagg_dict = {\n    'salary': ['mean', 'sum'],\n    'age': 'mean',\n    'employee_id': 'count'\n}\nresult = df.groupby('department').agg(agg_dict)\nprint(result)"),
        md("## 3. Top N per Group - nlargest()"),
        code("# Top 3 salaries per department\ntop_earners = df.groupby('department').apply(\n    lambda x: x.nlargest(3, 'salary')[['first_name', 'salary']]\n)\nprint(top_earners)"),
        md("## 4. Pivot Tables"),
        code("# Create pivot table\npivot = df.pivot_table(\n    values='salary',\n    index='department',\n    columns='position',\n    aggfunc='mean',\n    fill_value=0\n)\nprint(pivot)"),
        code("# With margins (totals)\npivot = df.pivot_table(\n    values='salary',\n    index='department',\n    columns='position',\n    aggfunc='mean',\n    margins=True\n)\nprint(pivot)"),
        md("## 5. Crosstab"),
        code("# Cross-tabulation\ncross = pd.crosstab(\n    df['department'],\n    df['position'],\n    margins=True\n)\nprint(cross)"),
        code("# With values\ncross_salary = pd.crosstab(\n    df['department'],\n    df['position'],\n    values=df['salary'],\n    aggfunc='mean'\n)\nprint(cross_salary)"),
        md("## Practice\n\n### Exercise 1: Find average age and salary by city"),
        code("# Your code here\n"),
        md("### Exercise 2: Create pivot showing count of employees by dept and position"),
        code("# Your code here\n"),
        md("**Next**: Notebook 06 - Advanced Indexing")
    ],
    
    "06_advanced_indexing.ipynb": [
        md("# Notebook 06: Advanced Indexing\n\n## Master complex selections\n- MultiIndex\n- Advanced boolean logic\n- Conditional assignment\n- Performance tips"),
        code("import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv('../datasets/employees.csv')"),
        md("## 1. Complex Boolean Masking"),
        code("# Multiple conditions\nmask = (\n    (df['salary'] > 80000) &\n    (df['age'] < 40) &\n    (df['department'].isin(['Engineering', 'IT'])) &\n    (~df['status'].str.contains('Leave', na=False))\n)\nfiltered = df[mask]\nprint(f'Found {len(filtered)} employees')"),
        md("## 2. Conditional Assignment with .loc"),
        code("# Good practice: use .loc\ndf.loc[df['salary'] > 100000, 'tier'] = 'Top'\ndf.loc[(df['salary'] <= 100000) & (df['salary'] > 70000), 'tier'] = 'Mid'\ndf.loc[df['salary'] <= 70000, 'tier'] = 'Entry'\n\nprint(df['tier'].value_counts())"),
        md("## 3. MultiIndex DataFrames"),
        code("# Create MultiIndex\ndf_multi = df.set_index(['department', 'position'])\nprint(df_multi.head())\n\n# Select from MultiIndex\nengineering = df_multi.loc['Engineering']\nprint(engineering.head())"),
        md("## 4. Advanced String Filtering"),
        code("# Regex patterns\npattern_match = df[df['email'].str.match(r'^[a-z]+\\d+@', na=False)]\n\n# Multiple string conditions\nname_filter = df[\n    df['first_name'].str.startswith('J') |\n    df['last_name'].str.endswith('son')\n]"),
        md("## 5. Date Range Filtering"),
        code("df['hire_date'] = pd.to_datetime(df['hire_date'])\n\n# Recent hires\nrecent = df[df['hire_date'] > '2020-01-01']\nprint(f'Recent hires: {len(recent)}')"),
        code("# Date range\ndate_range = df[\n    df['hire_date'].between('2018-01-01', '2020-12-31')\n]\nprint(f'Hired in 2018-2020: {len(date_range)}')"),
        md("## Practice\n\n### Exercise 1: Find high performers in Sales dept earning < 80k"),
        code("# performance_score >= 4 AND department == 'Sales' AND salary < 80000\n"),
        md("### Exercise 2: Create 'needs_review' flag for employees with low performance and high salary"),
        code("# performance_score <= 2 AND salary > 90000\n"),
        md("**Next**: Notebook 07 - Combining DataFrames")
    ],
    
    "07_combining_dataframes.ipynb": [
        md("# Notebook 07: Combining DataFrames\n\n## Join and merge data\n- Merge (SQL-like joins)\n- Concat (stacking)\n- Join operations\n- Handling conflicts"),
        code("import pandas as pd\nimport numpy as np\n\nemployees = pd.read_csv('../datasets/employees.csv')\norders = pd.read_csv('../datasets/orders.csv')\ncustomers = pd.read_csv('../datasets/customers.csv')\nproducts = pd.read_csv('../datasets/products.csv')"),
        md("## 1. Merge - SQL-Style Joins"),
        code("# Inner join\nmerged = pd.merge(\n    orders,\n    customers,\n    on='customer_id',\n    how='inner'\n)\nprint(f'Inner join result: {len(merged)} rows')"),
        code("# Left join\nmerged = pd.merge(\n    orders,\n    products,\n    on='product_id',\n    how='left'\n)\nprint(merged.head())"),
        code("# Multiple keys\n# If we had a composite key\n# merged = pd.merge(df1, df2, on=['key1', 'key2'])"),
        md("## 2. Different Column Names"),
        code("# When join columns have different names\n# merged = pd.merge(\n#     df1,\n#     df2,\n#     left_on='customer_id',\n#     right_on='id'\n# )"),
        md("## 3. Concat - Stacking DataFrames"),
        code("# Vertical stacking (rows)\ndf1 = employees.head(100)\ndf2 = employees.tail(100)\nstacked = pd.concat([df1, df2], ignore_index=True)\nprint(f'Stacked: {len(stacked)} rows')"),
        code("# Horizontal stacking (columns)\n# Be careful with index alignment!\ndf_left = employees[['employee_id', 'first_name']]\ndf_right = employees[['salary', 'department']]\ncombined = pd.concat([df_left, df_right], axis=1)\nprint(combined.head())"),
        md("## 4. Join on Index"),
        code("# Set index first\ndf1 = employees.set_index('employee_id')\ndf2 = employees[['employee_id', 'bonus']].set_index('employee_id')\n\n# Join\njoined = df1.join(df2, rsuffix='_bonus')\nprint(joined.head())"),
        md("## 5. Merge with Indicators"),
        code("# See where data came from\nmerged = pd.merge(\n    orders.head(100),\n    customers,\n    on='customer_id',\n    how='outer',\n    indicator=True\n)\nprint(merged['_merge'].value_counts())"),
        md("## Practice\n\n### Exercise 1: Create customer order summary"),
        code("# Merge orders with customers\n# Count orders per customer\n# Calculate total spent\n"),
        md("### Exercise 2: Product sales analysis"),
        code("# Merge orders with products\n# Find top-selling products\n"),
        md("**Next**: Notebook 08 - Time Series")
    ],
    
    "08_time_series.ipynb": [
        md("# Notebook 08: Time Series Operations\n\n## Work with temporal data\n- DateTime operations\n- Resampling\n- Rolling windows\n- Time-based filtering"),
        code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nfinancial = pd.read_csv('../datasets/financial_data.csv')\nfinancial['date'] = pd.to_datetime(financial['date'])\nfinancial = financial.set_index('date')"),
        md("## 1. DateTime Basics"),
        code("employees = pd.read_csv('../datasets/employees.csv')\nemployees['hire_date'] = pd.to_datetime(employees['hire_date'])\n\n# Extract components\nemployees['hire_year'] = employees['hire_date'].dt.year\nemployees['hire_month'] = employees['hire_date'].dt.month\nemployees['hire_day_of_week'] = employees['hire_date'].dt.day_name()\n\nprint(employees[['hire_date', 'hire_year', 'hire_month']].head())"),
        md("## 2. Time-Based Selection"),
        code("# Select by year\ndata_2024 = financial['2024']\nprint(f'2024 data: {len(data_2024)} days')"),
        code("# Date range\nq1_2024 = financial['2024-01':'2024-03']\nprint(f'Q1 2024: {len(q1_2024)} days')"),
        md("## 3. Resampling"),
        code("# Daily to weekly\nweekly = financial['revenue'].resample('W').sum()\nprint(weekly.head())"),
        code("# Daily to monthly\nmonthly = financial.resample('M').agg({\n    'revenue': 'sum',\n    'expenses': 'sum',\n    'profit': 'sum'\n})\nprint(monthly.head())"),
        md("## 4. Rolling Windows"),
        code("# 7-day rolling average\nfinancial['revenue_7d_avg'] = financial['revenue'].rolling(window=7).mean()\n\n# 30-day rolling sum\nfinancial['revenue_30d_sum'] = financial['revenue'].rolling(window=30).sum()\n\nprint(financial[['revenue', 'revenue_7d_avg', 'revenue_30d_sum']].tail())"),
        md("## 5. Time Differences"),
        code("# Calculate tenure\nemployees['tenure_days'] = (pd.Timestamp.now() - employees['hire_date']).dt.days\nemployees['tenure_years'] = employees['tenure_days'] / 365\n\nprint(employees[['hire_date', 'tenure_years']].head())"),
        md("## 6. Plotting Time Series"),
        code("# Plot revenue over time\nplt.figure(figsize=(12, 6))\nfinancial['revenue'].plot(label='Daily Revenue')\nfinancial['revenue_7d_avg'].plot(label='7-Day Average', linewidth=2)\nplt.title('Revenue Over Time')\nplt.xlabel('Date')\nplt.ylabel('Revenue ($)')\nplt.legend()\nplt.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.show()"),
        md("## Practice\n\n### Exercise 1: Find hiring trends by month"),
        code("# Count hires per month\n# Plot the trend\n"),
        md("### Exercise 2: Calculate monthly profit growth rate"),
        code("# Use pct_change() on monthly profit\n"),
        md("**Next**: Notebook 09 - Performance Optimization")
    ],
    
    "09_performance_optimization.ipynb": [
        md("# Notebook 09: Performance Optimization\n\n## Write faster pandas code\n- Vectorization\n- Memory optimization\n- Efficient operations\n- Chunking"),
        code("import pandas as pd\nimport numpy as np\nimport time\n\ndf = pd.read_csv('../datasets/employees.csv')"),
        md("## 1. Vectorization vs Loops"),
        code("# BAD: Loop approach\nstart = time.time()\ndf_copy = df.copy()\nfor i in range(len(df_copy)):\n    df_copy.loc[i, 'bonus_taxed'] = df_copy.loc[i, 'bonus'] * 0.7 if pd.notna(df_copy.loc[i, 'bonus']) else 0\nloop_time = time.time() - start\nprint(f'Loop approach: {loop_time:.4f} seconds')"),
        code("# GOOD: Vectorized approach\nstart = time.time()\ndf['bonus_taxed'] = df['bonus'].fillna(0) * 0.7\nvector_time = time.time() - start\nprint(f'Vectorized approach: {vector_time:.4f} seconds')\nprint(f'Speedup: {loop_time/vector_time:.1f}x faster!')"),
        md("## 2. Memory Optimization"),
        code("# Check memory usage\nprint('Original memory:')\nprint(df.memory_usage(deep=True).sum() / 1024**2, 'MB')"),
        code("# Optimize data types\ndf_optimized = df.copy()\n\n# Int64 -> Int32 for smaller numbers\nfor col in ['employee_id', 'age', 'performance_score']:\n    df_optimized[col] = df_optimized[col].astype('int32')\n\n# Object -> Category for low cardinality\nfor col in ['department', 'position', 'city', 'status']:\n    df_optimized[col] = df_optimized[col].astype('category')\n\nprint('\\nOptimized memory:')\nprint(df_optimized.memory_usage(deep=True).sum() / 1024**2, 'MB')"),
        md("## 3. Efficient Filtering"),
        code("# SLOW: Multiple filters separately\nstart = time.time()\nresult = df[df['salary'] > 70000]\nresult = result[result['age'] < 40]\nresult = result[result['department'] == 'Engineering']\nslow_time = time.time() - start"),
        code("# FAST: Single combined filter\nstart = time.time()\nresult = df[\n    (df['salary'] > 70000) &\n    (df['age'] < 40) &\n    (df['department'] == 'Engineering')\n]\nfast_time = time.time() - start\nprint(f'Combined filter: {(slow_time/fast_time):.1f}x faster')"),
        md("## 4. Using query() for Speed"),
        code("# query() can be faster for complex conditions\nstart = time.time()\nresult = df.query('salary > 70000 and age < 40 and department == \"Engineering\"')\nquery_time = time.time() - start\nprint(f'Query time: {query_time:.4f} seconds')"),
        md("## 5. Chunking Large Files"),
        code("# Read large file in chunks\nchunksize = 1000\ntotal_rows = 0\n\n# Uncomment to test with large file\n# for chunk in pd.read_csv('../datasets/website_traffic.csv', chunksize=chunksize):\n#     # Process each chunk\n#     total_rows += len(chunk)\n#     # Do calculations on chunk\n# print(f'Processed {total_rows} rows in chunks')"),
        md("## 6. Best Practices Summary"),
        code("# BEST PRACTICES:\nprint(\"\"\"\n1. Use vectorized operations instead of loops\n2. Convert to appropriate data types (int32, category)\n3. Use single combined boolean masks\n4. Use .loc[] for assignments to avoid chaining\n5. Read only needed columns: pd.read_csv(file, usecols=['col1', 'col2'])\n6. Use query() for complex filters\n7. Process large files in chunks\n8. Use inplace=False (default) unless memory is critical\n\"\"\")"),
        md("## Practice\n\n### Exercise 1: Optimize the sales dataset"),
        code("sales = pd.read_csv('../datasets/sales_data.csv')\n# Check memory usage\n# Optimize data types\n# Compare before/after\n"),
        md("### Exercise 2: Benchmark filtering methods"),
        code("# Compare speed of:\n# 1. Chained filters\n# 2. Combined boolean mask\n# 3. query() method\n"),
        md("**Next**: Notebook 10 - Real-World Projects")
    ],
    
    "10_real_world_projects.ipynb": [
        md("# Notebook 10: Real-World Projects\n\n## Complete end-to-end analyses\n1. E-commerce Sales Dashboard\n2. Customer Churn Analysis\n3. HR Analytics Report\n4. Financial Performance Review"),
        code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_style('whitegrid')"),
        md("## Project 1: E-Commerce Sales Dashboard\n\n### Business Question:\n*\"What are our top-performing products, regions, and sales channels?\"*"),
        code("# Load data\nsales = pd.read_csv('../datasets/sales_data.csv')\nproducts = pd.read_csv('../datasets/products.csv')\ncustomers = pd.read_csv('../datasets/customers.csv')\norders = pd.read_csv('../datasets/orders.csv')\n\n# Clean\nsales['date'] = pd.to_datetime(sales['date'])\nprint('✅ Data loaded')"),
        code("# Analysis 1: Top products by revenue\ntop_products = sales.groupby('product')['total_amount'].sum().sort_values(ascending=False)\nprint('\\nTop 5 Products by Revenue:')\nprint(top_products.head())"),
        code("# Analysis 2: Regional performance\nregional_sales = sales.groupby('region').agg({\n    'total_amount': 'sum',\n    'sale_id': 'count',\n    'quantity': 'sum'\n}).round(2)\nregional_sales.columns = ['Total_Revenue', 'Num_Sales', 'Units_Sold']\nprint('\\nRegional Performance:')\nprint(regional_sales)"),
        code("# Analysis 3: Sales channel effectiveness\nchannel_perf = sales.groupby('sales_channel').agg({\n    'total_amount': ['sum', 'mean'],\n    'sale_id': 'count'\n})\nprint('\\nChannel Performance:')\nprint(channel_perf)"),
        code("# Visualization\nfig, axes = plt.subplots(2, 2, figsize=(15, 10))\n\n# 1. Top products\ntop_products.head(10).plot(kind='barh', ax=axes[0,0], color='steelblue')\naxes[0,0].set_title('Top 10 Products by Revenue')\n\n# 2. Regional sales\nregional_sales['Total_Revenue'].plot(kind='bar', ax=axes[0,1], color='coral')\naxes[0,1].set_title('Revenue by Region')\n\n# 3. Sales over time\nsales.groupby('date')['total_amount'].sum().plot(ax=axes[1,0])\naxes[1,0].set_title('Daily Sales Trend')\n\n# 4. Channel distribution\nchannel_perf[('sale_id', 'count')].plot(kind='pie', ax=axes[1,1], autopct='%1.1f%%')\naxes[1,1].set_title('Sales by Channel')\n\nplt.tight_layout()\nplt.show()"),
        md("## Project 2: Customer Churn Analysis\n\n### Business Question:\n*\"Which customer segments are at risk of churning?\"*"),
        code("customers = pd.read_csv('../datasets/customers.csv')\norders = pd.read_csv('../datasets/orders.csv')\n\n# Prepare data\ncustomers['signup_date'] = pd.to_datetime(customers['signup_date'])\ncustomers['days_since_signup'] = (pd.Timestamp.now() - customers['signup_date']).dt.days"),
        code("# Define churn (no activity + low lifetime value)\ncustomers['at_risk'] = (\n    (customers['is_active'] == False) |\n    (customers['total_purchases'] == 0) |\n    (customers['lifetime_value'] < 500)\n)\n\nprint(f\"Customers at risk: {customers['at_risk'].sum()} ({customers['at_risk'].mean()*100:.1f}%)\")"),
        code("# Segment analysis\nsegment_risk = customers.groupby('customer_segment')['at_risk'].agg(['sum', 'mean'])\nsegment_risk.columns = ['At_Risk_Count', 'At_Risk_Rate']\nprint('\\nRisk by Segment:')\nprint(segment_risk)"),
        code("# Age analysis\nage_groups = pd.cut(customers['age'], bins=[0, 30, 45, 60, 100], labels=['18-30', '31-45', '46-60', '60+'])\nage_risk = customers.groupby(age_groups)['at_risk'].mean()\nprint('\\nRisk by Age Group:')\nprint(age_risk)"),
        md("## Project 3: HR Analytics Report\n\n### Business Question:\n*\"How can we improve employee retention and satisfaction?\"*"),
        code("employees = pd.read_csv('../datasets/employees.csv')\nemployees['hire_date'] = pd.to_datetime(employees['hire_date'])\nemployees['tenure_years'] = (pd.Timestamp.now() - employees['hire_date']).dt.days / 365"),
        code("# Key metrics\nprint('=== HR DASHBOARD ===')\nprint(f\"Total Employees: {len(employees)}\")\nprint(f\"Average Salary: ${employees['salary'].mean():,.2f}\")\nprint(f\"Average Tenure: {employees['tenure_years'].mean():.1f} years\")\nprint(f\"Average Performance: {employees['performance_score'].mean():.2f}/5\")"),
        code("# Department analysis\ndept_analysis = employees.groupby('department').agg({\n    'employee_id': 'count',\n    'salary': 'mean',\n    'age': 'mean',\n    'performance_score': 'mean',\n    'tenure_years': 'mean'\n}).round(2)\nprint('\\nDepartment Analysis:')\nprint(dept_analysis)"),
        code("# Identify retention risks\nemployees['retention_risk'] = (\n    (employees['performance_score'] <= 2) |\n    (employees['salary'] < employees['salary'].quantile(0.25)) |\n    (employees['tenure_years'] > 8)\n)\nprint(f\"\\nEmployees at retention risk: {employees['retention_risk'].sum()}\")"),
        md("## Project 4: Financial Performance Review\n\n### Business Question:\n*\"What is our financial trajectory and profitability?\"*"),
        code("financial = pd.read_csv('../datasets/financial_data.csv')\nfinancial['date'] = pd.to_datetime(financial['date'])\nfinancial = financial.set_index('date')"),
        code("# Monthly summary\nmonthly = financial.resample('M').sum()\nmonthly['profit_margin'] = (monthly['profit'] / monthly['revenue']) * 100\n\nprint('\\nMonthly Financial Summary:')\nprint(monthly.tail())"),
        code("# Key metrics\nprint('\\n=== FINANCIAL DASHBOARD ===')\nprint(f\"Total Revenue: ${financial['revenue'].sum():,.2f}\")\nprint(f\"Total Profit: ${financial['profit'].sum():,.2f}\")\nprint(f\"Average Profit Margin: {(financial['profit']/financial['revenue']*100).mean():.2f}%\")\nprint(f\"Best Month: {financial['profit'].idxmax().strftime('%Y-%m')}\")\nprint(f\"Worst Month: {financial['profit'].idxmin().strftime('%Y-%m')}\")"),
        code("# Trend analysis\nfinancial['profit_7d_avg'] = financial['profit'].rolling(7).mean()\nfinancial['profit_30d_avg'] = financial['profit'].rolling(30).mean()\n\nplt.figure(figsize=(14, 6))\nplt.plot(financial.index, financial['profit'], alpha=0.3, label='Daily Profit')\nplt.plot(financial.index, financial['profit_7d_avg'], label='7-Day Average')\nplt.plot(financial.index, financial['profit_30d_avg'], label='30-Day Average', linewidth=2)\nplt.title('Profit Trend Analysis', fontsize=14, fontweight='bold')\nplt.xlabel('Date')\nplt.ylabel('Profit ($)')\nplt.legend()\nplt.grid(True, alpha=0.3)\nplt.tight_layout()\nplt.show()"),
        md("## Your Turn: Build Your Own Project!\n\n### Ideas:\n1. Product recommendation system (using orders + products data)\n2. Marketing campaign effectiveness (using sales + customers data)\n3. Inventory optimization (using products + orders data)\n4. Employee performance prediction (using employees data)\n\nUse all the skills you've learned!"),
        code("# Your project here\n"),
        md("## Congratulations! \n\nYou've completed the Pandas Mastery Project!\n\n### What You've Learned:\n✅ Data inspection and profiling\n✅ Cleaning and preprocessing\n✅ Advanced selection and filtering\n✅ Data transformation\n✅ Aggregation and grouping\n✅ Combining datasets\n✅ Time series analysis\n✅ Performance optimization\n✅ Real-world projects\n\n### Next Steps:\n- Practice with your own datasets\n- Contribute to open-source projects\n- Build a portfolio project\n- Share your learning journey\n\n**Keep coding and stay curious!** 🐼✨")
    ]
}

# Create all notebooks
os.makedirs('notebooks', exist_ok=True)

for filename, cells in notebooks_config.items():
    notebook = create_notebook_structure(cells)
    filepath = os.path.join('notebooks', filename)
    with open(filepath, 'w') as f:
        json.dump(notebook, f, indent=1)
    print(f"Created {filename}")

print("\n All notebooks created successfully!")
print(f"Total notebooks: {len(notebooks_config) + 3}")  # +3 for already created ones
