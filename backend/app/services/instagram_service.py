def get_mock_instagram_data(username: str):
    """
    Returns mock data simulating a call to the Instagram API.
    In a real application, this function would use the Instagram Graph API.
    """
    print(f"--- MOCK INSTAGRAM API: Fetching data for {username} ---")

    # Mock profile data
    mock_profile = {
        "username": username,
        "full_name": f"{username.replace('_', ' ').title()}",
        "biography": f"Bio for {username} | Just a mock profile 🚀",
        "followers_count": 12345,
        "profile_pic_url": f"https://source.unsplash.com/200x200/?portrait,{username}",
    }

    # Mock posts data
    mock_posts = [
        {
            "id": f"mock_post_1_{username}",
            "display_url": "https://source.unsplash.com/800x800/?fashion",
            "caption": "Loving this new outfit! #fashion #style",
            "likes_count": 1500,
            "comments_count": 50
        },
        {
            "id": f"mock_post_2_{username}",
            "display_url": "https://source.unsplash.com/800x800/?travel",
            "caption": "Adventures in the mountains. #travel #adventure",
            "likes_count": 2200,
            "comments_count": 80
        },
        {
            "id": f"mock_post_3_{username}",
            "display_url": "https://source.unsplash.com/800x800/?food",
            "caption": "Best pasta I've ever had. #foodie #food",
            "likes_count": 1800,
            "comments_count": 120
        },
    ]
    
    print(f"--- MOCK INSTAGRAM API: Found profile and {len(mock_posts)} posts ---")

    return mock_profile, mock_posts 