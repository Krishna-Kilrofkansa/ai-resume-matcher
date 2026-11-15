import os
import torch
import numpy as np
from typing import List, Dict, Any, Optional

# Limit PyTorch to 4 threads to prevent pegging all CPU cores on Intel i5-1235U
torch.set_num_threads(4)

from sentence_transformers import SentenceTransformer

# Empirical calibration bounds derived from benchmark distribution
DEFAULT_C_FLOOR = 0.30     # 5th percentile of mismatched resume-JD pairs
DEFAULT_C_CEILING = 0.85   # 95th percentile of top-matching resume-JD pairs


class EmbeddingEngine:
    """
    Semantic embedding engine powered by bge-small-en-v1.5 (512-token context window).
    Implements Chunk-Level MaxSim late interaction:
      - Evaluates each JD requirement individually against candidate experience bullets.
      - Eliminates resume truncation.
      - Generates line-by-line semantic citations and calibrated scores.
    """

    _instance: Optional["EmbeddingEngine"] = None

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._load_model()

    @classmethod
    def get_instance(cls, model_name: str = "BAAI/bge-small-en-v1.5") -> "EmbeddingEngine":
        """Singleton accessor to ensure the model is loaded into memory only once."""
        if cls._instance is None:
            cls._instance = cls(model_name)
        return cls._instance

    def _load_model(self):
        try:
            print(f"Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print(f"Successfully loaded {self.model_name}.")
        except Exception as e:
            print(f"Warning: Failed to load {self.model_name} ({e}). Falling back to all-MiniLM-L6-v2...")
            self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
            self.model = SentenceTransformer(self.model_name)

    def encode(self, texts: List[str], batch_size: int = 16) -> np.ndarray:
        """Encodes a list of texts into normalized float32 embeddings."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        return np.asarray(embeddings, dtype=np.float32)

    def compute_maxsim(
        self,
        jd_requirements: List[str],
        resume_chunks: List[str],
        c_floor: float = DEFAULT_C_FLOOR,
        c_ceiling: float = DEFAULT_C_CEILING
    ) -> Dict[str, Any]:
        """
        Computes Requirement-Level MaxSim late-interaction matching:
        For every requirement r_i, finds the best matching resume chunk c_j.
        """
        if not jd_requirements:
            return {
                "semantic_score": 100.0,
                "raw_similarity": 1.0,
                "requirement_matches": []
            }

        if not resume_chunks:
            return {
                "semantic_score": 0.0,
                "raw_similarity": 0.0,
                "requirement_matches": []
            }

        # Encode both requirement lines and resume chunks
        req_vectors = self.encode(jd_requirements)
        chunk_vectors = self.encode(resume_chunks)

        # Pairwise cosine similarities: shape (num_requirements, num_chunks)
        sim_matrix = np.dot(req_vectors, chunk_vectors.T)

        requirement_matches: List[Dict[str, Any]] = []
        best_sims: List[float] = []

        for i, req in enumerate(jd_requirements):
            row_sims = sim_matrix[i]
            best_chunk_idx = int(np.argmax(row_sims))
            best_sim = float(row_sims[best_chunk_idx])
            best_chunk = resume_chunks[best_chunk_idx]

            best_sims.append(best_sim)
            requirement_matches.append({
                "requirement": req,
                "best_matching_chunk": best_chunk,
                "similarity": round(best_sim, 3),
                "is_satisfied": best_sim >= 0.50
            })

        # Average of best-matching similarities
        raw_avg_sim = float(np.mean(best_sims))

        # Calibrated min-max scaling
        calibrated_score = self.calibrate_similarity(raw_avg_sim, c_floor, c_ceiling)

        return {
            "semantic_score": calibrated_score,
            "raw_similarity": round(raw_avg_sim, 3),
            "requirement_matches": requirement_matches,
            "c_floor": c_floor,
            "c_ceiling": c_ceiling
        }

    @staticmethod
    def calibrate_similarity(sim: float, c_floor: float, c_ceiling: float) -> float:
        """Linearly scales cosine similarity from [c_floor, c_ceiling] into [0, 100]."""
        if c_ceiling <= c_floor:
            return 100.0 if sim >= c_floor else 0.0
        scaled = (sim - c_floor) / (c_ceiling - c_floor) * 100.0
        clamped = max(0.0, min(100.0, scaled))
        return round(clamped, 1)
