"""Fungsi foreachBatch untuk dashboard HTML real-time (disajikan lewat Nginx).

Contoh pemakaian pada query streaming Spark:
    query = stats.writeStream.foreachBatch(write_to_html).start()
`stats` = DataFrame agregasi dengan kolom quality_grade dan count.
"""
from html import escape


def write_to_html(df, epoch_id):
    rows = df.collect()
    html = """<html><head>
<title>IoT Orange Dashboard</title>
<meta http-equiv="refresh" content="2">
<style>
body{font-family:sans-serif;text-align:center;background:#2c3e50;color:white;margin-top:50px}
.card{display:inline-block;background:#e67e22;padding:20px;border-radius:10px;margin:10px;min-width:150px;box-shadow:0 4px 8px rgba(0,0,0,.2)}
h1{color:#f1c40f;text-transform:uppercase;letter-spacing:2px}
h2{margin:0;font-size:1.5em}
p{font-size:2em;font-weight:bold;margin:10px 0 0 0}
</style></head><body>
<h1>Live Monitoring Penyortiran Jeruk</h1><div class="container">"""
    for row in rows:
        html += (f"<div class='card'><h2>Grade {escape(str(row['quality_grade']))}</h2>"
                 f"<p>{escape(str(row['count']))}</p></div>")
    html += "</div><br><p style='font-size:.8em;color:#bdc3c7'>Update otomatis setiap 2 detik</p></body></html>"
    with open("/tmp/index.html", "w") as f:
        f.write(html)
