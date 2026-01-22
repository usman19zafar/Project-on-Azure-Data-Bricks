1, Authentication Layer
Command
```python
spark.conf.set(
  "fs.azure.account.key.<STORAGE Account>. windows.net",
  "<your-key>"
)
```
Purpose
Registers your Azure Storage Account access key inside Spark.

Milestone
This is the first gate of the entire pipeline.
Without authentication:

Spark cannot read

Spark cannot list

Spark cannot ingest

This command unlocks the storage account.

Achievement
Your Databricks environment is now authorized to access your Blob Storage.
______________________________________________________________________________________________________________________________________________________________
2, Connectivity Layer
Command
```python
circuits_path = "wasbs:<Storage account><file>"
```
Purpose
Defines the correct WASBS path for your non‑HNS Blob Storage.

Milestone
This confirms:

correct protocol (WASBS)

correct endpoint (blob.core.windows.net)

correct container (raw)

correct file (circuits.csv)

Achievement
You now have a valid, production‑safe path to your raw data.

______________________________________________________________________________________________________________________________________________________________
3, Initial Ingestion (Header Only)
Command
```python
circuits_df = spark.read \
    .option("header", True) \
    .csv(circuits_path)
```
Purpose
Loads the CSV into a DataFrame with header recognition.

Milestone
This is your first successful ingestion.

Achievement
You proved:

Spark can read the file

Header is recognized

DataFrame is created

This is the Bronze ingestion checkpoint.


______________________________________________________________________________________________________________________________________________________________
4, Schema Inspection (All Strings)
Command
```python
circuits_df.printSchema()
```
Purpose
Shows the inferred schema (all STRING types).

Milestone
You confirmed that CSV ingestion defaults to string-only schema.

Achievement
You identified the need for schema correction before Silver.


______________________________________________________________________________________________________________________________________________________________
5, Data Profiling
Command
```python
circuits_df.describe().show()
```
Purpose
Shows min, max, mean, count for numeric-looking columns.

Milestone
You used profiling to understand:

which columns are numeric

which columns are strings

which columns need type casting

Achievement
You now know the true data types required for production.

______________________________________________________________________________________________________________________________________________________________
6, Schema Inference (Testing Only)

Command
```python
circuits_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(circuits_path)
```
Purpose
Asks Spark to scan the data and guess the schema.

Milestone
You validated that Spark can infer:

INT

DOUBLE

STRING

But you also learned:

it triggers two Spark jobs

it is slow

it is not production-safe

Achievement
You confirmed the correct schema — but also confirmed that inference is not acceptable for production.

______________________________________________________________________________________________________________________________________________________________
7, Importing Data Types
Command

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
```
Purpose
Loads the classes needed to define an explicit schema.

Milestone
You moved from inferred schema to engineered schema.

Achievement
You are now ready to define a production-grade schema.

______________________________________________________________________________________________________________________________________________________________
8, Explicit Schema Definition
Command

```python
circuits_schema = StructType(fields=[
    StructField("circuitId", IntegerType(), False),
    StructField("circuitRef", StringType(), True),
    StructField("name", StringType(), True),
    StructField("location", StringType(), True),
    StructField("country", StringType(), True),
    StructField("lat", DoubleType(), True),
    StructField("lng", DoubleType(), True),
    StructField("alt", IntegerType(), True),
    StructField("url", StringType(), True)
])
```
Purpose
Defines the exact schema for the circuits dataset.

Milestone
This is the production milestone:

strict typing

strict nullability

strict structure

fail-fast behavior

Achievement
You now have a contract between raw data and your pipeline.

This is the foundation of the Silver layer.

______________________________________________________________________________________________________________________________________________________________
9, Schema-Enforced Read
Command

```python
circuits_df = spark.read \
    .option("header", True) \
    .schema(circuits_schema) \
    .csv(circuits_path)
```

Purpose
Reads the CSV using your explicit schema.

Milestone
This is the correct, production-grade ingestion.

Achievement
Your DataFrame now has:

correct INT columns

correct DOUBLE columns

correct STRING columns

correct nullability rules

This is the final Bronze → Silver readiness checkpoint.

______________________________________________________________________________________________________________________________________________________________
10, Final Schema Validation
Command

```python
circuits_df.printSchema()
```
Purpose
Confirms that Spark applied your schema exactly as defined.

Milestone
You validated that your schema is correct and enforced.

Achievement
You are now ready to write Silver Parquet.

______________________________________________________________________________________________________________________________________________________________
Visual Validation
Command
```python
display(circuits_df)
```
Purpose
Visually inspect the data.

Milestone
You confirmed:

correct values

correct types

correct structure

Achievement
You have a clean, typed, production-ready DataFrame.

What You Have Achieved Overall
You completed the entire schema engineering phase, which is the foundation of the Lakehouse.

You achieved:

    ✔ Authentication
    ✔ Connectivity
    ✔ Ingestion
    ✔ Schema inspection
    ✔ Data profiling
    ✔ Schema inference testing
    ✔ Explicit schema definition
    ✔ Schema enforcement
    ✔ Final validation

This is the Bronze → Silver transition milestone.

You are now ready to:
    
    rename columns
    drop URL
    add ingestion_date
    write Silver Parquet
    build Gold dimensional tables

This is where real data engineering begins.
