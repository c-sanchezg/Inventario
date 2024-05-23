from flask import Flask, render_template, request, redirect, url_for, jsonify
from controller.controllerObjetos import *

try:
    datos = listaObjetos()
    return render_template('public/layout.html', miData=datos)
except Exception as e:
    # Maneja la excepción de alguna manera adecuada, por ejemplo, imprime el error
    print("Error:", e)
    # También puedes devolver un mensaje de error en lugar de renderizar el template
    return "Ocurrió un error al cargar los datos."
