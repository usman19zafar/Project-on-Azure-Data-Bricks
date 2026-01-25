STEP 1: Create a folder name = presentation in azure storage account

Step 2: get the paths to read the data

```code
circuits_df = spark.read.parquet("abfss://aibronzelayer@uzi786.dfs.core.windows.net/circuits")
races_df = spark.read.parquet("abfss://aibronzelayer@uzi786.dfs.core.windows.net/races")
drivers_df = spark.read.parquet("abfss://aibronzelayer@uzi786.dfs.core.windows.net/drivers")
constructors_df = spark.read.parquet("abfss://aibronzelayer@uzi786.dfs.core.windows.net/constructor")
results_df = spark.read.parquet("abfss://aibronzelayer@uzi786.dfs.core.windows.net/results")
```


