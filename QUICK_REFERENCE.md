# 🐼 Pandas Quick Reference Card

## 📥 Loading Data
```python
df = pd.read_csv('file.csv')
df = pd.read_excel('file.xlsx')
df = pd.read_json('file.json')
```

## 👀 Quick Inspection
```python
df.head()              # First 5 rows
df.tail()              # Last 5 rows
df.info()              # Structure overview
df.describe()          # Statistics
df.shape               # (rows, cols)
df.columns             # Column names
df.dtypes              # Data types
```

## 🔍 Selection
```python
df['col']                          # Single column
df[['col1', 'col2']]              # Multiple columns
df.loc[0:5, 'name']               # Label-based
df.iloc[0:5, 0:3]                 # Position-based
df[df['age'] > 30]                # Boolean filtering
df.query('age > 30 and city == "NYC"')  # Query string
```

## 🧹 Cleaning
```python
df.dropna()                        # Drop missing
df.fillna(0)                       # Fill missing
df.fillna(df.mean())              # Fill with mean
df.drop_duplicates()               # Remove duplicates
df.replace(old, new)               # Replace values
df['col'] = df['col'].astype(int) # Convert type
```

## 🔄 Transformation
```python
df['new'] = df['col1'] + df['col2']     # Calculated column
df['cat'] = pd.cut(df['age'], bins=3)   # Binning
df['upper'] = df['text'].str.upper()    # String ops
df.apply(lambda x: x*2)                  # Apply function
```

## 📊 Aggregation
```python
df.groupby('col').mean()                      # Group & aggregate
df.groupby('col').agg(['mean', 'sum'])       # Multiple aggs
df.pivot_table(values='A', index='B', columns='C')  # Pivot
pd.crosstab(df['col1'], df['col2'])          # Cross-tabulation
```

## 🔗 Combining
```python
pd.merge(df1, df2, on='id')               # Join
pd.merge(df1, df2, on='id', how='left')   # Left join
pd.concat([df1, df2])                      # Stack vertically
pd.concat([df1, df2], axis=1)             # Stack horizontally
```

## ⏰ Time Series
```python
df['date'] = pd.to_datetime(df['date'])      # Convert to datetime
df.set_index('date', inplace=True)           # Set datetime index
df.resample('M').sum()                        # Resample to monthly
df['col'].rolling(7).mean()                   # 7-day rolling avg
```

## 🎯 Advanced Selection
```python
# Multiple conditions
df[(df['age'] > 30) & (df['city'] == 'NYC')]

# String operations
df[df['name'].str.contains('John')]
df[df['email'].str.endswith('@gmail.com')]

# isin for multiple values
df[df['city'].isin(['NYC', 'LA', 'Chicago'])]

# NOT operator
df[~df['status'].isin(['deleted'])]
```

## 💾 Saving Data
```python
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
df.to_json('output.json')
```

## ⚡ Performance Tips
```python
# Use vectorized operations
df['new'] = df['A'] * df['B']  # GOOD

# Avoid loops
for i in range(len(df)):  # BAD
    df.loc[i, 'new'] = df.loc[i, 'A'] * df.loc[i, 'B']

# Optimize dtypes
df['category_col'] = df['category_col'].astype('category')
df['int_col'] = df['int_col'].astype('int32')

# Read only needed columns
df = pd.read_csv('file.csv', usecols=['col1', 'col2'])
```

## 🔢 Statistics
```python
df['col'].mean()           # Average
df['col'].median()         # Median
df['col'].std()            # Standard deviation
df['col'].min()            # Minimum
df['col'].max()            # Maximum
df['col'].sum()            # Sum
df['col'].count()          # Count non-null
df['col'].nunique()        # Count unique
df['col'].value_counts()   # Frequency distribution
```

## 📋 Common Patterns
```python
# Check for missing
df.isna().sum()

# Check for duplicates
df.duplicated().sum()

# Create age groups
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100])

# Conditional column
df['label'] = np.where(df['value'] > 10, 'High', 'Low')

# Top N per group
df.groupby('category').apply(lambda x: x.nlargest(3, 'value'))
```

---

**Keep this handy while working through the notebooks!** 🚀
