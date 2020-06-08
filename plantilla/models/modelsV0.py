# -*- coding: utf-8 -*-
from odoo import models, fields, api

class vacia(models.Model):
    _name = 'plantilla.vacia'
    name = fields.Char('Nombre de plantilla', required=True)
    description = fields.Char('Descripcion', required=False)
    archivo = fields.Binary(string='Plantilla', required=True, help='Subir las plantillas en Word.')
    #tareas = fields.Many2many('tarea.flujolinea', string='Tareas Vinculadas con la Plantilla')
    active = fields.Boolean('Activo', default=True)

class rel(models.Model):
    _name = 'plantilla.rel'

    @api.depends('tarea_id', 'procedimiento_id')
    def _nombreAsociacion(self):
        tarea = self.tarea_id
        tramite = self.procedimiento_id
        if tarea and tramite:
            name_new = "Plantillas asociadas a tarea/tramite: " + str(tarea.codigo) + " - " + str(tarea.name) + '/'+ str(tramite.name)
        elif tarea:
            name_new = "Plantillas asociadas a tarea: " + str(tarea.codigo) + " - " + str(tarea.name)
        elif tramite:
            name_new = "Plantillas asociadas a tramite: " + str(tramite.name)
        else:
            name_new = str('Seleccione tarea y/o tramite.')
        self.name = name_new

    name = fields.Char('Nombre', required=False)# compute="_nombreAsociacion"
    plantilla_id = fields.Many2many('plantilla.vacia', string='Plantillas asociadas')
    tarea_id = fields.Many2one('tarea.tarea', string='Tarea asociada')
    procedimiento_id = fields.Many2one('procedimiento.procedimiento',
        string = 'Tramite asociado')


class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Plantillas"
        #_table = 'mrp_recep'
        #_order = "id desc"
        _columns = {}

        def plantillas(self):
            print (("ACCEDIENDO A LA FUNCION CORRECTA"))
            active_id = self.env.context.get('id_activo')
            print (("ENVIANDO .... " + str(active_id)))
            user_id = self.env.user.id
            #print (())
            expte_obj = self.browse([active_id])
            print (("OBJETO.... " + str(expte_obj.name)))
            depart_actual_id = expte_obj.ubicacion_actual
            if not depart_actual_id:
                print (("No hay oficina actual asignada."))
            else:
                print (("La oficina actual es: " + depart_actual_id.name))
            #CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
            plant_rel_proced_obj_cant = self.env['plantilla.rel'].search_count([('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
            plant_rel_proced_obj = self.env['plantilla.rel'].search([('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
            print (("Cantidad de plantillas relacionadas con el tramite: " + str(plant_rel_proced_obj_cant)  ))
            ids_plantillas = []
            for rel in plant_rel_proced_obj:
                ids_plantillas.append((rel.plantilla_id.id))
                print (("PLANTILLA 0" + str(rel.plantilla_id.name)))
            print (("La lista de encontrados es: " + str(ids_plantillas)))
            #FIN CONSULTANDO PLANTILLAS
            if plant_rel_proced_obj_cant > 0:
                #NUEVO PASE A OFICINA
                return {
                'name': "Plantillas Asociadas a la Tarea/Tramite",
                'view_mode': 'tree',
                'res_id': active_id,
                #'view_id': self.env.ref('pase.form_enviar').id,
                'res_model': 'plantilla.vacia',
                'type': 'ir.actions.act_window',
                #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                'domain': [('id', 'in', ids_plantillas)],
                'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                'views': [[self.env.ref('plantilla.vacia_list').id, "tree"]],
                'target': 'new',
                }
            else:
                print (('No existen plantillas asociadas.'))
            return True

    #def enviar(self):
        ##pase_obj = self.env['pase.pase']
        ##if not pase_obj:
            ##raise ValidationError(('Debe instalar el modulo de pases.'))
        ##active_id = self.env.context.get('active_ids')
        #active_id = self.env.context.get('id_activo')
        #print (("ENVIANDO .... " + str(active_id)))
        #user_id = self.env.user.id
        ##print (())
        #expte_obj = self.browse([active_id])
        #print (("OBJETO.... " + str(expte_obj.name)))
        #depart_id = self.userdepart(user_id)
        ##CONSULTANDO PASES
        #pase_obj = self.env['pase.pase']
        #pase_res = pase_obj.obtener_ultimo_pase(active_id, depart_id)
        ##FIN CONSULTANDO PASES
        #if not pase_res:
            ##NUEVO PASE A OFICINA
            #self.write({'observaciones': False})
            #if depart_id:
                #return {
                #'name': "Enviando Documento",
                #'view_mode': 'form',
                #'res_id': active_id,
                ##'view_id': self.env.ref('pase.form_enviar').id,
                #'res_model': 'expediente.expediente',
                #'type': 'ir.actions.act_window',
                ##'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                ##'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                #'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                #'views': [[self.env.ref('expediente.form_enviar').id, "form"]],
                #'target': 'new',#ESTA OPCION ABRE UN POP UP, MUY INTERESANTE
                #}
            #else:
                #raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        #else:
            #if depart_id:
                #return {
                #'name': "EL DOCUMENTO SE ENCUENTRA ENVIADO A: "+ expte_obj.oficina_destino.name,
                #'view_mode': 'form',
                #'res_id': active_id,
                ##'view_id': self.env.ref('pase.form_enviar').id,
                #'res_model': 'expediente.expediente',
                #'type': 'ir.actions.act_window',
                ##'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                ##'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                #'context': {'recibido': True, 'ultimo_pase_id': pase_res.id, 'oficina_destino': depart_id},
                #'views': [[self.env.ref('expediente.form_enviado').id, "form"]],
                #'target': 'new',#ESTA OPCION ABRE UN POP UP, MUY INTERESANTE
                #}
            #else:
                #raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        #return True