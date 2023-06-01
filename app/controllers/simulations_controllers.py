from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.helpers.standard_paths import get_standard_template_paths
from app.live_simulations.domain_model import LiveSimulation

from ..webapp import db


from ..webapp import task_runner
repo = task_runner.repository


bp_name = "simulations"

bp = Blueprint(bp_name, __name__)


properties = {
    "entity_name": "movie",
    "collection_name": "Movies",
    "list_fields": ["title", "rating", "description"],
}

class _to:
    def __to(method):
        return lambda **kwargs: url_for(f"{bp_name}.{method}", **kwargs)

    index = __to("index")
    show = __to("show")
    edit = __to("edit")
    delete = __to("delete")


tmpl = get_standard_template_paths(bp_name)


# class SimulationForm(FlaskForm):
#     title = StringField("title", validators=[InputRequired()])


@bp.route("/<int:id>/show", methods=["GET"])
def show(id: int):
    """
    Show page.
    :return: The response.
    """
    sim: LiveSimulation = repo.get(id)


    # sim = sim_repository.get(id)
    return render_template(tmpl.show, sim = sim) #, entity=sim, **properties)




