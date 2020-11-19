# from flask import jsonify

from app import create_app

def test_ping(client):
    response = client.get("/api/ping")
    data = response.get_json()
    assert data["success"] == True

def test_at_least_one_tag_posts(client):
    """
    """
    response = client.get("/api/posts")
    assert response.status_code == 400

def test_posts(client):
    """
    """
    params = {
        "tags":"history,tech",
        "sortBy":"likes",
        "direction":"desc"
    }
    response = client.get("/api/posts", query_string = params)
    assert response.status_code == 200