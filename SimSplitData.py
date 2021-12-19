from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import msvcrt
import re
import pandas as pd
import os

def appendDatanNewCategory(category,row,tipoCategory):
  new_data = []
  if tipoCategory == TC_porFecha: #Por Fecha
    new_data.append(category)
    new_data.append([row])
    porFecha.append(new_data)

    CategoryFecha.append(category) 

  elif tipoCategory == TC_porLesionados: #Por Lesionados
    new_data.append(category)
    new_data.append([row])
    porLesionados.append(new_data)

    CategoryLesionados.append(category) 

  elif tipoCategory == TC_porMuertos: #Por Muertes
    new_data.append(category)
    new_data.append([row])
    porMuertos.append(new_data)

    CategoryMuertos.append(category) 

  elif tipoCategory == TC_porTipoDeIncidente: #Por Tipo de Incidente
    new_data.append(category)
    new_data.append([row])
    porTipoDeIncidente.append(new_data)

    CategoryTipoDeIncidente.append(category)

  elif tipoCategory == TC_porCausas: #Por Causas
    new_data.append(category)
    new_data.append([row])
    porCausa.append(new_data)

    Categorycausa.append(category)


def appendData(index,row,tipoCategory):
  if tipoCategory == TC_porFecha: #Por Fecha
    porFecha[index][1].append(row)
  elif tipoCategory == TC_porLesionados: #Por Lesionados
    porLesionados[index][1].append(row)
  elif tipoCategory == TC_porMuertos: #Por Muertes
    porMuertos[index][1].append(row) 
  elif tipoCategory == TC_porTipoDeIncidente: #Por Tipo de Incidente
    porTipoDeIncidente[index][1].append(row)
  elif tipoCategory == TC_porCausas: #Por Causas
    porCausa[index][1].append(row)


if __name__ == "__main__":
    
    root = Tk() 
    root.geometry("200x200") 
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    
    arr_fn = root.filename.split('/')
    gv_path = ""
    for i in range(len(arr_fn)-1):
        gv_path = gv_path + arr_fn[i] + '/'
    
    
    data = pd.read_csv(root.filename,encoding='latin-1')
    
    root.destroy()
    
    #Estructuras con DF separados
    porFecha=[]
    porLesionados=[]
    porMuertos=[]
    porTipoDeIncidente=[]
    porCausa=[]
    
    #Arrays para guardar categorías 
    CategoryFecha=[]
    CategoryLesionados=[]
    CategoryMuertos=[]
    CategoryTipoDeIncidente=[]
    Categorycausa=[]
    
    #definir Tipo de categoría
    TC_porFecha = 1
    TC_porLesionados = 2
    TC_porMuertos = 3
    TC_porTipoDeIncidente = 4
    TC_porCausas = 5
    
    
    #Recorrido para separar información en varios dataframes
    for index, row in data.iterrows():
      anio = row['fecha'][6:]
      lesionados = 'SD' #SD=Sin Datos
      muertos = 'SD'  #SD=Sin Datos
    
      if str(row['lesionados']).isdigit():
        if row['lesionados'] > 0:
          lesionados = 'ConLesionados'
        else:
          lesionados = 'SinLesionados'
      
      if str(row['muertos']).isdigit():
        if row['muertos'] > 0:
          muertos = 'ConMuertos'
        else:
          muertos = 'SinMuertos'
    
      #inizializar estructuras base
      if index == 0:
        appendDatanNewCategory(anio,row,TC_porFecha)
        appendDatanNewCategory(lesionados,row,TC_porLesionados)
        appendDatanNewCategory(muertos,row,TC_porMuertos)
        appendDatanNewCategory(row['tipo_de_incidente'],row,TC_porTipoDeIncidente)
        appendDatanNewCategory(row['causa'],row,TC_porCausas)
        continue
    
      #Insert Por Fecha
      try:
        i = CategoryFecha.index(anio)
        appendData(i,row,TC_porFecha)
      except ValueError:
        appendDatanNewCategory(anio,row,TC_porFecha)
        i = -1
    
      #Insert Por Lesionados
      try:
        j = CategoryLesionados.index(lesionados)
        appendData(j,row,TC_porLesionados)
      except ValueError:
        appendDatanNewCategory(lesionados,row,TC_porLesionados)
        j = -1
    
      #Insert Por Muertos
      try:
        k = CategoryMuertos.index(muertos)
        appendData(k,row,TC_porMuertos)
      except ValueError:
        appendDatanNewCategory(muertos,row,TC_porMuertos)
        k = -1
    
      #Insert Por Tipo De Incidente
      try:
        l = CategoryTipoDeIncidente.index(row['tipo_de_incidente'])
        appendData(l,row,TC_porTipoDeIncidente)
      except ValueError:
        appendDatanNewCategory(row['tipo_de_incidente'],row,TC_porTipoDeIncidente)
        l = -1
    
      #Insert Por Causa
      try:
        m = Categorycausa.index(row['causa'])
        appendData(m,row,TC_porCausas)
      except ValueError:
        appendDatanNewCategory(row['causa'],row,TC_porCausas)
        m = -1
        
    #Generar Carpetas
    try:
      path = gv_path + 'Anio'
      os.mkdir(path)
    except OSError:
      print(f'La carpeta {path} ya existe')
    
    try:
      path = gv_path + 'Lesionados'
      os.mkdir(path)
    except OSError:
      print(f'La carpeta {path} ya existe')
    
    try:
      path = gv_path + 'Muertes'
      os.mkdir(path)
    except OSError:
      print(f'La carpeta {path} ya existe')
    
    try:
      path = gv_path + 'Tipo_de_incidente'
      os.mkdir(path)
    except OSError:
      print(f'La carpeta {path} ya existe')
    
    try:
      path = gv_path + 'Causas'
      os.mkdir(path)
    except OSError:
      print(f'La carpeta {path} ya existe')   
        
    #Descargar Archivos Por Fechas
    for index in range(len(CategoryFecha)):
      path = gv_path + '/Anio/' + CategoryFecha[index] + '.CSV'
      #print(path)
      df = pd.DataFrame(porFecha[index][1])
      df.to_csv(path)
    
    #Descargar Archivos Por Lesionados
    for index in range(len(CategoryLesionados)):
      path = gv_path + '/Lesionados/' + CategoryLesionados[index] + '.CSV'
      #print(path)
      df = pd.DataFrame(porLesionados[index][1])
      df.to_csv(path)
    
    #Descargar Archivos Por Muertes
    for index in range(len(CategoryMuertos)):
      path = gv_path + '/Muertes/' + CategoryMuertos[index] + '.CSV'
      #print(path)
      df = pd.DataFrame(porMuertos[index][1])
      df.to_csv(path)
    
    #Descargar Archivos Por Tipo de incidente
    for index in range(len(CategoryTipoDeIncidente)):
      path = gv_path + '/Tipo_de_incidente/' + str(CategoryTipoDeIncidente[index]).replace('/','_') + '.CSV'
      #print(path)
      df = pd.DataFrame(porTipoDeIncidente[index][1])
      df.to_csv(path)
    
    #Descargar Archivos Por Causa
    for index in range(len(Categorycausa)):
      path = gv_path + '/Causas/' + str(Categorycausa[index]).replace('/','_') + '.CSV'
      #print(path)
      df = pd.DataFrame(porCausa[index][1])
      df.to_csv(path)        
    
    print(f'Se generaron los archivos en la carpeta {gv_path}')
   
        