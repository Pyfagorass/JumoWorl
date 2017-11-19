# Transaction Reconciliation

The Problem Statement can be seen [here](JumoWorldAssessment.pdf).

The code has been tested with Python3 on Ubuntu 17.10

## Usage 

I have coded the processing under the assumption that it happens manually since I am not sure how the file arrives. If the file arrives automatically, say to an SFTP server, then one approach to automate the processing is to just have the script constantly scan for file changes (comparing hashes of previously processed files). If a new file arrives, it just automatically processes all new files. If processing happens automatically, it would be best to change the name of `output.csv` to include a timestamp, so that older files are not overwritten.

To run the file, simply navigate to the directory, and run `recon.py FILENAME`. 

## Comments

To speed up processing of the file, we read and process the file line-by-line instead of reading the entire file into memory and then processing. 

In order to process line-by-line, we created an `INDEX`, that essentially stores *where* the summed and counted amounts are located in the `RECON` array which stores our results.
 
We have set the script to retrieve the file's headers directly from the file. We do this for two reasons, because despite an agreed upon file format, one day:

* Someone will swap the columns around. If they do this, we can still process the file; or
* Someone will rename the columns, and so our script will throw an error.

When processing transaction data, you don't want to get it wrong. So you need to strike the right balance between hard-coded (to throw errors when something changes), and moderate flexibility for when the information is all there, but the ordering is different.

When processing, we do a simple sanity check of making sure that the number of lines we process and the number of items in our final file are correct. It is helpful that in addition to this, you are sent with the file the number of lines from the original supplier. Since a `.csv` file is plain text, the file is not corrupted if some of it is missing. If there are no hashes or counts, it's sometimes difficult to tell if you have the full file.

The current script simply prints a status notification. It would be best to turn this information into a summary email. Especially if the file is being processed automatically.

Note: We were asked for just the month, but I have included the year as well, since just the month doesn't make sense.


## Test Data

To test our script, we generated a transaction file that had 1 million entries. We then changed the possible number of different `Network` and `Loan Product` to measure the performance of `.index()`. The larger the number of `Network` and `Loan Product` combinations, the more searches have to be performed to find where the data must be inserted into our `RECON` array.
 
 As you can see from the table below, the higher the number of combinations, the longer the file takes to process:

| Combinations  | Time (Seconds) |
|---------------|----------------|
| 50            | 386            |
| 25            | 107            |
| 15            | 41             |
| 10            | 23             |
| 5             | 12             |

For 50 combinations, 386 seconds (about 6.5 minutes) is a very long time to process a file of about 63MB. 

Splitting the file, and running across different cores would linearly speed up the processing. 


## End Notes

To generate test data, simply run `python test_data.py FILENAME COMBINATIONS`.

You can see an additional coding challenge I have done [here](https://goo.gl/xYgBkf)
