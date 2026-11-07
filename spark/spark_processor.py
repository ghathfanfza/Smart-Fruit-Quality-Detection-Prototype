"""Penerima log deteksi: TCP server (port 9999) -> Spark DataFrame -> PostgreSQL (JDBC)."""
import json
import os
import socket

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.getenv("PG_PORT", "30432")
PG_DB = os.getenv("PG_DB", "grafana_db")
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
LISTEN_PORT = int(os.getenv("SPARK_PORT", "9999"))

spark = (
    SparkSession.builder.appName("SortirJerukBigDataProcessor")
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("kategori", StringType(), True),
    StructField("jumlah", IntegerType(), True),
])


def simpan_ke_postgres(kategori, jumlah):
    """Ubah satu log menjadi DataFrame lalu tulis ke tabel sortir_jeruk."""
    try:
        df = spark.createDataFrame([(kategori, jumlah)], schema=schema)
        (
            df.write.format("jdbc")
            .option("url", f"jdbc:postgresql://{PG_HOST}:{PG_PORT}/{PG_DB}")
            .option("dbtable", "sortir_jeruk")
            .option("user", PG_USER)
            .option("password", PG_PASSWORD)
            .option("driver", "org.postgresql.Driver")
            .mode("append")
            .save()
        )
        print(f"[SPARK] Tersimpan: {kategori} x{jumlah}")
    except Exception as exc:
        print(f"[SPARK] Gagal menulis ke database: {exc}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", LISTEN_PORT))
server.listen(5)
print(f"[SPARK] Menunggu log deteksi YOLO di port {LISTEN_PORT} ...")

try:
    while True:
        client, _ = server.accept()
        packet = client.recv(1024).decode("utf-8").strip()
        if packet:
            try:
                data = json.loads(packet)
                simpan_ke_postgres(data.get("kategori"), data.get("jumlah", 1))
            except json.JSONDecodeError:
                print(f"[SPARK] Data non-JSON diabaikan: {packet}")
        client.close()
except KeyboardInterrupt:
    print("\n[SPARK] Dihentikan.")
finally:
    server.close()
    spark.stop()
