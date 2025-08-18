from __future__ import annotations

import io
from datetime import datetime

from flask import Blueprint, Response, request, send_file

from backend.domain.services.export_service import ExportService
from backend.infrastructure.repositories.factory import get_influencer_repository
from backend.utils.validators import parse_pagination


export_bp = Blueprint("export_bp", __name__)
service = ExportService(repository=get_influencer_repository())


@export_bp.get("/csv")
def export_csv() -> Response:
	q = request.args.get("q")
	category = request.args.get("category")
	page, page_size = parse_pagination(request)
	csv_bytes = service.export_csv(query=q, category=category, language=None, page=page, page_size=page_size)
	filename = f"influencers_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
	return Response(csv_bytes, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@export_bp.get("/xlsx")
def export_xlsx():
	q = request.args.get("q")
	category = request.args.get("category")
	page, page_size = parse_pagination(request)
	xlsx_bytes = service.export_xlsx(query=q, category=category, language=None, page=page, page_size=page_size)
	filename = f"influencers_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"
	return send_file(io.BytesIO(xlsx_bytes), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True, download_name=filename)
