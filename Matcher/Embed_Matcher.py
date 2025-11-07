# matcher/embed_matcher.py
from sentence_transformers import SentenceTransformer, util
import sqlite3

MODEL_NAME = "all-MiniLM-L6-v2"

class EmbedMatcher:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

    def score(self, job_desc, resume_text):
        emb_job = self.model.encode(job_desc, convert_to_tensor=True)
        emb_resume = self.model.encode(resume_text, convert_to_tensor=True)
        score = float(util.cos_sim(emb_job, emb_resume))
        return score
