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
cache.file <- "data02_separated prefab.rds"
cachefile.id <- drive_sub_id(datastage.id, cache.file) # Get GDrive ID
cachefile.path <- file.path(proxydata.path, cache.file) # Set proxy data:// path
drive_download(as_id(cachefile.id), path = cachefile.path, overwrite = TRUE)

### Load
hr.ls <- readRDS(cachefile.path)