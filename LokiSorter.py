import sys
import os
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 LokiSorter.py <route/to/file_of_log.log>")
    sys.exit(1)

log_file = sys.argv[1]

if not os.path.isfile(log_file):
    print(f"The file '{log_file}' does not exist.")
    sys.exit(1)

data = []

with open(log_file, 'r') as file:
    for line in file:
        parts = line.strip().split(' ')
        date_time = parts[0]
        log_type = parts[3]
        if log_type in ['Alert:', 'Warning:', 'Notice:']:
            message = ' '.join(parts[4:])
            md5 = None
            created = None
            modified = None
            accessed = None

            # Finds MD5, CREATED, MODIFIED y ACCESSED inside the message
            if 'MD5:' in message:
                parts = message.split()
                md5_index = parts.index('MD5:')
                md5 = parts[md5_index + 1]
            
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

            data.append([date_time, log_type, message, md5, created, modified, accessed])

df = pd.DataFrame(data, columns=['Date/Time', 'Log Type', 'Message', 'MD5', 'CREATED', 'MODIFIED', 'ACCESSED'])


# Output File
output_file = os.path.splitext(log_file)[0] + ".xlsx"

# Creates an Excel file and saves the DataFrame
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Logs', index=False)

# Sorts the registers of Alert, Warning and Notice
filtered_df = df[df['Log Type'].isin(['Alert:', 'Warning:', 'Notice:'])]

# Creats separate Excel sheets for Alert, Warning and Notice
filtered_df[filtered_df['Log Type'] == 'Alert:'].to_excel(writer, sheet_name='Alerts', index=False)
filtered_df[filtered_df['Log Type'] == 'Warning:'].to_excel(writer, sheet_name='Warnings', index=False)
filtered_df[filtered_df['Log Type'] == 'Notice:'].to_excel(writer, sheet_name='Notices', index=False)

writer.save()
print(f"Excel file '{output_file}' succesfully created.")
