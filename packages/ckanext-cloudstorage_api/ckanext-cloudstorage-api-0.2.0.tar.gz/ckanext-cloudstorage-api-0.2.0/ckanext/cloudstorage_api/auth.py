"""Require authentication on endpoints."""

from ckan.logic import check_access


def get_auth_functions():
    """Collect all auth functions for plugin."""
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


def initiate_multipart(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_create", context, data_dict)}


def get_presigned_url_download(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_show", context, data_dict)}


def get_presigned_upload_url_multipart(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_create", context, data_dict)}


def get_presigned_upload_url_list_multipart(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_create", context, data_dict)}


def list_parts(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_show", context, data_dict)}


def finish_multipart(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_create", context, data_dict)}


def abort_multipart(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_create", context, data_dict)}


def check_multiparts(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": check_access("resource_show", context, data_dict)}


def clean_multiparts(context, data_dict):
    """Place auth in front of CKAN action."""
    return {"success": False}
