# Ingestion script header ################################################

library(googledrive)
drive_auth()

source("./scripts/template_fxns.R") # RStudio
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

## _data03_*.csv ####

### Download
cache.file <- "data02u_separated prefab.rds"
cachefile.id <- drive_sub_id(datastage.id, cache.file) # Get GDrive ID
cachefile.path <- file.path(proxydata.path, cache.file) # Set proxy data:// path
drive_download(as_id(cachefile.id), path = cachefile.path, overwrite = TRUE)

### Write to csv
hr.ls <- readRDS(cachefile.path)

pre.ls <- lapply(
	names(hr.ls),
	function(temp.data){
		temp.df <- hr.ls[[temp.data]]
		temp.file <- paste0("data03_", temp.data, ".csv")
		temp.path <- file.path(proxydata.path, temp.file)
		write.csv(temp.df, file = temp.path, row.names = FALSE)
		drive_upload(temp.path, as_id(datastage.id), temp.file)
		file.entry <- c(
			Datafile = temp.file,
			GDrive.id = drive_sub_id(as_id(datastage.id), temp.file)
		)
		return(file.entry)
	}
)
pre.ls

## __Download ####

library(stringr)

(data.files <- as_id(datastage.id) %>% drive_ls_from_id())

csv.files <- data.files$name %>% 
	str_subset("^data03_.+[.]csv")
csv.id <- sapply(
	csv.files,
	function(temp.file) drive_sub_id(as_id(datastage.id), temp.file)
)

lapply(
	names(csv.id),
	function(temp.filename){
		temp.id <- csv.id[temp.filename]
		# temp.file <- paste0("data03_", temp.filename) # already affixed w/ .csv
		temp.path <- file.path(proxydata.path, temp.filename)
		drive_download(as_id(temp.id), temp.path, overwrite = TRUE)
	}
)
