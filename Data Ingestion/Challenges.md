RAW → BRONZE Ingestion — Complete Challenge Inventory

1) Path & Storage Challenges
1.1 HTTPS vs ABFSS confusion

        Spark cannot read/write using HTTPS blob URLs
        Required converting to ABFSS
        Required correct container + account naming
        Required understanding Gen2 filesystem protocol

1.2 Folder vs file ingestion

    Some datasets are folders containing multiple files
    Spark must read the folder, not individual files
    Needed to validate with dbutils.fs.ls()
_____________________________________________________________________________________________________________________________________________________
2) File Format Challenges

2.1 Multi‑line JSON ingestion

    JSON files contained multiple objects
    Spark default expects single‑line JSON
    Required .option("multiLine", True)
    Required schema definition to avoid inference errors

2.2 Multiple files per dataset

    lap_times → multiple CSV files
    qualifying → multiple multi‑line JSON files
    pit_stops → single multi‑line JSON
    Needed consistent ingestion logic

2.3 Missing headers in CSV

    lap_times had no header
    Spark would misinterpret first row as header
    Required manual schema definition

_____________________________________________________________________________________________________________________________________________________
3) Schema & Data Type Challenges

3.1 Manual schema creation

    Needed StructType / StructField
    Needed correct IntegerType / StringType mapping
    Needed to avoid Spark’s incorrect inference

3.2 Nullable vs non‑nullable fields

    Understanding Spark’s behavior:
    Allows NULLs during read
    Rejects NULLs during write if schema says nullable=False
    Required NULL detection before writing

3.3 Consistency across datasets

    Ensuring race_id, driver_id, constructor_id always match type
    Avoiding type drift between datasets

_____________________________________________________________________________________________________________________________________________________
4) Transformation Challenges

4.1 Renaming conventions

    Converting camelCase → snake_case
    Ensuring consistent naming across all datasets
    Avoiding mismatches in downstream joins

4.2 Adding ingestion_date

    Required current_timestamp()
    Required correct import
    Ensured metadata consistency across all Bronze tables

4.3 Column ordering

    Ensuring ingestion_date appears at the end
    Ensuring renamed columns appear in correct order

_____________________________________________________________________________________________________________________________________________________
5) Code & Syntax Challenges

5.1 Multi‑line import syntax error

    Python does not allow line breaks without parentheses
    Required fixing import formatting

5.2 Missing imports

Needed to import:

    StructType, StructField, IntegerType, StringType
    current_timestamp
    Earlier datasets didn’t require these, causing confusion

5.3 Path string formatting

    Ensuring trailing slash
    Ensuring correct container spelling
    Ensuring correct account name

_____________________________________________________________________________________________________________________________________________________
6) Data Quality Challenges

6.1 Detecting NULLs before writing

    Required NULL count logic
    Required row-level NULL detection
    Prevented write failures due to non-nullable schema

6.2 Cleaning or filling missing values

    dropna
    fillna
    when/otherwise
    Ensuring business logic consistency

_____________________________________________________________________________________________________________________________________________________
7) Repeatability & Pattern Challenges
7.1 Creating a reusable ingestion pattern

        Read
        Schema
        Transform
        Write
        Validate

This pattern now applies to every dataset

7.2 Ensuring consistent Bronze output

    Parquet format
    Correct folder structure
    Correct naming
    Correct metadata columns

7.3 Avoiding drift between datasets

    Ensuring all ingestion notebooks follow the same SOP
    Ensuring consistent naming and metadata rules

_____________________________________________________________________________________________________________________________________________________
8) Environment & Platform Challenges
8.1 Databricks CE limitations

        No Unity Catalog
        No DBFS root persistence
        Required using ABFSS paths directly

8.2 Storage account permissions

    Required correct SAS or access configuration
    Required correct path formatting

_____________________________________________________________________________________________________________________________________________________
9) Human & Conceptual Challenges
9.1 Understanding why imports changed

        Earlier lessons didn’t require schema or timestamp
        Later lessons did
        Caused confusion about why imports suddenly appeared

9.2 Understanding why Spark behaves differently

    Why Spark allows NULLs during read
    Why Spark rejects NULLs during write
    Why multi-line JSON needs explicit options

_____________________________________________________________________________________________________________________________________________________
Final Summary (Architect‑Grade)

You solved challenges across:

    storage protocols
    file formats
    schema control
    transformation consistency
    data quality
    syntax correctness
    repeatable pipeline design
    platform constraints
    conceptual clarity
    
    This is the full mechanical truth of what you overcame.
