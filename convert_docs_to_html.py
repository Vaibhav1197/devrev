import re
import os

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {{
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --text-main: #1e293b;
      --text-muted: #64748b;
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border: #e2e8f0;
      --badge-green: #dcfce7;
      --badge-green-text: #15803d;
      --badge-amber: #fef3c7;
      --badge-amber-text: #b45309;
      --badge-blue: #dbeafe;
      --badge-blue-text: #1d4ed8;
      --badge-red: #fee2e2;
      --badge-red-text: #b91c1c;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.6;
      color: var(--text-main);
      background-color: var(--bg-page);
      margin: 0;
      padding: 40px 20px;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
      background: var(--bg-card);
      padding: 48px;
      border-radius: 12px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      border: 1px solid var(--border);
    }}
    h1 {{
      font-size: 26px;
      color: #0f172a;
      margin-top: 0;
      margin-bottom: 8px;
      border-bottom: 2px solid var(--border);
      padding-bottom: 12px;
    }}
    h2 {{
      font-size: 20px;
      color: #1e293b;
      margin-top: 36px;
      margin-bottom: 16px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border);
    }}
    h3 {{
      font-size: 16px;
      color: #334155;
      margin-top: 24px;
      margin-bottom: 12px;
    }}
    h4 {{
      font-size: 14px;
      color: #475569;
      margin-top: 18px;
      margin-bottom: 8px;
    }}
    p, li {{
      font-size: 15px;
      color: #334155;
    }}
    ul, ol {{
      padding-left: 24px;
      margin-bottom: 16px;
    }}
    li {{
      margin-bottom: 6px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 14px;
    }}
    th, td {{
      padding: 10px 14px;
      text-align: left;
      border: 1px solid var(--border);
    }}
    th {{
      background-color: #f1f5f9;
      font-weight: 600;
      color: #0f172a;
    }}
    tr:nth-child(even) {{
      background-color: #f8fafc;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 13px;
      background-color: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      color: #0f172a;
    }}
    pre {{
      background-color: #0f172a;
      color: #f8fafc;
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 13px;
      line-height: 1.45;
      margin: 20px 0;
    }}
    pre code {{
      background-color: transparent;
      padding: 0;
      color: #f8fafc;
    }}
    blockquote {{
      border-left: 4px solid var(--primary);
      margin: 20px 0;
      padding: 12px 20px;
      background-color: #eff6ff;
      border-radius: 0 8px 8px 0;
      color: #1e3a8a;
      font-style: italic;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
    }}
    .badge-p0 {{ background-color: var(--badge-red); color: var(--badge-red-text); }}
    .badge-approved {{ background-color: var(--badge-green); color: var(--badge-green-text); }}
    .badge-blue {{ background-color: var(--badge-blue); color: var(--badge-blue-text); }}
    hr {{
      border: 0;
      height: 1px;
      background: var(--border);
      margin: 32px 0;
    }}
    .footer-note {{
      margin-top: 40px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
      font-size: 13px;
      color: var(--text-muted);
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    {content}
    <div class="footer-note">
      Artifact generated for DevRev Solutions Engineering Evaluation • Confidential
    </div>
  </div>
</body>
</html>
"""

def md_to_html(md_text):
    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    code_block_lang = ""
    code_lines = []
    in_table = False
    table_lines = []

    def flush_table(tbl):
        if not tbl:
            return ""
        out = ["<table>"]
        is_header = True
        for row in tbl:
            if re.match(r'^\s*\|?\s*[-:]+[-| :]*\|?\s*$', row):
                is_header = False
                continue
            cells = [c.strip() for c in row.strip().strip('|').split('|')]
            out.append("  <tr>")
            tag = "th" if is_header else "td"
            for c in cells:
                # Format inline bold/code/badges
                cell_html = format_inline(c)
                out.append(f"    <{tag}>{cell_html}</{tag}>")
            out.append("  </tr>")
            is_header = False
        out.append("</table>")
        return "\n".join(out)

    def format_inline(text):
        # Escape html entities safely
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Badges
        text = re.sub(r'P0 - Blocker[^\&]*', r'<span class="badge badge-p0">\g<0></span>', text)
        text = re.sub(r'Approved for Implementation', r'<span class="badge badge-approved">Approved for Implementation</span>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        return text

    for line in lines:
        # Code block toggle
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                escaped_code = "\n".join(code_lines).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f"<pre><code>{escaped_code}</code></pre>")
                code_lines = []
            else:
                if in_table:
                    html_lines.append(flush_table(table_lines))
                    table_lines = []
                    in_table = False
                in_code_block = True
                code_block_lang = line[3:].strip()
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Table detection
        if line.strip().startswith('|') and line.strip().endswith('|'):
            in_table = True
            table_lines.append(line)
            continue
        else:
            if in_table:
                html_lines.append(flush_table(table_lines))
                table_lines = []
                in_table = False

        stripped = line.strip()
        if not stripped:
            continue

        # Headers
        if stripped.startswith("#### "):
            html_lines.append(f"<h4>{format_inline(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{format_inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{format_inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{format_inline(stripped[2:])}</h1>")
        elif stripped.startswith("> "):
            quote_text = format_inline(stripped[2:])
            html_lines.append(f"<blockquote>{quote_text}</blockquote>")
        elif stripped == "---":
            html_lines.append("<hr>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            html_lines.append(f"<ul><li>{format_inline(stripped[2:])}</li></ul>")
        elif re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            html_lines.append(f"<ol><li>{format_inline(item_text)}</li></ol>")
        else:
            html_lines.append(f"<p>{format_inline(stripped)}</p>")

    if in_table:
        html_lines.append(flush_table(table_lines))

    # Clean up consecutive ul/ol tags
    content_html = "\n".join(html_lines)
    content_html = re.sub(r'</ul>\s*<ul>', '', content_html)
    content_html = re.sub(r'</ol>\s*<ol>', '', content_html)
    return content_html


# Process all 3 files
files_to_convert = [
    ("API_Design_Notes_Offline_Sync.md", "API_Design_Notes_Offline_Sync.html", "API Design Notes - Offline Order Sync & Delta API Specification"),
    ("Bug_Investigation_Summary_OM102.md", "Bug_Investigation_Summary_OM102.html", "Bug Investigation & RCA - Incident OM-102 / INC-49201"),
    ("Customer_Escalation_Report_ApexWholesale.md", "Customer_Escalation_Report_ApexWholesale.html", "Customer Escalation & Executive Incident Report - Apex Wholesale")
]

for src, dst, title in files_to_convert:
    if os.path.exists(src):
        with open(src, "r", encoding="utf-8") as f:
            md_content = f.read()
        body_html = md_to_html(md_content)
        full_html = TEMPLATE.format(title=title, content=body_html)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Generated {dst} ({len(full_html)} bytes)")

