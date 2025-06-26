import time
from collections import Counter

from sqlmodel import Session, select
from app.core.celery_app import celery_app
from app.db.session import engine
from app.models.influencer import Influencer
from app.services.ai_service import categorize_image
from app.services.instagram_service import get_mock_instagram_data

@celery_app.task
def analyze_influencer_profile(influencer_id: int):
    """
    Celery task to analyze an influencer's profile.
    This simulates fetching data from Instagram and running AI analysis.
    """
    print(f"Starting analysis for influencer_id: {influencer_id}")
    with Session(engine) as session:
        # 1. Get influencer from DB
        influencer = session.get(Influencer, influencer_id)
        if not influencer:
            print(f"Influencer with id {influencer_id} not found.")
            return

        # 2. Fetch data from Instagram (mocked)
        # In a real scenario, this would call the Instagram Graph API
        profile_data, posts_data = get_mock_instagram_data(influencer.username)

        # 3. Update influencer profile with fetched data
        influencer.full_name = profile_data.get("full_name")
        influencer.bio = profile_data.get("biography")
        influencer.followers_count = profile_data.get("followers_count")
        influencer.profile_picture_url = profile_data.get("profile_pic_url")
        
        session.add(influencer)
        session.commit()
        session.refresh(influencer)

        print(f"Updated base profile for {influencer.username}")

        # 4. Analyze images and categorize
        if not posts_data:
            print(f"No posts found for {influencer.username} to analyze.")
            return

        categories = []
        for post in posts_data:
            category = categorize_image(post["display_url"])
            categories.append(category)
            time.sleep(1) # Avoid overwhelming the service

        # 5. Determine main category based on most frequent one
        if categories:
            most_common_category = Counter(categories).most_common(1)[0][0]
            influencer.main_category = most_common_category
            print(f"Main category for {influencer.username}: {most_common_category.value}")

        session.add(influencer)
        session.commit()

    print(f"Analysis complete for influencer_id: {influencer_id}")
    return {"status": "complete", "influencer_id": influencer_id} 