from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from backend.domain.services.influencer_service import InfluencerService
from backend.infrastructure.repositories.factory import get_influencer_repository
from backend.utils.validators import parse_pagination


influencer_bp = Blueprint("influencer_bp", __name__)
service = InfluencerService(repository=get_influencer_repository())


@influencer_bp.get("")
def list_influencers() -> Any:
	q = request.args.get("q")
	category = request.args.get("category")
	page, page_size = parse_pagination(request)
	result = service.search_influencers(query=q, category=category, language=None, page=page, page_size=page_size)
	return jsonify(result)


@influencer_bp.get("/trending")
def trending_influencers() -> Any:
	category = request.args.get("category")
	page, page_size = parse_pagination(request)
	result = service.get_trending(category=category, language=None, page=page, page_size=page_size)
	return jsonify(result)


@influencer_bp.get("/<string:influencer_id>")
def get_influencer(influencer_id: str) -> Any:
	data = service.get_by_id(influencer_id)
	return jsonify(data)


@influencer_bp.get("/hashtag/<string:hashtag>")
def by_hashtag(hashtag: str) -> Any:
	page, page_size = parse_pagination(request)
	data = service.search_by_hashtag(hashtag=hashtag, page=page, page_size=page_size)
	return jsonify(data)
