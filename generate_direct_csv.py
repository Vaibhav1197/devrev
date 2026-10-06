import csv
from generate_jira_csv import issues

# Let's write the ultra-clean, minimal-quoted CSV file
# Standard CSV: only fields with commas or newlines are quoted.
# Headers: exactly matching standard Jira fields.

fields = ['Summary', 'Issue Type', 'Priority', 'Labels', 'Description']

with open('jira_issues_direct.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fields)
    for it in issues:
        combined_labels = f"{it['component']} {it['labels']}"
        writer.writerow([
            it['summary'],
            it['type'],
            it['priority'],
            combined_labels,
            it['description']
        ])

print("Generated jira_issues_direct.csv successfully!")
