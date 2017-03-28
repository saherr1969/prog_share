# #############################################################
# Created by:  Tate Erickson
#       Date:  2017.03.21
#
# This program takes a comma-separated (CSV) file of a specific
# format of Business Student data and creates an output CSV file
# containing just the student's fullname and major
#
# Modified by:  S. Herr
#        Date:  2017.03.22
#
# Removed all sleep() calls as they only thing they do in the
# original program is to slow the processing of the data.
# There is no need for this particular code to sleep any length
# of time as it is never waiting for some other program or process
# to complete.  If so desired to make it seem like it is taking time
# to process various things, uncomment the sleep(1) statement in the
# print_stage subroutine.  This will make it take a minunum of X seconds
# to complete where X is the number of print_stage() calls throughout the
# program.

# Modifications included refactoring the user-output to a
# subroutine to make it easier to communicate progress status
# throughout the program and make it easier to add and remove
# sections as further development continues.
#
# Reordered the process flow to do output directory checking/
# creation earlier and to open the output file in a more
# logical place.
#
# Various comments added throughout to explain the code and
# changes made
#
# TODO:
# 1.  All programatically defined variables (not constants),
#         should probably be refactored to lowercase
# 2.  Change file open() functionality to use 'with'
# 3.  Change csv.reader/writer functionality to use csv.DictReader/DictWriter
#         to make code more readable
# 4.  Add mysql module and associated required elements to pull
#         needed data directly from database
# 5.  If the objective of this exercise is to create a re-usable
#         module for parsing known CSV files to a new type,
#         then input/output header definitions and output criteria
#         should be variablized so that they can be passed to the
#         future routine and thus the routine knows how to read/write
#         the CSV files and the criteria needed to determine whether
#         to include an input record in the output data
# 6.  Add an appropriate #! at the beginning if necessary
#
# #############################################################

# Reorder to have more universal modules first, more specific ones later.  (SAH personal preference)
import os
# shutil module not used so this comment and import line can be deleted
# import shutil
import time
import easygui
import csv

# GLOBAL VARIABLES/CONSTANTS
# Starting with the highest level objects/data and defining to the more specific
# TIMESTAMP never changes but is used right away
TIMESTAMP = time.strftime("%Y%m%d-%H%M%S")

# Path/filename string splitter character.
# '/' might not work on Windows.
# Change it here if needed.
SPLIT_CHAR = '/'

# Get current directory and define output directory
CWD = os.getcwd()
OUTPUT_DIR = (CWD + SPLIT_CHAR + 'Output')

# Get input filename from the user
INPUT_CSV = easygui.fileopenbox()

# INPUT_CSV is a fullpath/filename string.
# rsplit() splits the string into parts
#     '/' is the character to use to split it up
#     1 is how many times to cut it up  1 = 2 pieces, 2 = 3 pieces, etc.
INPUT_DIR, INPUT_FNAME = INPUT_CSV.rsplit(SPLIT_CHAR, 1)

# Define associated OUTPUT_FNAME as just a filename string
# and OUTPUT_CSV as a  fullpath/filename string
# [0:-3] takes all but the last 3 characters (csv) of the input file name
# leaving just the name with trailing period (.) and then appends "out-YYYYMMDD-HHMMSS.csv" to the end
OUTPUT_FNAME = (INPUT_FNAME[0:-3] + 'out-' + TIMESTAMP + '.csv')
OUTPUT_CSV = OUTPUT_DIR + SPLIT_CHAR + OUTPUT_FNAME

# Initialize Stage counting variable
STAGE = 0


# This routine takes a message, msg, and prints it to STDOUT
# pre-pending it with the STAGE counter incremented 1 higher
# than last time.  That way if the program does not need
# to create an Output Directory and the creation stage is
# not executed, there will not be a missing step in the
# list of stages
def print_stage(msg):
    # sleep(1)
    global STAGE
    STAGE += 1
    print("Stage %s:  %s" % (STAGE, msg))


# Create Output Directory if it doesn't already exist
# Do this first, not last so you can just open the file
# in the right place instead of opening it, writing to it,
# closing it and then moving it
print_stage("Output directory check/creation")

if not os.path.exists(OUTPUT_DIR):
    print_stage("Output directory creation")
    os.makedirs(OUTPUT_DIR)

# Create Output file objects
# This includes a file handle and a csv.writer() object
print_stage("Open Output File: %s" % OUTPUT_CSV)

OUTFILE_HANDLE = open(OUTPUT_CSV, 'w')
# Following line crashed on Mac, replaced with previous
# OUTFILE_HANDLE = open(OUTPUT_CSV, 'w', newline='')

OUTPUT_FIELDS = ['Full_Name', 'Major']
CSV_WRITER = csv.writer(OUTFILE_HANDLE, delimiter=',')

# Importing INPUT_CSV
print_stage("Start CSV file import")
print_stage("Open Input File: %s" % INPUT_CSV)
INFILE_HANDLE = open(INPUT_CSV)
CSV_READER = csv.reader(INFILE_HANDLE, delimiter=',')

# Begin Read/Write process
print_stage("Reading and Writing Data Started")

# Skip the first record
print_stage("Input:  Skip header row")
next(CSV_READER)

print_stage("Output:  Write header row")
CSV_WRITER.writerow(OUTPUT_FIELDS)    # Changed to OUTPUT_FIELDS as it was already defined

print_stage("Start Read/Write Loop")
rec_number = 1
for row in CSV_READER:
    print_stage("Input:  Read record %s" % rec_number)
    student_id, first_name, last_name, gender, school, school_id, major, major_id = row
# The following are unnecessary as the previous has assigned the first 8 comma-separated items
# to the variable names listed on the assignment line
#    first_name = row[1]
#    last_name = row[2]
    # The following used (row[1] + ' ' + row[2]) which was redundant because those two values
    # were already stored in first_name, last_name variables, first by the not commented assignment
    # student_id, first_name, last_name... = row but then again in the two lines commented out
    # after that i.e. first_name = row[1].
    full_name = (first_name + ' ' + last_name)

    # If Statement: Records the full name and major of students with a school_id of '100'
    # to the Output CSV file.  It also displays it to the screen
    if school_id == '100':
        print_stage("Output:  Record #%s has school_id of 100 so output record: %s,%s" % (rec_number, full_name, major))
        CSV_WRITER.writerow([full_name, major])
    else:
        print_stage("Output:  Skipping...")

    rec_number += 1

# Closing Files
print_stage("Reading and Writing Data Finished")
OUTFILE_HANDLE.close()
INFILE_HANDLE.close()

# Send the user information that the process is complete and where to find the output data
print_stage("Script Complete: See %s in the Output Directory, %s, for results" % (OUTPUT_FNAME, OUTPUT_DIR))
