# 📊 Data Dictionary

Complete reference for all datasets in the Pandas Mastery Project.

---

## 1. employees.csv (1,010 rows × 13 columns)

Company employee records with intentional data quality issues for practice.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| employee_id | int | Unique employee identifier | 1001, 1002, 1003 |
| first_name | str | Employee first name | John, Jane, Michael |
| last_name | str | Employee last name | Smith, Johnson, Williams |
| email | str | Work email address (has missing values) | emp1001@company.com |
| department | str | Department name | Sales, Engineering, Marketing, HR, Finance, Operations, IT |
| position | str | Job position level | Junior, Mid-Level, Senior, Lead, Manager, Director |
| salary | int | Annual salary in USD | 40000-150000 |
| hire_date | date | Date of hire | 2015-01-01 to 2024-01-01 |
| age | int | Employee age | 22-65 |
| city | str | Work location | New York, San Francisco, Chicago, Austin, Boston, Seattle, Los Angeles |
| status | str | Employment status | Active, On Leave, Inactive |
| bonus | float | Annual bonus (has missing values) | 0-20000 |
| performance_score | int | Performance rating | 1-5 (1=Poor, 5=Excellent) |

**Data Quality Issues:**
- 30 missing email addresses
- 20 missing bonus values
- 10 duplicate rows (for practice)

**Use Cases:**
- HR analytics
- Salary analysis
- Department comparisons
- Retention analysis

---

## 2. sales_data.csv (5,000 rows × 10 columns)

Transaction-level sales data for an electronics retailer.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| sale_id | int | Unique sale identifier | 5001, 5002, 5003 |
| date | date | Sale date | 2023-01-01 to 2023-12-31 |
| product | str | Product name | Laptop, Smartphone, Tablet, Headphones, Monitor, etc. |
| quantity | int | Units sold | 1-20 |
| unit_price | float | Price per unit | 15-699 |
| region | str | Sales region | North, South, East, West, Central |
| sales_channel | str | Channel of sale | Online, Retail, Wholesale, Direct |
| customer_id | int | Customer identifier | 10000-12000 |
| discount_percent | float | Discount applied (has missing values) | 0, 5, 10, 15, 20 |
| total_amount | float | Total sale amount | Calculated: quantity × unit_price × (1 - discount/100) |

**Data Quality Issues:**
- 50 missing discount_percent values

**Use Cases:**
- Revenue analysis
- Product performance
- Regional trends
- Channel effectiveness

---

## 3. customers.csv (2,000 rows × 12 columns)

Customer master data with demographics and metrics.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| customer_id | int | Unique customer identifier | 10000, 10001, 10002 |
| name | str | Full customer name | John Smith, Jane Brown |
| email | str | Email address | customer10000@email.com |
| phone | str | Phone number (has missing values) | +1-555-1234 |
| age | int | Customer age (has missing values) | 18-75 |
| gender | str | Gender | Male, Female, Other, Prefer not to say |
| city | str | City of residence | New York, San Francisco, Chicago, etc. |
| signup_date | date | Account creation date | 2020-01-01 to 2024-01-01 |
| customer_segment | str | Customer tier | Premium, Standard, Basic |
| total_purchases | int | Lifetime number of purchases | 0-50 |
| lifetime_value | float | Total customer spend | 100-10000 |
| is_active | bool | Active status | True, False |

**Data Quality Issues:**
- 40 missing phone numbers
- 25 missing age values

**Use Cases:**
- Customer segmentation
- Churn analysis
- Demographics study
- Lifetime value analysis

---

## 4. products.csv (500 rows × 10 columns)

Product catalog with pricing and inventory information.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| product_id | int | Unique product identifier | 1, 2, 3 |
| product_name | str | Product name | Pro Laptop, Ultra Smartphone |
| category | str | Product category | Electronics, Accessories, Computer, Audio, Video |
| price | float | Selling price | 10.00-1500.00 |
| cost | float | Product cost | 5.00-1000.00 |
| stock_quantity | int | Units in stock | 0-500 |
| supplier_id | int | Supplier identifier | 100-120 |
| rating | float | Average rating (has missing values) | 3.0-5.0 |
| reviews_count | int | Number of reviews | 0-1000 |
| launch_date | date | Product launch date | 2020-01-01 to 2024-01-01 |

**Data Quality Issues:**
- 15 missing rating values

**Use Cases:**
- Inventory management
- Pricing analysis
- Product performance
- Supplier analysis

---

## 5. orders.csv (10,000 rows × 9 columns)

Order transaction records linking customers and products.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| order_id | int | Unique order identifier | 20000, 20001, 20002 |
| customer_id | int | Customer who placed order | 10000-12000 |
| order_date | date | Date order was placed | 2023-01-01 to 2023-12-31 |
| product_id | int | Product ordered | 1-500 |
| quantity | int | Units ordered | 1-10 |
| total_price | float | Total order amount | 20.00-2000.00 |
| status | str | Order status | Completed, Shipped, Processing, Cancelled, Returned |
| shipping_cost | float | Shipping fee | 0.00-50.00 |
| payment_method | str | Payment type | Credit Card, PayPal, Debit Card, Bank Transfer |

**Use Cases:**
- Order fulfillment analysis
- Revenue tracking
- Customer purchasing patterns
- Join practice with customers and products

---

## 6. website_traffic.csv (50,000 rows × 10 columns)

Web analytics data capturing user sessions and behavior.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| session_id | int | Unique session identifier | 1, 2, 3 |
| timestamp | datetime | Session timestamp | 2024-01-01 00:00:00 |
| user_id | int | User identifier | 10000-15000 |
| page | str | Page visited | /home, /products, /checkout, /cart, /blog |
| time_spent_seconds | int | Time on page | 5-600 |
| device | str | Device type | Desktop, Mobile, Tablet |
| browser | str | Browser used | Chrome, Firefox, Safari, Edge, Other |
| country | str | User location | USA, UK, Canada, Australia, Germany, France |
| is_bounce | bool | Bounced (single page) | True, False |
| conversion | bool | Completed purchase | True, False |

**Use Cases:**
- Web analytics
- User behavior analysis
- Conversion optimization
- A/B testing analysis

---

## 7. financial_data.csv (365 rows × 7 columns)

Daily financial metrics for business performance tracking.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| date | date | Business date | 2024-01-01 to 2024-12-31 |
| revenue | float | Daily revenue | 50000-200000 |
| expenses | float | Daily expenses | 30000-150000 |
| marketing_spend | float | Marketing costs | 5000-30000 |
| employee_costs | float | Personnel expenses | 40000-80000 |
| operating_costs | float | Operational expenses | 10000-40000 |
| profit | float | Daily profit | revenue - expenses |

**Use Cases:**
- Financial reporting
- Time series analysis
- Trend identification
- Budget planning

---

## 8. survey_responses.csv (3,000 rows × 10 columns)

Customer satisfaction survey results.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| response_id | int | Unique response identifier | 1, 2, 3 |
| customer_id | int | Customer who responded | 10000-12000 |
| survey_date | date | Survey completion date | 2024-01-01 to 2024-06-30 |
| overall_satisfaction | str | Overall satisfaction level | Very Dissatisfied, Dissatisfied, Neutral, Satisfied, Very Satisfied |
| product_quality | int | Product quality rating | 1-5 |
| customer_service | int | Service quality rating | 1-5 |
| value_for_money | int | Value rating | 1-5 |
| would_recommend | str | Recommendation likelihood | Yes, No |
| nps_score | int | Net Promoter Score (has missing values) | 0-10 |
| comments | str | Open-ended feedback (has missing values) | Text responses or empty |

**Data Quality Issues:**
- 100 missing NPS scores

**Use Cases:**
- Customer satisfaction analysis
- NPS calculation
- Sentiment analysis
- Service improvement

---

## 9. sensor_data.csv (20,000 rows × 6 columns)

IoT sensor readings for monitoring and anomaly detection.

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| timestamp | datetime | Reading timestamp | 2024-01-01 00:00:00 |
| sensor_id | str | Sensor identifier | SENSOR_001, SENSOR_002 |
| temperature | float | Temperature in Celsius | 15.00-35.00 (normal), 50-100 (anomalies) |
| humidity | float | Humidity percentage | 30.00-80.00 |
| pressure | float | Atmospheric pressure | 990.00-1030.00 |
| status | str | Sensor status | Normal, Warning, Critical |

**Special Features:**
- Contains 50 temperature anomalies for practice
- 10-second intervals between readings
- 50 different sensors

**Use Cases:**
- Time series analysis
- Anomaly detection
- Monitoring systems
- Rolling statistics practice

---

## Dataset Relationships

```
customers (customer_id) ──┐
                           ├──> orders (customer_id, product_id)
products (product_id) ─────┘

sales_data (customer_id) ──> customers (customer_id)

survey_responses (customer_id) ──> customers (customer_id)

website_traffic (user_id) ≈ customers (customer_id)
```

---

## Data Generation Notes

All datasets were generated using Python's Faker library and numpy for reproducibility. Seeds are set to 42, so regenerating will produce identical data.

**Intentional Issues for Learning:**
- Missing values (various strategies needed)
- Duplicate rows (cleaning practice)
- Incorrect data types (conversion practice)
- Outliers (detection practice)
- Inconsistent formats (standardization practice)

---

## File Sizes

| Dataset | Rows | Columns | File Size |
|---------|------|---------|-----------|
| employees.csv | 1,010 | 13 | ~100 KB |
| sales_data.csv | 5,000 | 10 | ~400 KB |
| customers.csv | 2,000 | 12 | ~200 KB |
| products.csv | 500 | 10 | ~50 KB |
| orders.csv | 10,000 | 9 | ~600 KB |
| website_traffic.csv | 50,000 | 10 | ~3 MB |
| financial_data.csv | 365 | 7 | ~30 KB |
| survey_responses.csv | 3,000 | 10 | ~200 KB |
| sensor_data.csv | 20,000 | 6 | ~1 MB |

**Total:** ~5.5 MB

---

## Best Practices for Using These Datasets

1. **Start small**: Begin with employees.csv or customers.csv
2. **Read with dtypes**: Specify data types when loading for efficiency
3. **Check for issues**: Always inspect for missing values and duplicates
4. **Document findings**: Use notebook markdown cells
5. **Experiment freely**: Datasets can be regenerated

---

**Questions about the data?** Check the notebooks for examples of using each dataset!
