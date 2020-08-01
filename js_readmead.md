Prior to running any of the Jupyter Notbooks or data in this download the neccesary files and create the environments found within them.

# General Setup Guide:

Download [Andaconda](https://docs.anaconda.com/anaconda/install/) to be able to install the environment and use your preference of commandline options or Editor to view the data.

### From the list options below choose the environments within this neccesary envrionment for your operating system.

For Apple/Mac product user:

[`envrionment.yml`]

For windows/Linux users:

[`realestate.yml`]

To utilize Geopandas:

[`geopandas.yml`]

All files are located in the main directory and src folder.

# Directories of Project

### [Data](https://github.com/mattcarr17/time_series_project/tree/master/data): A directory that contains all of the data used for exploration and analysis.

### [Notebooks](https://github.com/mattcarr17/time_series_project/tree/master/notebooks): Directory that holds all of the notebooks used for data exploration and analysis.

### [References](https://github.com/mattcarr17/time_series_project/tree/master/references): This directory has all of the outside resources and helpful information [pertaining] to models and over all data analysis methodology.

### [Report](https://github.com/mattcarr17/time_series_project/tree/master/report/figures): Final notebook of the data analysis and PDF presentaion of the overall project.

### [[Src]](https://github.com/mattcarr17/time_series_project/tree/master/src): The modules/functions creater to aid in the data cleaning and analaysis process.


 # Overview of Project
 For this project the main objective was to analyze the given Zillow dataset and select the 5 best zipcodes based  on a particular metric. This will help investors and other individuals select profitables ways to increase their portfolio or overall income. For this project to a succes we need to accrurately predict the direction a housing price will head and have minimal error or risk for potential investors.
 
# Methodoly of the Project and Data Analysis:

### Data gathering

The overal all approach to the data set was the CRISP-DM data mining process. To start out  the CRISP-DM methodology we gathered byt visiting this wbesite [Website to download the Housing Data](https://www.zillow.com/research/data/).To get this the same data go under the Home Value section. The categories are ZHVIAll Homes. Geography is by Metro & US.

# Data understanding
This is where the exploratory data analysis occurs. We began by looking at all of the zipcodes and determined that was alot of of zipscodes with their own unique characteristics. We then decied to focus our efforts on one area. The chosen area was the Chicago metroolitian area. From those zip codes we need to filter it once more to select the one withs the most potential for being profitable. To do this we calculated the 5 Year return on investment(ROI) and the 2 year ROI. We then comparied the two sets of data and took the top zips codes that occrued within the 30 of both filters. 

We also looked into the data's time ranges and noticed there were NaN values in the earlier years dating in the 1996's and on. The next step we took was to filter the date's time zones. We decided to exclude data that was observed prior to 2013. This was due to the prior missing NaN values as well as the market crash of 2008. The was not a restabalization of the housing market until early 2013 based on the data set. After filtering the data for useful median house values and data ranges we were then ready to processing the data.



