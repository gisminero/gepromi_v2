# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode

class exped_person(models.Model):
        _name = 'exped_person'
        _order = "write_date desc"

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        # recibido = fields.Boolean('Recibido', readonly=True, compute=_is_recept_doc, store=False)
        name = fields.Char('Estado', readonly=True, store=True)
        empleado_seg = fields.Many2one('hr.employee', 'Empleado Asignado', readonly=False)
        recibir = fields.Boolean('Recibida', required=False, readonly=True)
        expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', copy=False, required=False, readonly=True)
        fecha_hora_asigna = fields.Datetime(string='Tiempo de Asignacion', default=fields.Datetime.now)


        def recibir_asignacion(self):
                active_id = self.env.context.get('id_activo')
                user_id = self.env.user.id
                expend_person_obj = self.browse([active_id])
                # print(("DIFERENCIA ENTRE IDSS--- Empleado asignado: " + str(expend_person_obj.empleado_seg.user_id.id) + " Usuario Actual: " + str(user_id)))
                if user_id != expend_person_obj.empleado_seg.user_id.id:
                        raise ValidationError(('No puede aceptar un expediente enviado a otro usuario...'))
                        # view = self.env.ref('sh_message.sh_message_wizard_false')
                        # view_id = view and view.id or False
                        # context = dict(self._context or {})
                        # context['message'] = 'No puede aceptar un expediente enviado a otro usuario.'
                        # return {
                        #         'name': 'Informacion',
                        #         'type': 'ir.actions.act_window',
                        #         'view_type': 'form',
                        #         'view_mode': 'form',
                        #         'res_model': 'sh.message.wizard',
                        #         'views': [(view.id, 'form')],
                        #         'view_id': view.id,
                        #         'target': 'new',
                        #         'context': context,
                        # }
                else:
                        # print (("YA ETOY RECIBIENDO EL EXOEDIENE: " + self.empleado_seg.name))
                        expend_person_obj.write({'recibir':  True})
                        self.actualizar_tenencia_exp('Recibido por ' + self.empleado_seg.name)
                return True

        def actualizar_tenencia_exp(self, mensaje):
                exp_obj = self.env['expediente.expediente']
                exp_obj_select = exp_obj.browse([self.expediente_id.id])
                exp_obj_select.write({'empleado_seg': mensaje})
                self.write({'name': mensaje})
                return True

        def guardar_envio(self, vals):
                if not (self._get_permiso_asignacion()):
                        raise ValidationError(('No tiene los permisos suficientes para asignar documentos a personas...'))
                        # vals = False
                        # view = self.env.ref('sh_message.sh_message_wizard_false')
                        # view_id = view and view.id or False
                        # context = dict(self._context or {})
                        # context['message'] = 'No tiene los permisos suficientes para asignar documentos a personas.'
                        # return {
                        #         'name': 'Informacion',
                        #         'type': 'ir.actions.act_window',
                        #         'view_type': 'form',
                        #         'view_mode': 'form',
                        #         'res_model': 'sh.message.wizard',
                        #         'views': [(view.id, 'form')],
                        #         'view_id': view.id,
                        #         'target': 'new',
                        #         'context': context,
                        # }
                else:
                        super(exped_person, self).write(vals)
                        self.actualizar_tenencia_exp('Enviado a ' + self.empleado_seg.name)
                        return True


class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"

        # empleado_seg = fields.Many2one('hr.employee', 'Empleado Asignado', readonly=False)
        empleado_seg = fields.Char('Tenencia de Expte.', readonly=True, store=True)

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        def selec_personas_depart(self, depart_id):
                legal_list = []
                # legal_list.append(False, )
                personas_obj = self.env['hr.employee'].search([('department_id', '=', depart_id)])
                if personas_obj:
                        for persona in personas_obj:
                                # print (("NOMBRE DE LAS PERSONAS QUE SE AGREGASN: " + persona.name + " --  " +  persona.department_id.name))
                                legal_list.append(persona.id)
                return legal_list

        def popup_asignar(self):
                #DEBER CREAR LA VISTA ENVIAR ESPECIFICA PARA ESTO
                active_id = self.env.context.get('id_activo')
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                depart_id = self.userdepart(user_id)
                if (depart_id is not self.ubicacion_actual.id) or (self.oficina_destino is not False and self.recibido is False):
                        raise ValidationError(
                                ('Solo puede asignar personas cuando el Documento se encuentra en su oficina y no se encuentra enviado.'))
                # CONSULTANDO PASES
                exped_person_obj = self.env['exped_person'].search([('expediente_id', '=', active_id), ('recibir', '=', False)], order="fecha_hora_asigna desc", limit=1)
                #print (("EL REGISTOR DE ASIGNACION DE PERSONAS ES EL : " + str(exped_person_obj) +" -- " + str(exped_person_obj.empleado_seg.name) ))
                # FIN CONSULTANDO PASES
                lista_oficina = self.selec_personas_depart(depart_id)
                if exped_person_obj:
                        return {
                                'name': "Asignar Empleado",
                                'view_mode': 'form',
                                'res_id': exped_person_obj[0].id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'exped_person',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                                'context': {'recibido': False, 'oficina_actual': depart_id,
                                            'default_expediente_id': expte_obj.id, 'permiso_asignacion': not(self._get_permiso_asignacion())
                                            , 'usuarios_oficina': lista_oficina},
                                'views': [[self.env.ref('exped_person.form').id, "form"]],
                                'target': 'new',
                                }
                elif self._get_permiso_asignacion():
                        return {
                                'name': "Asignar Empleado",
                                'view_mode': 'form',
                                #'res_id': exped_person_obj[0].id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'exped_person',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                                'context': {'recibido': False, 'permiso_asignacion': not(self._get_permiso_asignacion()),
                                            'default_expediente_id': expte_obj.id, 'usuarios_oficina': lista_oficina},
                                'views': [[self.env.ref('exped_person.form').id, "form"]],
                                'target': 'new',
                                }
                else:
                        view = self.env.ref('sh_message.sh_message_wizard_false')
                        context = dict(self._context or {})
                        context['message'] = 'No tiene los permisos suficientes para asignar documentos a personas.'
                        return {
                                'name': 'Informacion',
                                'type': 'ir.actions.act_window',
                                'view_type': 'form',
                                'view_mode': 'form',
                                'res_model': 'sh.message.wizard',
                                'views': [(view.id, 'form')],
                                'view_id': view.id,
                                'target': 'new',
                                'context': context,
                        }

        def proxima_tarea_enviar(self):
                print(("PASO POR EL MODULO ... EXPEDIENTE RELACION CON PERSONAS"))
                self.write({'empleado_seg': False})
                res = super(expediente, self).proxima_tarea_enviar()
                return res

        def proced(self):
                self.write({'tarea_proxima': False})
                res = super(expediente, self).cancel_return_mi_oficina()
                return res
