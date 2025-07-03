from django.core.management.base import BaseCommand
from cafe.models import Cafe
import faiss
import numpy as np

class Command(BaseCommand):
    help = "Build and save FAISS index from cafe embeddings"

    def handle(self, *args, **kwargs):
        cafes = Cafe.objects.exclude(embedding=[])
        vectors = [cafe.embedding for cafe in cafes]
        ids = [cafe.id for cafe in cafes]

        if not vectors:
            print("[ERROR] 벡터화된 카페가 없습니다.")
            return

        dim = len(vectors[0])
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(vectors).astype("float32"))

        faiss.write_index(index, "cafe_description.index")
        print(f"[DONE] {len(vectors)}개 벡터가 저장된 FAISS 인덱스를 생성했습니다.")