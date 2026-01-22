complete Bronze → Silver → Gold pipeline for circuits, in final notebook‑ready commands, using your non‑HNS Blob (WASBS) setup.

3 logical notebooks: Bronze, Silver, Gold

commands only (ready to run)

short notes on what each layer is doing

Shared config (top of every notebook)
```python
spark.conf.set(
  "fs.azure.account.key.uzi786.blob.core.windows.net",
  "<Security Key>"
)

raw_container_path     = "wasbs://raw@uzi786.blob.core.windows.net"
bronze_container_path  = "wasbs://bronze@uzi786.blob.core.windows.net"
silver_container_path  = "wasbs://silver@uzi786.blob.core.windows.net"
gold_container_path    = "wasbs://gold@uzi786.blob.core.windows.net"
```

_____________________________________________________________________________________________________________________________________________________________________
1 Bronze notebook – ingest raw CSV → Bronze Parquet
Goal: land raw data as‑is in Parquet (no business logic, just structure).

```python
# 1. Source path (raw CSV)
circuits_csv_path = f"{raw_container_path}/circuits.csv"

# 2. Read raw CSV with header
circuits_bronze_df = spark.read \
    .option("header", True) \
    .csv(circuits_csv_path)

# 3. Quick validation
circuits_bronze_df.show(5)
circuits_bronze_df.printSchema()

# 4. Write to Bronze as Parquet (partitioning optional here)
bronze_output_path = f"{bronze_container_path}/circuits"

circuits_bronze_df.write \
    .mode("overwrite") \
    .parquet(bronze_output_path)
What this makes you ready for:  
Silver can now assume consistent Parquet input, not fragile CSV.
```

_____________________________________________________________________________________________________________________________________________________________________
2, Silver notebook – clean + standardize → Silver Parquet
Goal: apply schema, rename columns, drop URL, add ingestion_date.

```python
from pyspark.sql.functions import col, current_timestamp
```

# 1. Read from Bronze

bronze_input_path = f"{bronze_container_path}/circuits"

circuits_bronze_df = spark.read.parquet(bronze_input_path)

# 2. Apply transformations (rename, drop, add ingestion_date)
circuits_silver_df = circuits_bronze_df \
    .withColumnRenamed("circuitId",  "circuit_id") \
    .withColumnRenamed("circuitRef", "circuit_ref") \
    .withColumnRenamed("lat",        "latitude") \
    .withColumnRenamed("lng",        "longitude") \
    .withColumnRenamed("alt",        "altitude") \
    .drop("url") \
    .withColumn("ingestion_date", current_timestamp())

# 3. Optional: cast numeric columns
circuits_silver_df = circuits_silver_df \
    .withColumn("circuit_id", col("circuit_id").cast("int")) \
    .withColumn("latitude",   col("latitude").cast("double")) \
    .withColumn("longitude",  col("longitude").cast("double")) \
    .withColumn("altitude",   col("altitude").cast("int"))

# 4. Validate
circuits_silver_df.show(5, truncate=False)
circuits_silver_df.printSchema()

# 5. Write to Silver
silver_output_path = f"{silver_container_path}/circuits"

circuits_silver_df.write \
    .mode("overwrite") \
    .parquet(silver_output_path)
What this makes you ready for:  
Gold can now trust clean, typed, business‑ready columns.
_____________________________________________________________________________________________________________________________________________________________________
3 Gold notebook – business view → Gold Parquet
For circuits, a simple Gold example is a dimension table (DimCircuits).

Goal: create a Gold‑layer dimension with only the fields needed for analytics.

python
# 1. Read from Silver
silver_input_path = f"{silver_container_path}/circuits"

circuits_silver_df = spark.read.parquet(silver_input_path)

# 2. Select business‑ready columns (dimension view)
circuits_gold_df = circuits_silver_df.select(
    "circuit_id",
    "circuit_ref",
    "name",
    "location",
    "country",
    "latitude",
    "longitude",
    "altitude",
    "ingestion_date"
)

# 3. Validate
circuits_gold_df.show(5, truncate=False)
circuits_gold_df.printSchema()

# 4. Write to Gold
gold_output_path = f"{gold_container_path}/dim_circuits"

circuits_gold_df.write \
    .mode("overwrite") \
    .parquet(gold_output_path)
What this makes you ready for:

Direct consumption by Power BI / reporting

Joining with other Gold tables (e.g., races, results)

Building a star schema around dim_circuits

Tiny ASCII view of the whole thing

_____________________________________________________________________________________________________________________________________________________________________
```text
RAW (CSV, blob)
    │
    ▼
BRONZE (Parquet, as‑is)
    │   minimal structure, no business rules
    ▼
SILVER (Parquet, cleaned)
    │   renamed, typed, URL dropped, ingestion_date added
    ▼
GOLD (Parquet, dimensional)
        dim_circuits for analytics & BI
```
