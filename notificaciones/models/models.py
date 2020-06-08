# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import time
from datetime import datetime as dt, timedelta, date
import dateutil.parser
from unidecode import unidecode



class tipos_aviso(models.Model):
    _name = 'tipos_aviso'

    name = fields.Char('Nombre', required=True)
    descripcion = fields.Char('Descripcion', required=False)

class notifica(models.Model):
    _name = 'notifica'
    _order = "write_date desc"

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user)

    def esFeriado(self, dia):
        res = self.env['feriados'].search([('fecha', '=', dia)])
        if res:
            return res
        else:
            return False

    def recalculaDias(self, dia_inicio, cant_dias, tipo):
        informacion = ""
        d = str(dateutil.parser.parse(dia_inicio).date())
        cont_dias = 0
        while cont_dias <= cant_dias:
            end_date = dt.strptime(d, '%Y-%m-%d') + datetime.timedelta(days = 1)
            d = str(dateutil.parser.parse(end_date.strftime('%Y-%m-%d')).date())
            dia_semana = end_date.strftime('%w')
            res_feriado = self.esFeriado(d)
            if res_feriado:
                feriado = True
            else:
                feriado = False
            if tipo == '1':
                if dia_semana is '0' or dia_semana is '6' or feriado:
                    if feriado:
                        informacion = informacion + end_date.strftime('%d-%m-%Y') + " - "+str(res_feriado.name) + "\n"
                else:
                    cont_dias = cont_dias + 1
            elif tipo == '2':
                cont_dias = cont_dias + 1
        self.info = informacion
        return end_date

    @api.depends('fecha_notificacion', 'plazo_id')
    def _onchangeInicioNotifica(self):
        fecha_inicio = self.fecha_notificacion
        plazo_id = self.plazo_id
        if not fecha_inicio:
            return False
        if not plazo_id:
            return False
        plazo_obj = self.env['tarea.plazo'].browse([plazo_id.id])
        cant_dias = plazo_obj.cant
        tipo_dias = plazo_obj.tipo
        dias_final = self.recalculaDias(fecha_inicio, cant_dias,tipo_dias)
        self.fecha_vencimiento = dias_final

    @api.depends('expediente_id', 'plazo_id')
    def _nombrePlazo(self):
        expediente = self.expediente_id
        plazo = self.plazo_id
        if expediente and plazo:
            name_new = unidecode(expediente.name) + ' - ' + unidecode(plazo.name)
            self.name = name_new
        else:
            self.name = str('Seleccione expediente y plazo.')

    @api.depends('expediente_id')
    def _onchangeExpte(self):
        exped_id = self.expediente_id
        if not self.expediente_id:
            return False
        exped_obj = self.env['expediente.expediente'].browse([exped_id.id])
        # cant_dias = plazo_obj.cant
        # tipo_dias = plazo_obj.tipo
        # dias_final = self.recalculaDias(fecha_inicio, cant_dias,tipo_dias)
        self.nombre_pedimento = exped_obj.nombre_pedimento

    name = fields.Char('Nombre', required=False, readonly=True, compute="_nombrePlazo", store=True)
    expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', required=True)
    nombre_pedimento = fields.Char('Nombre Pedimento', readonly=True, compute="_onchangeExpte", store=False)
    plazo_id = fields.Many2one('tarea.plazo', 'Plazo Asignado', required=True)
    fecha_notificacion = fields.Datetime('Fecha de Notificacion', readonly=False, required=True)#, default=fields.Datetime.now
    fecha_vencimiento = fields.Date('Fecha de Vencimiento', readonly=True, compute="_onchangeInicioNotifica", store=True)
    fecha_suspension_actual = fields.Date('Fecha de Inicio de Suspension', readonly=True, store=True)
    alertas_enviados = fields.Boolean('Alertas Enviados', default=False, readonly=True)
    notificar_plazo_vencidos = fields.Boolean('Notificar Plazo Vencido', default=True, readonly=True)
    user_creador_id = fields.Many2one('res.users','Creado por', required=False, readonly=True, default=default_user_id)
    state = fields.Selection([('draft', 'Borrador'), ('active', 'Vigente'),
        ('archive', 'Cancelado'), ('suspendido', 'Suspendido'), ('cumplido', 'Cumplido'), ('vencido', 'Vencido')], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")
    fecha_cumplido = fields.Datetime('Fecha Cumplido', readonly=False)#, default=fields.Datetime.now
    user_cumplido_id = fields.Many2one('res.users','Usuario Recibe Cumplimiento', required=False)#, default=default_user_id
    #pase_posterior_id = fields.Many2one('pase.pase','Pase Realizado Luego del Evento', required=False, default=False)
    info = fields.Text('Informacion', required=False, readonly=True, store=True)

    def nombrePlazo(self, expediente_id, plazo_id):
        if expediente_id and plazo_id:
            #print(("CAMBIANDO NOMBRE " + str(expediente_id) + str(plazo_id)))
            plazo_obj = self.env['tarea.plazo'].browse([plazo_id])
            exp_obj = self.env['expediente.expediente'].browse([expediente_id])
            #print(("CAMBIANDO NOMBRE " + str(plazo_obj.name) + str(exp_obj.name)))
            return {'value': { 'name': exp_obj.name + ' - ' + str(plazo_obj.name)}}
        else:
            return {'value': { 'name': 'Seleccione expediente y plazo.'}}

    def activar(self):
        active_id = self.env.context.get('id_activo')
        if not active_id:
            print (("DEBE GRABAR ANTES DE ACTIVAR"))
        user_id = self.env.user.id
        expte_obj = self.browse([active_id])
        expte_obj.write({'state': "active"})
        return True

    def recibir(self):
        active_id = self.env.context.get('id_activo')
        user_id = self.env.user.id
        expte_obj = self.browse([active_id])
        fecha_actual = str(datetime.date.today())
        expte_obj.write({'state': "cumplido", 'alertas_enviados': True, 'fecha_cumplido': fecha_actual,
                         'user_cumplido_id': user_id, 'notificar_plazo_vencidos': False})
        return True

    def crea_alertas(self):
        lista_encontrados = []
        print (("ENVIANDO ALERTAS A LOS INTEGRATES DEL GRUPO DE EVENTO"))
        hoy_str = str(datetime.date.today())
        hoy = datetime.date.today()
        #present = datetime.now()
        exptes_no_enviado_count = self.env['notifica'].search_count([('alertas_enviados', '=', False), ('state', '=', 'active')])
        print (("EL DIA DE HOY ES...: " + str(hoy) + " cantidad: " + str(exptes_no_enviado_count)))
        exptes_no_enviado = self.env['notifica'].search([('alertas_enviados', '=', False), ('state', '=', 'active')])
        for expte_obj in exptes_no_enviado:
            grupos = expte_obj.plazo_id.grupos_notificar
            dia_vencimiento = expte_obj.fecha_vencimiento
            user_creador_id = expte_obj.user_creador_id.id
            if not expte_obj.info:
                info_temp = " - "
            else:
                info_temp = unidecode(expte_obj.info)
            if not expte_obj.expediente_id.nombre_pedimento:
                pedimento_temp = " - "
            else:
                pedimento_temp = unidecode(expte_obj.expediente_id.nombre_pedimento)
            info = "Pedimento: " + pedimento_temp + " - Fecha de Notificacion: " + str(expte_obj.fecha_notificacion) + " - Otra Informacion: " + info_temp
            creador_incluido = False
            d = str(dateutil.parser.parse(dia_vencimiento).date())
            dia_venc_list = d.split("-")
            dia_venc_datetime = date(int(dia_venc_list[0]), int(dia_venc_list[1]), int(dia_venc_list[2]))
            #dia_venc_datetime = date(2019, 08, 15)
            if hoy >= dia_venc_datetime:
                alerta_obj = self.env['alerta']
                for g in grupos:
                    for u in g.user_notificar_id:
                        print (("Generando Alertas para Empleado: " + u.name + " Usuario: "+ str(u.user_id.login)))
                        alerta_obj.create({'notificacion_id': expte_obj.id,
                        'user_alerta_id': u.user_id.id, 'info': info})
                        if u.id == user_creador_id:
                            creador_incluido = True
                if creador_incluido == False:
                    alerta_obj.create({'notificacion_id' : expte_obj.id ,
                    'user_alerta_id' : user_creador_id, 'info': info})
                    print (("Crar Alerta para Usuario Iniciador: " + str(expte_obj.id) +  ' user_alerta_id: ' + str(u.user_id.id) + 'info: ' + str(info)))
                print(("Cambiando Estado a VENCIDO el EXPEDIENTE: " + str(expte_obj.expediente_id.name)))
                print(("El ID de NOTIFICA ES: " + str(expte_obj.id)))
                lista_encontrados.append(expte_obj.id)
                # expte_obj_nuevo = self.env['notifica'].browse([expte_obj.id])
                # print (("MI NUEVO OBJETO ES: " + expte_obj_nuevo[0].name))
                # expte_obj_nuevo[0].write({'alertas_enviados': True, 'state': 'vencido'})
                expte_obj.write({'alertas_enviados': True, 'state': 'vencido'})
                # self._cr.execute("""UPDATE public.notifica
                #         SET alertas_enviados = %s, state = %s
                #         WHERE id = %s;""" % (True, "vencido", expte_obj.id,))
                print("YA PASO POR LAS LINEAS QUE MODIFICAN !!! ")
            # else:
            #     print(("Aun no llega el dia de vencimieto"))
        # for elem in lista_encontrados:
        #     print(("ESTO ES LO QUE ENCARA LA LISTA: " + str(elem)))
        return True

    def busca_pases(self):
        #Debera buscar pases luego de que el evento vence
        #print (("ENVIANDO ALERTAS A LOS INTEGRATES DEL GRUPO DE EVENTO"))
        hoy_str = str(datetime.date.today())
        exptes_no_enviado_count = self.env['notifica'].search_count([('alertas_enviados', '=', False), ('state', '=', 'active')])
        #print (("EL DIA DE HOY ES...: " + hoy_str + " cantidad: " + str(exptes_no_enviado_count)))
        exptes_no_enviado = self.env['notifica'].search([('alertas_enviados', '=', False), ('state', '=', 'active')])
        for expte_obj in exptes_no_enviado:
            grupos = expte_obj.plazo_id.grupos_notificar
            dia_vencimiento = expte_obj.fecha_vencimiento
            user_creador_id = expte_obj.user_creador_id.id
            creador_incluido = False
            d = str(dateutil.parser.parse(dia_vencimiento).date())
            #print (('BUSCANDO GRUPOS A NOTIFICAR DE LA PRESENTE ALERTA     que vence: ' + str(d)))
            if hoy_str == str(d):
                alerta_obj = self.env['alerta']
                for g in grupos:
                    #print (("Iterando Grupo: " + g.name))
                    #print (("Iterando Grupo: " + str(g.user_notificar_id)))
                    for u in g.user_notificar_id:
                        #print (("Empleado: " + u.name + " Usuario: "+ str(u.user_id.login)))
                        alerta_obj.create({'notificacion_id' : expte_obj.id , 'user_alerta_id' : u.user_id.id})
                        if u.id == user_creador_id:
                            creador_incluido = True
                if creador_incluido == False:
                    alerta_obj.create({'notificacion_id' : expte_obj.id , 'user_alerta_id' : user_creador_id})
                expte_obj.write({'alertas_enviados': True, 'state': "vencido"})
            #else:
                #print (("No hay conincidencia en fecha de vencimiento."))
        return True

    def detalle_plazo(self):
        active_id = self.env.context.get('id_activo_plazo')
        user_id = self.env.user.id
        return {
            'name': "Detalle de Plazos Agendados",
            'view_mode': 'form',
            'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'notifica',
            'type': 'ir.actions.act_window',
            # 'views': [[self.env.ref('notificaciones.plazos_exp_form').id, "form"]],
            'views': [[self.env.ref('notificaciones.notifica_form_exped').id, "form"]],
            'target': 'new',
            }

    # def ingresar_flujo_ultima(self):
    #     #revisar esta funcion, al parecer no cumple con su objetivo
    #     active_id = self.env.context.get('id_activo')
    #     expte_obj = self.browse([active_id])
    #     expte_obj.write({'notificar_plazo_vencidos': False})
    #     return {'value': {'notificar_plazo_vencidos': False}}

    def desactiva_notificaciones(self):
        active_id = self.env.context.get('id_activo')
        notifica_obj = self.browse([active_id])
        notifica_obj.write({'notificar_plazo_vencidos': False})
        return {'value': {'notificar_plazo_vencidos': False}}


class alerta(models.Model):
    _name = 'alerta'
    _order = "id desc"
    # @api.depends('notificacion_id', 'alerta_recibido')
    # def _onchangeRecibido(self):
    #     notifica_id = self.notificacion_id
    #     if not notifica_id:
    #         print(("NO SE ENCONTRO EL ID DE NOTIFICACION "))
    #         return False
    #     print(("EL ID DE LA NOTIFICACION ES: " + str(notifica_id)))
        # notifica_obj = self.env['notifica'].browse([notifica_id.id])
        # cant_dias = plazo_obj.cant
        # tipo_dias = plazo_obj.tipo
        # dias_final = self.recalculaDias(fecha_inicio, cant_dias,tipo_dias)
        # self.nombre_pedimento = exped_obj.nombre_pedimento

    #name = fields.Char('Nombre', required=False, readonly=True, compute="_nombrePlazo", store=True)
    notificacion_id = fields.Many2one('notifica', 'Notificacion', required=False, ondelete='restrict')
    alerta_recibido = fields.Boolean('Recibido', readonly=False, default=False)
    user_alerta_id = fields.Many2one('res.users','Usuario Recibe', required=False, readonly=False)#, default=default_user_id
    info = fields.Text('Informacion', required=False, readonly=True, store=True)

    def assign_alerta(self):
        #user_id = self.default_user_id()
        #alerta_obj = self.env['notificaciones.notifica'].search([('plazo_id.grupos_notificar.user_notificar_id', '=', user_id)])
        print (("..." ))
        return True

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user).id

    def select_target(self):
        user_id = self.default_user_id()
        num_alerta = self.env['alerta'].search_count([('user_alerta_id', '=', [user_id]), ('alerta_recibido', '=', False)])
        if num_alerta > 0:
            return 'new'
        else:
            return 'current'

    def hay_alertas(self):
        user_id = self.default_user_id()
        num_alerta = self.env['alerta'].search_count([('user_alerta_id', '=', [user_id]), ('alerta_recibido', '=', False)])
        if num_alerta > 0:
            return True
        else:
            return False

    def recibido(self):
        active_id = self.env.context.get('id_alerta')
        alerta_obj = self.browse([active_id])
        alerta_ids_count = self.env['alerta'].search_count([('notificacion_id', '=', alerta_obj.notificacion_id.id)])
        alerta_objs = self.env['alerta'].search([('notificacion_id', '=', alerta_obj.notificacion_id.id)])
        if alerta_ids_count > 0:
            for alerta_enviado in alerta_objs:
                alerta_enviado.write({'alerta_recibido': True})
        if self.hay_alertas():
            return True
        else:
            return True

    def ir_a_expedientes(self):
        env = self.env
        return {
            'name': "Expedientes en Mi Oficina",
            'view_mode': 'tree, form',
            'res_model': 'expediente.expediente',
            'type': 'ir.actions.act_window',
            'context': {},
            'target': 'current',
            'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
            'views': [[env.ref('expediente.mi_oficina_list').id, "tree"], [env.ref('expediente.form').id, "form"]],
            #res_id (optional)
            }

    def ir_a_alertas(self):
        env = self.env
        return {
            'name': "Mis Alertas",
            'view_mode': 'tree, form',
            'res_model': 'alerta',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('user_alerta_id', '=', env['alerta'].default_user_id())],
            #'domain': [('recibido', '=', True), ('oficina_destino', '=', env['expediente.expediente'].depart_user())],
            'views': [[env.ref('notificaciones.alerta_list_pop').id, "tree"], [env.ref('notificaciones.alerta_form').id, "form"]],
            }

class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Agregar estado de plazos agendados."

    def cuenta_plazos_asociados_tarea(self):
        print(("BUSCANDO PLAZOS ASOCIADOS A LA TAREA"))
        cant_plazos = 0
        tarea_obj_plazos = self.env['tarea.tarea'].search([('id', '=', self.tarea_actual.id)]).plazos
        for plazo in tarea_obj_plazos:
            # print (("QUE PLAZO TIENE: " + plazo.name))
            cant_plazos = cant_plazos + 1
        # print(("LA CANTIDAD DE PLAZOS ASOCIADOS ES ; " + str(cant_plazos)))
        return cant_plazos

    def _estadoPlazo(self):
        vencido = False
        cant_plazos_asociados = self.cuenta_plazos_asociados_tarea()
        # if cant_plazos_asociados > 0:
        #     print (("VEO QUE TIENE PLAZOD"))
        # else:
        #     print (("NONO , sin PLAZODS"))
        # print(("EL EXPEDIENTE ACTUAL ES: " + self.name))
        notifica_ids_count = self.env['notifica'].search_count([('expediente_id', '=', self.id),
                                                                ('state', '!=', 'draft'),
                                                                ('notificar_plazo_vencidos', '=', True)])
        # print(("RESULTADO ES: " + str(notifica_ids_count)))
        if notifica_ids_count > 0:
            notifica_objs = self.env['notifica'].search([('expediente_id', '=', self.id),
                                                        ('state', '!=', 'draft'),
                                                        ('notificar_plazo_vencidos', '=', True)])
            # print(("RESULTADO: " + str(notifica_objs)))
            for noti_obj in notifica_objs:
                #print (("ITERANDO NOTIFICACIONES A REALIZAR: " + str(noti_obj.state)))
                if noti_obj.state == "vencido":
                    vencido = True
                    break
        if vencido:
            self.estado_plazos = str('Vencido')
            if cant_plazos_asociados == notifica_ids_count:
                self.estado_plazos = str('Vencido_todos')
        else:
            if cant_plazos_asociados == notifica_ids_count and cant_plazos_asociados != 0:
                self.estado_plazos = str('Todos_plazos_notificados')
            elif cant_plazos_asociados > notifica_ids_count:
                # Si la cantidad de plazos asociados es mayor que la cantidad de plazos que el usuario agendó.
                # Entonces sigue mostrando el boton apropiado "amarillo", para recordar al usuario que puede agendar
                if notifica_ids_count > 0:
                    self.estado_plazos = str('Un_plazo')
                else:
                    self.estado_plazos = str('Plazos_asociados')
            elif notifica_ids_count == 1:
                self.estado_plazos = str('Un_plazo')
            elif notifica_ids_count > 1:
                self.estado_plazos = str('Mas_plazo')
            else:
                self.estado_plazos = str('Sin_plazo')

    estado_plazos = fields.Char('Estado de Plazos', compute="_estadoPlazo", required=False)

    def plazos(self):
        active_id = self.env.context.get('id_activo')
        user_id = self.env.user.id
        print (("EL DEPARTAMENTO DEL USUARIO ES: "))
        expte_obj = self.browse([active_id])
        #tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
        depart_actual_expte_id = expte_obj.ubicacion_actual
        depart_user_actual_id = self.userdepart(user_id)
        if not depart_user_actual_id:
            print (("No hay oficina actual asignada."))
        # print (("QUE COMPARO: " + str(depart_user_actual_id)+ " con " + str(depart_actual_expte_id.id)))
        if depart_user_actual_id != depart_actual_expte_id.id:
            print (("No pertenece a la misma oficina que el expediente."))
            raise ValidationError(('Solo puede acceder a esta informacion si el expediente se encuentra en la oficina.'))
        #CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
        #FIN OBTENER LAS RELACIONES
        if 1 > 0:
            #NUEVO PASE A OFICINA
            return {
            'name': "Listado de Plazos Agendados",
            'view_mode': 'tree',
            #'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'notifica',
            'type': 'ir.actions.act_window',
            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
            'domain': [('expediente_id', '=', expte_obj.id)],
            # 'context': {'recibido': False, 'oficina_destino': False, 'expediente_id_tarea': expte_obj.id},
            'views': [[self.env.ref('notificaciones.plazos_exp_list').id, "tree"]],
            'target': 'new',
            }
        return True

    def plazos_asociados(self):
        active_id = self.env.context.get('id_activo')
        legal_list = []
        user_id = self.env.user.id
        #VALIDACION
        expte_obj = self.browse([active_id])
        # tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
        depart_actual_expte_id = expte_obj.ubicacion_actual
        depart_user_actual_id = self.userdepart(user_id)
        if not depart_user_actual_id:
            print(("No hay oficina actual asignada."))
        if depart_user_actual_id != depart_actual_expte_id.id:
            print(("No pertenece a la misma oficina que el expediente."))
            raise ValidationError(
                ('Solo puede acceder a esta informacion si el expediente se encuentra en la oficina.'))
        #FIN DE VALIDACION
        # print(("BUSCANDO PLAZOS ASOCIADOS A LA TAREA"))
        tarea_obj_plazos = self.env['tarea.tarea'].search([('id', '=', self.tarea_actual.id)]).plazos
        for plazo in tarea_obj_plazos:
            # print (("QUE PLAZO TIENE: " + plazo.name))
            legal_list.append(plazo.id)
        #FIN OBTENER LAS RELACIONES
        if len(legal_list) > 0:
            #NUEVO PASE A OFICINA
            return {
            'name': "Listado de Plazos Asociados a la Tarea Actual",
            'view_mode': 'tree',
            #'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'tarea.plazo',
            'type': 'ir.actions.act_window',
            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
            'domain': [('id', 'in', legal_list)],
            'context': {'recibido': False, 'oficina_destino': False, 'expediente_id_tarea': active_id},
            'views': [[self.env.ref('tarea.plazo_list_con_opcion').id, "tree"]],
            'target': 'new',
            }
        else:
            view = self.env.ref('sh_message.sh_message_wizard_false')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = 'No hay información asociada.'
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
        return True

class plazo(models.Model):
    _name = 'tarea.plazo'
    _inherit = 'tarea.plazo'
    _description = "Agregar funcionalidad a al modelo tarea.plazos."

    def agendar_plazo(self):
        active_plazo_id = self.env.context.get('id_activo_plazo')
        active_exp_id = self.env.context.get('expediente_id_tarea')
        print("LOS VALORES QUE TRAE EN AGENDAR PLAZO: "  )
        print("id PLAZO: "+ str(active_plazo_id))
        print("id EXP: " + str(active_exp_id))
        # legal_list = []
        # print(("BUSCANDO PLAZOS ASOCIADOS A LA TAREA"))
        # tarea_obj_plazos = self.env['tarea.tarea'].search([('id', '=', self.tarea_actual.id)]).plazos
        # for plazo in tarea_obj_plazos:
        #     print (("QUE PLAZO TIENE: " + plazo.name))
        #     legal_list.append(plazo.id)
        #FIN OBTENER LAS RELACIONES
        if 1 > 0:
            #NUEVO PASE A OFICINA
            return {
            'name': "Agenda de Plazo",
            'view_mode': 'form',
            #'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'notifica',
            'type': 'ir.actions.act_window',
            # 'domain': [('id', 'in', legal_list)],
            'context': {'default_expediente_id': active_exp_id, 'default_plazo_id': active_plazo_id},
            'views': [[self.env.ref('notificaciones.notifica_form_exped').id, "form"]],
            'target': 'new',
            }
        return True

    def tarea_plazo_detalle(self):
        active_plazo_id = self.env.context.get('id_activo_plazo')
        active_exp_id = self.env.context.get('expediente_id_tarea')
        ###########################################
        # VERIFICAR SI EL USUARIO ACTUAL PERTENECE A LA MISMA OFICINA QUE LA TAREA A LA CUAL SE ENCUENTRA
        # ASOCIADO EL PLAZO
        expte_obj = self.env['expediente.expediente'].browse([active_exp_id])
        depart_actual_expte_id = expte_obj.ubicacion_actual
        tarea_actual_expte_id = expte_obj.tarea_actual
        if depart_actual_expte_id != tarea_actual_expte_id.departament_id:
            view = self.env.ref('sh_message.sh_message_wizard_false')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context[
                'message'] = 'Solo podrá ingresar el plazo, cuando el documento sea recibido ' \
                             'en la oficna a la cual está asociada la tarea.'
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
        #########################################
        # print("LOS VALORES QUE TRAE: "  )
        # print("id PLAZO: "+ str(active_plazo_id))
        # print("id EXP: " + str(active_exp_id))
        # print(("BUSCANDO PLAZOS ASOCIADOS A LA TAREA"))
        tarea_plazo_obj = self.env['notifica'].search([('expediente_id', '=', active_exp_id), ('plazo_id', '=', active_plazo_id)], limit=1)
        if tarea_plazo_obj:
            #NUEVO PASE A OFICINA
            return {
            'name': "Agenda de Plazo",
            'view_mode': 'form',
            'res_id': tarea_plazo_obj.id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'notifica',
            'type': 'ir.actions.act_window',
            # 'domain': [('id', 'in', legal_list)],
            'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
            'views': [[self.env.ref('notificaciones.notifica_form_exped').id, "form"]],
            'target': 'new',
            }
        else:
            return {
            'name': "Agenda de Plazo",
            'view_mode': 'form',
            #'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'notifica',
            'type': 'ir.actions.act_window',
            # 'domain': [('id', 'in', legal_list)],
            'context': {'default_expediente_id': active_exp_id, 'default_plazo_id': active_plazo_id},
            'views': [[self.env.ref('notificaciones.notifica_form_exped').id, "form"]],
            'target': 'new',
            }
        return True
