DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  google_user_id TEXT UNIQUE NOT NULL,
  refresh_token TEXT NOT NULL,
  spreadsheet_id TEXT,
  sheet_id TEXT
);