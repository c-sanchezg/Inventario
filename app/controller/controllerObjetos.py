from random import sample
from conexionBD import *

def listaObjetos():
    conexion_MySQLdb = connectionBD() 
    cur      = conexion_MySQLdb.cursor(dictionary=True)

    querySQL = "SELECT * FROM objetos ORDER BY id DESC"
    cur.execute(querySQL) 
    resultadoBusqueda = cur.fetchall() #fetchall () Obtener todos los registros
    totalBusqueda = len(resultadoBusqueda) #Total de busqueda
    
    cur.close() #Cerrando conexion SQL
    conexion_MySQLdb.close() #cerrando conexion de la BD    
    return resultadoBusqueda

def updateObjetos(id=''):
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM objetos WHERE id = %s LIMIT 1", [id])
        resultQueryData = cursor.fetchone() #Devolviendo solo 1 registro
        return resultQueryData

def registrarObjetos(nombre='', marca='', color='', fragil='', peso='', descripcion='', nuevoNombreFile=''):       
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)
            
        sql         = ("INSERT INTO carros(nombre, marca, color, fragil, peso, descripcion, foto) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valores     = (nombre, marca, color, fragil, peso, descripcion, nuevoNombreFile)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        cursor.close() #Cerrando conexion SQL
        conexion_MySQLdb.close() #cerrando conexion de la BD
        
        resultado_insert = cursor.rowcount #retorna 1 o 0
        ultimo_id        = cursor.lastrowid #retorna el id del ultimo registro
        return resultado_insert

def detallesObjetos(idObjetos):
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM objetos WHERE id ='%s'" % (idObjetos,))
        resultadoQuery = cursor.fetchone()
        cursor.close() #cerrando conexion de la consulta sql
        conexion_MySQLdb.close() #cerrando conexion de la BD
        
        return resultadoQuery

def  recibeActualizarObjetos(nombre, marca, color, fragil, peso, descripcion, nuevoNombreFile, idObjetos):
        conexion_MySQLdb = connectionBD()
        cur = conexion_MySQLdb.cursor(dictionary=True)
        cur.execute("""
            UPDATE carros
            SET 
                nombre   = %s,
                marca  = %s,
                color    = %s,
                fragil   = %s,
                peso = %s,
                descripcion = %s,
                foto    = %s
            WHERE id=%s
            """, (nombre, marca, color, fragil, peso, descripcion, nuevoNombreFile,  idObjetos))
        conexion_MySQLdb.commit()
        
        cur.close() #cerrando conexion de la consulta sql
        conexion_MySQLdb.close() #cerrando conexion de la BD
        resultado_update = cur.rowcount #retorna 1 o 0
        return resultado_update

#Renombrar foto para evitar valores duplicados
def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio
    