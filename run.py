# run.py
import sqlite3, os
from scraper.indeed_scraper import scrape_indeed
from matcher.embed_matcher import EmbedMatcher
from sender.emailer import EmailSender
from reviewer.review_cli import review_and_send

DB_PATH = "Storage/Jobs.db"

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS jobs (
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
    )""")
    conn.commit()
    conn.close()

def insert_jobs(jobs, source="indeed"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for j in jobs:
        try:
            cur.execute("INSERT OR IGNORE INTO jobs (source, job_id, title, company, location, url, description, scraped_at) VALUES (?,?,?,?,?,?,?,?)",
                        (source, j["job_id"], j["title"], j["company"], j.get("location",""), j["url"], j.get("snippet",""), j["scraped_at"]))
        except Exception as e:
            print("Insert error", e)
    conn.commit()
    conn.close()

def compute_similarity(resume_text):
    matcher = EmbedMatcher()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, description FROM jobs WHERE similarity IS NULL OR similarity=0")
    rows = cur.fetchall()
    for row in rows:
        job_id, desc = row
        score = matcher.score(desc or "", resume_text)
        cur.execute("UPDATE jobs SET similarity=? WHERE id=?", (score, job_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    ensure_db()
    # 1) Scrape
    jobs = scrape_indeed("data scientist", "Vienna, Austria", max_results=20)
    insert_jobs(jobs, source="indeed")
    # 2) Similarity
    resume_text = open("materials/resume.txt").read()
    compute_similarity(resume_text)
    # 3) Launch reviewer
    email_sender = EmailSender()
    personal_info = {
        "name": "Your Name",
        "resume_path": "materials/resume.pdf",
        "intro": "I have 5 years experience in machine learning...",
        "body": "I led projects in ...",
        "min_similarity": float(os.getenv("MIN_SIMILARITY", 0.55)),
        "email_body": "Dear Hiring Team,\n\nPlease find attached my application.\n\nBest regards,\nYour Name"
    }
    review_and_send(personal_info, email_sender)
