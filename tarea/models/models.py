# -*- coding: utf-8 -*-

from odoo import models, fields, api
from unidecode import unidecode

class tarea(models.Model):
    _name = 'tarea.tarea'
    _description = 'Tareas a Ejecutar'
    _rec_name = 'name'

    @api.one
    def _get_value(self):
        print('INSIDE')
        if self.tipo == '4':
            self.fueraflujo=True
            print('TRUE')

    name = fields.Char('Nombre', required=True)
    codigo = fields.Char('Codigo', required=False)
    descrip = fields.Char('Descripcion', required=False)
    active = fields.Boolean('Activo', default=True)
    departament_id = fields.Many2one('hr.department', 'Oficina', copy=False, required=True)
    tipo = fields.Selection([
        ('1', 'Inicial'),
        ('2', 'Proceso'),
        ('6', 'Inicio de Subproceso'),#Solo usado para indicar que se esta entrando en subflujo
        ('3', 'Final_Archivo'),
        ('5', 'Final_Vuelve'),
        ('4', 'Fuera de Flujo')
                ], 'Tipo de Tarea', index=True, readonly=False, default='2', required=True)
    subproc =fields.Many2one('procedimiento.procedimiento', 'Subproceso', required=False, domain=[('iniciado', '=', 2)])
    plazos = fields.Many2many('tarea.plazo', string='Plazos de Tiempo', help="Only for tax excluded from price")
    estado_legal = fields.Many2one('estado_legal.estado_legal', 'Estado Legal', copy=False, required=False)
    fueraflujo = fields.Boolean('Suspende Plazo',required=False, compute='_get_value')

    def name_get(self):
        result = []
        for record in self:
            if not record.codigo:
                codigo = "-"
            else:
                codigo = unidecode(record.codigo)
            if not record.name:
                nombre = "-"
            else:
                nombre = unidecode(record.name)
            # if not record.tipo:
            #     tipo = "-"
            # else:
            #     tipo = dict(self._fields['tipo'].selection).get(self.tipo)
            # print (("ASI SE VE EL PARA: " + str(tipo)))
            record_name = codigo + ' - ' + nombre # + ' (' + str(tipo) + ')'
            result.append((record.id, record_name))
        return result

class plazo(models.Model):
    _name = 'tarea.plazo'
    _description = 'Plazos de Tiempo'
    name = fields.Char('Nombre', required=True)
    descrip = fields.Char('Descripcion', required=False)
    active = fields.Boolean('Activo', default=True)
    #voucher_id = fields.Many2one('tarea.tarea', 'Tarea', required=1, ondelete='cascade')
    cant = fields.Integer('Dias de Plazo', required=True)
    tipo = fields.Selection([
            ('1', 'Habiles'),
            ('2', 'Corridos'),
        ], 'Dias de Plazo', index=True, readonly=False, default='1')
    #07-03-19: Asociar grupos de usuarios que deben recibir el aviso
    #y de que forma
