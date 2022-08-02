from scielo_core.id_provider import (
    controller,
    exceptions,
)


def connect(config_SCIELO_CORE_ID_PROVIDER_DB_URI):
    return controller.connect(config_SCIELO_CORE_ID_PROVIDER_DB_URI)


def get_xml(v3):
    return controller.get_xml(v3)


def request_document_id(
        original_pkg_file_path,
        changed_pkg_file_path,
        username,
        id_provider_db_uri):
    """
    Request PID v3

    Parameters
    ----------
    original_pkg_file_path: str
        path of a zip file which contains at least one XML
    changed_pkg_file_path: str
        path of the resulting zip file
    username: str
        requester
    id_provider_db_uri: str
        location of mongodb

    Returns
    -------
        dict
            {"changed_xmls": changed_xmls, "pkg_path": changed_pkg_file_path}

    Raises
    ------
    exceptions.InputDataError
    exceptions.ConclusionError
    exceptions.ConnectionFailure
    exceptions.InvalidNewPackageError
    """
    try:
        return controller.request_document_ids_from_file(
            original_pkg_file_path, username, changed_pkg_file_path,
            id_provider_db_uri)
    except exceptions.ConnectionFailure:

        connect(id_provider_db_uri)

        return controller.request_document_ids_from_file(
            original_pkg_file_path, username, changed_pkg_file_path)
