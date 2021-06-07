# -*- coding: utf-8 -*-
from odoo import models, fields, api

class exp_historia_correcc(models.Model):
    _name = 'exp_historia_correcc'
    # _order = 'create_date desc'

    tramite_id = fields.Many2one('procedimiento.procedimiento', string="Trámite")
    # nombre_pedimento = fields.Char('Nombre Pedimento', required=False)
    nombre_titular = fields.Char('Nombre Titular', required=False)
    cuit_titular = fields.Char('CUIT del Titular', required=False)
    exp_id = fields.Many2one('expediente.expediente', string="Expediente al que correponde", reaonly=True)

    def write(self):
        print(("CAMBIANDO NOMBRE DE TITULAR" + self.nombre_titular))
        self.cambio_tramite_en_expte()
        self.exp_id.write({'cambio_de_tramite': False})
        vals = {'tramite_id': self.tramite_id.id, 'nombre_titular': self.nombre_titular,
                'cuit_titular': self.cuit_titular, 'exp_id': self.exp_id.id}
        return super(exp_historia_tramite, self).write(vals)

    def cambio_tramite_en_expte(self):
        exp_obj = self.env['expediente.expediente'].browse([self.exp_id.id])
        print ((" ESTE ES EL EXPEDIENTE ENCONTRADO: " + exp_obj.name))
        vals = {'procedimiento_id': self.tramite_id.id, 'solicitante': self.nombre_titular,
                'solicitante_cuit': self.cuit_titular}
        return exp_obj.write(vals)

class exp_envios_admin(models.Model):
    _name = 'exp_envios_admin'
    _description = "Listado de pases"

class pase(models.Model):
    _name = 'pase.pase'
    _inherit = 'pase.pase'
    _description = "Listado de pases"

    def enviados_sin_recepcion_view(self):
        print ("BUSCANDO MI OFICINA ################################")
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Expedientes en Mi Oficina",
                'view_mode': 'tree, form',
                'res_model': 'pase.pase',
                'type': 'ir.actions.act_window',
                'domain': [('depart_origen_id', '=', depart_user_id), ('fecha_hora_recep', '=', False)],
                'views': [[self.env.ref('exp_envios_admin.envios_no_rec_list').id, "tree"], [self.env.ref('exp_envios_admin.envios_no_rec_form').id, "form"]],
                }
        return action
    # self.env['expediente.expediente'].depart_user()

    def enviados_reclamados_view(self):
        # user_id = self.env.user.id
        # depart_user_id = self.userdepart(user_id)
        view = self.env.ref('sh_message.sh_message_wizard_false')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context[
            'message'] = 'Esta funcionalidad se encuentra en desarrollo.'
        return {
            'name': 'Correccion de envíos erroneos.',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def correccion_flujo_view(self):
        print ("BUSCANDO MI OFICINA ################################")
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Administrar ubicación de documentos.",
                'view_mode': 'tree',
                #, form
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'domain': [('ultimo_pase_id', '!=', False)],
                'views': [[self.env.ref('exp_cambio_tramite.expediente_corregir').id, "tree"]],
            # , [self.env.ref('exp_cambio_tramite.expediente_corregir_form').id, "form"]
                }
        return action

    def seleccionar_popup_cambio_tramite(self):
        # print (("ABRIENDO VENTANA DE CAMBIO DE TRAMITEEEEEEEE"))
        tramites_posibles = self.obtener_nuevos_tramites_posibles()
        if not tramites_posibles:
            popup_view = self.popup_sin_conf_cambio_tramite()
            return popup_view
        else:
            popup_view = self.popup_cambio_tramite(tramites_posibles)
            return popup_view

    def eliminar(self):
        print(("@@@@@@@@@@@@@@@@@@@@@@@BORRANDO EL PASE NO RECIBIDO - EXPEDIENTE: " + self.expediente_id.name))
        segu_obj = self.env['seguimiento']
        seguimiento_obj = segu_obj.search([('expediente_id', '=', self.expediente_id.id)])
        if not seguimiento_obj:
            return True
            # cant_tareas_seg = count(seguimiento_obj[0].seguimiento_lineas)
        obj_tarea_borrar = False
        tarea_actual_seleccionada = False
        for linea_tareas in seguimiento_obj[0].seguimiento_lineas:
            if linea_tareas.tarea_inicio == False:
                print (("TAREAS QUE SE PUEDEN BORRAR: " + str(linea_tareas.tarea.codigo) + " - " + str(linea_tareas.tarea.name)))
                if obj_tarea_borrar == False:
                    obj_tarea_borrar = linea_tareas
                else:
                    raise ValidationError(('Hay mas de una tarea solicitada sin iniciar, contáctese con el administrador.'))
            else:
                if tarea_actual_seleccionada == False:
                    tarea_actual_seleccionada = linea_tareas.tarea
        if obj_tarea_borrar != False:
            obj_tarea_borrar.unlink()
        # return True
        self.expediente_id.tarea_actual = tarea_actual_seleccionada
        self.expediente_id.tarea_proxima = False
        models.Model.unlink(self)
        return self.enviados_sin_recepcion_view()

class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Listado de pases"

    def envio_directo(self):
        # print ("ENVIO DIRECTO ################################: " + str(self.id))
        if not self.tramite_tiene_flujo():
            print ((" EL TRAMITE NO TIENE FLUJO DEFINIDO"))
            action = self.enviar()
        else:
            action = {
                'name': "Expedientes en el Sistema...",
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'target': 'new',
                # 'domain': [('ubicacion_actual', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('exp_cambio_tramite.expediente_corregir_form').id, "form"]],
                }
        return action

    def tramite_tiene_flujo(self):
        flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [self.procedimiento_id.id])])
        if not flujo_obj or self.ubicacion_actual.name.lower() == "Nube".lower():
            return False
        else:
            return True

    def oficina_en_flujo(self):
        flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [proced_id])])
        # print(("NO HAY FLUJO PARA ... " + expte_obj.procedimiento_id.name))
        # SI NO HAY FLUJO O EL EXPEDIENTE TIENE UBICACION ACTUAL EN LA NUBE--
        if not flujo_obj or expte_obj.ubicacion_actual.name.lower() == "Nube".lower():
            return self.enviar()
