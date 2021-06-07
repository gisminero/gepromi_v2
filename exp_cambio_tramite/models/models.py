# -*- coding: utf-8 -*-
from odoo import models, fields, api

class conf_tramites_posibles(models.Model):
    _name = 'conf_tramites_posibles'
    _description = 'Tramites posibles cuando se produce la combinacion requerida en cambio tramite.'
    tramite_id = fields.Many2one('procedimiento.procedimiento', 'Tramite Posible', copy=False, required=True)
    cambio_id = fields.Many2one('conf_cambio_tramite', 'Cambio de Tramite', required=1, ondelete='cascade')

class conf_cambio_tramite(models.Model):
    _name = 'conf_cambio_tramite'

    name = fields.Char('Nombre', required=True)
    tramite_inicial_id = fields.Many2one('procedimiento.procedimiento', string="Tramite")
    estado_legal_id = fields.Many2one('estado_legal.estado_legal', string="Estado Legal")
    tramites_posibles_ids = fields.One2many('conf_tramites_posibles', 'cambio_id', string='Tramites Posibles', required=False)
    active = fields.Boolean('Activo', default=True)

class exp_solicitantes_cambio(models.Model):
    _name = 'exp_solicitantes_cambio'
    _description = 'Solicitantes_cambio'

    solicitante = fields.Char('Solicitante', required=True)
    solicitante_cuit = fields.Char('CUIT/CUIL/DNI', required=False)
    hist_cambio_id = fields.Many2one('exp_historia_tramite', 'Solicitantes', required=1, ondelete='cascade')

class exp_historia_tramite(models.Model):
    _name = 'exp_historia_tramite'
    _order = 'create_date desc'

    tramite_id = fields.Many2one('procedimiento.procedimiento', string="Trámite", required=True)
    solicitante = fields.Char('Nombre Titular', required=False)#ELIMINAR
    solicitante_cuit = fields.Char('CUIT del Titular', required=False)#ELIMINAR
    solicitantes = fields.One2many('exp_solicitantes_cambio', 'hist_cambio_id', string='Solicitantes', required=False)
    exp_id = fields.Many2one('expediente.expediente', string="Expediente al que correponde", reaonly=True)

    # def write(self):
    #     print(("CAMBIANDO NOMBRE DE TITULAR" + self.nombre_titular))
    #     self.cambio_tramite_en_expte()
    #     self.exp_id.write({'cambio_de_tramite': False, 'procedimiento_id': self.tramite_id.id, 'solicitantes': self.solicitantes})
    #     vals = {'tramite_id': self.tramite_id.id, 'exp_id': self.exp_id.id}
    #     return super(exp_historia_tramite, self).write(vals)

    def cambio_tramite_en_expte(self):
        exp_obj = self.env['expediente.expediente'].browse([self.exp_id.id])
        print ((" ESTE ES EL EXPEDIENTE ENCONTRADO: " + exp_obj.name))
        vals = {'procedimiento_id': self.tramite_id.id, 'solicitante': self.nombre_titular,
                'solicitante_cuit': self.cuit_titular, 'solicitantes': (0, _, {'nombre_titular': 'PRUEBA', 'cuit_titular': 'PRUEBA DE CUIT'})}
        return exp_obj.write(vals)

    def historia_tramites(self):
        active_id = self.env.context.get('id_activo')
        print (("ENVIANDO .... " + str(active_id)))
        user_id = self.env.user.id
        expte_obj = self.env['expediente.expediente'].browse([active_id])
        print (("OBJETO.... " + str(expte_obj.name)))
        if True:
            return {
            'name': "Cambio de Trámites del Documento: " + expte_obj.name,
            'view_mode': 'tree',
            #'res_id': active_id, #SOLO PARA FORM
            'res_model': 'exp_historia_tramite',
            'type': 'ir.actions.act_window',
            'domain': [('exp_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('exp_cambio_tramite.cambio_tramite_historia').id, "tree"], [self.env.ref('exp_cambio_tramite.cambio_tramite_historia_form').id, "form"]],
            'target': 'new',
            'tag': 'reload',
            }
        return True

class expediente(models.Model):

    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Agregar Asociacion con Flujos de Tareas"

    cambio_de_tramite = fields.Boolean('Cambio de Tramite', readonly=False, store=True)
    historia_tramite = fields.One2many('exp_historia_tramite', 'exp_id', string='Historia del Trámite', required=False)

    def seleccionar_popup_cambio_tramite(self):
        # print (("ABRIENDO VENTANA DE CAMBIO DE TRAMITEEEEEEEE"))
        tramites_posibles = self.obtener_nuevos_tramites_posibles()
        if not tramites_posibles:
            popup_view = self.popup_sin_conf_cambio_tramite()
            return popup_view
        else:
            popup_view = self.popup_cambio_tramite(tramites_posibles)
            return popup_view

    def popup_cambio_tramite(self, tramites_posibles):
        # print(("LA LISTA ES. " + str(tramites_posibles)))
        if True:
            view = self.env.ref('exp_cambio_tramite.cambio_tramite_exp_form_popup')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context.update({'dominio': tramites_posibles, 'default_exp_id': self.id})
            context['message'] = 'Verifique que el valor de Oficina Destino se muestre en el formulario de envio. Vuelva a intentar el envio.'
            return {
                'name': 'Cambio de Trámite en el Expediente',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'expediente.expediente',
                'res_id': self.id,
                # 'domain': [('tramites_posibles_ids.tramite_id', 'in', tramites_posibles)],
                'views': [(self.env.ref('exp_cambio_tramite.cambio_tramite_exp_form_popup').id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }

    def write(self, vals):
        print(("CAMBIANDO DATOS DE DEL TRAMITE MINERO" ))
        # self.cambio_tramite_en_expte()
        # self.exp_id.write({'cambio_de_tramite': False, 'procedimiento_id': self.tramite_id.id, 'solicitantes': self.solicitantes})
        # vals = {'tramite_id': self.tramite_id.id, 'exp_id': self.exp_id.id}
        return super(expediente, self).write(vals)

    def obtener_nuevos_tramites_posibles(self):
        print (("OBTENIENDO TRAMITES POSIBLES PARA EL EXPEDIENTE : " + self.name))
        # obj_cambio_tramite = self.env['cambio_tramite_accion']
        cambio_obj = self.env['conf_cambio_tramite']
        config_obj_encontrados_count = cambio_obj.search_count([('tramite_inicial_id', '=', self.procedimiento_id.id),
                                                                ('estado_legal_id', '=', self.estado_legal_actual_id.id)])
        if config_obj_encontrados_count < 1:
            print (("Combinaciones encontradas son 0"))
            return False
        print (("EL PROCEDIMIENTO ID ES: " + str(self.procedimiento_id.id)))
        config_obj_encontrado = cambio_obj.search([('tramite_inicial_id', '=', self.procedimiento_id.id),
                                                   ('estado_legal_id', '=', self.estado_legal_actual_id.id)])[0]
        legal_list_tramites_posibles = []
        for config in config_obj_encontrado:
            for posible in config.tramites_posibles_ids:
                print(("IMPRIMIENDO LOS ESTADOS POSIBLES ENCONTRADOS. "))
                print((" -- " + posible.tramite_id.name))
                legal_list_tramites_posibles.append(posible.tramite_id.id)
        return legal_list_tramites_posibles

    def popup_sin_conf_cambio_tramite(self):
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        titulo = "Información sonbre cambio de trámite."
        context['message'] = "No hay configurados tramites posibles para esta situación. Contáctese con su administrador."
        return {
            'name': titulo,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def historia_tramites(self):
        print (("MOVIMIENTOS DEL DOCUMENTO"))
        # tipo_lista = self.env.context.get('tipo_historia')
        active_id = self.env.context.get('id_activo')
        print (("ENVIANDO .... " + str(active_id)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        print (("OBJETO.... " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        if True:
            return {
            'name': "Cambio de Trámites del Documento: " + expte_obj.name,
            'view_mode': 'tree',
            #'res_id': active_id, #SOLO PARA FORM
            'res_model': 'exp_historia_tramite',
            'type': 'ir.actions.act_window',
            'domain': [('exp_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('exp_cambio_tramite.cambio_tramite_historia').id, "tree"], [self.env.ref('exp_cambio_tramite.cambio_tramite_historia_form').id, "form"]],
            'target': 'new',
            'tag': 'reload',
            }
        if depart_id:
            return {
            'name': "Movimientos del Documento " + expte_obj.name,
            'view_mode': 'tree',
            #'res_id': active_id, #SOLO PARA FORM
            'res_model': 'pase.pase',
            'type': 'ir.actions.act_window',
            'domain': [('expediente_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('pase.list').id, "tree"]],
            'target': 'new',
            'tag': 'reload',
            }
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        return True

    def activar(self):
        vals = {'tramite_id': self.procedimiento_id.id, 'solicitante': self.solicitante,
                'solicitante_cuit': self.solicitante_cuit, 'exp_id': self.id,
                'solicitantes': [(0, 0, {'solicitante': 'PRUEBA', 'solicitante_cuit': 'PRUEBA DE CUIT'})] }
        historia_tramite_obj = self.env['exp_historia_tramite'].create(vals)
        print(("llamando al activar padre DESDE CAMBIO DE TRAMITE"))
        res = super(expediente, self).activar()
        return res

    def cambio_tramite_en_expte(self):
        print("@@@@@@@@@@@@@@@@@@@@@@@INGRESANDO NUEVA HISTORIA@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        lista_solic_para_vals = []
        for linea in self.solicitantes:
            lista_solic_para_vals.append(tuple((0, 0, {'solicitante' : linea.solicitante, 'solicitante_cuit' : linea.solicitante_cuit})))
            print (("CASO: " + str(linea.solicitante)+", "+str(linea.solicitante_cuit)))
        print (("LA LISTA LISTA  ES: "))
        print((str(lista_solic_para_vals)))
        print(("FIN DE LA LISTA LISTA "))
        vals = {'tramite_id': self.procedimiento_id.id, 'solicitante': self.solicitante,
                'solicitante_cuit': self.solicitante_cuit, 'exp_id': self.id,
                'solicitantes': lista_solic_para_vals}
        historia_tramite_obj = self.env['exp_historia_tramite'].create(vals)
        return True

    def no_cambiar(self):
        # active_id = self.id
        # print (("ENVIANDO .... " + str(active_id)))
        # expte_obj = self.browse([active_id])
        self.write({'cambio_de_tramite': False})
        return True