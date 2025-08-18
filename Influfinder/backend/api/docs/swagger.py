from __future__ import annotations

from typing import Any, Dict

from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = "/api/docs"
API_URL = "/api/openapi.json"

swagger_bp = get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={"app_name": "Influfinder API"},
)


def openapi_json(app) -> Dict[str, Any]:
	return {
		"openapi": "3.0.3",
		"info": {"title": "Influfinder API", "version": "1.0.0"},
		"servers": [{"url": "http://localhost:5000"}],
		"paths": {
			"/api/influencers": {
				"get": {
					"summary": "Buscar influencers",
					"parameters": [
						{"name": "q", "in": "query", "schema": {"type": "string"}},
						{"name": "category", "in": "query", "schema": {"type": "string"}},
						{"name": "language", "in": "query", "schema": {"type": "string"}},
						{"name": "page", "in": "query", "schema": {"type": "integer", "minimum": 1}},
						{"name": "page_size", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 100}},
					],
					"responses": {"200": {"description": "Resultados"}},
				},
			},
			"/api/influencers/trending": {"get": {"summary": "Trending", "responses": {"200": {"description": "OK"}}}},
			"/api/influencers/{id}": {
				"get": {
					"summary": "Detalle influencer",
					"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
					"responses": {"200": {"description": "OK"}, "404": {"description": "Not Found"}},
				},
			},
			"/api/influencers/hashtag/{hashtag}": {
				"get": {
					"summary": "Buscar por hashtag",
					"parameters": [
						{"name": "hashtag", "in": "path", "required": True, "schema": {"type": "string"}},
						{"name": "page", "in": "query", "schema": {"type": "integer", "minimum": 1}},
						{"name": "page_size", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 100}},
					],
					"responses": {"200": {"description": "OK"}},
				},
			},
			"/api/export/csv": {"get": {"summary": "Exportar CSV", "responses": {"200": {"description": "OK"}}}},
			"/api/export/xlsx": {"get": {"summary": "Exportar XLSX", "responses": {"200": {"description": "OK"}}}},
			"/api/health": {"get": {"summary": "Health", "responses": {"200": {"description": "OK"}}}},
			"/api/metrics": {"get": {"summary": "Métricas", "responses": {"200": {"description": "OK"}}}},
		},
	}
