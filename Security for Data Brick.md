Complete Notes: Accessing Azure Data Lake Storage (ADLS) from Databricks

    1. One word: Access
    2. Two words: Storage access
    3. Business analogy:

Think of ADLS as a warehouse.

Databricks is a forklift.

To enter the warehouse, the forklift must present one of four types of keys:

      Master Key (Storage Access Key)
      
      Temporary Pass (SAS Token)
      
      Employee Badge (Service Principal)
      
      Cluster Badge (Cluster Scoped Credentials)

Each method gives a different level of control and security.
```text
+-----------------+        +----------------------+        +------------------------+        +-----------------------------+
|     Customer    |        |   Application /      |        |   Service Principal    |        |     Azure Data Lake         |
| (User, Client)  | -----> |   Databricks / App   | -----> | (App Identity in AAD)  | -----> | (Storage Account + Containers) |
+-----------------+        +----------------------+        +------------------------+        +-----------------------------+
          |                          |                               |                                   |
          | 1. Sends request         |                               |                                   |
          | (UI, API, Notebook)      |                               |                                   |
          v                          |                               |                                   |
+-----------------+                  |                               |                                   |
|  Business Logic |------------------+                               |                                   |
+-----------------+  2. Needs data from ADLS                        |                                   |
                                   v                                |                                   |
                         +----------------------+                   |                                   |
                         |  Auth Config in     |--------------------+                                   |
                         |  Notebook / App     |   3. Use SP creds (client_id, secret, tenant_id)       |
                         +----------------------+                                                       |
                                   |                                                                    |
                                   v                                                                    |
                         +----------------------+                                                       |
                         |  Azure AD (AAD)     |<------------------------------------------------------+
                         +----------------------+   4. Issue token for Service Principal
                                   |
                                   v
                         +-----------------------------+
                         |   Azure Data Lake Storage   |
                         |   (Authorized via RBAC)     |
                         +-----------------------------+
                                   |
                                   v
                         5. Data returned to Application
                                   |
                                   v
                         6. Response back to Customer

```
------------------------------------------------------------
SECTION 1 — ACCESS KEYS (MASTER KEY)
------------------------------------------------------------
Why we need this?
Because the storage account key is the root password for the entire ADLS account.

If Databricks has this key, it can:

      Read any file
      
      Write any file
      
      Delete any file
      
      List any container

This is full, unrestricted access.

Where do we get this from?

Azure Portal → Storage Accounts → uzi786 →

Security + Networking → Access Keys

we will see:

Key1

Key2

Connection strings

we copy Key1 or Key2.

Why we need the HTTPS URL?

Azure Portal shows the file as:

```Code
https://uzi786.blob.core.windows.net/demo/circuits.csv
```
This is the Blob endpoint.

Databricks does NOT use this directly.

But you use it to confirm:

Storage account name = uzi786

Container name = demo

File name = circuits.csv

Why we need the ABFSS URL?

Databricks uses the ADLS Gen2 filesystem endpoint, not the blob endpoint.

So you convert:

```Code
https://uzi786.blob.core.windows.net/demo/circuits.csv
```
to:

```Code
abfss://demo@uzi786.dfs.core.windows.net/circuits.csv
```
This is the path Spark understands.

Command: Set Access Key in Databricks

```spark
spark.conf.set(
  "fs.azure.account.key.uzi786.dfs.core.windows.net",
  "<your-access-key>"
)
```
This tells Spark:

“Use this master key whenever accessing ADLS.”

Command: List files
```Code

display(dbutils.fs.ls("abfss://demo@uzi786.dfs.core.windows.net/"))
```

Command: Read file

```Code

display(
  spark.read.csv("abfss://demo@uzi786.dfs.core.windows.net/circuits.csv")
)
```
------------------------------------------------------------
SECTION 2 — SAS TOKEN (TEMPORARY PASS)
------------------------------------------------------------
Why we need this?

Because SAS tokens allow:

    Read‑only access
    
    Write‑only access
    
    Time‑limited access
    
    IP‑restricted access

This is safer than giving the master key.

Where do we get this from?

Azure Portal → Storage Accounts → uzi786 →

Shared access signature

You configure:

    Allowed services
    
    Allowed resource types
    
    Allowed permissions
    
    Start time
    
    Expiry time
    
    Allowed IPs
    
    Then Azure generates a SAS token.

Command: Configure SAS in Databricks

```Code
spark.conf.set("fs.azure.account.auth.type.uzi786.dfs.core.windows.net", "SAS")
spark.conf.set("fs.azure.sas.token.provider.type.uzi786.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
spark.conf.set("fs.azure.sas.fixed.token.uzi786.dfs.core.windows.net", "<sas-token>")
```
List files

```Code
display(dbutils.fs.ls("abfss://demo@uzi786.dfs.core.windows.net"))
Read file
Code
display(
  spark.read.csv("abfss://demo@uzi786.dfs.core.windows.net/circuits.csv")
)
```
------------------------------------------------------------
SECTION 3 — SERVICE PRINCIPAL (EMPLOYEE BADGE)
------------------------------------------------------------
Why we need this?
Because this is the enterprise‑grade method.

It allows:

    Identity‑based access
    
    Role‑based permissions
    
    No keys
    
    No tokens
    
    No expiry issues

This is the method used in real companies.

Where do we get the values?

1. Client ID

Azure Portal → Azure Active Directory → App Registrations → Your App → Application (client) ID

2. Tenant ID

Azure Portal → Azure Active Directory → Tenant ID

3. Client Secret

Azure Portal → App Registration → Certificates & Secrets → New client secret

4. Assign RBAC

Storage Account → Access Control (IAM) → Add Role Assignment →

Storage Blob Data Contributor → Select your App

Command: Configure OAuth
```Code
spark.conf.set("fs.azure.account.auth.type.uzi786.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.uzi786.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.uzi786.dfs.core.windows.net", client_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.uzi786.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.uzi786.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")
```
List files
```Code
display(dbutils.fs.ls("abfss://demo@uzi786.dfs.core.windows.net"))
```
Read file
```Code
display(
  spark.read.csv("abfss://demo@uzi786.dfs.core.windows.net/circuits.csv")
)
```

------------------------------------------------------------
SECTION 4 — CLUSTER SCOPED CREDENTIALS (CLUSTER BADGE)
------------------------------------------------------------

Why we need this?

    Because instead of setting credentials in the notebook,
    
    you set them once at the cluster level.
    
    This is useful when:
    
    Many notebooks need the same access
    
    You want central control
    
    You want to avoid storing secrets in code
    
    Where do we configure this?
    
    Databricks → Compute → Your Cluster →
    
    Advanced Options → Spark → Spark Config

You add:

```Code
fs.azure.account.key.uzi786.dfs.core.windows.net <your-key>
```
List files
```Code
display(dbutils.fs.ls("abfss://demo@uzi786.dfs.core.windows.net"))
```
Read file
```Code
display(
  spark.read.csv("abfss://demo@uzi786.dfs.core.windows.net/circuits.csv")
)
```

------------------------------------------------------------
FINAL SUMMARY TABLE
------------------------------------------------------------
Method	Security Level	Where Value Comes From	Best Use Case
Access Key	Weak	Storage Account → Access Keys	Quick testing
SAS Token	Medium	Storage Account → Shared Access Signature	Temporary or restricted access
Service Principal	Strong	Azure AD → App Registration	Enterprise production
Cluster Scoped	Medium	Databricks Cluster Config	Shared cluster access
