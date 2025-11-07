CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    source TEXT,
    job_id TEXT,
    title TEXT,
    company TEXT,
    location TEXT,
    url TEXT,
    description TEXT,
    scraped_at TEXT,
    similarity REAL,
    applied INTEGER DEFAULT 0,
    applied_at TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_jobs_source_jobid ON jobs(source, job_id);
