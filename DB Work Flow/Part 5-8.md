ENGINEERING DESIGN DOCUMENT — PARTS 5–8
Productionizing Databricks Ingestion Notebooks  
Author: Usman Zafar
Style: Engineering Design Document
Scope: Configuration Architecture, Common Functions Architecture, Implementation SOPs, Code Appendix, Validation Procedures

PART 5 — Configuration Architecture
1. Problem
The ingestion notebooks contain hardcoded folder paths for:

RAW container

PROCESSED container

PRESENTATION container

Hardcoding paths creates several issues:

Not portable across DEV → TEST → PROD

Requires editing multiple notebooks when paths change

Increases risk of inconsistent paths

Prevents environment‑based configuration

Makes debugging and maintenance difficult

A centralized configuration mechanism is required.

2. Constraints
Configuration must be accessible from all ingestion notebooks.

Configuration must support both mounted paths and ABFS paths.

Configuration must not require cluster restarts.

Configuration must be editable in one place.

Configuration must support future parameters (e.g., schema registry, checkpoints).

Configuration must work with %run imports.

3. Design Decision
Create a dedicated configuration notebook (configuration.py) inside an /includes folder.

Rationale:

Centralizes all environment‑specific values

Eliminates hardcoded paths

Enables environment portability

Supports both mount and ABFS access patterns

Integrates cleanly with %run

Supports future expansion

4. Implementation
4.1 Create /includes/configuration.py
This file contains:

RAW folder path

PROCESSED folder path

PRESENTATION folder path

Global defaults

Optional ABFS fallback paths

4.2 Import configuration into ingestion notebooks
python
%run ../includes/configuration
4.3 Replace hardcoded paths
Before:

python
"/mnt/formula1dl/raw/circuits.json"
After:

python
f"{raw_folder_path}/circuits.json"
5. Code
python
# ============================================
# configuration.py
# Centralized environment configuration
# ============================================

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
6. Validation
Import configuration using %run.

Print variables to confirm values load correctly.

Run ingestion notebook.

Confirm data is written to correct folder paths.

Switch to ABFS paths and validate again.

7. Impact on Data
None.  
Configuration only affects where data is written, not what is written.

8. Impact on Architecture
Introduces centralized configuration

Enables environment portability

Reduces duplication

Improves maintainability

Establishes /includes as a reusable module

PART 6 — Common Functions Architecture
1. Problem
Each ingestion notebook contains repeated logic, including:

Adding ingestion date

Repeated imports

Repeated transformations

This causes:

Code duplication

Inconsistent logic across notebooks

Higher maintenance cost

Increased risk of errors

A centralized function library is required.

2. Constraints
Functions must be reusable across all ingestion notebooks.

Functions must be importable using %run.

Functions must operate on Spark DataFrames.

Functions must not require cluster restarts.

Functions must be simple, deterministic, and side‑effect free.

3. Design Decision
Create a dedicated notebook (common_functions.py) inside /includes.

Rationale:

Centralizes reusable logic

Ensures consistency

Reduces duplication

Improves readability

Supports modular architecture

4. Implementation
4.1 Create /includes/common_functions.py
Contains reusable functions such as:

add_ingestion_date(df)

Future functions (e.g., schema validation, audit logging)

4.2 Import functions
python
%run ../includes/common_functions
4.3 Replace repeated logic
Before:

python
df.withColumn("ingestion_date", current_timestamp())
After:

python
df = add_ingestion_date(df)
5. Code
python
# ============================================
# common_functions.py
# Shared reusable functions
# ============================================

from pyspark.sql.functions import current_timestamp

def add_ingestion_date(input_df):
    """
    Adds ingestion_date column with current timestamp.
    """
    return input_df.withColumn("ingestion_date", current_timestamp())
6. Validation
Import functions using %run.

Apply function to a DataFrame.

Confirm ingestion_date column is added.

Confirm timestamp is correct.

Confirm schema remains consistent.

7. Impact on Data
None.  
The ingestion_date column already existed.
This only centralizes the logic.

8. Impact on Architecture
Introduces reusable function library

Improves consistency

Reduces duplication

Supports modular design

Prepares pipeline for future enhancements

PART 7 — Implementation SOPs
SOP 1 — Importing Configuration
Steps
Add this at the top of the notebook:

python
%run ../includes/configuration
Replace all hardcoded paths with variables:

python
f"{raw_folder_path}/drivers.json"
SOP 2 — Importing Common Functions
Steps
Add this at the top:

python
%run ../includes/common_functions
Replace ingestion date logic:

python
df = add_ingestion_date(df)
SOP 3 — Adding Parameters
Steps
Define widget:

python
dbutils.widgets.text("p_data_source", "")
Retrieve value:

python
v_data_source = dbutils.widgets.get("p_data_source")
Add to DataFrame:

python
df = df.withColumn("data_source", lit(v_data_source))
SOP 4 — Notebook Chaining
Steps
Run child notebook:

python
result = dbutils.notebook.run("1.ingest_circuits", 0, {"p_data_source": "Ergast API"})
Validate:

python
if result != "success": raise Exception("Failure")
SOP 5 — Creating Databricks Jobs
Steps
Jobs → Create Job

Select notebook

Configure Job Cluster

Add parameters

Run job

Validate logs

PART 8 — Code Appendix & Validation Procedures
Appendix A — Full Ingestion Notebook Template
python
# Import configuration and functions
%run ../includes/configuration
%run ../includes/common_functions

# Parameters
dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

# Read
df = spark.read.json(f"{raw_folder_path}/circuits.json")

# Transform
df = df.withColumn("data_source", lit(v_data_source))
df = add_ingestion_date(df)

# Write
df.write.mode("overwrite").parquet(f"{processed_folder_path}/circuits")
Appendix B — Validation Procedures
1. Configuration Validation
Print folder paths

Validate access

Validate ABFS fallback

2. Function Validation
Apply function to sample DataFrame

Confirm ingestion_date added

3. Parameter Validation
Pass parameter manually

Confirm value appears in output

4. Workflow Validation
Run master notebook

Confirm sequential execution

Confirm failure stops pipeline

5. Job Validation
Trigger job

Confirm job cluster spins up

Confirm logs and run history
