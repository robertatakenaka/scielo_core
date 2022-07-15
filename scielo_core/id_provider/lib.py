from scielo_core.id_provider import (
    controller,
)


def request_document_id(
        config_SCIELO_CORE_ID_PROVIDER_DB_URI,
        original_pkg_file_path,
        changed_pkg_file_path,
        username):
    controller.connect(config_SCIELO_CORE_ID_PROVIDER_DB_URI)
    controller.request_document_ids_from_file(
        original_pkg_file_path, username, changed_pkg_file_path)
    return changed_pkg_file_path
