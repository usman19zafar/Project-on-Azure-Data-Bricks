SOP: Ingesting circuits.csv from Raw → Process (Parquet)
1. Purpose
Ingest the circuits.csv file from the raw container, apply required transformations, and write the cleaned output to the process container in Parquet format.

______________________________________________________________________________________________________________________________________________________________
2. Inputs
Source file: circuits.csv

Source location: Raw container

Target location: Process container

Input columns:

circuitId, circuitRef, name, location, country, lat, lng, alt, url
______________________________________________________________________________________________________________________________________________________________
3. Outputs
Parquet file stored in the process container

Cleaned, standardized schema

Audit column: ingestion_date

______________________________________________________________________________________________________________________________________________________________
4. Responsibilities
Data Engineer: Execute ingestion logic

Data Architect: Ensure naming standards and schema consistency

Platform: Databricks (Spark DataFrame APIs)

______________________________________________________________________________________________________________________________________________________________
5. Procedure
Step 1 — Read CSV Using DataFrame Reader
Action: Load the raw CSV file into a Spark DataFrame using the Reader API.
Intent: Bring raw data into Spark for transformation.

Step 2 — Rename Columns (CamelCase → snake_case)
Action: Convert circuitId → circuit_id, circuitRef → circuit_ref.
Intent:

Enforce Python/PySpark naming standards

Improve readability in SQL (case‑insensitive environment)

Ensure consistent naming across Bronze → Silver → Gold layers

Step 3 — Expand Abbreviated Columns
Action: Rename:

lat → latitude

lng → longitude

alt → altitude  
Intent: Improve clarity and semantic meaning of fields.

______________________________________________________________________________________________________________________________________________________________
Step 4 — Drop Unnecessary Columns
Action: Remove the url column.
Intent:

Reduce noise

Remove non‑analytical fields

Optimize storage and schema clarity

______________________________________________________________________________________________________________________________________________________________
Step 5 — Add Audit Column
Action: Add ingestion_date with current timestamp.
Intent:

Enable traceability

Support audit and lineage requirements

Track when data entered the process layer

______________________________________________________________________________________________________________________________________________________________
Step 6 — Enforce Correct Data Types
Action: Cast numeric and geographic fields to appropriate types.
Intent:

Ensure Parquet output has correct schema

Support analytical workloads and SQL queries

______________________________________________________________________________________________________________________________________________________________
Step 7 — Write Data to Process Container (Parquet)
Action: Use DataFrame Writer API to save the transformed DataFrame as Parquet.
Intent:

Store optimized, columnar data

Prepare dataset for downstream analytics, ML, and SQL workloads

______________________________________________________________________________________________________________________________________________________________
6. Acceptance Criteria
DataFrame loads successfully from raw container

All renamed columns follow snake_case

Abbreviated fields expanded to meaningful names

url column removed

ingestion_date column present with correct timestamp

Schema validated with correct data types

Output written to process container in Parquet format

No errors during read/transform/write steps

______________________________________________________________________________________________________________________________________________________________
7. Notes
Column renaming is recommended but optional

Parquet is chosen for performance and analytics suitability

This ingestion pattern will be reused for other datasets
