-- Tabel tujuan penulisan dari Spark (mode append lewat JDBC)
CREATE TABLE IF NOT EXISTS sortir_jeruk (
    id         SERIAL PRIMARY KEY,
    kategori   TEXT NOT NULL,
    jumlah     INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
