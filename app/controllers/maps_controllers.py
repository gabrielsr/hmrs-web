from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired
from wtforms import (StringField, SubmitField, HiddenField)

from app.helpers.form_view import form_edit_view, form_validated, form_view
from app.helpers.standard_paths import get_standard_template_paths
from app.models.map import Map
from werkzeug.utils import secure_filename

from app.models.upload import Upload

from ..models import Map

bp_name = "maps"
bp = Blueprint(bp_name, __name__)

from ..webapp import db

properties = {
    "entity_name": "map",
    "collection_name": "Maps",
    "list_fields": ["name", "description"],
}

tmpl = get_standard_template_paths(bp_name)

@bp.route("/", methods=["GET"])
def index():
    """
    Index page.
    :return: The response.
    """
    entities = Map.query.all()
    return render_template(tmpl.index, entities=entities, **properties)


@bp.route("/<int:id>/show", methods=["GET"])
def show(id: int):
    """
    Show page.
    :return: The response.
    """
    entity = db.get_or_404(Map, id)
    return render_template(tmpl.show, entity=entity, **properties)

class MapForm(FlaskForm):
    name = StringField("name", validators=[InputRequired()])
    submit = SubmitField("Submit")

@bp.route("/new", methods=["GET"])
@login_required
@form_view(MapForm)
def new(form: MapForm):
    """
    Page to create new Entity
    :return: render create template
    """
    return render_template(tmpl.new, form=form, **properties)


@bp.route("/", methods=["POST"])
@form_validated(MapForm, new)
def create(form: MapForm):
    """
    Create new entity
    If form is valid, create new entity and redirect to show page
    If form is not valid, render new template with errors

    :return: redirect to view new entity
    """
    new = Map()
    form.populate_obj(new)
    db.session.add(new)
    db.session.commit()
    flash(f"'{ new.name}' created")
    return redirect(url_for('.show', id=new.id))


@bp.route("/<int:id>/edit", methods=["GET"])
@form_edit_view(MapForm, entitycls=Map)
def edit(form: MapForm, id: int):
    """
    Edit page.
    :return: The response.
    """
    return render_template(tmpl.edit,form=form, **properties)


# @bp.route("/<int:id>", methods=["UPDATE"])
@bp.route("/<int:id>/edit", methods=["POST"])
@form_validated(MapForm, edit)
def update(form: MapForm, id: int):
    """
    Save Edited Entity
    If form is valid, update entity and redirect to show page
    If form is not valid, render edit template with errors
    :return: redirect to show entity
    """
    entity = db.get_or_404(Map, id)
    form.populate_obj(entity)
    db.session.add(entity)
    db.session.commit()
    flash(f"'{ entity.name}' updated")
    return redirect(url_for('.upload', id=id))


# @bp.route("/<int:id>", methods=["DELETE"])
@bp.route("/<int:id>/delete", methods=["POST"])
def destroy(id: int):
    """
    Delete Entity
    :return: redirect to list
    """
    entity = db.get_or_404(Map, id)
    db.session.delete(entity)
    db.session.commit()
    flash(f"'{ entity.name}' deleted")
    return redirect(url_for('.index'))


class MapUploadForm(FlaskForm):
    map_id = HiddenField("map")
    map_file = FileField(validators=[FileRequired()])
    submit = SubmitField("Submit")

@bp.route("/<int:id>/upload", methods=["GET"])
@form_view(MapUploadForm)
def new_file(uploadform, id: int):
    """
    Edit page.
    :return: The response.
    """
    uploadform.map_id = id
    return render_template(tmpl.edit, uploadform=uploadform, **properties)

@bp.route("/<int:id>/upload", methods=["POST"])
@form_view(MapUploadForm)
def create_file(uploadform: MapUploadForm, id: int):
    """
    Save Edited Entity
    If form is valid, update entity and redirect to show page
    If form is not valid, render edit template with errors
    :return: redirect to show entity
    """
    map: Map = db.get_or_404(Map, id)

    f = uploadform.map_file.data
    filename = secure_filename(f.filename)
    upload = Upload(filename=filename, data=f.read())
    map.file = upload

    db.session.add(map)
    db.session.commit()
    flash(f"'{ map.name}' updated")
    return redirect(url_for('.show', id=id))
