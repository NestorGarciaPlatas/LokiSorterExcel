import sys
import os
import pandas as pd
import argparse

# command line arguments
parser = argparse.ArgumentParser(description="Sort and filter Loki records and export to Excel.")
parser.add_argument("log_file", help="Loki Log File")
parser.add_argument("filter_fields", nargs='*', help="Fields to filter (e.g. 'SHA256 NAME SCORE')")
args = parser.parse_args()

valid_fields = {'SHA256', 'NAME', 'SCORE'}
if args.filter_fields:
    for field in args.filter_fields:
        if field not in valid_fields:
            print(f"Cannot filter by the field '{field}'")
            sys.exit(1)

if not os.path.isfile(args.log_file):
    print(f"This file '{args.log_file}' does not exist.")
    sys.exit(1)

data = []

with open(args.log_file, 'r') as file:
    standard_columns = ['Date/Time', 'Log Type', 'Message', 'MD5', 'CREATED', 'MODIFIED', 'ACCESSED']
    additional_columns = []
    extra_data = []
    sha=False
    sco=False
    nam=False
    for line in file:
        parts = line.strip().split(' ')
        date_time = parts[0]
        log_type = parts[3]
        if log_type in ['Alert:', 'Warning:', 'Notice:']:
            message = ' '.join(parts[4:])
            md5 = None
            sha256 = None
            created = None
            modified = None
            accessed = None
            score = None
            name = None

            # Finds MD5, CREATED, MODIFIED y ACCESSED inside the message
            if 'NAME:' in message:
                parts = message.split()
                name_index = parts.index('NAME:')
                name = parts[name_index + 1]

            if 'SCORE:' in message:
                parts = message.split()
                score_index = parts.index('SCORE:')
                score = parts[score_index + 1]

            if 'MD5:' in message:
                parts = message.split()
                md5_index = parts.index('MD5:')
                md5 = parts[md5_index + 1]
            
            if 'SHA256:' in message:
                parts = message.split()
                sha256_index = parts.index('SHA256:')
                sha256 = parts[sha256_index + 1]

            if 'CREATED:' in message:
                created_start = message.find('CREATED:') + len('CREATED:')
                created_end = message.find('MODIFIED:')
                created = message[created_start:created_end].strip()

            if 'MODIFIED:' in message:
                modified_start = message.find('MODIFIED:') + len('MODIFIED:')
                modified_end = message.find('ACCESSED:')
                modified = message[modified_start:modified_end].strip()

            if 'ACCESSED:' in message:
                accessed_start = message.find('ACCESSED:') + len('ACCESSED:')
                accessed_end = message.find('REASON_1:')
                accessed = message[accessed_start:accessed_end].strip()
            
            
            # Filter based on the specified field
    
            if args.filter_fields:
                fields = ' '.join(args.filter_fields)
                row = [date_time, log_type, message, md5, created, modified, accessed]
                for field in fields.split():
                    if field == 'SHA256':
                        row.append(sha256)
                        sha = True
                    elif field == 'SCORE':
                        row.append(score)
                        sco = True
                    elif field == 'NAME':
                        row.append(name)
                        nam = True
                data.append(row)
            else:
                data.append([date_time, log_type, message, md5, created, modified, accessed])
    
    if sco==True:
        additional_columns.append('SCORE')
        
    if nam==True:
        additional_columns.append('NAME')
        
    if sha == True:
        additional_columns.append("SHA256")
        


columns= standard_columns + additional_columns
df = pd.DataFrame(data, columns=columns)

# Output File
output_file = os.path.splitext(args.log_file)[0] + ".xlsx"

# Creates an Excel file and saves the DataFrame
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
df = pd.DataFrame(data, columns=columns)
df.to_excel(writer, sheet_name='Logs', index=False)

# Sorts the registers of Alert, Warning and Notice
filtered_df = df[df['Log Type'].isin(['Alert:', 'Warning:', 'Notice:'])]

# Creates separate Excel sheets for Alert, Warning and Notice
filtered_df[filtered_df['Log Type'] == 'Alert:'].to_excel(writer, sheet_name='Alerts', index=False)
filtered_df[filtered_df['Log Type'] == 'Warning:'].to_excel(writer, sheet_name='Warnings', index=False)
filtered_df[filtered_df['Log Type'] == 'Notice:'].to_excel(writer, sheet_name='Notices', index=False)

writer.save()
print(f"Excel file '{output_file}' succesfully created.")
