CREATE TABLE IF NOT EXISTS secrets (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL,
    extra            TEXT DEFAULT '',
    password         TEXT NOT NULL
);