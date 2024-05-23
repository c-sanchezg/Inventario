from flask import Flask, render_template, request, redirect, url_for, jsonify
from controller.controllerObjetos import *


#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 


#Declarando nombre de la aplicación e inicializando
app = Flask(__name__)
application = app

msg  =''
tipo =''


#Creando mi decorador para el home, el cual retornara la Lista de Carros
@app.route('/', methods=['GET','POST'])
def inicio():
    return render_template('public/layout.html', miData = listaObjetos())


# ------ RUTAS
@app.route('/registrar-objeto', methods=['GET','POST'])
def addObjeto():
    return render_template('public/acciones/add.html')


 
#Registro Objeto
@app.route('/objeto', methods=['POST'])
def formAddObjeto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        color = request.form['color']
        fragil = request.form['fragil']
        peso = request.form['peso']
        descripcion = request.form['descripcion']
        
        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrarObjetos(nombre, marca, color, fragil, peso, descripcion, nuevoNombreFile)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaObjetos(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-objeto/<string:id>', methods=['GET','POST'])
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateObjetos(id)
        if resultData:
            return render_template('public/acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaObjetos(), msg='No existe el carro', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaObjetos(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalle-objeto/<int:idObjeto>', methods=['GET', 'POST'])
def viewDetalleCarro(idObjeto):
    msg =''
    if request.method == 'GET':
        resultData = detallesObjetos(idObjeto) #Funcion que almacena los detalle objeto
        
        if resultData:
            return render_template('public/acciones/view.html', infoCarro = resultData, msg='Detalles del Carro', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe el Carro', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-objeto/<string:idObjeto>', methods=['POST'])
def  formActualizarObjeto(idObjeto):
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        color = request.form['color']
        fragil = request.form['fragil']
        peso = request.form['peso']
        descripcion = request.form['descripcion']
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarObjetos(nombre, marca, color, fragil, peso, descripcion, fotoForm, idObjeto)
        else:
            fotoCarro  ='sin_foto.jpg'
            resultData = recibeActualizarObjetos(nombre, marca, color, fragil, peso, descripcion, fotoCarro, idObjeto)

        if(resultData ==1):
            return render_template('public/layout.html', miData = listaObjetos(), msg='Datos del carro actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layout.html', miData = listaObjetos(), msg='No se pudo actualizar', tipo=1)


#Eliminar liminar
@app.route('/borrar-objeto', methods=['GET', 'POST'])
def formViewBorrarObjeto():
    if request.method == 'POST':
        idObjeto = request.form['id']
        nombreFoto = request.form['nombreFoto']
        resultData = eliminarObjeto(idObjeto, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarObjeto(idObjeto='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM objetos WHERE id=%s', (idObjeto,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\objetos\app
    url_File = os.path.join (basepath, 'static/assets/foto_insert', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/foto_insert', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

       
  
  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)