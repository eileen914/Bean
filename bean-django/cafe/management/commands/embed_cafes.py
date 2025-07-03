from django.core.management.base import BaseCommand
from cafe.models import Cafe
from django.conf import settings

import openai
import numpy as np
import faiss
import time

openai.api_key = settings.OPENAI_API_KEY

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")  # 1️⃣
    response = openai.Embedding.create(  # 2️⃣
        input=[text],
        model=model
    )
    return response["data"][0]["embedding"]  # 3️⃣

class Command(BaseCommand):
    help = "Embed cafe descriptions and store in the Cafe model"

    def handle(self, *args, **kwargs):
        cafes = Cafe.objects.exclude(description="")

        print(f"[INFO] 벡터화할 카페 수: {cafes.count()}")

        for cafe in cafes:
            try:
                embedding = get_embedding(cafe.description)
                cafe.embedding = embedding
                cafe.save()
                print(f"[OK] Saved embedding for Cafe {cafe.id}: {cafe.name}")
                time.sleep(0.5)  # OpenAI API rate limit 대비
            except Exception as e:
                print(f"[ERROR] Failed on Cafe {cafe.id}: {e}")