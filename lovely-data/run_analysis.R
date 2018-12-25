#!/usr/bin/env Rscript

## This script reads the raw data and does the following:
## 1. Merges the training and the test sets to create one data set.
## 2. Extracts only the measurements on the mean and standard deviation for each measurement. 
## 3. Uses descriptive activity names to name the activities in the data set
## 4. Appropriately labels the data set with descriptive variable names. 
## 5. From the data set in step 4, creates a second, independent tidy data set with the average of each variable for each activity and each subject.
##
## The script should be run with the repository top level directory as the working directory
## The output will be saved to the same directory with the filename UCI_activity_recognition_summary.csv.
library(data.table)

# File paths
rawDir <- file.path(getwd(), "raw")
testDir <- file.path(rawDir, "test")
trainingDir <- file.path(rawDir, "train")
outputFilename <- file.path(getwd(), "UCI_activity_recognition_summary.csv")

if(!file.exists(testDir) || !file.exists(trainingDir)) {
    stop("Cannot find raw files. Please rerun script from the top level directory.")
} else {
    message("Cleaning data...")
}

# Load feature and activity names
features <- fread(file.path(rawDir, "features.txt"), header=FALSE)
activityLabels <- fread(file.path(rawDir, "activity_labels.txt"), header=FALSE)
setnames(activityLabels, c('V1', 'V2'), c('activityId', 'activity'))
setkey(activityLabels, 'activityId')

## Load the test or training set and combine feature/activity/subject into one table.
loadDataset <- function(setDir, setFilename, labelFilename, subjectFilename) {
    # Load data from files
    # fread isn't used for the main data files due to this bug:
    # https://github.com/Rdatatable/data.table/issues/956
    DT <- as.data.table(read.table(file.path(setDir, setFilename)))
    labels <- fread(file.path(setDir, labelFilename))
    subjects <- fread(file.path(setDir, subjectFilename))
    
    # Name all the features (part 4)
    setnames(DT, 1:561, features $ V2)

    # Add in the cols from separate files. The tuple of (subject, activityId) determines
    # which observation each row corresponds to in the final dataset.
    DT[, subject := subjects]
    DT[, activityId := labels]

    # Join in activity names, as a numeric ID is pretty useless (part 3)
    setkey(DT, 'activityId')
    DT <- DT[activityLabels]
    
    # Remove unwanted features and activityId column (part 2)
    unwantedFeatures <- grep("(mean|std)\\(\\)(-[XYZ])?$", features $ V2, invert=TRUE, perl=TRUE)
    set(DT, j=unwantedFeatures, value=NULL)
    DT[, activityId := NULL]
    
    # Convert activity and subject to factors
    DT[, activity := as.factor(activity)]
    DT[, subject := as.factor(subject)]
    
    DT
}

trainingSet <- loadDataset(trainingDir, "X_train.txt", "y_train.txt", "subject_train.txt")
testSet <- loadDataset(testDir, "X_test.txt", "y_test.txt", "subject_test.txt")

# Combine test and training sets (part 1)
# We could add a new column to keep track of the source, but I don't think this is neccessary for the assignment.
completeSet <- rbind(trainingSet, testSet)

# Part 5. Take the mean of all features by subject and activity. There should be 30x6 = 180 observations.
subjectActivityMeans <- completeSet[, lapply(.SD, mean), by=list(subject, activity)]

# Write to file
write.csv(subjectActivityMeans, outputFilename, row.names=FALSE)
message(paste("Output file written to", outputFilename))