import requests

from django.conf import settings


UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"


def get_recommended_images(query, per_page=12):
    if not settings.UNSPLASH_ACCESS_KEY:
        return []

    headers = {
        "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
    }

    params = {
        "query": query,
        "per_page": per_page,
        "order_by": "relevant",
        "content_filter": "high",
    }

    try:
        response = requests.get(
            UNSPLASH_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=5,
        )

        response.raise_for_status()
        data = response.json()

        recommendations = []

        for photo in data.get("results", []):
            recommendations.append({
                "id": photo["id"],
                "image_url": photo["urls"]["regular"],
                "small_url": photo["urls"]["small"],
                "alt_description": (
                    photo.get("alt_description")
                    or photo.get("description")
                    or query
                ),
                "photographer": photo["user"]["name"],
                "photographer_url": photo["user"]["links"]["html"],
                "unsplash_url": photo["links"]["html"],
                "download_location": photo["links"]["download_location"],
            })

        return recommendations

    except requests.RequestException as error:
        print("Unsplash API error:", error)
        return []
    
    
def track_unsplash_download(download_location):
    if not download_location or not settings.UNSPLASH_ACCESS_KEY:
        return False

    headers = {
        "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
    }

    try:
        response = requests.get(
            download_location,
            headers=headers,
            timeout=5,
        )

        response.raise_for_status()
        return True

    except requests.RequestException as error:
        print("Unsplash download tracking error:", error)
        return False    