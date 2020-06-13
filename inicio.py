# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:12:31 2020

@author: Mario
"""

#from tetodos import disJac,stimig,nlp,Tweet
from flask import Flask,render_template,request
import re
from unicodedata import normalize
import tweepy
import numpy as np
import json
import pandas as pd
import math
from sklearn import linear_model
from sklearn import model_selection
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob

n=stopwords.words("spanish")
n.append('n')
n.append('d')
n.append('y')
n.append('el')
n.append('n')
n.append("n\$")
n.append("a")
n.append("d")
n.append("y")
n.append("el")
n.append("rt")
n.append("t")
n.append("covid19")
n.append("covid*")
n.append("19")
n.append("co")
n.append("covid")
n.append("covid$*")
n.append("nhttps")
n.append("https")
#import distance

dic=[['Advierte', 'Abuso', 'Derrotados', 'Enemistarse', 'Estupor', 'Adicto', 'Desgracia', 'Alarmante', 'toxico', 'Decepcionar', 'Incorrecto', 'Inseguro', 'Incapacidad', 'Desilusión', 'Tension', 'fraudulenta', 'Desamparo', 'Destruir', 'Estremecimiento', 'Desidia', 'Arrrogante', 'Rabioso', 'Devaluación', 'Ausencia', 'Indiferente', 'Enfado', 'Resentido', 'Anticuado', 'Antisocial', 'Anarquía', 'Adicción', 'Pavor', 'Vengativo', 'Fracasar', 'Terror', 'Enfurecer', 'Horror', 'Antimonopolista', 'Desproteger', 'Insatisfacción', 'Terquedad', 'emergencia', 'Obnubilación', 'Obstinado', 'Antipatía', 'Manipular', 'Furioso', 'Impotencia', 'Rabia', 'Abyecto', 'Asustado', 'Amonestar', 'Parálisis', 'Persecución', 'Ambigüedad', 'Falleció', 'Enajenar', 'Disgustado', 'Desventura', 'Lamentable', 'detenidas', 'Rencor', 'Pesimismo', 'Inconforme', 'Abismo', 'Agitar', 'Deshonra', 'Desconcertado', 'Desgraciado', 'Engañar', 'Inestable', 'Pesadumbre', 'Afectación', 'Obstinación', 'Repudiar', 'Melancolía', 'Rechazado', 'Irritación', 'Miedoso', 'Incompatible', 'peor', 'Odioso', 'Aborrecer', 'protestas', 'Odio', 'fallecimientos', 'ocultando', 'Desconsolar', 'Lastimar', 'falleciendo', 'Coartada', 'Desconsolado', 'Lastimado', 'carece', 'Anormal', 'Devaluado', 'Asqueado', 'Exasperado', 'Enjuiciamiento', 'suponen', 'Artarse', 'Amputar', 'Aniquilar', 'Perseguido', 'congenita', 'Avergonzarse', 'Incredulo', 'Menospreciar', 'Censurar', 'Abrupto', 'Pobre de mí', 'Cólera', 'fallecidos', 'Desamor', 'Infeliz', 'Anarquista', 'vulnerable', 'Estremecido', 'pandemia', 'Insuficiente', 'Inestabilidad', 'Invasión', 'Discordia', 'muerte', 'Accidente', 'Disgustar', 'Adversidad', 'destruyo', 'Decepcionado', 'denuncian', 'Desorientado', 'fallecido', 'Incapacitar', 'Ambiguo', 'Destrozar', 'Desencanto', 'Fobia', 'irregularidades', 'Fiasco', 'muriendo', 'Censura', 'Impotente', 'Nostalgia', 'negligencia', 'Prepotencia', 'Desconfiado', 'Acuso', 'Abominable', 'murieron', 'Abrasivo', 'Desprecio', 'Agravación', 'Desanimado', 'asintomaticos', 'Deshonrado', 'Muriendo', 'Irritado', 'Lástima', 'Agresivo', 'Desaliento', 'Furia', 'Desconfiar', 'Melancolico', 'Rebelde', 'Hostilidad', 'mato', 'Mezquino', 'Pánico', 'A distancia', 'infrahumano', 'Enjuiciado', 'eufemismo', 'Infelicidad', 'Inconformidad', 'Traición', 'Aterrorizado', 'Venganza', 'Desprestigio', 'Incredulidad', 'Enojo', 'Deprimido', 'Injusticia', 'Abandono', 'Ira', 'Resentimiento', 'Angustia', 'Duelo', 'Sumiso', 'Vergüenza', 'Cadaver', 'Inseguridad', 'Agravar', 'Espantado', 'Fallecer', 'Terco', 'suspendio', 'Agonía', 'Decepción', 'Sumisión', 'Desdichado', 'Fracaso', 'paros', 'Ambivalente', 'Enfadado', 'Envidiar', 'Espanto', 'Desgarradoras', 'Rechazo', 'Adverso', 'Mal', 'Disminuir', 'Estremecer', 'Prepotente', 'Desmotivación', 'perseguidos', 'intensivas', 'Desconsuelo', 'Indignación', 'Engaño', 'Mordaz', 'Enfadar', 'Desdicha', 'Envidioso', 'Alegar', 'Frustración', 'Protesta', 'Huevada', 'Traicionado', 'Desconsiderado', 'apenado', 'Dolor', 'Desprotección', 'Desolado', 'Derrota', 'Resquemor', 'Murió', 'vagos', 'Impaciente', 'Disgusto', 'Molestar', 'excusa', 'escandalo', 'Desconsiderar', 'Fastidiar', 'Repudio', 'En contra', 'incumplir', 'Aniquilación', 'Preocupado', 'presos', 'Rechazar', 'indiferente', 'Rebeldía', 'Hastío', 'Humillado', 'Agresión', 'contra', 'Sin objetivo', 'Desánimo', 'Pésimo', 'Advertencia', 'Desdén', 'Temor', 'Hostil', 'Enfermedad', 'Fugarse', 'Alarma ', 'Cadaveres', 'Protestantes', 'Traicionar', 'Muertes', 'Acusación', 'Maldito', 'Insatisfecho', 'Impaciencia', 'Matando', 'Abandonar', 'Desesperar', 'Desconsideración', 'Muerto', 'Exasperación', 'Absurdo', 'Mató', 'Intolerancia', 'mierda', 'Irritar', 'Emboscada', 'Humillar', 'mamados', 'colmo', 'Temo', 'Frustrado', 'Afligir', 'Invadir', 'Manipulación', 'Disforia', 'Agonizar', 'riesgo', 'Antagonista', 'Altercado', 'Engañado', 'Incomprensible', 'infectada', 'fea', 'Abdicar', 'Despistado', 'murio', 'Amonestación', 'Agitación', 'violencia', 'Preocupación', 'Fastidio', 'Abolir', 'Antagonismo', 'Miedo', 'Cuidado', 'Fracasado', 'Odiar', 'Inquietud', 'Resignación', 'Rabieta', 'Arrogancia', 'Exasperar', 'Extraterrestre', 'Discrepar', 'Arto', 'Cuidar', 'Desesperado', 'Pena', 'Adulterio', 'reapertura', 'Alegación', 'Incongruencia', 'Temer', 'Horrorizado', 'Desesperación', 'Nostálgico', 'Desilusionado', 'Anomalía', 'Advertir', 'Desvalimiento', 'Animosidad', 'Desprotegido', 'Aflicción', 'Extrañeza', 'Agobiado', 'guerrilla', 'Vergonzoso', 'Acritud', 'denunciable', 'Destrucción', 'Ausente', 'Vil', 'Invasor', 'Espantar', 'Agresor', 'nunca', 'Desasosiego', 'Paralizado', 'Desolación', 'Humillación', 'asesino', 'Menosprecio', 'grave', 'enfermedad', 'alerta', 'Despreciado', 'Apedrean', 'Preocupante', 'Resignarse', 'Incompatibilidad', 'Adulteración', 'Quejandose', 'Desorientación', 'Agitador', 'Intolerante', 'Anómalo', 'Alienación', 'Desmotivado', 'Desprestigiado', 'Desgano', 'Fastidiado', 'delito', 'Resignado', 'Adversario', 'Asco', 'Agresividad', 'Abordar', 'Indignado', 'Injusto', 'Incapaz', 'Ofender', 'Rencoroso', 'disminuidos', 'Arta', 'Incomprensión', 'Desconcierto', 'Indiferencia', 'Envidia', 'Molestia', 'Enojado', 'Insuficiencia', 'Enojar', 'Desconfianza', 'Mezquindad', 'cuerpo', 'Inferioridad', 'Molestoso', 'Adulterar', 'Depresión', 'porfa'],
          ['Crecimiento', 'Adorable', 'Curar', 'Influencia', 'Gratitud', 'Cariñoso', 'Existir', 'Imaginacion', 'evitar', 'Gratamente', 'Conviccion', 'Afluencia', 'Hospitalario', 'Cielo', 'Agrado', 'Absorcion', 'Creatividad', 'amor', 'Temprano', 'Alegria', 'Interes', 'Unidad', 'Correcto', 'sobresalido', 'Facil', 'Ajuste', 'Adoracion', 'Defensor', 'Eficaz', 'Conciencia', 'Recomendacion', 'Facilidad', 'Satisfaccion', 'sanacion', 'Dichoso', 'Abundancia', 'Favorito', 'Bendicion', 'Correctamente', 'Cordialidad', 'Benevolo', 'EnhoraBuena', 'Equilibrado', 'Barato', 'Agradable', 'Completo', 'Agradecimiento', 'Aventurero', 'ganamos', 'Desicion', 'Amigo', 'derecho', 'Gran', 'Decencia', 'Emocionante', 'Habil', 'Caballerosidad', 'Considerado', 'Real', 'Adaptabilidad', 'Inspiracion', 'Investigacion', 'Recuperacion', 'Compasion', 'Ganar', 'Adorno', 'Alojamiento', 'Suficiente', 'Bondad', 'Apacible', 'Resultados', 'Crear', 'Respeto', 'desconfinamiento', 'Solucion', 'Absolucion', 'Preciso', 'resueltas', 'Igualdad', 'Devocion', 'Informado', 'Adecuado', 'enfrentar', 'Estabilidad', 'Amor', 'Transformar', 'Comunicacion', 'Accesible', 'Conocido', 'Disfrutar', 'eticos', 'Identificar', 'Afecto', 'Sanar', 'Util', 'Gusto', 'Humilde', 'Habilidad', 'Bonito', 'Homenaje', 'Decanso', 'Despreocupacion', 'Calidad', 'Agradecer', 'Adaptable', 'Afinidad', 'Inequivoco', 'Inteligencia', 'Vivir', 'Capacidad', 'Incomparable', 'Admitir', 'Divina', 'Equidad', 'Disfrutado', 'Admirable', 'Aumento', 'Afectuoso', 'Sobreviviente', 'Respaldar', 'Abundar', 'Heroe', 'Terapia', 'Bien', 'Influyente', 'Exactitud', 'Decisivo', 'Posible', 'juntos', 'Ejemplar', 'Oportunidad', 'digno', 'Positivo', 'Gracias', 'Conveniencia', 'Destacar', 'Salud', 'Caridad', 'Esfuerzo', 'Conocimiento', 'Adesivo', 'Bastante', 'Brillante', 'Fiel', 'Placer', 'Realidad', 'Maravilloso', 'prevenir', 'Gratis', 'Companero', 'Afirmar', 'Emprendedor', 'Acomodar', 'Grande', 'Acuerdo', 'Generar', 'Dando', 'desarrollan', 'Bella', 'Feliz', 'Aderente', 'Firme', 'control', 'Familia', 'Ganancias', 'Afabilidad', 'Cooperacion', 'Carisma', 'Acentuar', 'Idealismo', 'Dinamica', 'Desinteres', 'recomendaciones', 'Elogio', 'Capaz', 'Afiliado', 'Triunfo', 'Calma', 'Cariño', 'SALVANDO', 'Apoyo', 'Limpieza', 'Dignidad', 'Voluntad', 'Intuitivo', 'Adulacion', 'Superar', 'Animado', 'Fascinado', 'Intencion', 'vitales', 'Descubrir', 'Suerte', 'Libertad', 'Genial', 'Remedio', 'Adjunto', 'Educar', 'Aceptar', 'Cautivar', 'Aceptable', 'Responsabilidad', 'Delicia', 'Apasionado', 'Tolerancia', 'Valido', 'Acatar', 'Generosamente', 'Educacion', 'Hermoso', 'Edificar', 'Logro', 'Familiarizar', 'Deseo', 'Felicidad', 'Logico', 'Excelente', 'Avance', 'Seguro', 'Cumplir', 'Justo', 'Estudioso', 'consenso', 'Coherente', 'Amable', 'Aprender', 'Extraordinario', 'Factible', 'Lograr', 'Cuidado', 'Diplomatica', 'Acceder', 'Beneficios', 'Firmeza', 'Totalmente', 'Crecer', 'Parecido', 'Indiscutible', 'Exactamente', 'Confianza', 'Dulzura', 'Bonos', 'Increible', 'Amabilidad', 'Concideracion', 'Eficiencia', 'Gloria', 'Constructivo', 'Reconocimiento', 'Adaptacion', 'bienvenidos', 'Conciso', 'Diversidad', 'Hacer', 'Donacion', 'Afable', 'Absorbente', 'Educado', 'Fortaleza', 'Ganado', 'Liberacion', 'Honestidad', 'Acumularse', 'Imparcial', 'Aclamacion', 'Ventaja', 'cumpliendo', 'Disponible', 'Agilidad', 'Esperanza', 'Ensenar', 'Escuchar', 'Coraje', 'Explicable', 'Grandeza', 'Empatia', 'vida', 'Certeza', 'Alabar', 'Aderencia', 'Eficacia', 'conformidad', 'deseo', 'Bueno', 'Cumplimiento', 'Vencer', 'Futuro', 'Animo', 'Colaboracion', 'Solidaridad', 'Justicia', 'Amistad', 'Belleza', 'Absolver', 'Indudable', 'Creible', 'Celebrada', 'Competencia', 'Aliviar', 'Honesto', 'Lealtad', 'erradicado', 'Incondicional', 'Ley', 'Logica', 'Fresco', 'Realizar', 'Impresionante', 'Fabuloso', 'Poder', 'Celebrar', 'Beneficiario', 'Recibir', 'Competente', 'Calificar', 'Valor', 'Tranquilidad', 'Innovar', 'Fuerte', 'Dedicado', 'Aconsejable', 'acuerdo', 'Inclusion', 'milagrosa', 'Entrada', 'Defender', 'Exito', 'Acompañamiento', 'Comunidad', 'Compromiso', 'Compartir' ]] 


#import distance
twposi = pd.read_csv('twposi.csv',  sep=';',  comment='#').values
twnega = pd.read_csv('twnega.csv',  sep=';',  comment='#').values


# cadenas para la autenticacion
consumer_key = "bEEbhqust92eW4ClVdRx4YP2W"
consumer_secret = "8uk8s2AmvjzYzfblTLPMWs6ip3MLKFHttJfuc9QenYBQFhXoo0"
access_token = "1265021879854776320-a0CAaRozo8pPl7amUs3YNbujxjKOBQ"
access_token_secret = "ztRtOsaJ5h8Le7KafzxYPJu5WNDYTamXjF83qfeAenA58"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# con este objeto realizaremos todas las llamadas al API
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#esta funcion escribe un csv con los tweets



#metodo  similitud de coceno
def SimilConceno(x):
    matriz=[]
    for i in range(len(x)):
        vec=[]
        for j in range(len(x)):
            vec.append(round(np.sum(x[i]*x[j]),2))
        matriz.append(vec)
    
    return np.array(matriz)
#funcion normalizacion del vector     
def normaVec(x):
    for i in range(len(x)):
        denominador=math.sqrt(np.sum(x[i]**2))
        for j in range(len(x[i])):
            if(x[i][j]!=0):x[i][j]=x[i][j]/denominador
    return(x) 
    
def idf(matris):
    
    for i in range(len(matris)):
        for j in range( len(matris[i])):
            if(matris[i][j]!=0):matris[i][j]=math.log10(len(matris[i])/matris[i][j])
    return(np.array(np.transpose(matris)))

def bolsa(matriz):
    a=set(matriz[0])
    b=[]
    for i in range(1,len(matriz)):
        b=matriz[i]+b
    a=set(a)
    b=set(b)
    c=list(a.union(b))
    doc=[]
    bolsa=[]
    for i in range(len(c)):
        doc=[]
        #doc.append(c[i])
        
        for j in range(len(matriz)):
            
            doc.append(matriz[j].count(c[i]))
        bolsa.append(doc)
    return bolsa   

def df(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if(matriz[i][j]!=0):matriz[i][j]=math.log10( matriz[i][j] )+1
            else: matriz[i][j]=matriz[i][j]
    return matriz  


#esta funcion quita las //http: de los tweets
def remove_urls (vTEXT): 
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize( "NFD", json.dumps(vTEXT,ensure_ascii=False)) , 0, re.I)
    s=re.sub('[^A-Za-z0-9]+',' ',s)
    
    return(s) 





def nlp(pala):
    
    for i in range(0,len(pala)):
        for j in pala[i]:
           pala[i]=re.sub('[^A-Za-z]+',' ', j.lower()).split()
   
    for i in range(len(pala)):
        for j in pala[i]:
            if j in n:
                 
                pala[i].remove(j)
   
       
    return pala
def stimig(pala):
           
    for i in range(0,len(pala)):
        for j in range(0,len(pala[i])):
            pala[i][j]=(PorterStemmer().stem(pala[i][j].lower()))
    return(pala)




def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def disJac(twets,dic):
    
    final=[]
    for i in range(len(twets)):
        for j in range(len(dic)):
            if j==1:final.append(round(jaccard_similarity(twets[i],dic[j]),3))
            else:final.append(round(jaccard_similarity(twets[i],dic[j]),3))
            
    return final


def Tweet(cantidad):
    data=[]
    for tweet in tweepy.Cursor(api.search,q="covid-19",geocode="-0.749907,-78.97,450km", tweet_mode="extended",lang="es",since="2020-06-10", 
          until="2020-06-11", ).items(cantidad):
      dat=[]
      if hasattr(tweet,"retweeted_status"):
          try:
              s= remove_urls(tweet.retweeted_status.extended_tweet["full_text"])
             
              dat.append(s)
              data.append(dat)
               
          except AttributeError:
              s= remove_urls(tweet.retweeted_status.full_text)
              dat.append(s)
              data.append(dat)
              
      else:
        try:
          s= remove_urls(tweet.extended_tweet["full_text"])

          dat.append(s)
          data.append(dat)
          
        except AttributeError:  # Not a Retweet
          s=remove_urls(tweet.full_text)
          
          dat.append(s)
          data.append(dat)
    
       
    return data   

def pnl (p):
  p1=[]
  for i in p:
    p1.append(re.sub('[^A-Za-z]+',' ', i.lower()))
  return p1

#funcion tokenizacion stopwords
def deswo (p):
  for i in range(0,len(p)):
    p[i]=re.sub('[^A-Za-z0-9]+',' ',p[i].lower()).split()
    for k in p[i]:
      if k in n:
        p[i].remove(k)
  return p

##funcion Stimming##
def stiming(pala):
  for i in range(0,len(pala)):
    for j in range(0,len(pala[i])):
      pala[i][j]=(PorterStemmer().stem(pala[i][j]))
  return pala
variables = []
def Bolsa(matriz):
    a=set(matriz[0])
    b=[]
    for i in range(1,len(matriz)):
        b=matriz[i]+b
    a=set(a)
    b=set(b)
    c=list(a.union(b))
    doc=[]
    bolsa=[]
    for i in range(len(c)):
        doc=[]
        variables.append(c[i])
        
        for j in range(len(matriz)):
            
            doc.append(matriz[j].count(c[i]))
        bolsa.append(doc)
    return bolsa
##funcion prediccion
def txbolf(tweet):
    analysis = TextBlob(tweet)
    language = analysis.detect_language()
    a=analysis.translate(to='en')
    print(a.sentiment)
    if a.sentiment.polarity > 0:
        return("Positivo")
    elif a.sentiment.polarity == 0:
        return("neutral")
    else:
        return("negativo")    

########################################################################
dicci=stimig(dic)




app =Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html') 
@app.route('/ajax-data',methods=["POST"])
def ajdata():
    content = request.get_json(force=True)
      
    t=Tweet(content)
    p=[]
    for i in range(len(t)):
        p.append(t[i][0])
    data=stimig(nlp(t))
    jack=disJac(data, dicci)
    vec=SimilConceno(normaVec((idf(df(bolsa(data+dicci))))))
  
    response={}
    jp=1
    jn=0
    for i in range(len(t)):
        tx= txbolf(p[i])
        valorjac=""
        if(jack[jn]>jack[jp]):valorjac="Negativo"
        elif(jack[jn]<jack[jp]):valorjac="Positivo"
        else:valorjac="Neutro"
        valorcoce=""
        if(vec[i][len(vec[i])-2]>vec[i][len(vec[i])-1]):valorcoce="Negativo"
        elif(vec[i][len(vec[i])-2]<vec[i][len(vec[i])-1]):valorcoce="Positivo"
        else:valorcoce="Neutro"
            
        tw={'tweet':p[i],'textblob':tx,'jaccard':valorjac,'Coceno':valorcoce}
    
    
        response.setdefault(str(i),tw)
        jp=jp+2
        jn=jn+2
    
    return json.dumps(response)
 

    
@app.route('/ajax-regre',methods=["POST"])
def regre():
    def prediccion(dato,tw):
      p=model.predict(dato)
      pre=[p[0]]+tw
      return pre
    #EJECUCION
    
    ###################
    
    #dicci=stimig(dic)
    ctw=3
    tw=Tweet(1)
    
    #print(tw)
    #data=stimig(nlp(tw))
    
    dtw=[]
    for i in tw:
      dtw.append(stiming(deswo(pnl(i))))
    
    #print("\n Dis Jacckard \n")
    #disJac(data, dicci)
    #print("\n Dis Coceno \n")
    #vec=SimilConceno(normaVec((idf(df(bol)))))
    #print("\n Negativo: ",vec[1][1],"Pocitivo: \n",vec[1][2])
    ###################################
    #proceso de nlp tokenizacion stimming
    twp = stiming(deswo(pnl(twposi[:,0])))
    twn = stiming(deswo(pnl(twnega[:,0])))
    #Variables que contienen la calificacion de los documentos
    twpc = twposi[:,1]
    twnc = twnega[:,1]
    twc=[]
    for i in twpc:
      twc.append(i)
    twc.append(twpc[1])
    for i in twnc:
      twc.append(i)
    twc.append(twnc[1])
    
    #Bolsa de twitter´s, diccionario de palabras: positivas, negativas 
    btw1 = np.array(twp + [dic[0]] + twn + [dic[1]])
    
    btw2 = np.array(twp + [dic[0]] + twn + [dic[1]]+dtw[0])
    
    bol=Bolsa(btw2)
    #print(np.shape(bol))
    
    #pesado tf bolsa de tw
    tf=np.array(df(bol))
    
    
    #pesado idf bolsa de tw
    Idf=np.transpose(idf(bol))
    
    #print(np.shape(tf))
    #print(np.shape(idf))
    
    #tabla tf_idf
    tf_idf= np.transpose(np.array(tf * Idf))
    #print(np.shape(tf_idf))
    
    #print("##########tf#############")
    #for i in tf:
    #  print(i)
    #print("#############idf##########")
    #for i in idf:
    #  print(i)
    #print("#############tf-idf##########")
    
    #insertamos la calificacion de cada tw
    twpredecir= tf_idf[-1,:]
    #print(len(twpredecir))
    
    #Dataframe datos para la nueva consulta del algoritmo de clasificacion 
    X_new = pd.DataFrame([twpredecir],columns=variables)
    
    #Datos para ecrear el algoritmo de regresion 
    tf_idf=tf_idf[:-1,:]
    tf_idf = np.insert(tf_idf, tf_idf.shape[1], np.array(twc), 1)
    #for i in tf_idf:
    #  print(i)
    
    #ingresamos la etiqueta para la calificacion 
    variables.append('calificacion')
    
    #Creacion de dataframe con los datos del pesado tf-idf y la calicacion de cada documento 
    #con etiquetas de cada variable
    dataframe=pd.DataFrame(tf_idf,columns=variables)
    
    #imprecion dataframe
    #print(dataframe)
    
    #Ahora cargamos las variables de las 4 columnas de entrada en X excluyendo la columna «clase» con el método drop(). 
    #En cambio agregamos la columna «clase» en la variable y. Ejecutamos X.shape para comprobar la dimensión de nuestra matriz con datos
    X = np.array(dataframe.drop(['calificacion'],1))
    y = np.array(dataframe['calificacion'])
    X.shape
    
    #creamos nuestro modelo y hacemos que se ajuste (fit) a nuestro conjunto de entradas X y salidas ‘y’.
    model = linear_model.LogisticRegression()
    print("esto si vale")
    model.fit(X,y)
    
    #Una vez compilado nuestro modelo, le hacemos clasificar todo nuestro conjunto de entradas X utilizando el método «predict(X)» y 
    #revisamos algunas de sus salidas y vemos que coincide con las salidas reales de nuestro archivo
    predictions = model.predict(X)
    #print(predictions)
    
    #Y confirmamos cuan bueno fue nuestro modelo utilizando model.score() que nos devuelve la precisión media de las predicciones
    model.score(X,y)
    
    #Validación de nuestro modelo
    #subdividimos nuestros datos de entrada en forma aleatoria (mezclados) utilizando 80% de registros para entrenamiento y 20% para validar
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, y, test_size=validation_size, random_state=seed)
    
    #Volvemos a compilar nuestro modelo de Regresión Logística pero esta vez sólo con 80% de los datos de entrada y calculamos el nuevo scoring
    name='Logistic Regression'
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    #print(msg)
    
    # hacemos las predicciones -en realidad clasificación- utilizando nuestro «cross validation set», es decir del subconjunto que habíamos apartado.
    predictions = model.predict(X_validation)
    #print(accuracy_score(Y_validation, predictions))
    
    #la «matriz de confusión» donde muestra cuantos resultados equivocados tuvo de cada clase (los que no están en la diagonal)
    #print(confusion_matrix(Y_validation, predictions))
    
    #reporte de clasificación
    #print(classification_report(Y_validation, predictions))
    
    #Clasificación (o predicción) de nuevos valores
     ##funcion prediccion
    regre=prediccion(X_new,tw[0])
    
    tw={'tweet':regre[1],'regrecion':regre[0]}
    
    return(json.dumps(tw))
    
    


if __name__ == '__main__':
    app.run()#ejecuta el servidor 5000


