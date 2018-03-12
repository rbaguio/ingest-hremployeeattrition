# ingest-hremployeeattrition
Ingest HR Employee Attrition by IBM Watson

| | |
|--:|:--|
| `author-name` | [IBM Watson](https://www.ibm.com/communities/analytics/watson-analytics-blog/guide-to-sample-datasets/)
| `data-source` | HR Employee Attrition |
| `data-files` | [`WA_Fn UseC_ HR Employee Attrition.csv`](https://community.watsonanalytics.com/wp-content/uploads/2015/03/WA_Fn-UseC_-HR-Employee-Attrition.csv) |

> **Environment paths**
>
> | | |
> |--:|:--|
> | `repo://` | [GitHub](https://github.com/dataseer-carl/ingest-hremployeeattrition.git)
> | `data://` | [GDrive](https://drive.google.com/drive/folders/1hOHLPmvDvycpnxNYOMgIV5Z6uVcoSyuq?usp=sharing) |
> | Tracker | [Trello](https://trello.com/b/RU87srsJ) |

## Documentation

| Document | Location |
|:--|:--|
| Raw data dictionary | [`data:///docs/IBM Watson - HR Employee Attrition data dictionary`](https://docs.google.com/document/d/1mEhNCV_y2L9-2_3Zht9-hIc2Ts26st50KFvIOC1IDQQ/edit?usp=sharing) |
| Fabricated data schema design | [`data:///docs/HR db`](https://docs.google.com/document/d/1zEPq1AugDTmH0Talx7ACLHrWa-q4JgotMNiIrMbWhqI/edit?usp=sharing) |

## Data files

### Raw

| Data name | Description | Data filepath | GDrive ID |
|:--|:--|:--|:--|
| *HR Employee Attrition* | Current "Singe Employee View" | [`data:///raw/WA_Fn-UseC_-HR-Employee-Attrition.csv`](https://drive.google.com/open?id=1p-Pb-bVYD5xD3xjbHF9GpyUix15JJUZ3) |`1p-Pb-bVYD5xD3xjbHF9GpyUix15JJUZ3`|

### Fabricated

#### Pre-fabrication

Ingestion (parsing and cleaning) of raw data files.

| Data name | Description | Data filepath | GDrive ID | Input data | Processing script |
|:--|:--|:--|:--|:--|:--|
| Raw ingest | Raw ingest of *HR Employee Attrition* | [`data:///data/data00_raw ingest.rds`](https://drive.google.com/open?id=1D3cyht8tytCJrbxEwxcBd_o1palVLD7l) |`1D3cyht8tytCJrbxEwxcBd_o1palVLD7l`| *HR Employee Attrition* raw | `script00_raw ingest.R` |
| Parsed ingest | Parsed ingest of *HR Employee Attrition* | [`data:///data/data01_raw ingest.rds`](https://drive.google.com/open?id=1DN3gt-cV3xWUONNXpdQQy58mV4ksvCvm) |`1DN3gt-cV3xWUONNXpdQQy58mV4ksvCvm`| *HR Employee Attrition* raw ingest | `script01_clean ingest.ipynb` |
| Separated raw data | Separated *HR Employee Attrition* datasets per table | [`data:///data/data02_separated prefab.rds`](https://drive.google.com/open?id=1gw9tDFMCwAfu7ifbEruaUc0mdOGNwbhQ) |`1gw9tDFMCwAfu7ifbEruaUc0mdOGNwbhQ`| *HR Employee Attrition* parsed ingest | `script02_prefab.R` |
| Pre-employee action logs | For *employee action logs* | [`data:///data/data03_preAction.csv`](https://drive.google.com/open?id=1kqVQn4PqZIlyQVexUxYwoNgH5SIf2-Yd) |`1kqVQn4PqZIlyQVexUxYwoNgH5SIf2-Yd`|  | `script03_prep fab.R` |
| Pre-employee profiles | For *employee profiles* | [`data:///data/data03_Profiles.csv`](https://drive.google.com/open?id=1VE8kpX_Ojh1ZVVTK7wYycZ-Cl1bYShoL) |`1VE8kpX_Ojh1ZVVTK7wYycZ-Cl1bYShoL`|  | `script03_prep fab.R` |
| Pre-survey results | For *survey results* | [`data:///data/data03_Surveys.csv`](https://drive.google.com/open?id=19i0rF0Gd4Wlx20MId_K_0s85IB_zU0NV) |`19i0rF0Gd4Wlx20MId_K_0s85IB_zU0NV`|  | `script03_prep fab.R` |
| Pre-personnel roles list | For *personnel roles* | [`data:///data/data03_Roles.csv`](https://drive.google.com/open?id=1-V3BQ1emBvQiGKCXf69tufTtusJuBkId) |`1-V3BQ1emBvQiGKCXf69tufTtusJuBkId`|  | `script03_prep fab.R` |
| Pre-request logs | For *request logs* | [`data:///data/data03_Requests.csv`](https://drive.google.com/open?id=1E5DFMab_WQHsJVU5pgz9xE7kopZvGs3z) |`1E5DFMab_WQHsJVU5pgz9xE7kopZvGs3z`|  | `script03_prep fab.R` |