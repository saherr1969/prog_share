import csv
import time
import os
import shutil
import easygui

#Global Varriables
TIMESTAMP = time.strftime("%Y%m%d-%H%M%S")
INPUT_CSV = easygui.fileopenbox()
OUTPUT_CSV = ('Output-' + TIMESTAMP + '.csv')
CWD = os.getcwd()
OUTPUT_DIRECTORY = (os.getcwd() + '/Output')

#User Update/Info
print('Stage 1: Importing CSV')
time.sleep(0.5)

#Importing INFILE
INFILE = open(INPUT_CSV)
CSV_READER = csv.reader(INFILE, delimiter=',')
next(CSV_READER)

#User Update/Info
time.sleep(0.5)
print('Stage 2: Creating Output File: ' + OUTPUT_CSV)
time.sleep(0.5)

#Creating/Updating OUTFILE
OUTFILE = open(OUTPUT_CSV, 'w', newline='')
FIELDNAMES = ['Full_Name', 'Major']
CSV_WRITER = csv.writer(OUTFILE, delimiter=',')

#User Update/Info
print('Stage 3: Generating Output')
time.sleep(0.5)

#Creating Header Row and Assigning Values for INFILE
CSV_WRITER.writerow(['Full_Name', 'Major'])
for row in CSV_READER:
    student_id, first_name, last_name, gender, school, school_id, major, major_id = row
    first_name = row[1]
    last_name = row[2]
    full_name = (row[1] + ' ' + row[2])

#If Statement: Records the full name and major of students with a school_id of '100'
    if school_id == '100':
        CSV_WRITER.writerow([full_name, major])
    else:
        pass

#Closing Files
OUTFILE.close()
INFILE.close()

#Create Output Directory if it doesn't already exisit
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)


#Move Output File to Output Directory
shutil.move(OUTPUT_CSV, OUTPUT_DIRECTORY)

#User Update/Info
time.sleep(0.5)
print('Script Complete: See ' + OUTPUT_CSV + ' in the Output Directory for results')
time.sleep(1)
