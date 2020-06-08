import connexion
import six

from swagger_server.models.estado_item import EstadoItem  # noqa: E501
from swagger_server import util


def buscar_estado(estadoItem=None):  # noqa: E501
    """Validacion de numero de expediente

    Adds an item to the system # noqa: E501

    :param estadoItem: Inventory item to add
    :type estadoItem: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        estadoItem = EstadoItem.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def search_expediente(searchString, skip=None, limit=None):  # noqa: E501
    """Buscar todos los registros coincidentes a un numero de expediente

    Tenga en cuenta las caracteristicas propias del expediente valido de su provincia.  # noqa: E501

    :param searchString: pasar un string para busqueda en el campo name
    :type searchString: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[EstadoItem]
    """
    return 'do some magic!'
