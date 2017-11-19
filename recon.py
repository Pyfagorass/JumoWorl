import csv
import time
import sys


def get_month(date_time_string):
    """
    Split the date string, and return new month-year
    """
    DTS = date_time_string
    DTS = DTS.split("-")
    M = DTS[1].strip() + "-" + DTS[2].strip()
    return M


def do_recon(file_name, OutputHeader):
    """
    This function takes in the raw transaction file and returns the recon'ed files,
     as well as a line count that serves as a sanity check.
    """
    header = []
    INDEX = []
    RECON = []
    sanity_check = 0
    with open(file_name, "r") as ins:
        for line in ins:
            L = line.strip().split(",")
            if len(header) == 0:
                header = L
            else:
                sanity_check += 1
                network = L[header.index('Network')].replace("'", "").strip()
                product = L[header.index('Product')].replace("'", "").strip()
                month = get_month(L[header.index('Date')].replace("'", "").strip())
                amount = int(L[header.index('Amount')].replace("'", "").strip())
                I = [network, product, month]
                if I not in INDEX:
                    INDEX.append(I)
                    RECON.append(I + [amount, 1])
                else:
                    RECON[INDEX.index(I)][OutputHeader.index('Amount')] += amount
                    RECON[INDEX.index(I)][OutputHeader.index('Count')] += 1
    return RECON, sanity_check


def do_sanity_check(recon, sanity_check):
    """
    We perform a sanity check, totalling the number of product occurrences in 
    the recon, compared to the number of lines in the raw file.
    """
    check_sanity_check = 0
    for row in recon:
        check_sanity_check += row[4]
    return (check_sanity_check == sanity_check)


def write_output(recon, sanity_check, output_header):
    """
    Write the recon array to file, but iff the sanity_check passes.  
    """
    if do_sanity_check(recon, sanity_check):
        with open('Output.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(output_header)
            for row in recon:
                csvwriter.writerow(row)
        return True
    else:
        return False

start_time = time.time() # Measure performance

file_name = sys.argv[1].strip()
print("File name: {}".format(file_name))
output_header = ['Network', 'Product', 'Month', 'Amount', 'Count']
if True:
    recon, sanity_check = do_recon(file_name, output_header)
    if write_output(recon, sanity_check, output_header):
        print("File successfully processed, sanity check passes")
    else:
        print("File did not process, sanity failed")
else:
    print("Cataclysmic failure in processing the file")

end_time = time.time() # Measure performance
print("Total recon processing time: {}s".format(end_time - start_time))