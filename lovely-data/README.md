# Human Activity Recognition Using Smartphones Summary Dataset

This repository contains a solution to the class project for the [Getting and Cleaning Data Coursera Course](https://class.coursera.org/getdata-011).

## Source
The raw data was taken from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones).

> The experiments have been carried out with a group of 30 volunteers within an age bracket of 19-48 years. Each person performed six activities (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING) wearing a smartphone (Samsung Galaxy S II) on the waist. Using its embedded accelerometer and gyroscope, we captured 3-axial linear acceleration and 3-axial angular velocity at a constant rate of 50Hz. The experiments have been video-recorded to label the data manually.

> The sensor signals (accelerometer and gyroscope) were pre-processed by applying noise filters and then sampled in fixed-width sliding windows of 2.56 sec and 50% overlap (128 readings/window). The sensor acceleration signal, which has gravitational and body motion components, was separated using a Butterworth low-pass filter into body acceleration and gravity. The gravitational force is assumed to have only low frequency components, therefore a filter with 0.3 Hz cutoff frequency was used. From each window, a vector of features was obtained by calculating variables from the time and frequency domain.

# Dataset information
`raw` contains the files from the UCI dataset.

`UCI_activity_recognition_summary.csv` contains the summarised dataset. Each row contains mean values of the measured variables over all sample windows associated with one combination of subject and activity. See [CodeBook.md](CodeBook.md) for more information.

`run_analyse.R` reproduces the dataset from the raw data. This should be executed directly with no arguments, or manually run through Rscript, e.g.

    Rscript run_analyse.R

You could also just run it from RStudio, but you will need to set your working directory to be the same as the script first.
