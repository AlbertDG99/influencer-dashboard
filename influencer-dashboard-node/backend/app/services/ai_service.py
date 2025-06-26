import clip
import torch
from PIL import Image
import requests
from io import BytesIO

from app.models.influencer import InfluencerCategory

# Ensure the model is loaded only once
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Pre-compute text features for categories
categories = [f"a photo of a person related to {category.value}" for category in InfluencerCategory]
text_features = clip.tokenize(categories).to(device)
encoded_text = model.encode_text(text_features)
encoded_text /= encoded_text.norm(dim=-1, keepdim=True)


def get_image_from_url(url: str) -> Image:
    """
    Downloads an image from a URL and returns a PIL Image object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def categorize_image(image_url: str) -> InfluencerCategory:
    """
    Categorizes an image from a URL using CLIP.
    """
    image = get_image_from_url(image_url)
    if not image:
        return InfluencerCategory.OTHER

    image_input = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
    
    # Normalize the image features
    image_features /= image_features.norm(dim=-1, keepdim=True)
    
    # Find the similarity
    similarity = (100.0 * image_features @ encoded_text.T).softmax(dim=-1)
    best_match_idx = similarity.cpu().numpy().argmax()
    
    return list(InfluencerCategory)[best_match_idx] 