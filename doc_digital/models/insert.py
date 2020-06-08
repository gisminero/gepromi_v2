#Libreria a Importar
import psycopg2


#Campos a incorporar en la clase
        'informe_file' : fields.binary('Informe T�cnico', readonly=True),
        'informe_fname': fields.char('Informe', size=32, readonly=True),


#Funcion Insertar
        def insertar(self, cr, uid, ids, context):
            #INSERTAR ARCHIVO EN LA BASE

            full_path = '/srv/informes/informe.docx'
            #full_path = open('/tmp/ruta.txt', 'w+')
            #comienzo prueba 7***
            f = open(full_path, 'rb')
            binary = f.read().encode('base64')

            binary_texto = f2.read().encode('base64')
            cr.execute("UPDATE mrp_production"\
                        " SET"\
                        " (informe_file) = (%s)"\
                        " WHERE id = %s"\
                        " ;" % (psycopg2.Binary(binary), ids[0]))
            #FIN INSERTAR ARCHIVO EN LA BASE
            obj_prod = self.pool.get('mrp.production')
            vals = {'informe_fname': full_path}
            obj_prod.write(cr, uid, ids, vals, context=None)
            return True



#EN LA VISTA debe quedar algo así

            <group>
                <button name="exportar_word" on_click="exportar_word" string="Exportar a Word" type="object" class="oe_highlight"/>
                <field name="informe_fname"   invisible="1"/>
                <field name="informe_file" filename="informe_fname" attrs="{'invisible':[('informe_file_final' , '!=' , False)] }" />
            </group>