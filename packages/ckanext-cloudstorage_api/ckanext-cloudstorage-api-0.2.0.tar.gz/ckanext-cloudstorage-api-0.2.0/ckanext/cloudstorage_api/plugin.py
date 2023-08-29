"""Init plugin with CKAN interfaces."""

import logging
import os

from ckan.plugins import SingletonPlugin, implements, interfaces

from ckanext.cloudstorage_api.auth import get_auth_functions
from ckanext.cloudstorage_api.blueprints import get_blueprints
from ckanext.cloudstorage_api.cli import get_cli_commands
from ckanext.cloudstorage_api.logic import (
    abort_multipart,
    check_multiparts,
    clean_multiparts,
    finish_multipart,
    get_presigned_upload_url_list_multipart,
    get_presigned_upload_url_multipart,
    get_presigned_url_download,
    initiate_multipart,
    list_parts,
)

log = logging.getLogger(__name__)


class CloudstorageAPIPlugin(SingletonPlugin):
    """CloudstoragePlugin.

    Plugin to add endpoints for S3-like object storage.
    """

    implements(interfaces.IConfigurable)
    implements(interfaces.IActions)
    implements(interfaces.IAuthFunctions)
    implements(interfaces.IBlueprint, inherit=True)
    implements(interfaces.IClick)
    implements(interfaces.IResourceController, inherit=True)

    # IConfigurable
    def configure(self, config):
        """Config variable checks."""
        required_keys = (
            "ckanext.cloudstorage_api.bucket_name",
            "ckanext.cloudstorage_api.host",
            "ckanext.cloudstorage_api.region",
            "ckanext.cloudstorage_api.access_key",
            "ckanext.cloudstorage_api.secret_key",
        )

        for rk in required_keys:
            if config.get(rk) is None:
                raise RuntimeError(f"Required configuration option {rk} not found.")

        # Put all into single driver_options var
        config["ckanext.cloudstorage_api.driver_options"] = {
            "host": config.get("ckanext.cloudstorage_api.host"),
            "region_name": config.get("ckanext.cloudstorage_api.region"),
            "key": config.get("ckanext.cloudstorage_api.access_key"),
            "secret": config.get("ckanext.cloudstorage_api.secret_key"),
        }

    # IActions
    def get_actions(self):
        """Actions to be accessible via the API."""
        # TODO coordinate with frontend to rename
        # TODO also rename in auth.py
        # "cloudstorage_initiate": initiate_multipart,
        # "cloudstorage_presign_download": get_presigned_url_download,
        # "cloudstorage_presign_upload": get_presigned_upload_url_multipart,
        # "cloudstorage_presign_upload_list": get_presigned_upload_url_list_multipart,
        # "cloudstorage_list_parts": list_parts,
        # "cloudstorage_finish": finish_multipart,
        # "cloudstorage_abort": abort_multipart,
        # "cloudstorage_check": check_multiparts,
        # "cloudstorage_clean_multiparts": clean_multiparts,
        return {
            "cloudstorage_initiate_multipart": initiate_multipart,
            "cloudstorage_get_presigned_url_download": get_presigned_url_download,
            "cloudstorage_get_presigned_url_multipart": (
                get_presigned_upload_url_multipart
            ),
            "cloudstorage_get_presigned_url_list_multipart": (
                get_presigned_upload_url_list_multipart
            ),
            "cloudstorage_multipart_list_parts": list_parts,
            "cloudstorage_finish_multipart": finish_multipart,
            "cloudstorage_abort_multipart": abort_multipart,
            "cloudstorage_check_multipart": check_multiparts,
            "cloudstorage_clean_multipart": clean_multiparts,
        }

    # IBlueprint
    def get_blueprint(self):
        """Get blueprints, i.e. direct URLs from plugin."""
        return get_blueprints(self.name, self.__module__)

    # IAuthFunctions
    def get_auth_functions(self):
        """API actions that require auth first."""
        return get_auth_functions()

    # IClick
    def get_commands(self):
        """Get click CLI commands for CKAN."""
        return get_cli_commands()

    # IResourceController
    def before_resource_delete(self, context, resource, resources):
        """Delete the resource from the bucket on CKAN deletion."""
        # let's get all info about our resource. It somewhere in resources
        # but if there is some possibility that it isn't(magic?) we have
        # `else` clause

        for res in resources:
            if res["id"] == resource["id"]:
                break
        else:
            return
        # just ignore simple links
        if res["url_type"] != "s3":
            return

        # we don't want to change original item from resources, just in case
        # someone will use it in another `before_delete`. So, let's copy it
        # and add `clear_upload` flag
        res_dict = dict(list(res.items()) + [("clear_upload", True)])

        uploader = self.get_resource_uploader(res_dict)

        # to be on the safe side, let's check existence of container
        container = getattr(uploader, "container", None)
        if container is None:
            return

        # and now uploader removes our file.
        uploader.upload(resource["id"])

        # and all other files linked to this resource
        if not uploader.leave_files:
            upload_path = os.path.dirname(
                uploader.path_from_filename(resource["id"], "fake-name")
            )

            old_files = uploader.driver.iterate_container_objects(
                uploader.container, upload_path
            )

            for old_file in old_files:
                old_file.delete()
