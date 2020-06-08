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

    @api.depends('name', 'tarea_id', 'procedimiento_id')
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
#LA SIGUIENTE CLASE SERIA PARA ASOCIAR LAS PLANTILLAS A LAS TAREAS
#nO LO DEJO PORQUE SOLO VA A SERVIR PARA LOS TRAMITES QUE SE ENCUENTREN
# EN EL FLUJO NO ASI LOS QUE NO TENGAN TAREAS ESTABLECIDAS
#class tarea(models.Model):
    #_name = 'tarea.tarea'
    #_inherit = 'tarea.tarea'

    #plazos = fields.Many2many('plantilla.vacia', string='Plantillas Asociadas', help="Plantillas vacias asociadas a la tarea.")


class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Agregar Asociacion con Plantillas"
    #_table = 'mrp_recep'
    #_order = "id desc"
    _columns = {}

    def tiene_flujo(self, proced_id):
        print(("COMPROBANDO SI HAY FLUJO PARA EL PROCED CON EL ID: " + str(proced_id)))
        #bus = self.env['tarea_fujo.flujo'].search_count([('name.id', 'in', [proced_id])])
        bus = self.env['tarea_flujo.flujo'].search([('name.id', 'in', [proced_id])])
        if not bus:
            print(("EL PROCEDIMIENTO NO TIENE FLUJO... "))
            return False
        tff_obj = self.env['tarea_flujo.flujo'].browse(bus.id)
        #print (("EL NOMBRE DEL PROCEDIMIENTO ES ;: " + tff_obj.name.name))
        # for inicial in ta_obj.lineflujo_ids:
        #     print(("INGRESA EN EL FOR"))
        #     if inicial.tarea_padre.tipo == '1':
        #         return inicial.tarea_padre.id
        return True
        #return 147

    def plantillas(self):
        active_id = self.env.context.get('id_activo')
        # print (("ENVIANDO .... " + str(active_id)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
        depart_actual_id = expte_obj.ubicacion_actual
        if not depart_actual_id:
            print (("No hay oficina actual asignada."))
        #CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
        if tiene_flujo_asociado and expte_obj.tarea_actual:
            plant_rel_proced_obj_cant = self.env['plantilla.rel'].search_count([('tarea_id', '=', expte_obj.tarea_actual.id)])
            plant_rel_proced_obj = self.env['plantilla.rel'].search([('tarea_id', '=', expte_obj.tarea_actual.id)])
        else:
            plant_rel_proced_obj_cant = self.env['plantilla.rel'].search_count([('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
            plant_rel_proced_obj = self.env['plantilla.rel'].search([('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
        # print(("Cantidad de plantillas relacionadas con el tramite: " + str(plant_rel_proced_obj)))
        ids_plantillas = []
        ids_plantillas_rel = []
        for rel in plant_rel_proced_obj:
            for plant in rel:
                print ((str(plant.id)))
                ids_plantillas_rel.append(plant.id)
        ids_plantillas_rel_str = ''
        for i in ids_plantillas_rel:
            if ids_plantillas_rel_str == '':
                ids_plantillas_rel_str = '(' + str(i)
            else:
                ids_plantillas_rel_str = ids_plantillas_rel_str + ", "+str(i)
        if ids_plantillas_rel_str != '':
            ids_plantillas_rel_str = ids_plantillas_rel_str + ')'
            #print (("La lista STRING de encontrados es: " + ids_plantillas_rel_str))
            self.env.cr.execute("""SELECT plantilla_vacia_id FROM plantilla_rel_plantilla_vacia_rel WHERE plantilla_rel_id IN """+ids_plantillas_rel_str+""";""")
            plant_rel_ids = self.env.cr.fetchall()
            #print (("SALIDA: " + str(plant_rel_ids)))
            for e in plant_rel_ids:
                ids_plantillas.append(e)
        #FIN OBTENER LAS RELACIONES
        if plant_rel_proced_obj_cant > 0:
            #NUEVO PASE A OFICINA
            return {
            'name': "Plantillas Asociadas a la Tarea/Tramite",
            'view_mode': 'tree',
            #'res_id': active_id,
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
            return {
            'name': "No se Encontraron Plantillas Asociadas a la Tarea/Tramite",
            'view_mode': 'tree',
            #'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'plantilla.vacia',
            'type': 'ir.actions.act_window',
            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
            'domain': [('id', 'in', ids_plantillas)],
            'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
            'views': [[self.env.ref('plantilla.vacia_list').id, "tree"]],
            'target': 'new',
            }
        return True

