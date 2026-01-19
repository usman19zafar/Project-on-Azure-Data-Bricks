```text
===============================================================
                 DATABRICKS DBUTILS — ECOSYSTEM MAP
===============================================================

                               ┌──────────────────────┐
                               │      dbutils         │
                               └──────────┬───────────┘
                                          │
     ┌────────────────────────────────────┼────────────────────────────────────┐
     │                                    │                                    │

┌──────────────┐                 ┌────────────────┐                 ┌────────────────┐
│ dbutils.fs   │                 │ dbutils.secrets│                 │ dbutils.widgets│
└───────┬──────┘                 └─────────┬──────┘                 └────────┬───────┘
        │                                  │                                 │
        │                                  │                                 │
 File operations                     Secret scopes & keys                 Notebook UI controls
 (DBFS / ADLS / S3)                  (secure credential mgmt)             (parameters, dropdowns)

        │                                  │                                    │
        ▼                                  ▼                                    ▼

 ls, cp, mv, rm,                     get, list, listScopes             text, dropdown,
 mkdirs, head, tail,                                                     combobox, multiselect,
 put, mount, unmount                                                     get, remove, removeAll


     ┌────────────────────────────────────┼────────────────────────────────────┐
     │                                    │                                    │

┌──────────────┐                 ┌────────────────┐                 ┌──────────────────┐
│ dbutils.jobs │                 │ dbutils.library│                 │ dbutils.notebook │
└───────┬──────┘                 └─────────┬──────┘                 └─────────┬────────┘
        │                                  │                                  │
        │                                  │                                  │
 Workflow task values               Install/uninstall libs               Run/exit notebooks
 (job orchestration)                (cluster-scoped)                     (pipeline chaining)

        │                                    │                                    │
        ▼                                    ▼                                    ▼

 taskValues.get/set                install, uninstall,                  run(path, args),
                                   restartPython                        exit(value)


                               ┌──────────────────────┐
                               │ dbutils.utilities    │
                               └──────────┬───────────┘
                                          │
                                          ▼
                                       help()

===============================================================
```

```mermaid
flowchart TD

    A[dbutils]

    subgraph FS[dbutils.fs]
        FS1[ls cp mv rm]
        FS2[mkdirs head tail]
        FS3[put mount unmount]
    end

    subgraph SEC[dbutils.secrets]
        SEC1[get]
        SEC2[list]
        SEC3[listScopes]
    end

    subgraph W[dbutils.widgets]
        W1[text dropdown]
        W2[combobox multiselect]
        W3[get remove removeAll]
    end

    subgraph JOB[dbutils.jobs]
        JOB1[taskValues get set]
    end

    subgraph LIB[dbutils.library]
        LIB1[install uninstall]
        LIB2[restartPython]
    end

    subgraph NB[dbutils.notebook]
        NB1[run notebook]
        NB2[exit notebook]
    end

    subgraph UTIL[dbutils.utilities]
        U1[help]
    end

    A --> FS
    A --> SEC
    A --> W
    A --> JOB
    A --> LIB
    A --> NB
    A --> UTIL
```
