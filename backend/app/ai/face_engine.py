"""InsightFace engine for face recognition."""
import numpy as np
import logging
from typing import Optional, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

class FaceEngine:
    """
    Wraps InsightFace buffalo_l model.
    Provides embedding extraction and comparison.
    """

    def __init__(self):
        self.app = None
        self.model_name = settings.INSIGHTFACE_MODEL

    def load_model(self):
        logger.info(f"Loading InsightFace model: {self.model_name}")
        from insightface.app import FaceAnalysis

        self.app = FaceAnalysis(
            name=self.model_name,
            root=settings.INSIGHTFACE_MODEL_DIR,
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        logger.info(f"✅ InsightFace {self.model_name} loaded")

    def _bytes_to_bgr(self, img_bytes: bytes) -> Optional[np.ndarray]:
        try:
            import cv2

            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Could not decode image")
            return img
        except Exception as e:
            logger.error(f"Image decode error: {e}")
            return None

    def compute_quality(self, face) -> float:
        """Score face quality 0-1"""
        score = 0.0
        score += min(float(face.det_score), 1.0) * 0.5
        
        bbox = face.bbox.astype(int)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        face_area = w * h
        area_score = min(face_area / (150*150), 1.0)
        score += area_score * 0.3

        if hasattr(face, 'pose') and face.pose is not None:
            yaw = abs(float(face.pose[1]))
            pose_score = max(0, 1.0 - yaw/45.0)
            score += pose_score * 0.2
        else:
            score += 0.1

        return round(score, 3)

    def extract_embedding(self, img_bytes: bytes) -> Tuple[Optional[np.ndarray], float]:
        """Extract best face embedding and quality score"""
        if self.app is None:
            raise RuntimeError("Face engine is not loaded. Install AI dependencies or set LOAD_FACE_ENGINE_ON_STARTUP=true.")

        img_bgr = self._bytes_to_bgr(img_bytes)
        if img_bgr is None:
            return None, 0.0

        faces = self.app.get(img_bgr)
        if not faces:
            return None, 0.0

        scored = [(face, self.compute_quality(face)) for face in faces]
        best_face, best_quality = max(scored, key=lambda x: x[1])

        embedding = best_face.normed_embedding
        return embedding, best_quality

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings"""
        return float(np.dot(a, b))
