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
import csv
import json
import nltk
import math
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

n=stopwords.words("spanish")
n.append('n')
n.append('d')
n.append('y')
n.append('el')
n.append('n')
#import distance

dic=[["Desgarradoras","toxico","guerrilla","infrahumano","detenidas","detenidas","delito","fallecimientos","denuncian","riesgo","vulnerable","intensivas","nunca","asintomaticos","congenita","enfermedad","grave","fea",'Insuficiente', 'disminuidos', 'Matando', 'Rabieta', 'Despistado', 'indiferente', 'Ambivalente', 'Hostilidad', 'Hostil', 'Obnubilación', 'Desprestigio', 'suponen', 'Destrozar', 'Enfado', 'Desprecio', 'Humillado', 'alerta', 'Enfadar', 
 'Inquietud', 'Prepotencia', 'Desorientado', 'Falleció', 'Dolor', 'Envidia', 'Indiferencia', 'Irritado', 'Furioso', 'Asqueado', 'Inconformidad', 'Desasosiego', 'Estremecimiento', 'Desgracia', 'Hastío', 'Inestabilidad', 'Devaluado', 
 'Adicto', 'Adverso', 'Incomprensible', 'Resignado', 'Antagonista', 'Disforia', 'Enjuiciado', 'Incorrecto', 'Horrorizado', 'Abolir', 'Prepotente', 'Desconfiado', 'Fracasar', 'Incomprensión', 'Insatisfecho', 'Inconforme', 'Alarma ',
 'Censura', 'Impaciencia', 'Incompatibilidad', 'Desconsolado', 'Antimonopolista', 'Abrasivo', 'Desmotivado', 'Odio', 'Enajenar', 'Incompatible', 'Desconfianza', 'Fastidio', 'Desconsiderar', 'Agravar', 'Temo', 'Amputar', 'Fastidiar',
 'Desconfiar', 'Adulterar', 'Emboscada', 'Manipulación', 'Pesimismo', 'Injusto', 'Resignación', 'Anticuado', 'Abrupto', 'Obstinación', 'Incredulidad', 'Arto', 'Aborrecer', 'Estupor', 'Rencoroso', 'Espanto', 'Disgustado', 'fraudulenta',
 'Invasión', 'A distancia', 'Agresivo', 'Arta', 'Abandono', 'Advertir', 'Aterrorizado', 'asesino', 'Terror', 'Espantar', 'Engañar', 'Alienación', 'Muriendo', 'Desdicha', 'murieron', 'Lastimar', 'Melancolía', 'Abuso', 'Desconcertado', 
 'Desanimado', 'Extrañeza', 'Duelo', 'Abismo', 'Agravación', 'Advertencia', 'Apedrean', 'Insuficiencia', 'Deprimido', 'ocultando', 'Abominable', 'muriendo', 'Ira', 'Angustia', 'Desamparo', 'Ausente', 'Antagonismo', 'Anomalía', 'mato',
 'Terquedad', 'Irritación', 'Acusación', 'Odioso', 'Aniquilar', 'perseguidos', 'Agresor', 'Arrrogante', 'Desconsuelo', 'Resentido', 'Preocupante', 'Exasperar', 'Coartada', 'Nostálgico', 'Depresión', 'Agitación', 'Desprotección', 'Molestar',
 'Decepcionado', 'Desmotivación', 'Desencanto', 'Desesperar', 'Abdicar', 'Frustración', 'Sin objetivo', 'Odiar', 'Artarse', 'Abyecto', 'murio', 'Lástima', 'Enojo', 'Despreciado', 'Desesperado', 'Murió', 'Aniquilación', 'Anómalo', 'Traicionar',
 'Incongruencia', 'Inseguridad', 'Desesperación', 'apenado', 'Advierte', 'Exasperación', 'Melancolico', 'mamados', 'Traición', 'Enojado', 'Enemistarse', 'Fracasado', 'Horror', 'Cadaveres', 'Repudio', 'Mató', 'Muerto', 'Engañado', 'protestas', 
 'Mal', 'Decepcionar', 'Agresividad', 'destruyo', 'Rechazar', 'Paralizado', 'Incapacitar', 'Terco', 'Indignado', 'Envidiar', 'Deshonra', 'Persecución', 'Quejandose', 'Engaño', 'Molestia', 'Protesta', 'Infelicidad', 'Indiferente', 'Rechazado', 
 'Desproteger', 'Vil', 'Pánico', 'Irritar', 'Fiasco', 'Rebeldía', 'violencia', 'Lamentable', 'Arrogancia', 'Desorientación', 'Resignarse', 'Desolado', 'Anormal', 'Disminuir', 'denunciable', 'Venganza', 'Desdén', 'Mezquino', 'Desaliento', 'incumplir',
 'En contra', 'Estremecer', 'Pavor', 'Fastidiado', 'Obstinado', 'Nostalgia', 'Asustado', 'Menospreciar', 'Adulterio', 'Impaciente', 'Envidioso', 'Invasor', 'Afectación', 'Preocupado', 'Repudiar', 'Ambigüedad', 'Traicionado', 'Derrota', 'Desidia',
 'Animosidad', 'cuerpo', 'Estremecido', 'Anarquía', 'Agresión', 'Aflicción', 'Anarquista', 'Molestoso', 'Pena', 'Muertes', 'vagos', 'Furia', 'fallecidos', 'Injusticia', 'Adicción', 'Adversidad', 'Mezquindad', 'Desvalimiento', 'Frustrado', 'Resentimiento', 
 'Mordaz', 'Desilusión', 'Humillación', 'Manipular', 'Enjuiciamiento', 'Afligir', 'Preocupación', 'Fallecer', 'peor', 'Extraterrestre', 'Fobia', 'Espantado', 'Enfadado', 'Desdichado', 'Inseguro', 'Antisocial', 'Accidente', 'Huevada', 'Alarmante', 'Enfurecer',
 'Protestantes', 'Cólera', 'Humillar', 'Temor', 'Destruir', 'Inestable', 'Rechazo', 'Desgraciado', 'Desolación', 'Amonestación', 'muerte', 'carece', 'eufemismo', 'negligencia', 'Sumisión', 'presos', 'Resquemor', 'pandemia', 'Insatisfacción', 'Indignación', 
 'Desconsolar', 'Miedo', 'Agonizar', 'colmo', 'denuncian', 'Asco', 'Intolerante', 'Incredulo', 'Acuso', 'Sumiso', 'Agobiado', 'Ofender', 'Devaluación', 'Desventura', 'Enfermedad', 'Censurar', 'Disgustar', 'Agitador', 'Ambiguo', 'Impotencia', 'Agonía', 'Vergüenza',
 'Desconsiderado', 'Decepción', 'Desconsideración', 'Tension', 'Desconcierto', 'Desilusionado', 'Rebelde', 'Incapaz', 'Adulteración', 'Desgano', 'Antipatía', 'Pésimo', 'porfa', 'Discrepar', 'Miedoso', 'irregularidades', 'Alegación', 'Amonestar', 'Abandonar', 'Vergonzoso',
 'Pobre de mí', 'Fugarse', 'Rencor', 'Desánimo', 'Inferioridad', 'Intolerancia', 'Abordar', 'contra', 'Pesadumbre', 'Lastimado', 'Enojar', 'Adversario', 'Desprotegido', 'Incapacidad', 'infectada', 'Cadaver', 'Invadir', 'Desamor', 'paros', 'Rabia', 'Menosprecio', 'Exasperado',
 'Infeliz', 'Destrucción', 'escandalo', 'Disgusto', 'Agitar', 'Desprestigiado', 'Impotente', 'Acritud', 'Parálisis', 'Discordia', 'Deshonrado', 'Alegar', 'Rabioso', 'excusa', 'Cuidado', 'falleciendo', 'Perseguido', 'fallecido', 'Maldito', 'Derrotados', 'Cuidar', 'reapertura',
 'Altercado', 'Absurdo', 'mierda', 'Ausencia', 'Temer', 'Vengativo', 'Avergonzarse', 'Fracaso', 'emergencia', 'suspendio'],
          ["desarrollan","control","desconfinamiento","derecho","digno","prevenir","deseo","resueltas","sanacion","SALVANDO","recomendaciones","evitar","erradicado","sobresalido",'Afluencia', 'Eficiencia', 'Firmeza', 'Bonito', 'Grandeza', 'Cooperacion', 'Vivir', 'Barato', 'Absorbente', 'Destacar', 'Absorcion', 'Belleza', 'Util', 'Educacion', 'Increible', 'Afinidad', 'Familiarizar', 'Maravilloso', 'Bien', 'Divina', 'Delicia', 'Gusto', 'Beneficios', 'Ejemplar', 'Adjunto', 'Voluntad', 'Fresco', 'Aderente', 'Influencia', 'Admitir', 'Calificar', 'Estabilidad', 'Incondicional', 'Imparcial', 'Intencion', 'Conviccion', 'Ganancias', 'Dando', 'Diversidad', 'Conveniencia', 'Genial', 'Cordialidad', 'Cumplimiento', 'Posible', 'Ajuste', 'Diplomatica', 'Alabar', 'Indiscutible', 'Gratis', 'Esfuerzo', 'Totalmente', 'Agradecimiento', 'Informado', 'Conciso', 'Agradecer', 'Ganar', 'Excelente', 'Escuchar', 'Terapia', 'Hermoso', 'Tolerancia', 'consenso', 'Concideracion', 'Fuerte', 'Lograr', 'Sanar', 'Idealismo', 'Caridad', 'Recuperacion', 'acuerdo', 'Adaptable', 'Triunfo', 
 'Coherente', 'Inteligencia', 'Agradable', 'Descubrir', 'Placer', 'Parecido', 'Preciso', 'Bastante', 'Afabilidad', 'Igualdad', 'Exito', 'ganamos', 'Hacer', 'Adaptacion', 'Gratitud', 'Donacion', 'Felicidad', 'Suerte', 'Adaptabilidad', 'Temprano', 'Aceptar', 'Inclusion', 'Cautivar', 'Correcto', 'Amor', 'Animo', 'Caballerosidad', 'Tranquilidad', 'Realizar', 'Eficacia', 'Facilidad', 'Fascinado', 'Aceptable', 'Afectuoso', 'Responsabilidad', 'Limpieza', 'Competente', 'Transformar', 'Exactitud', 'Aventurero', 'Conocimiento', 'Ensenar', 'Adorno', 'Existir', 'Agilidad', 'Honestidad', 'Firme', 'Seguro', 'Crecimiento', 'Aprender', 'Realidad', 'Despreocupacion', 'Aumento', 'Impresionante', 'Identificar', 'Investigacion', 'Completo', 'Habil', 'Amable', 'Ventaja', 'Feliz', 'Inspiracion', 'Dinamica', 'Indudable', 'Emocionante', 'Confianza', 'Fortaleza', 'Curar', 'bienvenidos', 'Generar', 'vida',
 'Conocido', 'Amistad', 'Innovar', 'Cumplir', 'Acceder', 'Brillante', 'Extraordinario', 'Disponible', 'Incomparable', 'Ley', 'Bella', 'Gloria', 'Apoyo', 'Crear', 'Bueno', 'Avance', 'Sobreviviente', 'Equidad', 'Oportunidad', 'Considerado', 'Compartir', 'Disfrutado', 'Carisma', 'Bonos', 'Generosamente', 'Compasion', 'Decanso', 'Conciencia', 'Abundancia', 'Ganado', 'Interes', 'vitales', 'Dignidad', 'Afirmar', 'Bondad', 'Elogio', 'Celebrar', 'Logica', 'Liberacion', 'Emprendedor', 'Apasionado', 'Influyente', 'Fiel', 'Amigo', 'Salud', 'Superar', 'Compromiso', 'Gran', 'Familia', 'Colaboracion', 'Calidad', 'Resultados', 'milagrosa', 'Gratamente', 'Defender', 'Logro', 'Justicia', 'Creatividad', 'Cielo', 'Celebrada', 'Equilibrado', 'Intuitivo', 'Deseo', 'EnhoraBuena', 'Admirable', 'Habilidad', 'Vencer', 'Solidaridad', 'Inequivoco', 'Respaldar', 'Favorito', 'amor', 'Alegria', 'Amabilidad', 
 'Adesivo', 'Real', 'Dedicado', 'Decisivo', 'Animado', 'Adecuado', 'Coraje', 'Recomendacion', 'Reconocimiento', 'Devocion', 'Homenaje', 'Acumularse', 'Adulacion', 'Adoracion', 'juntos', 'Comunicacion', 'Solucion', 'Acomodar', 'Adorable', 'Facil', 'Remedio', 'Beneficiario', 'Lealtad', 'Defensor', 'Crecer', 'Capacidad', 'Alojamiento', 'Dichoso', 'Correctamente', 'Heroe', 'Justo', 'Satisfaccion', 'Estudioso', 'Acompañamiento', 'Edificar', 'Capaz', 'Bendicion', 'Recibir', 'Fabuloso', 'Valor', 'Apacible', 'Calma', 'Suficiente', 'Explicable', 'Benevolo', 'Hospitalario', 'Educado', 'Absolver', 'Disfrutar', 'Imaginacion', 'Gracias', 'Afecto', 'Constructivo', 'Educar', 'Exactamente', 'Factible', 'Certeza', 'enfrentar', 'Libertad', 'Grande', 'Aclamacion', 'Aderencia', 'Dulzura', 'Abundar', 'Agrado', 'Accesible', 'Desicion', 'Decencia', 'Creible', 'eticos', 'Eficaz', 'Logico', 'Competencia',
  'Honesto', 'Acuerdo', 'Entrada', 'Empatia', 'Acatar', 'Positivo', 'Comunidad', 'Acentuar', 'conformidad', 'Desinteres', 'Unidad', 'Esperanza', 'Cuidado', 'Futuro', 'Humilde', 'Respeto', 'Absolucion', 'Afable', 'Companero', 'Valido', 'Cariño',"cumpliendo", 'Cariñoso', 'Aliviar', 'Poder', 'Aconsejable', 'Afiliado' ]] 



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

def Escribir(datos): 
    with open("3tweets.csv","w",newline='')as myFile:
            writer = csv.writer(myFile,delimiter="\n")
            writer.writerow(datos)
            print("Documento Escrito \n")

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

def df(textos):
    matris=[]
    for i in range(0,len(textos)):
        for j in range(0,len(textos[i])):
            vect=[]
            #vect.append(textos[i][j])
            for con in range(len(textos)):
                if textos[con].count(textos[i][j]) >0:vect.append(math.log10( textos[con].count(textos[i][j]) )+1)
                else: vect.append(textos[con].count(textos[i][j]))
            matris.append(vect)
    return(matris)    


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
    for tweet in tweepy.Cursor(api.search,q="covid-19",geocode="-0.749907,-78.97,450km", tweet_mode="extended",lang="es").items(cantidad):
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
    vec=SimilConceno(normaVec((idf(df(data+dicci)))))
  
    response={}
    jp=1
    jn=0
    for i in range(len(t)):
    
        tw={'tweet':p[i],'jaccard':{'negativo':jack[jn],'pocitivo':jack[jp]},'Coceno':{'negativo':vec[i][len(vec[i])-2],'pocitivo':vec[i][len(vec[i])-1]}}
    
    
        response.setdefault(str(i),tw)
        jp=jp+2
        jn=jn+2
    
    return json.dumps(response)
  

if __name__ == '__main__':
    app.run()#ejecuta el servidor 5000


