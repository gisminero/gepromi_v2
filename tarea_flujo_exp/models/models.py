# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode
import datetime

import time

class seguimiento_subproc(models.Model):
        _name = 'seguimiento_subproc'
        _order = "write_date desc"
        seguimiento_id = fields.Many2one('seguimiento', 'Seguimiento al que pertenece el subflujo', required=True)
        subproc_id = fields.Many2one('procedimiento.procedimiento', 'Sub procedimiento', required=0, ondelete='cascade', select=True)
        momento_inicio = fields.Datetime('Momento de Inicio', readonly=True, default=fields.Datetime.now)
        subproc_cerrado = fields.Boolean('Sub Procedimiento Cerrado', readonly=False)
        tarea_regreso = fields.Many2one('tarea.tarea', 'Tarea Regreso', copy=False, required=False)

        def def_buscar_subflujo_abierto(self, seguimiento_obj):
                print (("BUSCANDO SUBFLUJO ABIERTO  ABIERTO" + str(seguimiento_obj)))
                seguim_subproc_obj_encontrado = self.search([('seguimiento_id', '=', seguimiento_obj.id), ('subproc_cerrado', "=", False)], limit=1)
                if seguim_subproc_obj_encontrado == False:
                        print(("CONTROLADOR DE SUBFLUJO ABIERTO NO ENCONTRADO "))
                else:
                        print(("CONTROLADOR DE SUBFLUJO ABIERTO ENCONTRADO " + str(seguim_subproc_obj_encontrado)))
                return seguim_subproc_obj_encontrado

        def def_buscar_subflujo(self, seguimiento_obj):
                print (("BUSCANDO SUBFLUJO" + str(seguimiento_obj)))
                seguim_subproc_obj_encontrado = self.search([('seguimiento_id', '=', seguimiento_obj.id)], limit=1)
                print(("CONTROLADOR DE SUBFLUJO ENCONTRADO " + str(seguim_subproc_obj_encontrado)))
                return seguim_subproc_obj_encontrado

        @api.multi
        @api.depends('subproc_cerrado')
        def def_cerrar_segu_subproc(self):
                print (("CERRANDO EL SUBPROCESO "))
                self.subproc_cerrado = True
                return True

class seguimiento_linea(models.Model):
        _name = 'seguimiento_linea'
        _order = "id desc"

        name = fields.Char('Nombre Seguimiento', required=False, readonly=False)
        seguimiento_id = fields.Many2one('seguimiento', 'Seguimiento', required=0, ondelete='cascade', select=True)
        tarea = fields.Many2one('tarea.tarea', 'Tarea', copy=False, required=False)
        tarea_inicio = fields.Datetime('Fecha Solicitada', readonly=True)#default=fields.Datetime.now
        tarea_fin = fields.Datetime('Fecha Fin', readonly=True)
        subproc = fields.Many2one('procedimiento.procedimiento', 'Pertenece a Sub Procedimiento', copy=False, required=False)
        observ_segui = fields.Text(string='Observaciones', translate=True, readonly=True)
        #subproc_pertenece = fields.Boolean('Pertenece a Sub Procedimiento', readonly=False)

class seguimiento(models.Model):
        _name = 'seguimiento'
        _order = "write_date desc"

        @api.depends('expediente_id', 'name')
        @api.one
        def default_name(self):
                print (("COLOCANDO EL NOMBRE"))
                valor = '---'
                # if self.expediente_id:
                #         valor = self.expediente_id.name
                # else:
                #         valor = '-+-'
                # return name
                self.name = valor
        def asignar_nombre(self, expediente_id):
                expte_obj = self.env['expediente.expediente']
                expte_obj_instan = expte_obj.browse([expediente_id])
                #print(("ASIGNANDO NOMBRE: " + str(expte_obj_instan.name)))
                valor = expte_obj_instan.name
                return {'vals': {'name':  valor}}

        name = fields.Char('Nombre Seguimiento', required=False, readonly=False)#, default=default_name, store=False
        expediente_id = fields.Many2one('expediente.expediente','Expediente', required=True)
        seguimiento_lineas = fields.One2many('seguimiento_linea', 'seguimiento_id', 'Flujo Seguimiento Lineas', )
        _sql_constraints = [('exp_uniq_exp', 'unique(expediente_id)', 'El numero de Expediente para seguimientos por tareas')]

        def ultima_linea_historial_tarea(self, expte_id):
                segu_obj = self.env['seguimiento']
                seguimiento_obj_count = segu_obj.search_count([('expediente_id', '=', expte_id)])
                if seguimiento_obj_count < 1:
                        return False
                seguimiento_obj = segu_obj.search([('expediente_id', '=', expte_id)], limit=1)
                print(("SEGUIMIENTO OBJ " + str(seguimiento_obj)))
                ordenar_por = "id desc"
                seguimiento_linea_obj = self.env['seguimiento_linea']
                ultima_linea_obj = seguimiento_linea_obj.search([('seguimiento_id', '=', seguimiento_obj.id)],
                                                                order=ordenar_por, limit=1)
                if ultima_linea_obj == False:
                        print((" LA ULTIMA LINEA ENCONTRADA DEVUELVE FALSE --- ES DECIR QUE NO TIENE LINEAS CARFGADAS "))
                else:
                        print ((" ENCONTRADA LA ULTIMA LINEA : " + str(ultima_linea_obj.tarea_inicio) + " ---- " + str(ultima_linea_obj.tarea_fin)))
                return ultima_linea_obj

        def tarea_selec_en_subflujo_abierto(self, subfproced_id, tarea_selec_id):
                # returns True, si la tarea seleccionada por el usuario pertenece al subflujo abierto, para este documento
                # returns False, si la tarea seleccionada no pertenece al subflujo abierto.
                proc_obj = self.env['tarea_flujo.flujo']
                proc_obj_instan = proc_obj.search([('name', '=', subfproced_id)])[0]
                # proc_obj_instan = proc_obj.browse([subflujoabierto_id])
                print ((" EL subflujo ABIERTO encontrado pertenece al procedimiento " + str(proc_obj_instan.name.name)))
                print((" Los codigos de la tareas encontradas son las siguientes: " ))
                count = 1
                pertenece_subflujo = False
                for linea in proc_obj_instan.lineflujo_ids:
                        print ((str(count) + " - Padre: " + linea.tarea_padre.codigo +  " Tarea: " + linea.tarea.codigo))
                        if tarea_selec_id == linea.tarea_padre.id:
                                return True
                return pertenece_subflujo

        def obtener_ultimo_pase_oficina(self, expte_id):
                print(("OBTENER ULTIMO PASE OFICINA" + str(expte_id.id)))
                obj_pase = self.env['pase.pase']
                obj_pase_encontr = obj_pase.search([('expediente_id','=', expte_id.id)])#limit=1,, order='desc'
                for pase in obj_pase_encontr:
                        print(" ####################### PASE ENCONTRADO: " + pase.name)
                return True

        def comienzo_nueva_tarea(self):
                now = datetime.datetime.now()
                #Inserta la fecha de comienzo de la nueva tarea
                #Si hay cambio de oficina, la fecha de comienzo ingresará cuando el expediente sea recibido por la
                #Nueva oficina, caso contrario la fecha de comienzo ingresara la misma fecha de finalizaciòn de la tarea
                #anterior
                ordenar_por = "id desc"
                seguimiento_linea_obj = self.env['seguimiento_linea'].search([('tarea_inicio', '=', False)],
                                                                             order=ordenar_por, limit=1)[0]
                seguimiento_linea_obj.write({'tarea_inicio': now})
                return True

        def obtener_config_cambio(self, tramite_id, estado_legal_id):
                # @retuns: Una lista de nuevos
                # tramites posibles, segun el tramite y estado legal que es enviado por parametro
                #  Ej. tramite enviado por parametro "Manifestarion de primera categoria" y estado "COncedido"  puede
                #  retornar [ ('id de Concesion Minera', 'id de Otro Tramite posible')]
                cambio_obj = self.env['conf_cambio_tramite']
                config_obj_encontrados_count = cambio_obj.search_count([('tramite_inicial_id', '=', tramite_id.id),
                                                                        ('estado_legal_id', '=', estado_legal_id.id)])
                if config_obj_encontrados_count < 1:
                        return False
                config_obj_encontrado = cambio_obj.search([('tramite_inicial_id', '=', tramite_id.id),
                                                        ('estado_legal_id', '=', estado_legal_id.id)])[0]
                lista_tramites_posibles = []
                for linea_config in config_obj_encontrado.tramites_posibles_ids:
                        lista_tramites_posibles.append(linea_config.tramite_id.id)
                        print((" LA LISTA DE VALORES ENCONTRADOS ES: " + str(linea_config.tramite_id.name)))
                return lista_tramites_posibles

        def hay_cambio_tramite(self, linea):
                #Disparo Cambio de Trámite
                print((" IIIIIIIIIIIIIIIIIIIIIIII DISPARANDO EL CAMBIO DE ESTADO LEGAL ACTUAL IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII "))
                print((" iD TRAIDO ES: " + str(linea.id)))
                nombre_exp = linea.seguimiento_id.expediente_id.name
                obj_exp = linea.seguimiento_id.expediente_id
                obj_tarea_que_termina = linea.tarea
                lista_config_cambio = self.obtener_config_cambio(obj_exp.procedimiento_id, obj_tarea_que_termina.estado_legal)
                if not lista_config_cambio:
                        #No hay registros configurados para este tamite y tarea qeu termina
                        return False
                else:
                        #Marcar el expediente, para realizar el cambio de tramite
                        obj_exp.cambio_de_tramite = True
                        return True

        def fin_tarea_actual(self, seguim_obj_encontrado):
                #CONTIENE LA LOGICA DE INGRESO DE FECHAS DE TAREAS
                for linea in seguim_obj_encontrado.seguimiento_lineas:
                    print (("LINEA PARA INSERTAR LA FECHA: " + str(linea.name) + " TAREA: " + str(linea.tarea.name) + " Fecha inicio: " + str(linea.tarea_inicio)+ " Fecha Fin: " + str(linea.tarea_fin)))
                    if linea.tarea_fin == False:
                            linea.write({'tarea_fin': datetime.datetime.now()})
                            self.hay_cambio_tramite(linea)
                            # linea.tarea_fin = datetime.datetime.now()
                return True

        def ingresa_tarea_actual(self, expte_id, tarea_actual_obj, tarea_proxima_obj, pase_de_oficina):
                # Parametros recibidos Expediente, tarea actual, tarea seleccionada por el usuario
                # 06/05/2021 Se agrega el parametro pase_de_oficina, el mismo posibilita la logistica de saber si se
                # deben ingresar las fechas de terminacion inicio o terminacion de tarea
                seguim_obj_encontrado = self.search([('expediente_id', '=', expte_id.id)], limit=1)
                #AVERIGUAR SI HAY SUBPROCEDIMIENTO ABIERTO
                obj_seguim_subproc = self.env['seguimiento_subproc']
                subproc_a_asignar = False
                now = datetime.datetime.now()
                if seguim_obj_encontrado:
                        print(("SEGUIMIENTO ABIERTO ENCONTRADO ##############################"))
                        control_subproc_obj = obj_seguim_subproc.def_buscar_subflujo_abierto(seguim_obj_encontrado)
                        if not control_subproc_obj:
                                subproc_a_asignar = tarea_proxima_obj.subproc.id
                                #Tarea 6 es una tarea de ingreso a subproceso, para tareas de otro tipo
                                #sigue el curso normal, fuera de este IF
                                if tarea_proxima_obj.tipo == '6':
                                        #print(("NO SE HA ENCONTRADO SUBFLUJO ABIERTO, SE HARA EL ALTA DE UN REGISTRO DE SUBPROCESO"))
                                        #print(("PORQUE LA TAREA ES DEL TIPÒ SUBPROCESO"))
                                        #CREANDO EL CONTROLADOR DE SUBFLUJO ANTE EL INGRESO AL SUBFLUJO
                                        control_subproc_obj = obj_seguim_subproc.create({'seguimiento_id': seguim_obj_encontrado.id, 'subproc_id': subproc_a_asignar,
                                                        'subproc_cerrado': False, 'tarea_regreso': tarea_actual_obj.id})
                        else:
                                subproc_a_asignar = control_subproc_obj.subproc_id.id
                                # print(("TAREA ACTUAL TIPO: " + str(tarea_actual_obj.tipo)))
                                # if tarea_actual_obj.tipo == '5':
                                #24/03/2021
                                #Se cambia el if anterior que consulta por la tarea del tipo 5, por la logica de consultar
                                # si el usuario ha seleccionado una tarea qie se encuentra fuera del subflujo, si es asi
                                # el controlador de subflujo debe cerrarse.
                                # A continuacion se llama a la funcion que determina si la tarea selecionada pertenece al
                                # subflujo, si no es asi , el controlador de sublujo debe cerrarse.
                                pertenece_a_subflujo = self.tarea_selec_en_subflujo_abierto(subproc_a_asignar, tarea_proxima_obj.id)
                                if pertenece_a_subflujo == False:
                                        control_subproc_obj.write({'subproc_cerrado': True})
                                        # print(("CERRANDOOO   ---- SE DEBE CERRAR EL CONTROLADOR DE SUBPROCESOS"))
                        #Se cierra la tarea actual mediante la asignación de fecha de fin,
                        # antes de crear la nueva linea, correspondiente a la proxima tarea
                        self.fin_tarea_actual(seguim_obj_encontrado)
                        #Si no hay pase de oficina, se debera asignar la fecha de inicio de la nueva tarea
                        #Si Hay pase de oficina se deja, para que el inicio de tarea sea asignado al recibir el expediente
                        #en la nueva oficina.
                        if pase_de_oficina == True:
                            print ((" @@@@@@@@@@@@@@@@@@ PASE DE OFICINA"))
                            #Caso probado
                            fecha_inicio_nueva_tarea = False
                        else:
                            print((" @@@@@@@@@@@@@@@@@@ NO HAY PASE DE OFICINA"))
                            # Falta probar este caso
                            fecha_inicio_nueva_tarea = now
                        seguim_obj_encontrado.write({'seguimiento_lineas': [(0, 0, {'tarea': tarea_proxima_obj.id,
                                                                                     'subproc': subproc_a_asignar,
                                                                                     'tarea_inicio': fecha_inicio_nueva_tarea,
                                                                                     'observ_segui': expte_id.observ_pase})]})
                else:
                        print(("SEGUIMIENTO CERRADO ENCONTRADO ##############################"))
                        id_creado = self.create({'name': str(expte_id.name), 'expediente_id': expte_id.id})
                        # print (("EL IB DEL OBJETO CREADO ES:  " + str(id_creado.id)))
                        # print(("LA TAREA ACTUAL QUE LLEGA ES:  " + str(tarea_actual_obj)))
                        seguimiento_obj_lineas = self.ultima_linea_historial_tarea(expte_id.id)
                        # print(("LA TAREA SELECCIONADA POR EL USUARIO QUE LLEGA ES:  " + str(
                        #         tarea_proxima_obj) + " VALOR DE SEGUIMIENTO ES: " + str(seguimiento_obj_lineas)))
                        tarea_a_ingresar_id = tarea_proxima_obj.id
                        if seguimiento_obj_lineas == False:# and not tarea_proxima_obj
                                # print (("Asignando la tarea actual como proxima..............."))
                                #Significa que no hay lineas de seguimiento previas y se esta ingresando en el flujo
                                tarea_a_ingresar_id = tarea_actual_obj.id
                        #amsterdam = pytz.timezone('America/Argentina/Buenos_Aires')
                        #hoy_str = datetime.date.today()
                        id_creado.write({'seguimiento_lineas': [(0, 0, {'tarea': tarea_a_ingresar_id,
                                                                        'subproc': subproc_a_asignar,
                                                                        'tarea_inicio': now,
                                                                        'observ_segui': expte_id.observ_pase})]})
                        return id_creado
                return True

class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"

        @api.multi
        def _selec_prox_tarea_segun_flujo(self, flujo_obj, tarea_actual, en_flujo, id_active):
                print (("QUE RECIBE PROX TAREA SEGUN FLUJO: OBJ_FLUJO " + str(flujo_obj.name.name)))
                print(("TAREA ACTUAL: " + str(tarea_actual.name) + "   ---- EN FLUJO: " + str(en_flujo)))
                # id_active = self._get_current_id()
                # id_active = self.id
                print((" EL ID DE DE EXPEDIENTE ENCONTRADO EN LA FUNCION DE SELECC PROX TAREA ES : " + str(id_active)))
                legal_list = []
                legal_list.append(False, )
                obj_seguim = self.env['seguimiento']
                seguim_obj_encontrado = obj_seguim.search([('expediente_id', '=', id_active)], limit=1)
                print (("DESPES DEL SEARCH .... " + seguim_obj_encontrado.name))
                obj_seguim_subproc = self.env['seguimiento_subproc']
                control_subproc_obj = obj_seguim_subproc.def_buscar_subflujo(seguim_obj_encontrado)
                print((" EL NOMBRE DEL SUBPROCESO ENCONTRADO ES : " + str(control_subproc_obj.seguimiento_id.name)))
                if control_subproc_obj:
                        if not control_subproc_obj.subproc_cerrado:
                                # if control_subproc_obj and tarea_actual.tipo == '3':
                                if tarea_actual.tipo == '3':
                                        #print(("ESTABLECER TODOS LOS MECANISMOS PARA EL ARCHIVO DLE EXPEDIENTE ########################"))
                                        # !!!!
                                        #SE ESTABLECE EL ARCHIVADO EN EL LUGAR EN EL QUE SE GRABA LA SELECCION DEL USUARIO
                                        #!!!!
                                        self._archivar_exped()
                                        # control_subproc_obj.def_cerrar_segu_subproc()
                                elif tarea_actual.tipo == '5':
                                        #print(("VOLVIENDO  A LA TAREA DE INICIO DE EXPEDIENTE #######24/010/2019#################"))
                                        legal_list.append(control_subproc_obj.tarea_regreso.id)
                                        return legal_list
                                else:
                                        print (("EL OBJETO FLUJO TRAIDO ES: " + str(flujo_obj)))
                                        flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [control_subproc_obj.subproc_id.id])])
                        else:
                                #print(("EL CONTROL DE SUBFLUJO ESTA CERRADO ########################"))
                                if tarea_actual.tipo == '5':
                                        #print(("ASIGNANDO CONTRO DEL FLUJO TAREA DE REGRESO #####///###################"))
                                        legal_list.append(control_subproc_obj.tarea_regreso.id)
                                        return legal_list
                # 24/03/2021
                # Nota: La siguiente linea es muy importante, si no hubo subprocedimiento abierto, entonces significa
                # que la variable flujo_obj, no fue alterada y la siguiente iteracion se realiza sobre las tareas
                # configuradas en el flujo principal.
                lineas = flujo_obj.lineflujo_ids
                for lin in lineas:
                        # print(("ANTES DE INGRESA EN EL FOR DE LINEAS - Tarea Padre: " + lin.tarea_padre.codigo + " - "
                        #        + " Tarea: " + lin.tarea_padre.codigo ))
                        if self.def_si_esta_en_subflujo(flujo_obj, tarea_actual):
                                #No esta en subflujo, por lo tanto, sigue el curso norma
                                # print(("ENTRÓ EN EL FOR DE LINEAS"))
                                if en_flujo:
                                        # print(("EN FLUJO"))
                                        if lin.tarea_padre.id == tarea_actual.id:
                                                legal_list.append(lin.tarea.id)
                                                # print(("TAREA AGREGADA A LA LISTA POR SER LA TAREA PADRE IGUAL A LA TAREA ACTUAL"))
                                        # else:
                                        #         print(("NOOOO TAREA AGREGADA A LA LISTA POR SER LA TAREA PADRE IGUAL A LA TAREA ACTUAL"))
                                        #         legal_list.append(lin.tarea.id)
                                else:
                                        legal_list.append(lin.tarea.id)
                #print ((" RETOENANOD LISTA LEGAL, antes de salir de la funcion: " + str(legal_list)))
                return legal_list

        @api.multi
        @api.depends("tarea_actual")
        def _proxima_tarea_list(self):
            print(("BUSCANDO LISTA LEGAL #############################"))
            #####IMPORTACION DE ACCIONES DESDE LA FUNCION ORIGINAL################
            print(("TAREA ENVIAR 2021"))
            permiso_de_ingreso = self._get_permiso_ingreso()
            legal_list = []
            legal_list_office = []
            active_id = self.env.context.get('id_activo')
            print (("EL ID ACTIVO EN ESTE EXPEDIENTE ES 2021: " + str(active_id)))
            expte_obj = self.browse([active_id])
            tarea_actual = expte_obj.tarea_actual
            en_flujo = expte_obj.en_flujo
            proced_id = expte_obj.procedimiento_id.id
            # NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
            user_id = self.env.user.id
            depart_id = self.userdepart(user_id)
            flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [proced_id])])
            # print(("NO HAY FLUJO PARA ... " + expte_obj.procedimiento_id.name))
            # SI NO HAY FLUJO O EL EXPEDIENTE TIENE UBICACION ACTUAL EN LA NUBE--
            if flujo_obj:
                print(("SE ENCONTRO UN FLUJO CORRESPONDIENTE A " + expte_obj.procedimiento_id.name))
            pase_obj = self.env['pase.pase']
            user_id = self.env.user.id
            depart_id = self.userdepart(user_id)
            pase_cerrado = pase_obj.ultima_condicion_recibido(active_id)
            # FIN CONSULTANDO PASES
            if not en_flujo:
                t_activ = self.env['tarea.tarea'].search([('active', '=', True), ('departament_id', '=', depart_id)])
                for id_tarea in t_activ:
                    if permiso_de_ingreso:
                        if self.en_procedimiento_actual(proced_id, id_tarea.id):
                            legal_list_office.append(id_tarea.id)
                    # else:
                    #         print (("Lista Vacia: El usuario no tiene permisos para ingresar en el flujo"))
            else:
                # print (("LAMANDO A SELEC PROXIMA TAREA... 2021"))
                legal_list = self._selec_prox_tarea_segun_flujo(flujo_obj, tarea_actual, en_flujo, active_id)
            #####FIN DE IMPORTACION DE ACCIONES DESDE LA FUNCION ORIGINAL###############################################
            #26/03/2021 A continuacion se agrega la lista de tareas posibles obtenidas desde un subflujo.
            # Es el caso en el cual el documento, ingresa en un subflujo por lo tanto, el manejador de subflujos se encuentra
            # abtierto.
            # Fin tareas desde subflujo
            print(("LISTA LEGAL TRAIDA Y ENVIADA AL DOMAIN: " + str(legal_list)))
            return [('id', 'in', legal_list)]

        def _actual_tarea_list(self):
            """
            Define la tarea actual, en caso de encontrarse en el flujo, es la tarea asignada en el paso anterior del flujo
            En caso de no encontrarse en el flujo la funcion devuelve todas las tareas posibles para el procedimiento
            seleccionado para esa oficina.
            Para retornar la lista completa de tareas en la oficina debera tener permisos de ingreso.
            :return: lista de tareas actuales
            """
            ##################################DEFINIENDO LA TAREA ACTUAL EN EL FLUJO
            print(("TAREA actual de la oficina"))
            permiso_de_ingreso = self._get_permiso_ingreso()
            legal_list_office = []
            active_id = self.env.context.get('id_activo')
            expte_obj = self.browse([active_id])
            tarea_actual = expte_obj.tarea_actual
            en_flujo = expte_obj.en_flujo
            proced_id = expte_obj.procedimiento_id.id
            # NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
            user_id = self.env.user.id
            depart_id = self.userdepart(user_id)
            flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [proced_id])])
            # print(("NO HAY FLUJO PARA ... " + expte_obj.procedimiento_id.name))
            # SI NO HAY FLUJO O EL EXPEDIENTE TIENE UBICACION ACTUAL EN LA NUBE--
            if not flujo_obj or expte_obj.ubicacion_actual.name.lower() == "Nube".lower():
                return False
            if not en_flujo:
                t_activ = self.env['tarea.tarea'].search([('active', '=', True), ('departament_id', '=', depart_id)])
                for id_tarea in t_activ:
                    if permiso_de_ingreso:
                        if self.en_procedimiento_actual(proced_id, id_tarea.id):
                            legal_list_office.append(id_tarea.id)
                    # else:
                    #         print (("Lista Vacia: El usuario no tiene permisos para ingresar en el flujo"))
            else:
                legal_list_office.append(tarea_actual.id)
            return (legal_list_office)

        tarea_actual = fields.Many2one('tarea.tarea', 'Tarea Actual', required=False, readonly=True, domain=_actual_tarea_list)
        tarea_proxima = fields.Many2one('tarea.tarea', 'Tarea Prox.', required=False, readonly=False, domain=_proxima_tarea_list)
        #, domain=_proxima_tarea_list(), domain=[('id','in', [12387, 12388])]
        en_flujo = fields.Boolean('En Flujo', required=False, readonly=True)
        #web_service = fields.Char(compute='_compute_upper',)# inverse='_inverse_upper', search='_search_upper'
        id_form_solicitud = fields.Integer('Formulario Web ID Solicitud', required=False)

        @api.multi
        def _get_current_id(self):
                return self.id

        @api.multi
        @api.depends("emeu_sector_id.emeu_education_ids")
        def _get_education_domain(self):
                return True

        def cambia_estado_plazos(self, exp_id, nuevo_estado):
                #Cambia el estado de todos los plazos asignados al exp envido por parametro
                #Dado que existen gran cantidad de estados posibles es importante aclarar que
                # en esta funcion nos interesa solo conmutar entre estados desde 'activo' a 'suspendido' y viceversa
                today = datetime.datetime.now()
                plazo_obj = self.env['notifica']
                if nuevo_estado == 'suspendido':
                        info = "Este plazo se suspendió el día " + str(fields.Datetime.now)
                        plazo_obj = plazo_obj.search([('expediente_id', '=', exp_id), ('state', '=', 'active')])
                        if plazo_obj:
                                for plazo_obj_unico in plazo_obj:
                                        plazo_obj_unico.write({'state': 'suspendido', 'fecha_suspension_actual': fields.datetime.now(), 'info': info})
                                self.write({'estado_plazos' : 'Plazos_suspendidos'})
                if nuevo_estado == 'active':
                        info = "Este plazo se se reatableció el día " + str(today.strftime('%d-%m-%Y')) + " por lo cual la nueva fecha de vencimiento es "
                        plazo_obj = plazo_obj.search([('expediente_id', '=', exp_id), ('state', '=', 'suspendido')])
                        if plazo_obj:
                                for plazo_obj_unico in plazo_obj:
                                        #cant_dias_suspendido = datetime.date.today() - plazo_obj_unico.fecha_suspension_actual
                                        # plazo_id = plazo_obj_unico.plazo_id
                                        # if not plazo_id:
                                        #         return False
                                        # plazo_obj = self.env['tarea.plazo'].browse([plazo_id.id])
                                        cant_dias = plazo_obj_unico.plazo_id.cant
                                        tipo_dias = plazo_obj_unico.plazo_id.tipo
                                        nueva_fecha_vencimiento = plazo_obj_unico.recalculaDias(plazo_obj_unico.fecha_notificacion, cant_dias, tipo_dias)
                                        plazo_obj_unico.write({'state': 'active',
                                                       'fecha_suspension_actual': False,
                                                       'info': info + str(nueva_fecha_vencimiento),
                                                       'fecha_vencimiento': nueva_fecha_vencimiento})
                                self.write({'estado_plazos': 'Mas_plazo'})
                                # self.estado_plazos = 'Mas_plazo'
                return True

        def busca_plazos_activos(self, exp_id):
            # expte_obj = self.browse([exp_id])
            plazo_obj = self.env['notifica']
            plazo_obj_cant = plazo_obj.search_count([('expediente_id', '=', exp_id), ('state', '=', 'active')])
            # tarea_obj_prox = tarea_obj.browse([proxima_tarea_id])
            # print(("LA CANTIDAD DE PLAZOS ENCONTRADOS ACTIVOS, ES " + str(plazo_obj_cant)))
            if plazo_obj_cant > 0:
                return False
            else:
                return True

        def proxima_tarea_enviar(self):
                # print(("¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿ENVIANDO PASE DE TAREA Y OFICINA 2021_¡¡¡¡???????????????????????????"))
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                #OBTENIENDO VALORES DESDE CONTEX DEL POP UP
                tarea_actual_new = self.env.context.get('tarea_actual_new')#TAREA ACTUAL
                proxima_tarea_id = self.env.context.get('tarea_proxima_cont')#PROXIMA TAREA SELECCIONADA POR EL USUARIO
                fojas_new = self.env.context.get('fojas_new')#NUEVO NUMERO DE FOJAS
                destino_new = self.env.context.get('oficina_destino_new')#NUEVA OFICINA DESTINO
                observaciones_new = self.env.context.get('observaciones_new')#oBSERVACIONES DEL PASE
                #tarea_actual_old = self.env.context.get('tarea_actual')#CANDIDATO A SER BORRADO PORQUE NO TRAE NADA DESDE LA VISTA
                en_flujo_new = self.env.context.get('en_flujo_new')
                tipo_vista = self.env.context.get('vista_padre')
                notifica_obj = self.env['notifica']
                #Validacion OFICINA VACIA#
                if destino_new is False and proxima_tarea_id is not False:
                        view = self.env.ref('sh_message.sh_message_wizard_false')
                        view_id = view and view.id or False
                        context = dict(self._context or {})
                        context['message'] = 'Verifique que el valor de Oficina Destino se muestre en el formulario de envio. Vuelva a intentar el envio.'
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
                #Fin de Validacion OFICINA VACIA#
                #FIN OBTENIENDO VALORES DESDE CONTEX DEL POP UP
                #Validacion de Destino#
                if tarea_actual_new == proxima_tarea_id and destino_new == self.ubicacion_actual:
                        view = self.env.ref('sh_message.sh_message_wizard_false')
                        view_id = view and view.id or False
                        context = dict(self._context or {})
                        context[
                                'message'] = 'Tarea y oficina de origen y destino son iguales. Seleccione otra tarea u oficina.'
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
                #Fin de Validacion de Destino#
                sacar_de_flujo = expte_obj.en_flujo
                tarea_obj = self.env['tarea.tarea']
                tarea_obj_prox = tarea_obj.browse([proxima_tarea_id])
                tarea_char_prox_est_legal = tarea_obj_prox.estado_legal.name
                tarea_id_prox_est_legal = tarea_obj_prox.estado_legal.id
                seguimiento_obj = self.env['seguimiento']
                #SI LA TAREA ACTUAL ES 5 DEBO OBLIGAR EL CIERRE DEL CONTROLADOR DE SUBFLUJO
                # if tarea_obj_prox.tipo == '4':
                #         #SACAR DE FLUJO
                #         sacar_de_flujo = False
                #         return self.write({'tarea_actual': proxima_tarea_id,
                #                 'folios': fojas_new, 'en_flujo': sacar_de_flujo})
                #FIN  --- SI LA TAREA ACTUAL ES 5 DEBO OBLIGAR EL CIERRE DEL CONTROLADOR DE SUBFLUJO
                if tarea_obj_prox.tipo == '4':
                        #SACAR DE FLUJO
                        self.cambia_estado_plazos(expte_obj.id, 'suspendido')
                        sacar_de_flujo = False
                        seguimiento_obj.ingresa_tarea_actual(expte_obj, tarea_obj.browse([tarea_actual_new]), tarea_obj.browse([proxima_tarea_id]), True)
                        return self.write({'tarea_actual': proxima_tarea_id, 'folios': fojas_new, 'en_flujo': sacar_de_flujo})
                #if tarea_actual_new and not tarea_actual_old and not self.en_flujo:
                elif tarea_actual_new and not self.en_flujo:
                        #Se esta ingresando un expediente en flujo
                        print(("SE ESTA INTRODUCIENDO EL EXPETE EN EL FLUJO 28-11-2019"))
                        self.cambia_estado_plazos(expte_obj.id, 'active')
                        seguimiento_obj.ingresa_tarea_actual(expte_obj, tarea_obj.browse([tarea_actual_new]), tarea_obj.browse([proxima_tarea_id]), True)
                        return self.write({'tarea_actual': tarea_actual_new,
                        'folios': fojas_new, 'en_flujo': True,
                        'estado_legal_actual': tarea_obj.browse([tarea_actual_new]).estado_legal.name,
                        'estado_legal_actual_id': tarea_obj.browse([tarea_actual_new]).estado_legal.id})
                elif tarea_obj_prox.tipo == '3':
                        #Archivar el expediente
                        # print(("ARCHIVANDO EÑ EXPEDIENTE #########################"))
                        if not self.busca_plazos_activos(expte_obj.id):
                                view = self.env.ref('sh_message.sh_message_wizard_false')
                                view_id = view and view.id or False
                                context = dict(self._context or {})
                                context[
                                        'message'] = 'No se puede archivar el porque tiene un plazo de tiempo activo. Resuelva esta situación e intente nuevamente.'
                                return {
                                        'name': 'La Tarea Actual Solicita Archivo de Documento',
                                        'type': 'ir.actions.act_window',
                                        'view_type': 'form',
                                        'view_mode': 'form',
                                        'res_model': 'sh.message.wizard',
                                        'views': [(view.id, 'form')],
                                        'view_id': view.id,
                                        'target': 'new',
                                        'context': context,
                                }
                        seguimiento_obj.ingresa_tarea_actual(expte_obj, tarea_obj.browse([tarea_actual_new]), tarea_obj.browse([proxima_tarea_id]), False)
                        return self.write({'tarea_actual': proxima_tarea_id,
                                           'folios': fojas_new, 'en_flujo': sacar_de_flujo,
                                           'oficina_destino': destino_new,
                                           'estado_legal_actual': tarea_char_prox_est_legal,
                                           'estado_legal_actual_id': tarea_id_prox_est_legal,
                                           'state': 'archive'})
                elif destino_new == expte_obj.ubicacion_actual.id:
                        #ASIGNANDO TAREA SIN PASE DE OFICINA
                        print(("OFICINA ORIGEN IGUAL A DESTINP #########################"))
                        print((str(destino_new) + " /// " + str(expte_obj.ubicacion_actual.id)))
                        seguimiento_obj.ingresa_tarea_actual(expte_obj, tarea_obj.browse([tarea_actual_new]), tarea_obj.browse([proxima_tarea_id]), False)
                        return self.write({'tarea_actual': proxima_tarea_id,
                        'folios': fojas_new, 'en_flujo': sacar_de_flujo,
                        'oficina_destino': expte_obj.ubicacion_actual.id,
                        'estado_legal_actual': tarea_char_prox_est_legal,
                        'estado_legal_actual_id': tarea_id_prox_est_legal})
                else:
                        #ASIGNANDO TAREA Y PASE DE OFICINA
                        print(("ULTIMA OPCION - LA OFICINA DESTINO Y ORIGEN SON DFERENTES#########################"))
                        self = self.with_context(oficina_destino_new=destino_new)
                        self.enviar_conf()
                        self.write({'tarea_actual': proxima_tarea_id,
                                'folios': fojas_new, 'en_flujo': sacar_de_flujo,
                                'estado_legal_actual': tarea_char_prox_est_legal,
                                'estado_legal_actual_id': tarea_id_prox_est_legal})
                        # self.hay_cambio_tramite(expte_obj.id)
                        print (("RETORNANDO POR EL MODULO DE SEGUIMIENTO DE TAREAS"))
                        seguimiento_obj.ingresa_tarea_actual(expte_obj, tarea_obj.browse([tarea_actual_new]), tarea_obj.browse([proxima_tarea_id]), True)
                        return self.mi_oficina_view()

        def user_permiso_ingreso_flujo(self):
                user_id = self.env.user.id
                #print(("Buscanco el permiso"))
                #user = self.env.user
                self._cr.execute('SELECT * FROM ir_module_category INNER JOIN '
                                 ' res_groups ON ir_module_category.id=res_groups.category_id WHERE name = %s',
                           ('GeProMi.Ingresar en Flujo',))
                rows = self.env.cr.dictfetchall()
                ids = [x['id'] for x in rows]
                return True

        def _get_permiso_ingreso(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Ingresar_en_flujo')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        def def_si_esta_en_subflujo(self, flujo_obj, tarea_actual):
                #Determinar si la tarea actual se encuentra transitando un subflujo
                #En ese caso volver el id de subflujo, caso contrario vuelve False
                #Hay dos formas de determinar si el expediente se encuentra en subproceso
                # 1-Si la tarea actual es del tipo subproceso
                # 2-Si la tarea actual es distinta a subrpoceso y en el seguimiento de flujo se ha marcado la tarea actual como subproceso
                # lo cual significa que ya se encuentra transitando el subproceso.
                # SALIDAS DE LA FUNCIÓN:
                # 0: Continua el flujo normal del proceso
                # 1: Se encuentra en un subproceso
                # Esta Retornando de Un subproceso. Por lo tanto se deberá calcular a que tarea del proceso principal debe volver.
                return True

        def en_procedimiento_actual(self, proced_actual_id, tarea_id):
                ###BUSCAR EL FLUJO DEL PROCEDIMIENTO ACTUAL
                obj_flujo = self.env['tarea_flujo.flujo']
                flujo_obj_encontrado = obj_flujo.search([('name', '=', proced_actual_id)], limit=1)
                #####FIN BUSCAR EL FLUJO DEL PROCEDIMIENTO ACTUAL
                obj_flujolinea = self.env['tarea_flujo.flujolinea']
                flujolinea_obj_encontrado = obj_flujolinea.search([('flujo_id', '=', flujo_obj_encontrado.id), ('tarea_padre', '=', tarea_id)], limit=1)
                if flujolinea_obj_encontrado:
                        return True
                else:
                        return False

        def proxima_tarea(self):
                print(("TAREA ENVIAR 2"))
                permiso_de_ingreso = self._get_permiso_ingreso()
                #user_ingreso_flujo = self.user_permiso_ingreso_flujo()
                legal_list = []
                legal_list_office = []
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                en_flujo = expte_obj.en_flujo
                tarea_actual = expte_obj.tarea_actual
                en_flujo = expte_obj.en_flujo
                proced_id = expte_obj.procedimiento_id.id
                # NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
                user_id = self.env.user.id
                depart_id = self.userdepart(user_id)
                if depart_id != expte_obj.ubicacion_actual.id:
                        view = self.env.ref('sh_message.sh_message_wizard')
                        view_id = view and view.id or False
                        context = dict(self._context or {})
                        context['message'] = 'Para enviar el Expte. es necesario que se encuentre en su oficina.'
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
                # FIN NO SE PUEDE ENVIAR SI NO ESTA EN MI OFICINA
                flujo_obj = self.env['tarea_flujo.flujo'].search([('name', '=', [proced_id])])
                #print(("NO HAY FLUJO PARA ... " + expte_obj.procedimiento_id.name))
                #SI NO HAY FLUJO O EL EXPEDIENTE TIENE UBICACION ACTUAL EN LA NUBE--
                if not flujo_obj or expte_obj.ubicacion_actual.name.lower() == "Nube".lower():
                        return self.enviar()
                if flujo_obj:
                        # print(("SE ENCONTRO UN FLUJO CORRESPONDIENTE A " + expte_obj.procedimiento_id.name))
                        if not permiso_de_ingreso and not en_flujo:
                                #En este punto se encotró se debe dejar claro que si el tramite cuenta con un flujo definido
                                # el expediente no debe moverse hasta que se ingrese nuevamente en el flujo por alguien que
                                # tenga los permisos correspondientes
                                view = self.env.ref('sh_message.sh_message_wizard')
                                view_id = view and view.id or False
                                context = dict(self._context or {})
                                context['message'] = 'Este usuario no tiene permisos para ingresar expedientes en el flujo de tareas. ' \
                                                     'Si el trámite tiene flujo definido y no está dentro del mismo. No debe avanzar por oficinas.' \
                                                     'Contacte al administrador.'
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
                #CONSULTANDO PASES
                pase_obj = self.env['pase.pase']
                user_id = self.env.user.id
                depart_id = self.userdepart(user_id)
                pase_cerrado = pase_obj.ultima_condicion_recibido(active_id)
                #FIN CONSULTANDO PASES
                if not en_flujo:
                        t_activ = self.env['tarea.tarea'].search([('active', '=', True), ('departament_id', '=', depart_id)])
                        for id_tarea in t_activ:
                                if permiso_de_ingreso:
                                        if self.en_procedimiento_actual(proced_id, id_tarea.id):
                                                legal_list_office.append(id_tarea.id)
                                # else:
                                #         print (("Lista Vacia: El usuario no tiene permisos para ingresar en el flujo"))
                # else:
                        #legal_list = self.selec_prox_tarea_segun_flujo(flujo_obj, tarea_actual, en_flujo)[0]
                        # print (("LISTA LEGAL TRAIDA: " + str(legal_list)))
                if pase_cerrado:
                    #NUEVO PASE A OFICINA
                    print (("ID ACTIVO: " + str(active_id)))
                    return {
                            'name': "Seleccionar la próxima tarea",
                            'view_mode': 'form',
                            'res_id': active_id,
                            # 'view_id': self.env.ref('pase.form_enviar').id,
                            'res_model': 'expediente.expediente',
                            'type': 'ir.actions.act_window',
                            # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                            # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                            'context': { 'actual_tarea_list': legal_list_office, 'default_tarea_proxima': False,
                                'default_oficina_destino' : False, 'default_recibido': False, 'permiso_de_ingreso': permiso_de_ingreso},
                            #24/03/2021 REvisar la correspondencia en la visa de la variable enviada en el contexto, llamdad
                            #permiso_de_ingreso
                            'views': [[self.env.ref('tarea_flujo_exp.exp_pop_prox_tarea').id, "form"]],
                            #'permiso__ingreso': permiso_de_ingreso, 'default_tarea_proxima': False,'proxima_tarea_list': legal_list,
                            'target': 'new',
                    }
                else:
                    if not expte_obj.oficina_destino.name:
                        of_enviado = "-"
                    else:
                        of_enviado = unidecode(expte_obj.oficina_destino.name)
                    return {
                            'name': "EL DOCUMENTO SE ENCUENTRA ENVIADO A: " + str(of_enviado),
                            'view_mode': 'form',
                            'res_id': active_id,
                            #'view_id': self.env.ref('pase.form_enviar').id,
                            'res_model': 'expediente.expediente',
                            'type': 'ir.actions.act_window',
                            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                            #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                            #'context': {'recibido': True, 'ultimo_pase_id': pase_res.id, 'oficina_destino': depart_id},
                            'context': {'recibido': True, 'oficina_destino': depart_id},
                            'views': [[self.env.ref('expediente.form_enviado').id, "form"]],
                            'target': 'new',
                    }

        #def onchange_define_pase(self, tarea_prox, expte_obj):
        @api.onchange('tarea_proxima')
        def onchange_define_pase(self):
                obj_tarea = self.tarea_proxima
                #self.write({'oficina_destino': 2})
                print (("OBTENIENDO OFICINA DESTINO DE LA TAREA : " + str(obj_tarea.name)))
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                # tarea_obj = self.env['tarea.tarea']
                # tarea_obj_prox = tarea_obj.browse([tarea_prox])
                expte_obj.write({'oficina_destino': obj_tarea.departament_id.id})
                self = self.with_context(oficina_destino_new=obj_tarea.departament_id.id)
                print(("IMPRIMIENDO CONTEXTO des pues de actualizar la oficina: " + str(self.env.context)))
                # self.env.context.update({'oficina_destino_new': obj_tarea.departament_id.id})
                return {'value': {'oficina_destino': obj_tarea.departament_id }}

        def enviar_tarea_pase(self):
                #DEBER CREAR LA VISTA ENVIAR ESPECIFICA PARA ESTO
                active_id = self.env.context.get('id_activo')
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                depart_id = self.userdepart(user_id)
                # CONSULTANDO PASES
                pase_obj = self.env['pase.pase']
                pase_res = pase_obj.obtener_ultimo_pase(active_id)
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

        def obtener_tarea_inicial(self, pr_id):
                # print(("OBTENIENDO TAREA INICIAL ..." + str(pr_id)))
                fluj_count = self.env['tarea_flujo.flujo'].search_count([('name.id', 'in', [pr_id])])
                fluj = self.env['tarea_flujo.flujo'].search([('name.id', 'in', [pr_id])])
                if fluj_count < 1:
                        return False
                for inicial in fluj.lineflujo_ids:
                        if inicial.tarea_padre.tipo == '1':
                                print (("RETORNANDO LA OFICINA DE LA TAREA PADRE: " + inicial.tarea_padre.name))
                                return inicial.tarea_padre.id
                return False

        def existe_flujo(self, procedimiento_id):
                obj_flujo_tarea = self.env['tarea_flujo.flujo']
                obj_flujo_tarea_cant = obj_flujo_tarea.search_count([('name', '=', procedimiento_id)])
                # print (("LA CANTIDAD DE FLUJOS ENCONTRADOES ES: " + str(obj_flujo_tarea_cant)))
                if obj_flujo_tarea_cant == 0:
                        return False
                else:
                        return True

        def activar(self):
                # active_id_2 = self.env.context.get('id_activo')
                active_id_2 = self._get_current_id()
                print(("ACTIVANDO ... DESDE ... TAREA_FLUJO_EXP: " + str(active_id_2)))
                expte_obj_2 = self.browse([active_id_2])
                tarea_inicial_id = self.obtener_tarea_inicial(expte_obj_2.procedimiento_id.id)
                user_id = self.env.user.id
                depart_id = self.userdepart(user_id)
                depart_user_obj = self.env['hr.department'].browse([depart_id])
                tarea_obj = self.env['tarea.tarea']
                seguimiento_obj = self.env['seguimiento']
                if not tarea_inicial_id:
                        valor_en_flujo = False
                else:
                        valor_en_flujo = True
                tarea_obj_inicial = tarea_obj.browse([tarea_inicial_id])
                # print(("EL NOMBRE DEL DEPARTAMENTO  ES: " + depart_user_obj.name))
                if depart_user_obj.name == "Nube":
                        # print (("INGRESANDO POR NUBE"))
                        self.write({'en_flujo': False, 'tarea_actual': False,
                                    'estado_legal_actual': False,
                                    'estado_legal_actual_id': False})
                else:
                        if tarea_inicial_id:
                                print(("INGRESANDO POR TAREA INICIAL "))
                                self.write({'en_flujo': valor_en_flujo, 'tarea_actual': tarea_inicial_id,
                                        'estado_legal_actual': unidecode(tarea_obj_inicial.estado_legal.name),
                                        'estado_legal_actual_id': tarea_obj_inicial.estado_legal.id})
                                # seguimiento_obj.ingresa_tarea_actual(expte_obj_2, tarea_obj_inicial)
                                seguimiento_obj.ingresa_tarea_actual(expte_obj_2, tarea_obj_inicial, tarea_obj_inicial, False)
                                # self.hay_cambio_tramite(active_id_2)
                        else:
                                if self.existe_flujo(expte_obj_2.procedimiento_id.id):
                                        view = self.env.ref('sh_message.sh_message_wizard_false')
                                        view_id = view and view.id or False
                                        context = dict(self._context or {})
                                        context['message'] = 'No se encontro la tarea inicial del flujo de tareas: ' + expte_obj_2.procedimiento_id.name
                                        return {
                                        'name': 'Error: Contactese con el Administrador',
                                        'type': 'ir.actions.act_window',
                                        'view_type': 'form',
                                        'view_mode': 'form',
                                        'res_model': 'sh.message.wizard',
                                        'views': [(view.id, 'form')],
                                        'view_id': view.id,
                                        'target': 'new',
                                        'context': context,
                                        }
                print (("llamando al activar padre"))
                res = super(expediente, self).activar()
                return res

        def cancel_return_mi_oficina(self):
                #print (("PASANDO POR LA FUNCION HEREDADA"))
                self.write({'tarea_proxima': False, 'oficina_destino': False})
                res = super(expediente, self).cancel_return_mi_oficina()
                return res

        def ingresar_flujo_ultima(self):
                user_id = self.env.user.id
                fojas_new = self.env.context.get('fojas_new')
                destino_new = self.env.context.get('oficina_destino_new')
                observaciones_new = self.env.context.get('observaciones_new')
                depart_id = self.userdepart(user_id)
                #Ingresa en flujo en la ultima tarea, que hizo salir al mismo del flujo-
                # print (("INSERTANDO EN EL FLUJO ... *** ... "))
                active_id = self.env.context.get('id_activo')
                expte_obj = self.browse([active_id])
                seguimiento_obj = self.env['seguimiento']
                seguimiento_obj_lineas = seguimiento_obj.search([('expediente_id', '=', expte_obj.id)], limit=1)
                # for lineas in seguimiento_obj_lineas.seguimiento_lineas:
                #         if lineas.tarea.name != False:
                #                 print (("SACANDO COSAS: " + unidecode(lineas.tarea.name)))
                #Obtengo la ultima tarea, desde el historial de tareas.
                if not seguimiento_obj_lineas:
                         #El Documento no tiene historial de tareas.
                         raise ValidationError(('No es correcto utilizar esta función. No hay historial de tareas. '
                                                'Utilice la opción - Enviar - y seleccione tarea actual.'))
                lineas = seguimiento_obj_lineas.seguimiento_lineas[0]
                depart_id_ultima_tarea = lineas.tarea.departament_id.id
                if lineas.tarea.name != False:
                        print (("SACANDO COSAS: " + unidecode(lineas.tarea.name)))
                        print(("Oficina de la tarea: " + unidecode(lineas.tarea.departament_id.name)))
                if self.ubicacion_actual.id == depart_id_ultima_tarea:
                        #Si la ubicacion actual coincide con la oficina en la cual se ejecuta la tarea.
                        self.write({'en_flujo': True, 'tarea_actual': lineas.tarea.id, 'ubicacion_actual': lineas.tarea.departament_id.id})
                else:
                        #Si la ubicacion actual no coincide con la oficina en la cual se ejecuta la tarea.
                        pase_obj = self.env['pase.pase']
                        pase_obj.create({'user_origen_id': user_id,
                                         'name': str(expte_obj.name), 'expediente_id': active_id,
                                         'depart_origen_id': depart_id,
                                         'depart_destino_id': lineas.tarea.departament_id.id,
                                         'folios': fojas_new,
                                         'observ_pase': observaciones_new})
                        expte_obj.write({'folios': fojas_new,
                                         'recibido': False,
                                         'oficina_destino': lineas.tarea.departament_id.id,
                                         'observ_pase': "Reingreso Directo en Flujo de Tareas.",
                                         'en_flujo': True,
                                         'tarea_actual': lineas.tarea.id})
                seguimiento_obj.ingresa_tarea_actual(expte_obj, lineas.tarea, lineas.tarea)
                #############################################################################################
                #REHABILITAR PLAZOS SUSPENDIDOS!!!
                self.cambia_estado_plazos(expte_obj.id, 'active')
                #################################################################################################
                return True

        def recibir_conf(self):
                id_active = self._get_current_id()
                print((" EL ID ACTIVO QUE ME ESTA FALLANDO ES ......................... : " + str(id_active)))
                seguimiento_obj_count = self.env['seguimiento'].search_count([('expediente_id', '=', id_active)])
                if seguimiento_obj_count < 1:
                    seguimiento_obj = self.env['seguimiento'].ingresa_tarea_actual(self, self.tarea_actual, self.tarea_proxima, False)
                    seguimiento_obj.comienzo_nueva_tarea()
                else:
                    seguimiento_obj = self.env['seguimiento'].search([('expediente_id', '=', id_active),], limit=1)[0]
                    seguimiento_obj.comienzo_nueva_tarea()
                """
                self.write({'': True,
                                 'oficina_destino': False,
                                 'ubicacion_actual': depart_id,
                                 'observ_pase': ''})
                """
                res = super(expediente, self).recibir_conf()
                return res