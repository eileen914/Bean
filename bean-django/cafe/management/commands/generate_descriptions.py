from django.core.management.base import BaseCommand
from cafe.models import Cafe
from gpt.views import review_description
from review.models import Review


class Command(BaseCommand):
    help = "Generate and save GPT-based cafe descriptions"

    def handle(self, *args, **options):
        cafes = Cafe.objects.all()
        for cafe in cafes:
            reviews = Review.objects.filter(cafe = cafe)
            combined_review = "\n".join([r.content for r in reviews])
            if len(combined_review.strip()) == 0:
                continue
            
            try:
                print(f"Generating description for {cafe.name}...")
                description = review_description(combined_review)
                cafe.description = description
                cafe.save()
                print(f"Saved: {description[:50]}...")
            except Exception as e:
                print(f"Error for {cafe.name}: {str(e)}")