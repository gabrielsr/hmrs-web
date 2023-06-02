
# import all libraires
from io import BytesIO
from flask import Blueprint, send_file
from ..models import Upload

bp_name = "uploads"
bp = Blueprint(bp_name, __name__)

# create download function for download files
@bp.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data),
                     download_name=upload.filename, as_attachment=True)
