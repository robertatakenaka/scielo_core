import logging
import os
from zipfile import ZipFile, BadZipFile


LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class XMLReadError(Exception):
    ... 


def get_xml_content(xml_sps_file_path):
    """
    Get XML content from XML file or Zip file

    Arguments
    ---------
        xml_sps_file_path: str

    Return
    ------
    str
    """
    LOGGER.info(
        "Try to get xml content from zipfile %s" % xml_sps_file_path
    )
    name, ext = os.path.splitext(xml_sps_file_path)
    try:
        if ext == ".zip":
            return get_xml_content_from_zip_file(xml_sps_file_path)
        if ext == ".xml":
            return get_xml_content_from_xml_file(xml_sps_file_path)
    except IOError as e:
        raise XMLReadError(
            "Unable to get xml content from %s: %s %s" %
            (xml_sps_file_path, type(e), e)
        )


def get_xml_content_from_zip_file(xml_sps_file_path):
    """
    Return the first XML content in the Zip file.

    Arguments
    ---------
        xml_sps_file_path: str
        content: bytes

    Return
    ------
    str
    """
    with ZipFile(xml_sps_file_path) as zf:
        for item in zf.namelist():
            if item.endswith(".xml"):
                return zf.read(item).decode("utf-8")


def get_xml_content_from_xml_file(xml_sps_file_path):
    with open(xml_sps_file_path, "rb") as fp:
        return fp.read().decode("utf-8")


def update_zip_file_xml(xml_sps_file_path, xml_file_path, content):
    """
    Save XML content in a Zip file.
    Return saved zip file path

    Arguments
    ---------
        xml_sps_file_path: str
        content: bytes

    Return
    ------
    str
    """
    with ZipFile(xml_sps_file_path, "w") as zf:
        LOGGER.debug("Try to write xml %s %s %s" %
                     (xml_sps_file_path, xml_file_path, content[:100]))
        zf.writestr(xml_file_path, content)

    return xml_sps_file_path


def create_xml_zip_file(xml_sps_file_path, content):
    """
    Save XML content in a Zip file.
    Return saved zip file path

    Arguments
    ---------
        xml_sps_file_path: str
        content: bytes

    Return
    ------
    str
    """
    dirname = os.path.dirname(xml_sps_file_path)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)

    basename = os.path.basename(xml_sps_file_path)
    name, ext = os.path.splitext(basename)

    with ZipFile(xml_sps_file_path, "w") as zf:
        zf.writestr(name + ".xml", content)
    return os.path.isfile(xml_sps_file_path)


def get_xml_content_items(xml_sps_file_path, filenames=None):
    """
    Get XML content items from XML file or Zip file

    Arguments
    ---------
        xml_sps_file_path: str

    Return
    ------
    dict
    """
    name, ext = os.path.splitext(xml_sps_file_path)
    try:
        if ext == ".zip":
            return get_xml_content_items_from_zip_file(xml_sps_file_path, filenames)
        if ext == ".xml":
            xml = get_xml_content_from_xml_file(xml_sps_file_path)
            item = os.path.basename(xml_sps_file_path)
            return {item: xml}

    except IOError as e:
        raise XMLReadError(
            "Unable to get xml content items from %s: %s %s" %
            (xml_sps_file_path, type(e), e)
        )


def get_xml_content_items_from_zip_file(xml_sps_file_path, filenames):
    LOGGER.info(
        "Try to get xml content items from zipfile %s" % xml_sps_file_path
    )
    bad_xmls = []
    items = {}

    with ZipFile(xml_sps_file_path) as zf:
        for item in zf.namelist():
            name, ext = os.path.splitext(item)
            if ext == ".xml":
                if filenames and item not in filenames:
                    continue
                try:
                    items[item] = zf.read(item).decode("utf-8")
                except Exception as e:
                    bad_xmls.append((item, e))

    if bad_xmls:
        raise XMLReadError("\n".join([
            "Unable to read %s from %s: %s %s" % (item, xml_sps_file_path, type(e), e)
            for item, e in bad_xmls
        ]))
    return items
