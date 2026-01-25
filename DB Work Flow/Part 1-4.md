ENGINEERING DESIGN DOCUMENT — PARTS 1–4
Productionizing Databricks Ingestion Notebooks  
Author: Usman Zafar
Style: Engineering Design Document
Scope: Notebook Reuse, Parameterization, Notebook Workflows, Databricks Jobs

PART 1 — Notebook Reuse Using %run
1. Problem
The ingestion notebooks contain repeated logic and hardcoded values.
Examples include:

Hardcoded folder paths for RAW, PROCESSED, PRESENTATION

Repeated ingestion‑date logic

Repeated imports

Repeated helper logic

This creates:

High maintenance overhead

High risk of inconsistency

Difficulty migrating between DEV → TEST → PROD

Difficulty debugging

Difficulty enforcing standards across notebooks

A mechanism is required to reuse code across notebooks without duplication.

2. Constraints
Databricks notebooks do not support traditional Python module imports unless files are stored in DBFS or workspace.

The reuse mechanism must work inside Databricks notebooks, not only Python scripts.

The mechanism must allow importing:

Variables

Functions

Constants

Configuration

The mechanism must not require cluster restarts.

The mechanism must support relative paths.

3. Design Decision
Use the Databricks %run magic command to import the contents of one notebook into another.

Rationale:

%run executes the target notebook in the same context

All variables, functions, and imports become available

Supports relative paths

Supports modular architecture

Enables centralization of configuration and common functions

No cluster restart required

Works across all Databricks runtimes

4. Implementation
4.1 Create an includes folder
Code
/includes
    configuration.py
    common_functions.py
4.2 Use %run to import notebooks
Each ingestion notebook begins with:

python
%run ../includes/configuration
%run ../includes/common_functions
4.3 Replace hardcoded values with imported variables
Example:

Before:

python
"/mnt/formula1dl/raw/circuits.json"
After:

python
f"{raw_folder_path}/circuits.json"
4.4 Replace repeated logic with imported functions
Before:

python
df.withColumn("ingestion_date", current_timestamp())
After:

python
df = add_ingestion_date(df)
5. Code
configuration.py
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
common_functions.py
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
Run %run ../includes/configuration

Confirm variables load

Confirm no errors

Run %run ../includes/common_functions

Confirm functions load

Execute ingestion notebook

Confirm folder paths resolve correctly

Confirm ingestion_date is added

Validate output

Schema unchanged

Data written to correct location

7. Impact on Data
None.  
No schema changes.
No Parquet rewrites.
Only code structure improved.

8. Impact on Architecture
Introduces modular architecture

Enables environment portability

Reduces duplication

Improves maintainability

Establishes /includes as a reusable code library

PART 2 — Parameterizing Notebooks Using Widgets
1. Problem
The ingestion notebooks must support multiple data sources:

Ergast API

Formula1 official website

Future sources

Hardcoding the data source inside each notebook:

Prevents reuse

Prevents automation

Prevents job‑level parameterization

Prevents environment‑specific overrides

A mechanism is required to pass parameters into notebooks at runtime.

2. Constraints
Parameters must be passed from:

Databricks Jobs

Notebook Workflows

Manual execution

Parameters must be accessible inside the notebook.

Parameters must support string values.

Parameters must be optional (default empty).

Parameters must integrate with Spark DataFrame operations.

3. Design Decision
Use Databricks Widgets to define and retrieve parameters:

dbutils.widgets.text()

dbutils.widgets.get()

Use lit() to convert Python strings into Spark column types.

4. Implementation
4.1 Define widget
python
dbutils.widgets.text("p_data_source", "")
4.2 Retrieve widget value
python
v_data_source = dbutils.widgets.get("p_data_source")
4.3 Add parameter to dataframe
python
from pyspark.sql.functions import lit

df = df.withColumn("data_source", lit(v_data_source))
4.4 Use parameter in downstream logic
Logging

Metadata

Partitioning (optional)

Lineage tracking

5. Code
python
dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

from pyspark.sql.functions import lit

df = df.withColumn("data_source", lit(v_data_source))
6. Validation
Set widget value manually

Run notebook

Read output Parquet

Confirm data_source column contains correct value

Confirm schema unchanged except for new column

7. Impact on Data
Yes — one new column added earlier:  
data_source STRING

This was already implemented in your pipeline.
No further changes required.

8. Impact on Architecture
Enables runtime parameterization

Enables job‑level overrides

Enables multi‑source ingestion

Enables environment‑specific configuration

PART 3 — Notebook Workflows Using dbutils.notebook.run()
1. Problem
The ingestion pipeline consists of eight notebooks.
Running them manually:

Is error‑prone

Is not scalable

Does not enforce dependencies

Does not support conditional execution

Does not support orchestration

A mechanism is required to chain notebooks and control execution flow.

2. Constraints
Must run notebooks sequentially.

Must detect failures.

Must pass parameters to child notebooks.

Must return status codes.

Must support conditional branching.

Must not require external orchestration tools (ADF will come later).

3. Design Decision
Use:

dbutils.notebook.run() to execute child notebooks

dbutils.notebook.exit() to return status codes

This creates a notebook workflow inside Databricks.

4. Implementation
4.1 Run a child notebook
python
result = dbutils.notebook.run(
    "../ingestion/1.ingest_circuits",
    0,
    {"p_data_source": "Ergast API"}
)
4.2 Exit from child notebook
python
dbutils.notebook.exit("success")
4.3 Conditional execution
python
if result != "success":
    raise Exception("Ingestion failed")
4.4 Chain all notebooks
Create a master notebook:

Code
0.ingest_all_files
5. Code
Master Notebook
python
result = dbutils.notebook.run("1.ingest_circuits", 0, {"p_data_source": "Ergast API"})
if result != "success": raise Exception("Circuits failed")

result = dbutils.notebook.run("2.ingest_drivers", 0, {"p_data_source": "Ergast API"})
if result != "success": raise Exception("Drivers failed")

...
Child Notebook Exit
python
dbutils.notebook.exit("success")
6. Validation
Run master notebook

Confirm each child notebook executes

Confirm failure stops pipeline

Confirm success returns correct status

Confirm parameters propagate correctly

7. Impact on Data
None.  
Workflow logic does not modify data.

8. Impact on Architecture
Introduces notebook‑level orchestration

Enables dependency control

Enables conditional execution

Prepares pipeline for ADF orchestration

PART 4 — Databricks Jobs
1. Problem
Running ingestion manually or via notebook workflows:

Does not support scheduling

Does not support automated retries

Does not support cluster lifecycle management

Does not support operational monitoring

Does not support run history

A mechanism is required to schedule ingestion notebooks and run them automatically.

2. Constraints
Must support manual and scheduled execution.

Must support job clusters.

Must support parameter passing.

Must support retries and timeouts.

Must support run history and logs.

Must not require external tools (ADF will come later).

3. Design Decision
Use Databricks Jobs to schedule and execute notebooks.

Rationale:

Native to Databricks

Supports job clusters

Supports parameters

Supports scheduling

Supports run history

Supports alerts

4. Implementation
4.1 Create Job
Jobs → Create Job

Name: F1 Ingestion

4.2 Configure Task
Task type: Notebook

Notebook: 0.ingest_all_files

Cluster: Job Cluster (Single Node recommended)

Parameters:

Code
p_data_source = "E API"
4.3 Configure Scheduling
Manual or Scheduled

Daily, hourly, weekly, etc.

4.4 Configure Advanced Settings
Retries: 0

Timeout: 0

Alerts: On failure

4.5 Run Job
Click Run Now

Inspect logs

Inspect run history

5. Code
Job Parameter Example
json
{
  "p_data_source": "E API"
}
Notebook Parameter Retrieval
python
v_data_source = dbutils.widgets.get("p_data_source")
6. Validation
Trigger job manually

Confirm job cluster spins up

Confirm notebook executes

Confirm parameters pass correctly

Confirm run history logs execution

Confirm cluster terminates after run

7. Impact on Data
None.  
Job execution does not modify data schema.

8. Impact on Architecture
Introduces scheduled execution

Introduces job clusters

Introduces operational monitoring

Prepares pipeline for ADF orchestration

END OF PARTS 1–4
When you're ready, I will produce:

Part 5 — Configuration Architecture

Part 6 — Common Functions Architecture

Part 7 — Implementation SOPs

Part 8 — Code Appendix + Validation Procedures
