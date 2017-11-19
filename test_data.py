import random
import csv
import sys


file_name = sys.argv[1].strip()
Combinations = int(sys.argv[2].strip())


with open(file_name, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['MSISDN', 'Network', 'Date', 'Product', 'Amount'])
    for i in range(10**6):
        row_data = [
            random.random(),
            "Network {}".format(int(Combinations*random.random()+1)),
            ['12-April-2016', '12-March-2016'][int(2*random.random())],
            "Loan Product {}".format(int(Combinations*random.random()+1)),
            int(1000*random.random())
            ]
        csvwriter.writerow(row_data)