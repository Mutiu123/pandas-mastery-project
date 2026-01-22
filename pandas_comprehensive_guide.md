# 🐼 Comprehensive Pandas DataFrame Guide

## Table of Contents
1. [Basic Data Inspection](#basic-data-inspection)
2. [Data Cleaning](#data-cleaning)
3. [Data Selection & Indexing](#data-selection--indexing)
4. [Data Transformation](#data-transformation)
5. [Aggregation & Grouping](#aggregation--grouping)
6. [Advanced Indexing & Selection](#advanced-indexing--selection)
7. [Combining DataFrames](#combining-dataframes)

---

## Basic Data Inspection

### `df.duplicated()`
**Find duplicate rows**
```python
# Check for duplicate rows
df.duplicated()  # Returns boolean Series

# Check duplicates in specific columns
df.duplicated(subset=['column1', 'column2'])

# Keep first occurrence, mark rest as duplicates
df.duplicated(keep='first')  # default

# Keep last occurrence
df.duplicated(keep='last')

# Mark all duplicates (including first)
df.duplicated(keep=False)

# Example
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice', 'Charlie'],
    'age': [25, 30, 25, 35]
})
print(df.duplicated())  # [False, False, True, False]
```

### `df.isna().sum()`
**Count missing values per column**
```python
# Count missing values in each column
df.isna().sum()

# Get percentage of missing values
(df.isna().sum() / len(df)) * 100

# Check which rows have any missing values
df.isna().any(axis=1)

# Count total missing values in entire DataFrame
df.isna().sum().sum()

# Example
df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [5, None, None, 8]
})
print(df.isna().sum())
# A    1
# B    2
```

### `df.describe()`
**Get statistics summary (mean, median, std)**
```python
# Basic statistics for numerical columns
df.describe()

# Include all columns (including non-numeric)
df.describe(include='all')

# Only categorical columns
df.describe(include=['object', 'category'])

# Custom percentiles
df.describe(percentiles=[.1, .25, .5, .75, .9])

# Example output:
#          age     salary
# count   100.0    100.0
# mean     32.5  55000.0
# std       8.2  15000.0
# min      22.0  30000.0
# 25%      27.0  45000.0
# 50%      31.0  52000.0
# 75%      37.0  65000.0
# max      55.0  95000.0
```

---

## Data Cleaning

### `df.drop_duplicates(keep='last')`
**Remove duplicates, keep latest**
```python
# Drop duplicate rows, keep first occurrence
df.drop_duplicates()

# Keep last occurrence
df.drop_duplicates(keep='last')

# Drop duplicates based on specific columns
df.drop_duplicates(subset=['name', 'email'])

# Mark all duplicates for removal (keep none)
df.drop_duplicates(keep=False)

# In-place modification
df.drop_duplicates(inplace=True)

# Example
df = pd.DataFrame({
    'id': [1, 2, 1, 3],
    'value': [10, 20, 30, 40]
})
df.drop_duplicates(subset=['id'], keep='last')
# Keeps: id=2, id=1 (with value=30), id=3
```

### `df.replace({dict})`
**Replace multiple values at once**
```python
# Replace single value
df.replace('old_value', 'new_value')

# Replace multiple values
df.replace(['yes', 'no'], ['Y', 'N'])

# Replace with dictionary (column-specific)
df.replace({'col1': {'A': 1, 'B': 2}, 'col2': {'X': 10}})

# Replace NaN values
df.replace(np.nan, 0)

# Regex replacement
df.replace(r'[0-9]+', 'NUMBER', regex=True)

# Example
df = pd.DataFrame({
    'status': ['active', 'inactive', 'active'],
    'level': ['low', 'high', 'medium']
})
df.replace({
    'status': {'active': 1, 'inactive': 0},
    'level': {'low': 1, 'medium': 2, 'high': 3}
})
```

### `df.fillna()`
**Handle missing values**
```python
# Fill with a specific value
df.fillna(0)

# Fill with mean of column
df.fillna(df.mean())

# Fill with different values per column
df.fillna({'col1': 0, 'col2': 'Unknown', 'col3': df['col3'].mean()})

# Forward fill (use previous value)
df.fillna(method='ffill')  # or method='pad'

# Backward fill (use next value)
df.fillna(method='bfill')

# Fill with interpolation
df.interpolate()

# Limit number of consecutive fills
df.fillna(method='ffill', limit=2)

# Example
df = pd.DataFrame({
    'A': [1, None, 3, None, 5],
    'B': ['a', None, 'c', 'd', None]
})
df.fillna({'A': df['A'].mean(), 'B': 'missing'})
```

---

## Data Selection & Indexing

### Basic Selection: `df["column"]`
```python
# Select single column (returns Series)
df["name"]
df.name  # Alternative syntax

# Select multiple columns (returns DataFrame)
df[["name", "age", "city"]]

# Select columns by condition
df[[col for col in df.columns if 'price' in col]]
```

### **ADVANCED**: `df[df["condition"]]` - Boolean Indexing
```python
# Basic filtering
df[df["age"] > 30]

# Multiple conditions with &, |, ~
df[(df["age"] > 25) & (df["city"] == "NYC")]
df[(df["salary"] > 50000) | (df["bonus"] > 10000)]
df[~df["status"].isin(["inactive", "deleted"])]  # NOT in list

# String methods
df[df["name"].str.contains("John")]
df[df["email"].str.endswith("@gmail.com")]
df[df["city"].str.startswith("New")]

# Complex conditions
df[df["age"].between(25, 35)]
df[df["hire_date"] > pd.Timestamp('2020-01-01')]

# Chain conditions
mask = (df["department"] == "Sales") & (df["salary"] > 60000)
df[mask]
```

### **ADVANCED**: Column Assignment with Boolean Indexing
```python
# Create new column based on condition
df["senior"] = df["age"] > 50

# Conditional assignment
df.loc[df["age"] > 50, "category"] = "Senior"
df.loc[df["age"] <= 50, "category"] = "Junior"

# Multiple conditions with np.where
df["bonus_level"] = np.where(
    df["sales"] > 100000, "High",
    np.where(df["sales"] > 50000, "Medium", "Low")
)

# Using np.select for multiple conditions
conditions = [
    df["score"] >= 90,
    df["score"] >= 80,
    df["score"] >= 70
]
choices = ["A", "B", "C"]
df["grade"] = np.select(conditions, choices, default="F")

# Copy column with condition
df["high_earners"] = df.loc[df["salary"] > 80000, "name"]

# Apply function based on condition
df.loc[df["age"] > 30, "age"] = df.loc[df["age"] > 30, "age"] * 1.1
```

### `.loc[]` - Label-based indexing
```python
# Select by row and column labels
df.loc[0, "name"]  # Single cell
df.loc[0:5, "name"]  # Slice rows, single column
df.loc[:, ["name", "age"]]  # All rows, multiple columns

# Boolean indexing with loc
df.loc[df["age"] > 30, ["name", "salary"]]

# Set values with loc
df.loc[df["city"] == "NYC", "region"] = "Northeast"

# Multi-index selection
df.loc[("2023", "Q1"), :]  # For MultiIndex DataFrames
```

### `.iloc[]` - Position-based indexing
```python
# Select by integer position
df.iloc[0]  # First row
df.iloc[0, 1]  # First row, second column
df.iloc[0:5, 0:3]  # Rows 0-4, columns 0-2

# Negative indexing
df.iloc[-1]  # Last row
df.iloc[:, -1]  # Last column

# Select non-consecutive rows/columns
df.iloc[[0, 5, 10], [1, 3]]

# Slice with step
df.iloc[::2, :]  # Every other row
```

### `.at[]` and `.iat[]` - Fast scalar access
```python
# Fast access to single value by label
value = df.at[5, "name"]
df.at[5, "name"] = "New Name"

# Fast access to single value by position
value = df.iat[0, 1]
df.iat[0, 1] = "New Value"

# Much faster than .loc[] or .iloc[] for single values
```

### `df.query()` - Filter rows with readable syntax
```python
# String-based filtering
df.query("age > 30")
df.query("age > 30 and city == 'NYC'")
df.query("salary >= 50000 or bonus > 10000")

# Using variables
min_age = 25
df.query("age > @min_age")

# Complex queries
df.query("age > 30 and (city == 'NYC' or city == 'LA')")
df.query("name.str.startswith('A')")

# Column names with spaces (use backticks)
df.query("`first name` == 'John'")

# In operator
df.query("city in ['NYC', 'LA', 'Chicago']")
```

---

## Data Transformation

### `pd.crosstab()`
**Create pivot table summary**
```python
# Basic crosstab
pd.crosstab(df["department"], df["gender"])

# With percentages
pd.crosstab(df["dept"], df["gender"], normalize='all')  # Total
pd.crosstab(df["dept"], df["gender"], normalize='index')  # By row
pd.crosstab(df["dept"], df["gender"], normalize='columns')  # By column

# With aggregation
pd.crosstab(df["dept"], df["gender"], values=df["salary"], aggfunc='mean')

# Multiple grouping variables
pd.crosstab([df["dept"], df["level"]], df["gender"])

# With margins (totals)
pd.crosstab(df["dept"], df["gender"], margins=True)

# Example
#           Female  Male
# dept               
# HR             5     3
# IT             2     8
# Sales          6     4
```

### `df.value_counts(normalize=True)`
**Calculate percentages of each value**
```python
# Count occurrences
df["category"].value_counts()

# Get percentages
df["category"].value_counts(normalize=True)

# Include NaN values
df["category"].value_counts(dropna=False)

# Sort by index instead of value
df["category"].value_counts().sort_index()

# Bin continuous data first
pd.cut(df["age"], bins=[0, 18, 30, 50, 100]).value_counts()

# Multiple columns
df.value_counts(["dept", "level"])

# Example
# category
# A    0.40
# B    0.35
# C    0.25
```

### `pd.cut()`
**Create bins from numbers**
```python
# Equal-width bins
pd.cut(df["age"], bins=5)

# Custom bin edges
pd.cut(df["age"], bins=[0, 18, 30, 50, 100])

# Custom labels
pd.cut(df["age"], 
       bins=[0, 18, 30, 50, 100],
       labels=["Child", "Young Adult", "Adult", "Senior"])

# Include right edge (default) or left edge
pd.cut(df["age"], bins=5, right=False)

# Return bin indices
pd.cut(df["age"], bins=5, labels=False)

# Use with value_counts
pd.cut(df["salary"], bins=5).value_counts()

# Example
df["age_group"] = pd.cut(df["age"], 
                         bins=[0, 25, 50, 100],
                         labels=["Young", "Middle", "Senior"])
```

### `df.sort_values()`
**Sort by one or more columns**
```python
# Sort by single column
df.sort_values("age")

# Sort descending
df.sort_values("age", ascending=False)

# Sort by multiple columns
df.sort_values(["dept", "salary"], ascending=[True, False])

# Handle NaN values
df.sort_values("age", na_position='first')  # or 'last' (default)

# In-place sorting
df.sort_values("age", inplace=True)

# Sort by index
df.sort_index()

# Custom sort key
df.sort_values(by="name", key=lambda x: x.str.lower())

# Example
df.sort_values(["dept", "salary"], ascending=[True, False])
# Sorts by dept A-Z, then salary high to low within each dept
```

---

## Aggregation & Grouping

### `df.groupby().nlargest()`
**Get top N rows per group**
```python
# Top 3 salaries per department
df.groupby("department")["salary"].nlargest(3)

# Top 2 rows per group (all columns)
df.groupby("category").apply(lambda x: x.nlargest(2, "value"))

# Get indices of top N
df.groupby("dept")["salary"].nlargest(3).index

# Combine with reset_index
df.groupby("dept")["salary"].nlargest(3).reset_index()

# Alternative: sort and group head
df.sort_values("salary", ascending=False).groupby("dept").head(3)

# Example
# department
# HR        25    85000
#           12    78000
#           45    76000
# IT        8     95000
#           33    92000
#           67    88000
```

### `df.nlargest(n, 'col')`
**Get top N rows by column**
```python
# Top 5 highest salaries
df.nlargest(5, "salary")

# Top 10 by multiple columns
df.nlargest(10, ["salary", "bonus"])

# Keep all ties
df.nlargest(5, "salary", keep='all')

# Get smallest values instead
df.nsmallest(5, "salary")

# Select specific columns from result
df.nlargest(5, "salary")[["name", "salary", "dept"]]

# Example
#      name  salary    dept
# 42   Alice  95000    IT
# 17   Bob    92000    IT
# 89   Carol  88000    Sales
# 5    Dave   85000    HR
# 23   Eve    83000    Sales
```

### GroupBy Operations
```python
# Basic aggregations
df.groupby("dept")["salary"].mean()
df.groupby("dept")["salary"].agg(["mean", "median", "std"])

# Multiple columns, multiple functions
df.groupby("dept").agg({
    "salary": ["mean", "max"],
    "age": "mean",
    "bonus": "sum"
})

# Custom aggregation
df.groupby("dept")["salary"].agg(
    avg_salary=("salary", "mean"),
    total_salary=("salary", "sum"),
    count=("salary", "size")
)

# Filter groups
df.groupby("dept").filter(lambda x: len(x) > 5)

# Transform (return same shape)
df["dept_avg_salary"] = df.groupby("dept")["salary"].transform("mean")

# Apply custom function
df.groupby("dept").apply(lambda x: x["salary"].max() - x["salary"].min())
```

---

## Advanced Indexing & Selection

### Complex Boolean Masking
```python
# Combine multiple conditions
mask1 = df["age"] > 30
mask2 = df["city"] == "NYC"
mask3 = df["salary"] > 60000
df[mask1 & mask2 | mask3]

# Using isin() for multiple values
df[df["city"].isin(["NYC", "LA", "Chicago"])]
df[~df["status"].isin(["deleted", "archived"])]  # NOT in list

# String operations
df[df["name"].str.contains("John", case=False, na=False)]
df[df["email"].str.match(r"^[a-z]+@gmail\.com$")]

# Date filtering
df[df["date"] >= pd.Timestamp("2023-01-01")]
df[df["date"].between("2023-01-01", "2023-12-31")]

# Null/Not null
df[df["column"].notna()]
df[df["column"].isna()]
```

### Fancy Indexing
```python
# Select specific rows by condition, specific columns
df.loc[df["age"] > 30, ["name", "salary"]]

# Chain selections
df[df["dept"] == "IT"][df["salary"] > 70000]

# Select rows where any column meets condition
df[df.isin(["NYC", "LA"]).any(axis=1)]

# Select rows where all columns meet condition
df[(df[["col1", "col2", "col3"]] > 0).all(axis=1)]

# Use query for complex conditions
df.query("age > @min_age and salary > @min_salary")
```

### Conditional Column Creation (Advanced)
```python
# Method 1: Direct boolean assignment
df["is_senior"] = df["age"] > 50

# Method 2: np.where (if-else)
df["level"] = np.where(df["score"] > 80, "High", "Low")

# Method 3: np.select (multiple conditions)
conditions = [
    df["score"] >= 90,
    df["score"] >= 70,
    df["score"] >= 50
]
choices = ["A", "B", "C"]
df["grade"] = np.select(conditions, choices, default="F")

# Method 4: pd.cut (binning)
df["age_group"] = pd.cut(df["age"], 
                         bins=[0, 18, 35, 50, 100],
                         labels=["Youth", "Young", "Middle", "Senior"])

# Method 5: apply with lambda
df["bonus"] = df.apply(
    lambda row: row["salary"] * 0.2 if row["performance"] == "Excellent"
                else row["salary"] * 0.1 if row["performance"] == "Good"
                else 0,
    axis=1
)

# Method 6: map/replace
df["status_code"] = df["status"].map({"active": 1, "inactive": 0})

# Method 7: loc for conditional assignment
df.loc[df["age"] > 50, "category"] = "Senior"
df.loc[df["age"] <= 50, "category"] = "Junior"

# Method 8: Assign new columns from existing with conditions
df["high_performer"] = df.loc[
    (df["sales"] > 100000) & (df["rating"] >= 4.5),
    "name"
]
```

### Copy vs View
```python
# Create a copy (safe, but uses memory)
df_copy = df.copy()
df_subset = df[["col1", "col2"]].copy()

# View (references original, saves memory, but changes affect original)
df_view = df[["col1", "col2"]]  # This might be a view or copy

# Safe assignment (avoid SettingWithCopyWarning)
df.loc[df["age"] > 30, "category"] = "Senior"  # Good
df[df["age"] > 30]["category"] = "Senior"  # Bad (chained indexing)

# Check if it's a view or copy
df._is_view  # True if view, False if copy
```

---

## Combining DataFrames

### `df.merge()`
**Join two dataframes**
```python
# Inner join (default)
pd.merge(df1, df2, on="id")

# Left join
pd.merge(df1, df2, on="id", how="left")

# Right join
pd.merge(df1, df2, on="id", how="right")

# Outer join (full)
pd.merge(df1, df2, on="id", how="outer")

# Multiple keys
pd.merge(df1, df2, on=["id", "date"])

# Different column names
pd.merge(df1, df2, left_on="customer_id", right_on="id")

# Merge on index
pd.merge(df1, df2, left_index=True, right_index=True)

# Add suffix to overlapping columns
pd.merge(df1, df2, on="id", suffixes=("_left", "_right"))

# Indicator column (shows merge type)
pd.merge(df1, df2, on="id", how="outer", indicator=True)

# Example
df1 = pd.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
df2 = pd.DataFrame({"id": [1, 2, 4], "score": [90, 85, 95]})
result = pd.merge(df1, df2, on="id", how="left")
#    id name  score
# 0   1    A   90.0
# 1   2    B   85.0
# 2   3    C    NaN
```

### `pd.concat()`
**Stack dataframes vertically or horizontally**
```python
# Vertical stacking (rows)
pd.concat([df1, df2])

# Ignore index (create new sequential index)
pd.concat([df1, df2], ignore_index=True)

# Horizontal stacking (columns)
pd.concat([df1, df2], axis=1)

# Only keep common columns (intersection)
pd.concat([df1, df2], join="inner")

# Keep all columns (union, fill with NaN)
pd.concat([df1, df2], join="outer")  # default

# Add keys to identify source
pd.concat([df1, df2], keys=["first", "second"])

# Verify index integrity
pd.concat([df1, df2], verify_integrity=True)  # Error if duplicate indices
```

### `df.join()`
**Join on index**
```python
# Default: left join on index
df1.join(df2)

# Inner join
df1.join(df2, how="inner")

# Join on specific column
df1.join(df2, on="id")

# Join multiple DataFrames
df1.join([df2, df3, df4])

# With suffix
df1.join(df2, lsuffix="_left", rsuffix="_right")
```

### `df.pivot_table()`
**Create flexible pivot tables**
```python
# Basic pivot
df.pivot_table(
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum"
)

# Multiple aggregations
df.pivot_table(
    values="sales",
    index="region",
    columns="product",
    aggfunc=["sum", "mean", "count"]
)

# Multiple values
df.pivot_table(
    values=["sales", "profit"],
    index="region",
    columns="product",
    aggfunc="sum"
)

# With margins (totals)
df.pivot_table(
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    margins=True,
    margins_name="Total"
)

# Fill missing values
df.pivot_table(
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

# Multiple index levels
df.pivot_table(
    values="sales",
    index=["region", "city"],
    columns=["year", "quarter"],
    aggfunc="sum"
)
```

---

## Performance Tips

### Efficient Operations
```python
# Use vectorized operations instead of loops
df["total"] = df["price"] * df["quantity"]  # Fast
# vs
# for i in range(len(df)):  # Slow
#     df.loc[i, "total"] = df.loc[i, "price"] * df.loc[i, "quantity"]

# Use .loc for conditional assignment
df.loc[df["age"] > 30, "category"] = "Senior"  # Good
df[df["age"] > 30]["category"] = "Senior"  # Bad (chained indexing)

# Use categorical data type for repeated strings
df["category"] = df["category"].astype("category")

# Use query for complex filters (often faster)
df.query("age > 30 and salary > 50000")

# Read only needed columns
df = pd.read_csv("file.csv", usecols=["col1", "col2"])

# Use chunks for large files
for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    process(chunk)
```

---

## Common Patterns & Examples

### Example 1: Data Cleaning Pipeline
```python
# Complete cleaning workflow
df = (
    df
    .drop_duplicates()  # Remove duplicates
    .fillna({"age": df["age"].mean(), "city": "Unknown"})  # Fill missing
    .replace({"status": {"Y": True, "N": False}})  # Replace values
    .query("age > 0 and age < 120")  # Filter invalid ages
    .sort_values("created_date")  # Sort by date
    .reset_index(drop=True)  # Clean index
)
```

### Example 2: Feature Engineering
```python
# Create multiple features
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 50, 100])
df["is_senior"] = df["age"] > 50
df["high_earner"] = df["salary"] > df.groupby("dept")["salary"].transform("median")
df["tenure_years"] = (pd.Timestamp.now() - df["hire_date"]).dt.days / 365
df["full_name"] = df["first_name"] + " " + df["last_name"]
```

### Example 3: Complex Filtering
```python
# Multi-condition filtering
result = df[
    (df["age"].between(25, 45)) &
    (df["city"].isin(["NYC", "LA", "Chicago"])) &
    (df["salary"] > 60000) &
    (df["department"] != "HR") &
    (df["hire_date"] >= "2020-01-01")
]
```

### Example 4: Grouped Operations
```python
# Complex grouped analysis
result = (
    df
    .groupby(["department", "level"])
    .agg({
        "salary": ["mean", "median", "std", "count"],
        "age": "mean",
        "bonus": "sum"
    })
    .round(2)
    .sort_values(("salary", "mean"), ascending=False)
)
```

---

## Quick Reference Card

```python
# Selection
df["col"]                          # Single column
df[["col1", "col2"]]              # Multiple columns
df[df["age"] > 30]                # Filter rows
df.loc[0:5, "name"]               # Label-based
df.iloc[0:5, 0:3]                 # Position-based
df.query("age > 30")              # String-based query

# Cleaning
df.drop_duplicates()               # Remove duplicates
df.fillna(0)                       # Fill missing values
df.replace(old, new)               # Replace values
df.dropna()                        # Drop missing values

# Transformation
df.sort_values("col")              # Sort
df.groupby("col").mean()           # Group and aggregate
pd.cut(df["col"], bins=5)         # Create bins
df.apply(lambda x: x*2)           # Apply function

# Combining
pd.merge(df1, df2, on="id")       # Join DataFrames
pd.concat([df1, df2])             # Stack DataFrames
df.pivot_table(...)                # Create pivot table

# Analysis
df.describe()                      # Statistics
df.value_counts()                  # Count unique values
df.corr()                          # Correlation matrix
df.isna().sum()                    # Count missing values
```

---

## Tips & Best Practices

1. **Always use `.copy()`** when creating subsets you'll modify
2. **Use `.loc[]` instead of chained indexing** to avoid warnings
3. **Prefer vectorized operations** over loops for performance
4. **Use `query()`** for readable complex filters
5. **Convert repeated strings to categorical** for memory efficiency
6. **Chain operations** with method chaining for cleaner code
7. **Use `inplace=False`** (default) to avoid unintended modifications
8. **Test on small samples first** before running on large datasets
9. **Use `df.memory_usage(deep=True)`** to monitor memory
10. **Read pandas documentation** - it's excellent!

---

Happy Data Wrangling! 🐼✨
