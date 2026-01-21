SAS Shared Access Signature

    Provides fine grained access to the storage
    Restricted Access to specifi resource types/services
    Allow specific permisssions
    Restrict access to specific time period
    limit access to specific IP addresses
    Recommended access pattern for external clients

Summary:
With this level of fine grained access control offered, 
SAS tokens are the recommended access pattern for external clients, 
who cannot be trusted with full access to your storage account.

Command FORMAT:

The first parameter here defines the authentication type as SAS or Shared Access Signature.
The second one defines the SAS token provider to fixed SAS token provider, and the last one is the
one in which we will set the value of the SAS token.
Using these configuration parameters, Databricks will be able to now authenticate to the storage account.

```code
spark.conf.set("fs.azure.account.auth.type.uzi786.dfs.core.windows.net", "SAS")
spark.conf.set("fs.azure.sas.token.provider.type.uzi786.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
spark.conf.set("fs.azure.sas.fixed.token.uzi786.dfs.core.windows.net", "")
```

