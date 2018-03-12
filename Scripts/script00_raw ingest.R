# Ingestion script header ################################################

library(googledrive)
drive_auth()

source("./Scripts/template_fxns.R") # RStudio
# source("./template_fxns.R") # Jupyter

## data://
datapath.id <- as_id("1hOHLPmvDvycpnxNYOMgIV5Z6uVcoSyuq")

## proxy data://
proxydata.path <- file.path(".", "Data") # For RStudio
# proxydata.path <- file.path("..", "Data") # For Jupyter

## Get IDs of raw data file dump and Data stage
rawdump.id <- drive_sub_id(datapath.id, "raw")
datastage.id <- drive_sub_id(datapath.id, "data")

#************************************************************************#

## ls of raw data file dump
(rawdata.files <- drive_ls_from_id(rawdump.id))

## _WA_Fn-UseC_-HR-Employee-Attrition.csv ####

### __Download ####
raw.file <- "WA_Fn-UseC_-HR-Employee-Attrition.csv"
rawfile.id <- drive_sub_id(rawdump.id, raw.file) # Get GDrive ID
rawfile.path <- file.path(proxydata.path, raw.file) # Set proxy data:// path
drive_download(as_id(rawfile.id), path = rawfile.path, overwrite = TRUE)

### __Import ####

library(readr)

hr.raw <- read_csv(
	rawfile.path,
	col_types = cols(
	  .default = col_number(), # Unless specified below, parse as integer
	  Attrition = col_character(),
	  BusinessTravel = col_character(),
	  Department = col_character(),
	  EducationField = col_character(),
	  EmployeeNumber = col_character(),
	  Gender = col_character(),
	  JobRole = col_character(),
	  MaritalStatus = col_character(),
	  Over18 = col_character(),
	  OverTime = col_character()
	)
)

### Inspect columns
#### Discrete integers that could be coded columns
#### Dummy fields (only 1 unique value)

### __Fix metadata ####

lapply(hr.raw, unqSort)

#### Discrete integer
### Education
### EnvironmentSatisfaction
### JobInvolvement
### JobLevel
### JobSatisfaction
### PerformanceRating
### RelationshipSatisfaction
### StockOptionLevel
### WorkLifeBalance

#### Dummy fields
### Over18
### EmployeeCount
### StandardHours

library(dplyr)
library(stringr)

hr.df <- hr.raw %>% 
	# Remove dummy fields
	select(-EmployeeCount, -Over18, -StandardHours) %>% 
	# Create factors
	mutate(
		# Factors
		Attrition = as.factor(Attrition),
		OverTime = as.factor(OverTime),
    Department = as.factor(Department),
    Gender = as.factor(Gender),
    MaritalStatus = as.factor(MaritalStatus),
    StockOptionLevel = as.factor(StockOptionLevel),
    BusinessTravel = BusinessTravel %>% 
      str_replace_all(c("^Travel_" = "")) %>% 
      factor(c("Non-Travel", "Rarely", "Frequently")),
	  Education = factor(
	      Education,
	      levels = 1:5, labels = c("Below College", "College", "Bachelor", "Master", "Doctor")
	  ),
	  EnvironmentSatisfaction = factor(
	      EnvironmentSatisfaction,
	      levels = 1:4, labels = c("Low", "Medium", "High", "Very high")
	  ),
	  JobInvolvement = factor(
	      JobInvolvement,
	      levels = 1:4, labels = c("Low", "Medium", "High", "Very high")
	  ),
	  JobSatisfaction = factor(
	      JobSatisfaction,
	      levels = 1:4, labels = c("Low", "Medium", "High", "Very high")
	  ),
	  PerformanceRating = factor(
	      PerformanceRating,
	      levels = 1:4, labels = c("Low", "Good", "Excellent", "Outstanding")
	  ),
	  RelationshipSatisfaction = factor(
	      RelationshipSatisfaction,
	      levels = 1:4, labels = c("Low", "Medium", "High", "Very high")
	  ),
	  WorkLifeBalance = factor(
	      WorkLifeBalance,
	      levels = 1:4, labels = c("Bad", "Good", "Better", "Best")
	  ),
	  # Prettify
	  EmployeeNumber = str_pad(
	      EmployeeNumber,
	      max(str_length(EmployeeNumber)),
	      side = "left", pad = "0"
	  )
	)

### __Output ####

ingested.file <- "data00_raw ingest.rds"
#### Save to proxy data://
ingested.filepath <- file.path(proxydata.path, ingested.file)
saveRDS(hr.df, ingested.filepath)
#### Stage to data://
drive_upload(ingested.filepath, as_id(datastage.id), ingested.file)
#### Get ID
drive_ls_from_id(as_id(datastage.id))
drive_sub_id(as_id(datastage.id), ingested.file)
# 1D3cyht8tytCJrbxEwxcBd_o1palVLD7l
