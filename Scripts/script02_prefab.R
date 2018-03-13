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

# Get Data ####

(data.files <- as_id(datastage.id) %>% drive_ls_from_id())

## _data01_parsed ingest.rds ####

### Download
cache.file <- "data01_parsed ingest.rds"
cachefile.id <- drive_sub_id(datastage.id, cache.file) # Get GDrive ID
cachefile.path <- file.path(proxydata.path, cache.file) # Set proxy data:// path
drive_download(as_id(cachefile.id), path = cachefile.path, overwrite = TRUE)

### Load
hr.df <- readRDS(cachefile.path)
str(hr.df)

# Separate Data ####

hr.source <- hr.df

## _Records ####

records.names <- c(
	"Gender", "Age", "MaritalStatus", "Education", "EducationField", "NumCompaniesWorked"
)
records.df <- hr.source %>% 
	mutate(
		priorWorkXP = TotalWorkingYears - YearsAtCompany
	) %>% 
	select(EmployeeNumber, one_of(records.names), priorWorkXP)
hr.source %<>% 
	select(-one_of(records.names), EducationField, -TotalWorkingYears, -DistanceFromHome)

## _Surveys ####

survey.names <- c(
	## Satisfaction survey
	"EnvironmentSatisfaction", "RelationshipSatisfaction", "JobSatisfaction", 
	"JobInvolvement", "WorkLifeBalance",
	## Performance appraisal
	"PerformanceRating"
)
survey.df <- hr.source %>% select(EmployeeNumber, one_of(survey.names))
hr.source %<>% select(-one_of(survey.names))

## _Roles ####

role.names <- c("Department", "JobLevel", "JobRole", "EducationField")
role.df <- hr.source %>% 
	select(one_of(role.names)) %>% 
	distinct() %>% 
	arrange(Department, JobLevel, JobRole) %>% 
	mutate(
		Dept.code = abbreviate(Department, minlength = 3),
		Role.code = abbreviate(JobRole, minlength = 4) %>% tolower(),
		RoleID = paste(Dept.code, JobLevel, Role.code, sep = "-")
	) %>% 
	select(-Dept.code, -Role.code)

## Check if RoleID is a valid key
n_distinct(role.df$RoleID) # 31
nrow(role.df) # 31

hr.source %<>% 
	left_join(role.df) %>% 
	select(-Department, -JobLevel, -JobRole)

## _Requests ####
### Does not include transfers and personnel requests

request.names <- c("BusinessTravel", "OverTime", "TrainingTimesLastYear")
request.df <- hr.source %>% 
	select(EmployeeNumber, one_of(request.names))
hr.source %<>% select(-one_of(request.names))

# Save separations ####

hr.ls <- list(
	preAction = hr.source,
	Profiles = records.df,
	Surveys = survey.df,
	Roles = role.df,
	Requests = request.df
)

separated.file <- "data02u_separated prefab.rds"
#### Save to proxy data://
separated.filepath <- file.path(proxydata.path, separated.file)
saveRDS(hr.ls, separated.filepath)
#### Stage to data://
drive_upload(separated.filepath, as_id(datastage.id), separated.file)
#### Get ID
drive_ls_from_id(as_id(datastage.id))
drive_sub_id(as_id(datastage.id), separated.file)
# 1gw9tDFMCwAfu7ifbEruaUc0mdOGNwbhQ