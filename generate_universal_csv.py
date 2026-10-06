import csv

# Load base issues from generate_jira_csv.py
from generate_jira_csv import issues

# 1. UNIVERSAL ZERO-FAILURE CSV
# Guaranteed to work on ANY Jira project type (Team-managed, Company-managed, Free trial)
# - No Issue Key collision
# - No Component feature dependency (component added to Labels)
# - No Workflow / Resolution validation blocks
universal_headers = ['Summary', 'Issue Type', 'Priority', 'Labels', 'Description']

with open('jira_issues_universal_import.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(universal_headers)
    for it in issues:
        # Merge component into labels so it's captured safely without requiring Jira Components setup
        combined_labels = f"{it['component']} {it['labels']}"
        writer.writerow([
            it['summary'],
            it['type'],
            it['priority'],
            combined_labels,
            it['description']
        ])

# 2. FULL CSV WITH RESOLUTION & STATUS
# If importing via Jira Admin External System Import with Status, Jira requires 'Resolution' for Closed issues!
full_headers = ['Summary', 'Issue Type', 'Status', 'Resolution', 'Priority', 'Component/s', 'Labels', 'Description']

with open('jira_issues_full_with_resolution.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(full_headers)
    for it in issues:
        resolution = 'Done' if it['status'] == 'Closed' else ''
        writer.writerow([
            it['summary'],
            it['type'],
            it['status'],
            resolution,
            it['priority'],
            it['component'],
            it['labels'],
            it['description']
        ])

print("Generated jira_issues_universal_import.csv and jira_issues_full_with_resolution.csv successfully!")
