import csv
from generate_jira_csv import issues

# 1. PRIMARY CSV: GUARANTEED 1-CLICK IMPORT (Zero-Failure)
# Contains only the 5 universal fields that never trigger Jira workflow or key update blocks
with open('jira_issues_import.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Summary', 'Issue Type', 'Priority', 'Labels', 'Description'])
    for it in issues:
        combined_labels = f"{it['component']} {it['labels']}"
        writer.writerow([
            it['summary'],
            it['type'],
            it['priority'],
            combined_labels,
            it['description']
        ])

# 2. ADVANCED CSV: All fields with Resolution included
with open('jira_issues_advanced_all_fields.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Issue Key', 'Summary', 'Issue Type', 'Status', 'Resolution', 'Priority', 'Component/s', 'Labels', 'Description'])
    for it in issues:
        res = 'Done' if it['status'] == 'Closed' else ''
        writer.writerow([
            it['id'],
            it['summary'],
            it['type'],
            it['status'],
            res,
            it['priority'],
            it['component'],
            it['labels'],
            it['description']
        ])

print("Both primary and advanced CSV files written successfully!")
