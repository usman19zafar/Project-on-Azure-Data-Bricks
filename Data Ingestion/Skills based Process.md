First:
Before getting into any further details we need to understand a big picture.
Big picture is to know what we are trying to achieve through a particular step, what will be the benifit!
Do we need to remember all the APIs?

```code
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
|     BUSINESS UTILITY      |     WHAT ENGINEER IS TRYING TO DO    |   SPARK API FIT     |                           WHY IT FITS                       |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Data Acquisition          | Load raw files into a DataFrame      | spark.read           | Reader API pulls data from CSV/JSON/Parquet into memory.    |
|                           |                                      |                      | It is the ingestion entry point for all workloads.          |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Schema Enforcement        | Apply structure, types, column names | df.printSchema       | Confirms schema correctness after load.                     |
|                           |                                      |                      | Ensures downstream transformations are predictable.         |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Data Quality              | Inspect sample rows for anomalies    | df.show              | Quick visual validation of data shape and quality.          |
|                           |                                      |                      | Helps catch header issues, nulls, and formatting errors.    |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Column Standardization    | Add audit columns, rename fields     | df.withColumn        | Adds ingestion_date, source, casts, and derived fields.     |
|                           |                                      |                      | Core transformation primitive.                              |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Row Filtering             | Remove bad rows, filter conditions   | df.filter            | Applies business rules (e.g., year > 2000).                 |
|                           |                                      |                      | Ensures only valid data moves forward.                      |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Data Shaping              | Select only required columns         | df.select            | Reduces width, improves performance, enforces contracts.    |
|                           |                                      |                      | Architect-level control of schema exposure.                 |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Deduplication             | Remove duplicates                    | df.distinct          | Ensures uniqueness for keys, dimensions, and joins.         |
|                           |                                      |                      | Critical for clean analytical models.                       |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Data Integration          | Join multiple datasets               | df.join              | Combines tables using keys (driverId, raceId, etc.).        |
|                           |                                      |                      | Foundation of Silver/Gold transformations.                  |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Aggregation               | Summaries, counts, metrics           | df.groupBy           | Enables business KPIs, rollups, and analytical metrics.     |
|                           |                                      |                      | Core for Gold-layer modeling.                               |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Ordering                  | Sort for reporting or validation     | df.orderBy           | Helps validate sequences, timestamps, and ranking logic.    |
|                           |                                      |                      | Useful for debugging and business logic checks.             |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Data Export               | Write processed data to storage      | df.write             | Writes Parquet, Delta, JSON, CSV.                           |
|                           |                                      |                      | Foundation of Bronze → Silver → Gold pipelines.             |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
| Pipeline Validation       | Count rows for sanity checks         | df.count             | Ensures completeness, detects missing or duplicate loads.   |
|                           |                                      |                      | Used in every ingestion SOP.                                |
+---------------------------+--------------------------------------+----------------------+--------------------------------------------------------------+
```

THE ONE SENTENCE VERSION
Spark SQL API looks huge, but it’s really just 12 verbs grouped into 4 layers.

THE FOUR‑LAYER MODEL (Architect View)

```Code
+----------------------+---------------------------------------------+
| LAYER 1: ENTRY       | spark session, read, write                  |
+----------------------+---------------------------------------------+
| LAYER 2: SHAPING     | select, filter, withColumn, drop, cast      |
+----------------------+---------------------------------------------+
| LAYER 3: RELATION    | join, groupBy, agg, orderBy                 |
+----------------------+---------------------------------------------+
| LAYER 4: ACTION      | show, count, collect                        |
+----------------------+---------------------------------------------+
```
Everything in the giant Spark API list fits into one of these four layers.

THE TWELVE VERBS (Engineer View)
These are the only ones you need to remember.

```Code
1. read
2. write
3. select
4. filter
5. withColumn
6. drop
7. cast
8. join
9. groupBy
10. orderBy
11. show
12. count
```

Everything else is a variation, alias, or helper.

THE MENTAL MODEL (How to Think About the API)

    1. “How do I get data?” → read
    CSV, JSON, Parquet, Delta — all through spark.read.
    
    2. “How do I save data?” → write
    Parquet, Delta, partitioning, modes — all through df.write.
    
    3. “How do I shape columns?” → select / withColumn / drop / cast
    These four cover 80% of transformations.
    
    4. “How do I shape rows?” → filter
    Row-level business rules.
    
    5. “How do I combine datasets?” → join
    Silver-layer logic.
    
    6. “How do I summarize?” → groupBy
    Gold-layer metrics.
    
    7. “How do I order or rank?” → orderBy
    Useful for debugging and reporting.
    
    8. “How do I inspect?” → show / printSchema
    Quick validation.
    
    9. “How do I validate counts?” → count
    Pipeline sanity checks.

ASCII TABLE: API REFERENCE → WHAT IT REALLY MEANS
```Code
+------------------------------+----------------------------------------------+
| API CATEGORY                 | WHAT IT REALLY MEANS                         |
+------------------------------+----------------------------------------------+
| SparkSession                 | Entry point to everything                    |
| DataFrame                    | Your table in memory                         |
| DataFrameReader              | How you load data                            |
| DataFrameWriter              | How you save data                            |
| Column                       | How you manipulate a single column           |
| Functions (F)                | Helpers for expressions                      |
| GroupedData                  | Aggregations                                 |
| Window                       | Ranking, row numbers, advanced analytics     |
| Types                        | Schema definitions                           |
+------------------------------+----------------------------------------------+
```
This is the entire API reference compressed into one table.

THE SECRET: YOU DON’T LEARN THE API — YOU LEARN THE PATTERNS
Spark is predictable.

If you know the pattern:

```Code
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| SPARK OPERATION               | PROBLEM / ISSUE                                              | UTILITY (BUSINESS BENEFIT)                                   | OBJECTIVE (ENGINEER INTENT)                                 |
|                               |                                                              |                                                              | CODE PATTERN                                                 |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| spark.read.format().option().load()                                                                                                                             |
|                               | Problem: Raw data is stuck in files and cannot be used       | Benefit: Brings data into the platform for processing        | Intent: Ingest files/tables into a DataFrame with            |
|                               |          for analytics or transformation.                    |          and analytics.                                      |         correct format, options, and schema.                 |
|                               |                                                              |                                                              | Code: spark.read.format("csv").option("header", True).load()|
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.write.format().mode().save()                                                                                                                                |
|                               | Problem: Processed data is not stored anywhere,              | Benefit: Makes curated data available for ML, reporting,     | Intent: Persist DataFrame as Parquet/Delta with correct      |
|                               |          causing reprocessing and duplication.               |          SQL analytics, and downstream pipelines.            |         mode (overwrite/append) and folder structure.        |
|                               |                                                              |                                                              | Code: df.write.format("parquet").mode("overwrite").save()   |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.select()                   | Problem: Dataset contains unnecessary or sensitive columns   | Benefit: Reduces data width, improves performance,           | Intent: Choose, rename, or reorder columns to enforce        |
|                               |          that violate business rules or slow pipelines.      |          enforces schema contracts.                          |         business schema contracts.                           |
|                               |                                                              |                                                              | Code: df.select("col1", "col2")                             |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.filter()                   | Problem: Dataset contains invalid, outdated, or irrelevant   | Benefit: Ensures only business‑valid rows move forward       | Intent: Apply row‑level business rules (e.g., year > 2000,   |
|                               |          rows that break analytics.                          |          into Silver/Gold layers.                            |         status = 'active').                                  |
|                               |                                                              |                                                              | Code: df.filter("year > 2000")                              |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.withColumn()               | Problem: Missing audit fields, derived metrics, or           | Benefit: Adds business logic, lineage, and traceability      | Intent: Create derived columns, cast types, add              |
|                               |          transformations needed for reporting.               |          required for governance.                            |         ingestion_date, data_source, etc.                    |
|                               |                                                              |                                                              | Code: df.withColumn("ingestion_date", current_timestamp())  |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.join()                     | Problem: Business entities are split across multiple tables  | Benefit: Creates unified, enriched datasets for analytics    | Intent: Link datasets using keys (driverId, raceId, etc.)    |
|                               |          and cannot be analyzed together.                    |          and reporting.                                      |         to build Silver/Gold layers.                         |
|                               |                                                              |                                                              | Code: df1.join(df2, "driverId", "inner")                    |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.groupBy().agg()            | Problem: Raw data cannot answer business questions           | Benefit: Produces KPIs, metrics, and aggregated insights     | Intent: Aggregate data (counts, sums, averages) for          |
|                               |          like totals, averages, rankings.                    |          required by reporting teams.                        |         reporting and analytics.                             |
|                               |                                                              |                                                              | Code: df.groupBy("team").agg(count("*"))                    |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.orderBy()                  | Problem: Data is unsorted, making trends, sequences,         | Benefit: Enables meaningful analysis, ranking, and           | Intent: Sort by date, ranking, or business priority          |
|                               |          or validations difficult to see.                    |          validation checks.                                  |         for validation or reporting.                         |
|                               |                                                              |                                                              | Code: df.orderBy("date")                                    |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.show()                     | Problem: Engineer cannot visually confirm if ingestion       | Benefit: Quick visual validation of data quality,            | Intent: Display sample rows to validate ingestion,           |
|                               |          or transformation worked correctly.                 |          schema, and transformations.                        |         schema, and transformations.                         |
|                               |                                                              |                                                              | Code: df.show(5)                                            |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
| df.count()                    | Problem: No way to confirm completeness, detect missing      | Benefit: Ensures pipeline correctness and prevents           | Intent: Confirm row counts before/after transformations       |
|                               |          rows, or validate incremental loads.                |          silent data loss.                                   |         to ensure no data is lost or duplicated.             |
|                               |                                                              |                                                              | Code: df.count()                                            |
+-------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+--------------------------------------------------------------+
```
You can “guess” 90% of the API without memorizing anything.

THE ULTRA‑SIMPLE VERSION (Your Brain Only Needs This)

```Code
READ → TRANSFORM → WRITE → VALIDATE
```
Everything in the giant Spark API list is just a variation of these four words.





How to use Data frame reader API to read the data from CSV. file into Spark data frame 

