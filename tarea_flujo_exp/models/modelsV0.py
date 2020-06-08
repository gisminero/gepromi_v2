# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class seguimiento(models.Model):
    _name = 'tarea_flujo_exp.seguimiento'
    plantilla_id = fields.Many2many('plantilla.vacia', string='Plantillas asociadas')

class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"
        #_table = 'mrp_recep'
        #_order = "id desc"
        tarea_actual = fields.Many2one('tarea.tarea', 'Tarea Actual', required=False, readonly=True)
        tarea_proxima = fields.Many2one('tarea.tarea', 'Tarea Prox.', required=False, readonly=False)
        en_flujo = fields.Boolean('En Flujo', required=False, readonly=False,
                                  write=['expediente.access_group_expte_flujo'], default=True)
        #info_tarea = fields.Text(string='Info', translate=True)

        @api.multi
        @api.depends("emeu_sector_id.emeu_education_ids")
        def _get_education_domain(self):
                return True
                """
                for object in self:
                        education_list = []
                        if object.emeu_sector_id.id:
                                education_ids = object.emeu_sector_id.emeu_education_ids
                                education_list = [x.id for x in education_ids]
                        object.education_list = [(6, 0, education_list)]
                """

        def proxima_tarea_enviar(self):
                #print(("TAREA ENVIAR "))
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                fojas_new = self.env.context.get('fojas_new')
                destino_new = self.env.context.get('oficina_destino_new')
                observaciones_new = self.env.context.get('observaciones_new')
                proxima_tarea_id = self.env.context.get('tarea_proxima_cont')
                tarea_actual_new = self.env.context.get('tarea_actual_new')
                en_flujo_new = self.env.context.get('en_flujo_new')
                sacar_de_flujo = expte_obj.en_flujo
                tarea_obj = self.env['tarea.tarea']
                tarea_obj_prox = tarea_obj.browse([proxima_tarea_id])
                if tarea_obj_prox.tipo == '4':
                        sacar_de_flujo = False
                        return self.write({'tarea_actual': proxima_tarea_id,
                                'folios': fojas_new, 'en_flujo': sacar_de_flujo})
                # if not destino_new:
                #         self.write({'oficina_destino': expte_obj.ubicacion_actual})
                #print (("EL CONTEXTO ES: " + str(self.env.context)))
                #self.onchange_define_pase(proxima_tarea_id, expte_obj)
                if (expte_obj.en_flujo == False) and (en_flujo_new == True):
                        #Se esta ingresando un expediente en flujo
                        print(("SE ESTA INTRODUCIENDO EL EXPETE EN EL FLUJO"))
                        return self.write({'tarea_actual': tarea_actual_new,
                        'folios': fojas_new, 'en_flujo': en_flujo_new})
                if destino_new == expte_obj.ubicacion_actual.id:
                        print (("SON IGUALES"))
                        print ((str(destino_new) + " /// " + str(expte_obj.ubicacion_actual)))
                        return self.write({'tarea_actual': proxima_tarea_id,
                        'folios': fojas_new, 'en_flujo': sacar_de_flujo, 'oficina_destino': expte_obj.ubicacion_actual.id})
                else:
                        print (("SON DIFERENTES"))
                        print ((str(destino_new) + " /// " + str(expte_obj.ubicacion_actual)))
                        self.enviar_conf()
                        return self.write({'tarea_actual': proxima_tarea_id,
                                'folios': fojas_new, 'en_flujo': sacar_de_flujo})
                #return self.write({'tarea_actual': proxima_tarea_id,
                #'folios': fojas_new, 'oficina_destino': destino_new,
                #'observ_pase': observaciones_new})
                #return True

        def user_permiso_ingreso_flujo(self):
                user_id = self.env.user.id
                print(("Buscanco el permiso"))
                #user = self.env.user
                self._cr.execute('SELECT * FROM ir_module_category INNER JOIN '
                                 ' res_groups ON ir_module_category.id=res_groups.category_id WHERE name = %s',
                           ('GeProMi.Ingresar en Flujo',))
                rows = self.env.cr.dictfetchall()
                ids = [x['id'] for x in rows]
                print (("ESCRIBIENDO FILA : " + str(ids)))
                return True

        def proxima_tarea(self):
                print(("TAREA ENVIAR 2"))
                #user_ingreso_flujo = self.user_permiso_ingreso_flujo()
                legal_list = []
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                en_flujo = expte_obj.en_flujo
                tarea_actual = expte_obj.tarea_actual
                en_flujo = expte_obj.en_flujo
                proced_id = expte_obj.procedimiento_id.id
                flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [proced_id])])
                if not en_flujo and not flujo_obj:
                    return self.enviar()
                #CONSULTANDO PASES
                pase_obj = self.env['pase.pase']
                user_id = self.env.user.id
                depart_id = self.userdepart(user_id)
                pase_res = pase_obj.obtener_ultimo_pase(active_id, depart_id)
                #FIN CONSULTANDO PASES
                if not en_flujo:
                        t_activ = self.env['tarea.tarea'].search([('active', '=', True)])
                        for id_tarea in t_activ:
                                legal_list.append(id_tarea.id)
                else:
                        lineas = flujo_obj.lineflujo_ids
                        for lin in lineas:
                                if en_flujo:
                                        if lin.tarea_padre.id == tarea_actual.id:
                                                legal_list.append(lin.tarea.id)
                                else:
                                        legal_list.append(lin.tarea.id)
                if not pase_res:
                    #NUEVO PASE A OFICINA
                    return {
                            'name': "Seleccionar la próxima tarea",
                            'view_mode': 'form',
                            'res_id': active_id,
                            # 'view_id': self.env.ref('pase.form_enviar').id,
                            'res_model': 'expediente.expediente',
                            'type': 'ir.actions.act_window',
                            # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                            # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                            'context': {'proxima_tarea_list': legal_list,
                                'default_oficina_destino' : [2], 'default_recibido': False},
                            'views': [[self.env.ref('tarea_flujo_exp.exp_pop_prox_tarea').id, "form"]],
                            'target': 'new',
                    }
                else:
                    return {
                            'name': "EL DOCUMENTO SE ENCUENTRA ENVIADO A: "+ str(expte_obj.oficina_destino.name),
                            'view_mode': 'form',
                            'res_id': active_id,
                            #'view_id': self.env.ref('pase.form_enviar').id,
                            'res_model': 'expediente.expediente',
                            'type': 'ir.actions.act_window',
                            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                            #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                            'context': {'recibido': True, 'ultimo_pase_id': pase_res.id, 'oficina_destino': depart_id},
                            'views': [[self.env.ref('expediente.form_enviado').id, "form"]],
                            'target': 'new',
                    }

        #def onchange_define_pase(self, tarea_prox, expte_obj):
        def onchange_define_pase(self, tarea_prox):
                #self.write({'oficina_destino': 2})
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                tarea_obj = self.env['tarea.tarea']
                tarea_obj_prox = tarea_obj.browse([tarea_prox])
                return {'value': { 'oficina_destino' : tarea_obj_prox.departament_id }}

        def enviar_tarea_pase(self):
                #DEBER CREAR LA VISTA ENVIAR ESPECIFICA PARA ESTO
                active_id = self.env.context.get('id_activo')
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                depart_id = self.userdepart(user_id)
                # CONSULTANDO PASES
                pase_obj = self.env['pase.pase']
                pase_res = pase_obj.obtener_ultimo_pase(active_id, depart_id)
                # FIN CONSULTANDO PASES
                if depart_id:
                        return {
                                'name': "Enviando Documento",
                                'view_mode': 'form',
                                'res_id': active_id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'expediente.expediente',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                                'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                                'views': [[self.env.ref('expediente.form_enviar').id, "form"]],
                                'target': 'new',
                                }
                else:
                        raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
                        return True

        def onchange_no_sacar(self, en_flujo):
                return {'value': {'en_flujo': True}}

        def obtener_tarea_inicial(self, pr_id):
                bus = self.env['tarea_flujo.flujo'].search_count([('name.id', '=', [pr_id])])
                if bus < 1:
                        return False
                ta_obj = self.env['tarea_flujo.flujo'].browse([pr_id])
                for inicial in ta_obj.lineflujo_ids:
                        if inicial.tarea_padre.tipo == '1':
                                return inicial.tarea_padre.id
                print(("EL FLUJO NO TIENE UNA TAREA DEL TIPO INICIAL"))
                return True

        def activar(self):
                active_id_2 = self.env.context.get('id_activo')
                expte_obj_2 = self.browse([active_id_2])
                tarea_inicial_id = self.obtener_tarea_inicial(expte_obj_2.procedimiento_id.id)
                if tarea_inicial_id:
                        self.write({'en_flujo': True, 'tarea_actual': tarea_inicial_id})
                else:
                        print ((" EL TRAMITE NO TIEBNE UN FLUJO CREADO"))
                res = super(expediente, self).activar()
                return res