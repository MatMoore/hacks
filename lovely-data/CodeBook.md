# Code Book

See also [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones), [raw/README.txt](raw/README.txt), and [raw/features_info.txt](raw/features_info.txt).

## Experimental design

A group of 30 volunteers between 19-48 years performed six activities wearing a Samsung Galaxy S II smartphone at waist level.

Accelerometer and gyroscope readings were measured (indicated by acc/gyro respectively).

## Raw data

### Initial processing
Both signals were filtered using a median filter and a 3rd order low pass Butterworth filter with a corner frequency of 20 Hz to remove noise. The acceleration signal was then separated into body and gravity acceleration signals (tBodyAcc-XYZ and tGravityAcc-XYZ) using another low pass Butterworth filter with a corner frequency of 0.3 Hz.

### Resulting signals
This resulted in the following time signals. XYZ indicates that a seperate variable is recorded for each axis.

Name              | Description
----------------- | -----------------------------------------------
tBodyAcc-XYZ      | Acceleration due to the body in standard gravity units 'g'
tGravityAcc-XYZ   | Acceleration due to gravity in standard gravity units 'g'
tBodyAccJerk-XYZ  | Rate of change of acceleration due to the body
tBodyGyro-XYZ     | Gyroscope angular velocity in each direction in radians per second
tBodyGyroJerk-XYZ | Rate of change of the tBodyGyro-XYZ
tBodyAccMag       | Euclidian norm of tBodyAcc-XYZ
tGravityAccMag    | Euclidian norm of tGravityAcc-XYZ
tBodyAccJerkMag   | Euclidian norm of tBodyAccJerk-XYZ
tBodyGyroMag      | Euclidian norm of tBodyGyro-XYZ
tBodyGyroJerkMag  | Euclidian norm of tBodyGyroJerk-XYZ

Fast Fourier Transforms were also computed for each tBody signal, producing these additional signals:

- fBodyAcc-XYZ
- fBodyAccJerk-XYZ
- fBodyGyro-XYZ
- fBodyAccMag
- fBodyAccJerkMag
- fBodyGyroMag
- fBodyGyroJerkMag

This naming convention has been retained in the processed dataset.

From each of these signal, various variables were estimated. The only variables that were actually used in the processed dataset are the mean and standard deviation of each signal, i.e. tBodyAcc-mean()-XYZ, tBodyGyro-std()-XYZ, etc.

All of these variables have been normalised so that they range from -1 to 1.

## Processed Data

### Inclusion of subject and activity columns

Columns were added to the dataset to identify the source of each sample.

* **subject** is an integer between 1 and 30 identifying the subject who performed the activity.
* **activity** is a factor variable with 6 levels, indicating the activity performed (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING).

### Aggregation of samples

The mean was then taken for every variable per subject per activity, to produce 30 observations for each activity (180 rows in total).

For each of the signals described above (tBodyAcc..., tGravityAcc... etc.), there are two features in the processed dataset:

Name                | Description
------------------- | -------------------------------------------------------------
[signal]-mean()-XYZ | The mean across all samples of the sample means
[signal]-std()-XYZ  | The mean accross all samples of the sample standard deviation

Each of these is a column in the final dataset.

Note that the measurements are still using normalised units, so a value close to 1 indicates that the mean accross all samples is close to the maximum recorded sample mean/standard deviation.
