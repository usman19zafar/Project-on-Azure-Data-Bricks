They exist because Databricks is a multi‑language, multi‑persona, multi‑workflow platform, and each magic command enables a different business capability.

1️⃣ %python — Business Purpose
Purpose: Enable data engineers to write PySpark, ETL logic, and automation in the most widely used language in data engineering.

Business value:

Faster development cycles

Larger talent pool

Easy integration with ML, APIs, automation

Reduces cost of training and onboarding

In short:  
Python = productivity + flexibility

2️⃣ %sql — Business Purpose
Purpose: Allow analysts, BI developers, and engineers to query data using SQL — the universal language of data.

Business value:

Democratizes access to data

Enables self‑service analytics

Reduces dependency on engineering teams

Standardizes transformations

In short:  
SQL = accessibility + governance

3️⃣ %scala — Business Purpose
Purpose: Provide access to Spark’s native, JVM‑level APIs for high‑performance workloads.

Business value:

Maximum performance for large ETL jobs

Access to low‑level Spark optimizations

Supports legacy Scala Spark pipelines

In short:  
Scala = performance + control

4️⃣ %r — Business Purpose
Purpose: Support data scientists who rely on R for statistical modeling and visualization.

Business value:

Enables cross‑functional collaboration

Supports specialized statistical workflows

Reduces tool fragmentation

In short:  
R = statistics + science

5️⃣ %md — Business Purpose
Purpose: Document pipelines, logic, decisions, and business rules directly inside the notebook.

Business value:

Improves knowledge transfer

Reduces operational risk

Creates audit‑ready documentation

Enhances collaboration

In short:  
Markdown = clarity + governance

6️⃣ %fs — Business Purpose
Purpose: Provide a simple interface for interacting with cloud storage (ADLS/S3/GCS).

Business value:

Quick validation of data landing

Faster debugging

Reduces dependency on cloud portal

Enables operational checks inside pipelines

In short:  
File system = visibility + control

7️⃣ %sh — Business Purpose
Purpose: Allow engineers to run operating‑system commands on the driver node.

Business value:

Environment debugging

Installing system tools

Checking network connectivity

Validating cluster configuration

In short:  
Shell = diagnostics + environment control

8️⃣ %pip — Business Purpose
Purpose: Install Python libraries directly into the cluster runtime.

Business value:

Rapid experimentation

Supports ML and API integrations

Reduces DevOps overhead

Enables custom ETL logic

In short:  
Pip = extensibility + speed

9️⃣ %run — Business Purpose, interconnecting the parent and child notebook. 

Purpose: Import reusable notebooks (shared functions, ETL modules, configs).

Business value:

Modular code

Reusable logic

Cleaner pipelines

Faster development

In short:  
Run = modularity + reuse

```text
+---------+------------------------+
| Command | Two‑word Purpose       |
+---------+------------------------+
| %python | Build Logic            |
| %sql    | Query Data             |
| %scala  | Optimize Performance   |
| %r      | Statistical Modeling   |
| %md     | Document Decisions     |
| %fs     | Inspect Storage        |
| %sh     | Diagnose Environment   |
| %pip    | Extend Runtime         |
| %run    | Reuse Code             |
+---------+------------------------+
```



%python, %sql, %scala, %r = switch to a different language for a specific cell
%md Markdown for documenting notebooks
%fs = Run file system commands
%sh = Run shell commands (Driver Node Only)
%pip = Install Python liberaries
%run = include/ Import another notebook into the currnt notebook

```code
+---------+-------------------------------------------+-------------------------------------------+
| Command | Definition                                 | Utility / SOP                             |
+---------+-------------------------------------------+-------------------------------------------+
| %python | Run Python code in the current cell        | Use when writing PySpark, Python logic,   |
|         |                                            | UDFs, ETL transformations.                |
+---------+-------------------------------------------+-------------------------------------------+
| %sql    | Run SQL queries in the current cell        | Use for table queries, DDL, DML,          |
|         |                                            | aggregations, Delta operations.           |
+---------+-------------------------------------------+-------------------------------------------+
| %scala  | Run Scala code in the current cell         | Use for Spark internals, performance      |
|         |                                            | tuning, JVM-based transformations.        |
+---------+-------------------------------------------+-------------------------------------------+
| %r      | Run R code in the current cell             | Use for statistical analysis, R notebooks |
|         |                                            | or ML workflows using R.                  |
+---------+-------------------------------------------+-------------------------------------------+
| %md     | Render Markdown in the cell                | Use for documentation, headings, notes,   |
|         |                                            | diagrams, explanations.                   |
+---------+-------------------------------------------+-------------------------------------------+
| %fs     | Run Databricks File System commands        | Use for listing, copying, moving,         |
|         | (dbutils.fs wrapper)                       | deleting files in DBFS/ADLS/S3.           |
+---------+-------------------------------------------+-------------------------------------------+
| %sh     | Run shell commands on the driver node      | Use for Linux commands, pip installs,     |
|         |                                            | debugging environment issues.             |
+---------+-------------------------------------------+-------------------------------------------+
| %pip    | Install Python libraries into the cluster  | Use for installing packages needed for    |
|         |                                            | notebooks (cluster-scoped).               |
+---------+-------------------------------------------+-------------------------------------------+
| %run    | Import/execute another notebook            | Use for modular code, shared functions,   |
|         |                                            | reusable ETL logic.                       |
+---------+-------------------------------------------+--------------------------------------------+
```

1️⃣ %python — Definition, Utility, SOP
Definition:
Executes Python code in the current notebook cell.

Utility:
Used for PySpark, ETL logic, UDFs, data transformations, plotting.

SOP:
Code
%python
df = spark.read.csv("/path")
df.display()


2️⃣ %sql — Definition, Utility, SOP
Definition:
Executes SQL queries directly in the notebook.

Utility:
DDL, DML, Delta operations, aggregations, table creation.

SOP:
```Code
%sql
SELECT * FROM silver.orders LIMIT 10;
```

3️⃣ %scala — Definition, Utility, SOP
Definition:
Runs Scala code in the cell.

Utility:
Used for JVM-level Spark operations, performance tuning, advanced APIs.

SOP:
```Code
%scala
val df = spark.read.json("/path")
df.show()
```

4️⃣ %r — Definition, Utility, SOP
Definition:
Runs R code in the cell.

Utility:
Statistical analysis, R-based ML, visualization.

SOP:
```Code
%r
library(ggplot2)
```

5️⃣ %md — Definition, Utility, SOP
Definition:
Renders Markdown.

Utility:
Documentation, headings, diagrams, explanations.

SOP:
```Code
%md
# Bronze Layer
Raw ingestion zone.
```

6️⃣ %fs — Definition, Utility, SOP
Definition:
Runs Databricks File System commands (wrapper around dbutils.fs).

Utility:
List, copy, move, delete files in DBFS/ADLS/S3.

SOP:
```Code
%fs ls abfss://demo@storage.dfs.core.windows.net/
```

7️⃣ %sh — Definition, Utility, SOP

Definition:
Runs shell commands on the driver node.

%sh is like telling the Databricks computer:
“Hey robot, do something in your house, not in my notebook.”

Your notebook is one room.
The robot’s house (the driver node) is another room.

When you write:

```Code
%sh
ls
```
%sh is You’re saying: “Robot, go to your room and tell me what’s inside your closet.”

🧸 Even simpler
%python → talk in Python

%sql → talk in SQL

%sh → talk to the computer like it’s a robot that understands computer commands
Utility:
Linux commands, debugging, environment checks.

Two‑word logic
Robot commands

SOP:
```Code
%sh
ls -l
```
8️⃣ %pip — Definition, Utility, SOP
Definition:
Installs Python libraries into the cluster environment.

Utility:
Add missing packages for ML, ETL, APIs.

SOP:
```Code
%pip install pandas```
```
9️⃣ %run — Definition, Utility, SOP

Definition:
Imports and executes another notebook.

Utility:
Modular ETL, shared functions, reusable code blocks.

SOP:
```Code
%run ./Includes/Setup
```
