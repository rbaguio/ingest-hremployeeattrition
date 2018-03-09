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

| Data name | Description | Data filepath | GDrive ID | Input data | Processing script |
|:--|:--|:--|:--|:--|:--|
| Raw ingest | Raw ingest of *HR Employee Attrition* | [`data:///data/data00_raw ingest.rds`](https://drive.google.com/open?id=1D3cyht8tytCJrbxEwxcBd_o1palVLD7l) |`1D3cyht8tytCJrbxEwxcBd_o1palVLD7l`| *HR Employee Attrition* | `script00_raw ingest.R` |
