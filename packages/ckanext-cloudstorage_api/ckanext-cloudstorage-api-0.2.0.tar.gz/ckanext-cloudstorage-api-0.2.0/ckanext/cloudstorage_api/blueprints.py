"""Blueprints for plugin."""

import logging

from ckan import model
from ckan.common import g
from ckan.logic import NotFound
from ckan.plugins import toolkit
from flask import Blueprint

from ckanext.cloudstorage_api.logic import get_presigned_url_download

log = logging.getLogger(__name__)


def get_blueprints(name, module):
    """Create Blueprint for plugin."""
    blueprint = Blueprint(name, module)

    blueprint.add_url_rule(
        "/download/<resource_id>",
        view_func=download_presigned_via_redirect,
        methods=["GET"],
    )

    return blueprint


def download_presigned_via_redirect(resource_id):
    """Get a presigned download URL, then redirect.

    :param id: the id of the resource
    :type id: string

    Returns: None
    """
    log.debug("Getting presigned download link and redirecting...")

    context = {
        "model": model,
        "session": model.Session,
        "user": g.user,
        "auth_user_obj": g.userobj,
    }
    data_dict = {"id": resource_id}

    # Check access to resource allowed
    try:
        toolkit.get_action("resource_show")(context, data_dict)
    except NotFound:
        return {"success": False, "error": {"message": "Does not exist, or is hidden."}}

    download_url = get_presigned_url_download(context, data_dict)
    return toolkit.redirect_to(download_url, code=302)
