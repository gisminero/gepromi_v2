# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.estado_item import EstadoItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDevelopersController(BaseTestCase):
    """DevelopersController integration test stubs"""

    def test_buscar_estado(self):
        """Test case for buscar_estado

        Validacion de numero de expediente
        """
        estadoItem = EstadoItem()
        response = self.client.open(
            '/dariojr/mineria-provincial-api/1.0.0/estado',
            method='POST',
            data=json.dumps(estadoItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_expediente(self):
        """Test case for search_expediente

        Buscar todos los registros coincidentes a un numero de expediente
        """
        query_string = [('searchString', 'searchString_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/dariojr/mineria-provincial-api/1.0.0/estado',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
