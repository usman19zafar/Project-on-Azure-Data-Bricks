Requirements:

    Ingest All Files into the data lake
    Ingested data must have the schema application
    injested data must have audit columns
    ingested data must be stored in columnar format 
    must be able to analyze the ingested data via SQL
    ingestion logic must be able to handle incremental load

Structured Summary: Data Ingestion Overview

1. Project Ingestion Requirements

        Ingest all raw Formula 1 files into the processed container.
        Apply correct schemas (column names + data types).
        Add audit columns
        ingestion_date
        data_source

Store ingested data as Parquet.

      Ensure data is usable for:
      Machine learning
      Transformations for reporting
      SQL-based analytics
      Build ingestion logic that supports incremental loads (future lesson).


2. Spark Capabilities for Ingestion

Input Sources
1, Files: CSV, JSON, etc.

Tables
Real-time streams

ETL Flow
Read input data

2, Transform:

    Apply schema
    Fix data quality issues
    Perform aggregations
    Write output to:
    File stores
    Databases
    Streams

Spark APIs Used

    DataFrame Reader API → read data
    DataFrame API → transform data
    DataFrame Writer API → write data

These three APIs form the backbone of the ingestion pipeline.

3. Three-Part Ingestion Plan

Portion 1:
Process CSV files.

Portion 2:
Process JSON files.

Portion 3:
Process split CSV + JSON files.

Build reusable ingestion logic aligned with the project’s architectural requirements.
