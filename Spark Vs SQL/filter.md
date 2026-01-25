```code
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Topic                     | SQL-Style Filter ("...")                   | Pythonic Filter (df.col == ...)               |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Syntax style              | SQL WHERE clause inside a string           | Python boolean expressions on columns         |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Single condition example  | df.filter("race_year = 2019")              | df.filter(df["race_year"] == 2019)            |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Column reference          | Plain column name                          | df.col or df["col"]                           |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Equality operator         | =                                          | ==                                            |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| AND operator              | AND                                        | &                                             |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| OR operator               | OR                                         | |                                             |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Parentheses needed?       | No                                         | Yes, around each condition                    |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Multiple conditions ex.   | df.filter("race_year=2019 AND round<=5")   | df.filter((df["race_year"]==2019) &           |
|                           |                                            |            (df["round"]<=5))                  |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Readability               | Familiar to SQL users                      | Familiar to Python/PySpark users              |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Error sensitivity         | Fewer syntax errors                        | Must follow Python rules strictly             |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Supports functions        | Yes (inside SQL string)                    | Yes (PySpark functions)                       |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| Alias                     | where("...")                               | where() also works                            |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| When to use               | When thinking in SQL logic                 | When building programmatic expressions        |
+---------------------------+--------------------------------------------+-----------------------------------------------+
```

Filter Transformation — Finalized Notes (Rewritten, Not Summarized)
Section Introduction
This section focuses on two important Spark transformations: Filter and Join.
In most data projects, the incoming data is larger than what is required, so filtering is necessary to extract only the relevant subset. Spark provides the Filter Transformation for this purpose.

Similarly, data is often distributed across multiple tables or files. To combine these datasets and derive business value, Spark provides a rich set of Join Transformations.
After learning both transformations, they will be applied in the project by combining data from five different tables into a single table suitable for analysis and reporting.

By the end of this section, the goal is to understand Filter and Join transformations and know when to use specific join types.

Filter Transformation Lesson
Purpose of Filtering
In any data project, filtering is commonly required.
Examples include selecting data for the current tax year or the last three tax years.
In SQL, this is equivalent to using a WHERE clause.
Spark provides the Filter Transformation for the same purpose.

Documentation Reference
The Filter transformation is documented under the DataFrame APIs.
Scrolling through the API documentation reveals the filter method.

Filter behaves the same as SQL’s WHERE clause.

Spark also provides where() as an alias for filter().

Both return rows that satisfy the specified condition.

Filter takes one parameter: the condition to evaluate.

Example usage:

Python expression style:
df.age > 3

SQL expression style:
"age > 3"

Both approaches are valid.

Notebook Demonstration Setup
A folder named Demo was created inside the Formula1 workspace.
Inside it, a notebook named 1.filter  demo was created to demonstrate filter operations.
This notebook includes the configuration notebook so that folder paths defined earlier can be reused.

The demonstration reads data from the races file.
This dataset includes a year column, which is useful for filtering examples.
The notebook also demonstrates filtering using multiple conditions.

Reading the Data
The cluster is started, and the races data is read into a DataFrame.
Displaying the DataFrame shows approximately 1058 records, representing all races across all years.

Filtering by Year — SQL Style
To filter data for a specific year (e.g., 2019):

python
races_filtered_df = races_df.filter("race_year = 2019")
2019 is chosen because 2020 was an unusual year due to COVID.
The result returns 21 records, corresponding to the 21 races held in 2019.

Filtering by Year — Pythonic Style
Using DataFrame column notation:

python
races_filtered_df = races_df.filter(races_df["race_year"] == 2019)
Notes:

In Python, equality requires ==, not =.

Columns can be referenced using dot notation or bracket notation.

This produces the same 21 records.

Filtering with Multiple Conditions — SQL Style
Example: filter for 2019 races where the round number is less than or equal to 5:

python
races_filtered_df = races_df.filter("race_year = 2019 AND round <= 5")
This returns the first five rounds of the 2019 season.

Filtering with Multiple Conditions — Pythonic Style
Equivalent Python expression:

python
races_filtered_df = races_df.filter(
    (races_df["race_year"] == 2019) & (races_df["round"] <= 5)
)
Important details:

Use & for AND

Use | for OR

Each condition must be wrapped in parentheses

Column references must use DataFrame notation

The result matches the SQL-style filter.

Key Points to Remember
SQL-style filters use SQL syntax inside a string.

Python-style filters use DataFrame column expressions.

SQL-style conditions do not require parentheses for multiple conditions.

Python-style conditions must use parentheses around each condition.



filter() and where() are interchangeable in Spark.
