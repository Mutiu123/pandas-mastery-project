# 🚀 Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Python
Ensure you have Python 3.8 or higher:
```bash
python --version
# or
python3 --version
```

### Step 2: Navigate to Project Directory
```bash
cd pandas-mastery-project
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Step 4: Launch Jupyter Notebook
```bash
jupyter notebook
```

This will open Jupyter in your browser automatically.

### Step 5: Start Learning!
1. Navigate to the `notebooks/` folder
2. Open `01_basic_inspection.ipynb`
3. Run cells sequentially (Shift + Enter)

---

## Project Structure

```
pandas-mastery-project/
├── notebooks/              # 10 learning notebooks
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
├── datasets/               # 9 realistic datasets
│   ├── employees.csv
│   ├── sales_data.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── website_traffic.csv
│   ├── financial_data.csv
│   ├── survey_responses.csv
│   └── sensor_data.csv
├── README.md               # Full documentation
├── requirements.txt        # Python dependencies
└── QUICKSTART.md          # This file
```

---

## Learning Path

### For Beginners (Start Here)
1. **01_basic_inspection** - Learn to explore data
2. **02_data_cleaning** - Handle messy data
3. **03_data_selection** - Extract what you need
4. **04_data_transformation** - Create new features

### For Intermediate Users
5. **05_aggregation_grouping** - Summarize data
6. **06_advanced_indexing** - Complex selections
7. **07_combining_dataframes** - Join datasets

### For Advanced Users
8. **08_time_series** - Temporal analysis
9. **09_performance** - Optimize code
10. **10_real_world_projects** - Complete projects

---

## Keyboard Shortcuts (Jupyter)

| Action | Shortcut |
|--------|----------|
| Run cell | `Shift + Enter` |
| Run cell, stay in place | `Ctrl + Enter` |
| Insert cell above | `A` (in command mode) |
| Insert cell below | `B` (in command mode) |
| Delete cell | `D D` (press D twice) |
| Convert to Markdown | `M` (in command mode) |
| Convert to Code | `Y` (in command mode) |
| Save notebook | `Ctrl + S` or `Cmd + S` |

**Command mode**: Press `Esc`
**Edit mode**: Press `Enter` or click in cell

---

## Troubleshooting

### "Module not found" error
```bash
pip install [module_name]
```

### Jupyter won't start
```bash
# Reinstall jupyter
pip install --upgrade jupyter notebook
```

### Can't find datasets
Make sure you're running Jupyter from the project root directory.

### Kernel dies or restarts
- Restart kernel: Kernel → Restart
- Clear outputs: Cell → All Output → Clear
- Check memory usage with `df.memory_usage()`

---

## Tips for Success

✅ **Work sequentially** - Each notebook builds on previous concepts

✅ **Code along** - Don't just read, type and run the code

✅ **Do exercises** - They reinforce learning

✅ **Experiment** - Modify examples to see what happens

✅ **Take notes** - Document insights in markdown cells

✅ **Practice daily** - 30 minutes/day beats 5 hours/week

✅ **Ask questions** - Use comments to note confusions

---

## Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Real Python - Pandas Tutorials](https://realpython.com/learning-paths/pandas-data-science/)

---

## Need Help?

1. Check the notebook's markdown cells for explanations
2. Review the README.md for detailed information
3. Look at solution notebooks (coming soon!)
4. Search Stack Overflow with [pandas] tag

---

**Ready to master Pandas?** Open `01_basic_inspection.ipynb` and let's begin! 🐼

**Happy Learning!** 🚀
