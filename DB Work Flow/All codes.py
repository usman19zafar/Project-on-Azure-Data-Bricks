# ============================================================
# GRAND PYTHON FILE
# All core Python code used in Parts 1–8
# Productionizing Databricks Ingestion Notebooks
# ============================================================

# ============================================================
# 1. configuration.py
# Centralized environment configuration
# ============================================================

# --- Storage Paths (Mounted) ---
raw_folder_path = "/mnt/formula1dl/raw"
processed_folder_path = "/mnt/formula1dl/processed"
presentation_folder_path = "/mnt/formula1dl/presentation"

# --- Storage Paths (ABFS fallback) ---
# raw_folder_path = "abfs://raw@<storage_account>.dfs.core.windows.net"
# processed_folder_path = "abfs://processed@<storage_account>.dfs.core.windows.net"
# presentation_folder_path = "abfs://presentation@<storage_account>.dfs.core.windows.net"

# --- Global Defaults ---
default_data_source = "Ergast API"
job_timeout_seconds = 0
job_retries = 0


# ============================================================
# 2. common_functions.py
# Shared reusable functions
# ============================================================

from pyspark.sql.functions import current_timestamp, lit

def add_ingestion_date(input_df):
    """
    Adds ingestion_date column with current timestamp.
    """
    return input_df.withColumn("ingestion_date", current_timestamp())


# ============================================================
# 3. Widget-based parameterization
# (Used inside notebooks)
# ============================================================

# Define widget
dbutils.widgets.text("p_data_source", "")

# Retrieve parameter
v_data_source = dbutils.widgets.get("p_data_source")

# Example: add parameter as a column to a DataFrame
# (Assumes df already exists)
df = df.withColumn("data_source", lit(v_data_source))


# ============================================================
# 4. Notebook workflow with dbutils.notebook.run / exit
# ============================================================

# In child notebook (e.g., 1.ingest_circuits)
# -------------------------------------------
# At the end of successful execution:
dbutils.notebook.exit("success")


# In master notebook (e.g., 0.ingest_all_files)
# ---------------------------------------------

# Example: run circuits ingestion
result = dbutils.notebook.run(
    "1.ingest_circuits",          # notebook path
    0,                            # timeout (0 = no timeout)
    {"p_data_source": "Ergast API"}  # arguments
)
if result != "success":
    raise Exception("Circuits ingestion failed")

# Example: run drivers ingestion
result = dbutils.notebook.run(
    "2.ingest_drivers",
    0,
    {"p_data_source": "Ergast API"}
)
if result != "success":
    raise Exception("Drivers ingestion failed")

# ...repeat pattern for remaining ingestion notebooks...


# ============================================================
# 5. Full ingestion notebook template (single dataset)
# ============================================================

# NOTE: The following block represents the core logic
# of a single ingestion notebook, e.g., ingest_circuits.

# Import configuration and common functions via %run
# (These lines live in the notebook, not in a .py module)
# %run ../includes/configuration
# %run ../includes/common_functions

# Define widget for data source
dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

# Read RAW data
circuits_df = spark.read.json(f"{raw_folder_path}/circuits.json")

# Transform: add data_source and ingestion_date
circuits_df = circuits_df.withColumn("data_source", lit(v_data_source))
circuits_final_df = add_ingestion_date(circuits_df)

# Write to PROCESSED layer
circuits_final_df.write.mode("overwrite").parquet(
    f"{processed_folder_path}/circuits"
)

# Exit with success status (for workflows)
dbutils.notebook.exit("success")


# ============================================================
# 6. Example: Using configuration variables directly
# ============================================================

# Reading from RAW
raw_example_df = spark.read.parquet(f"{raw_folder_path}/some_raw_table")

# Writing to PROCESSED
raw_example_df.write.mode("overwrite").parquet(
    f"{processed_folder_path}/some_raw_table"
)

# Writing to PRESENTATION
raw_example_df.write.mode("overwrite").parquet(
    f"{presentation_folder_path}/some_presentation_table"
)


# ============================================================
# 7. Example: Databricks Job parameter usage (inside notebook)
# ============================================================

# When a Databricks Job passes p_data_source,
# the same widget/get pattern is used:

dbutils.widgets.text("p_data_source", "")
job_data_source = dbutils.widgets.get("p_data_source")

job_df = spark.read.json(f"{raw_folder_path}/job_example.json")
job_df = job_df.withColumn("data_source", lit(job_data_source))
job_df = add_ingestion_date(job_df)

job_df.write.mode("overwrite").parquet(
    f"{processed_folder_path}/job_example"
)


# ============================================================
# 8. Minimal master orchestration pattern (all files)
# ============================================================

# This is a compact example of orchestrating all ingestion notebooks.

ingestion_notebooks = [
    "1.ingest_circuits",
    "2.ingest_drivers",
    "3.ingest_constructors",
    "4.ingest_results",
    "5.ingest_pit_stops",
    "6.ingest_lap_times",
    "7.ingest_qualifying",
    "8.ingest_races"
]

for nb in ingestion_notebooks:
    result = dbutils.notebook.run(
        nb,
        0,
        {"p_data_source": "Ergast API"}
    )
    if result != "success":
        raise Exception(f"Ingestion failed for notebook: {nb}")

# End of grand Python file
