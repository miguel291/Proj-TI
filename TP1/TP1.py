# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import matplotlib.image as mpimg
import huffmancodec
import sys
import subprocess
import os

def histograma(f_name,amostra,alf): #----------//----------//---------- 
    leitura = dict.fromkeys(alf)
    
    #inicialização da leitura a 0s
    for i in range(len(alf)):
        leitura[alf[i]] = 0
     
    #Redução dos canais das fontes
    if f_name[-1] != 't': 
        if (amostra.ndim>2):
            amostra= amostra[:,:,0]
        tam = (amostra.size)
    #exceção para o texto (array simples) 
    else:
        tam = len(amostra)
     
    #verificação do match alfabeto-amostra (leitura propriamente dita)
    for i in leitura:
        count = np.count_nonzero(amostra == i)
        leitura[i] += count
    
    #colocação plot            
    for i in leitura:
        if f_name[-1] == 't':
            plt.bar(chr(i), leitura[i],color="blue",width=1) 
        else:
            plt.bar(i, leitura[i],color="blue",width=1)
     
    #cálculo entropia
    entropia(leitura, tam,1) 
    
    #cálculo nº médio bits (Huffman)
    codec = huffmancodec.HuffmanCodec.from_data(leitura) 
    symbols, lenghts = codec.get_code_len()
    num = 0
    count = 0
    e = 0    

    for i in leitura:
       num+=leitura[i]*lenghts[count]  
       e += leitura[i]*(lenghts[count]**2)
       count+=1
    
    var = e/tam-((num/tam)**2)   
    
    #plt.savefig('texto.png', dpi=199)
    print("Nº médio de bits por símbolo: "+str(num/tam)) #num/tam=nº medio
    print("Variância: "+str(var))

def entropia(leitura,tam,flag): #----------//----------//---------- 
    
    ent = 0

    for i in leitura:
        prob = leitura[i]/tam
        if (prob!= 0):
            ent += prob * np.log2(1/prob)
    if(flag==1):
        print("Entropia: " + str(ent))
    return ent
    
def agrupados(amostra,f_name): #----------//----------//---------- 
    
    #Redução dos canais das fontes e flatten
    if f_name[-1] != 't': 
        if (amostra.ndim>2):
            amostra = amostra[:,:,0]
        amostra = amostra.flatten()
    
    tam = len(amostra)  
    
    leitura={}
    for i in range(1,tam,2):
            tuplo=(amostra[i-1],amostra[i])
            if tuplo in leitura:
                 leitura[tuplo] += 1
            else:
                 leitura[tuplo] = 1
        
    ent = 0.
        
    prob = [float(c)/(tam/2) for c in leitura.values()]
    ent = sum(prob * np.log2(prob))
    print("Entropia (símbolos 2 a 2): " + str(-ent/2))
    

def contaOcorr(amostra, alf): #----------//----------//---------- 
    leitura = dict.fromkeys(alf)
    
    #inicialização da leitura a 0s
    for i in range(len(alf)):
        leitura[alf[i]] = 0
    
    for i in leitura:
        count = np.count_nonzero(amostra == i)
        leitura[i] += count   
     
    return leitura
    
def infoMa(query, target ,passo, alf): #----------//----------//---------- 
    infoM=[]
    
    #verificação do match query-alfabeto
    cont = contaOcorr (query, alf)
    
    #Cálculo da entropia da query
    Hquery=entropia(cont,len(query),0)
    for i in range (len(target)-len(query)+1): 
         jan = target[i:i+len(query)] #janela para comparação query-target    
         infoM.append(infoMutua(query,Hquery,alf,jan)) #Cálculo da informação mutua
    print("inforMutua: ",infoM)

def infoM6a(query, target ,passo, alf, flag, name, tab): #----------//----------//---------- 
    infoM=[]
    pas= int(passo)
    
    #verificação do match query-alfabeto
    cont = contaOcorr (query, alf)
    
    #Cálculo da entropia da query
    Hquery=entropia(cont,len(query),0)
    
    aux = int((int(len(target)-len(query))+1)/pas)+1
    
    #Cálculo da informação mutua
    for i in range (aux): 
        j = int((len(query)/4)*i)
        jan = target[j:j+len(query)] #janela para comparação query-target    
        infoM.append(infoMutua(query,Hquery,alf,jan))
    
    #ex 6b
    if (flag == 2):
        plt.figure(figsize=(9, 3))
        plt.xlabel("Janela")
        plt.ylabel("Informação mútua")
        plt.title(name)
        print("inforMutua: ",infoM)
        plt.plot(np.arange(aux), infoM,color="blue")
    
    #ex 6c
    if (flag == 3):
         print("inforMutua: ",infoM)
         max_value = np.max(infoM)
         print("Informação mútua máxima: ",max_value)
         
def infoMutua(query,hQuery,alfabeto,target):
    
    #verificação do match target-alfabeto
    contTarget = contaOcorr(target,alfabeto)
    
    #Cálculo da entropia do target
    hTarget=entropia(contTarget,len(target),0)

    #Cria um array com as dimensões do alfabeto
    conj = np.zeros(shape=(len(alfabeto),len(alfabeto)))
    
    #Encontra as combinações e incrementa as mesmas
    for i in range(len(query)):
        conj_x = alfabeto[query[i]-alfabeto[0]]
        conj_y = alfabeto[target[i]-alfabeto[0]]
        conj[conj_x-alfabeto[0],conj_y-alfabeto[0]] +=1
    
    #Retira os zeros
    conj = conj[conj!=0]
    #Cálculo da probabilidade 
    probConj = conj / len(query)
    
    #Cálculo da entropia do conj
    hConj= -(np.sum(probConj * np.log2(probConj)))
    
    return hQuery + hTarget - hConj #Cálculo da entropia conjunta

##############################################################################         

def main():
    # install needed modules
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scipy'])

    # change working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

   
    nomes1 = {"lena.bmp","ct1.bmp","binaria.bmp","saxriff.wav","texto.txt"}
    nomes2 = {"target01 - repeat.wav","target02 - repeatNoise.wav"}
    nomes3 = {"Song01.wav","Song02.wav","Song03.wav","Song04.wav","Song05.wav","Song06.wav","Song07.wav"}
   
    for f_name in nomes1: #----------//----------//----------
        f_name = os.getcwd() + "/data/" + f_name
        plt.figure(figsize=(9, 3))
        plt.xlabel("Valor")
        plt.ylabel("Frequencia")
        plt.title(f_name)
        print(f_name+" ----------//----------//----------")
    
        #ficheiros imagem ".bmp" ----------//----------//----------  
        if f_name[-1] == 'p':
            fich = mpimg.imread(f_name)
            histograma(f_name,fich,np.arange(256))
            agrupados(fich,f_name)
            
        #ficheiros som ".wav" ----------//----------//---------- 
        if f_name[-1] == 'v': 
            [fs, data] = wavfile.read(f_name)
            fich= data[:,0]
            histograma(f_name,fich,np.arange(100,150))
            agrupados(fich,f_name)
                
        #ficheiros texto ".txt" ----------//----------//---------- 
        if f_name[-1] == 't': 
            file = open(f_name,'r',encoding='utf-8',errors='ignore')
            fich=[]
                    
            #contrução array com os caracteres filtrados
            for line in file:
                for i in line:
                    if((i>=chr(65) and i<=chr(90)) or (i>=chr(97) and i<=chr(122))):
                        fich.append(ord(i))
                                
            file.close()           
            histograma(f_name,fich,np.arange(65,123))
            agrupados(fich,f_name)  
        print("")
    
    #ex6a ----------//----------//----------//----------//----------
    alfa=np.arange(0,11)
    query=[2,6,4,10,5,9,5,8,0,8]
    target = [6,8,9,7,2,4,9,9,4,9,1,4,8,0,1,2,2,6,3,2,0,7,4,9,5,4,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6]
    print("Exercício 6)a) ----------//----------//----------")
    infoMa(query,target,1,alfa)
    print("")
    
    #Nome do ficheiro usado como query
    [fa, dat] = wavfile.read(os.getcwd() + "/data/" + "saxriff.wav")
    dat= dat[:,0]
    alf=np.arange(0,255) 
    pas=round(len(dat)/4)
   
    #ex6b
    for f_name in nomes2: #----------//----------//---------- 
        f_name = os.getcwd() + "/data/" + f_name
        print(f_name+" ----------//----------//----------")
        [fs, data] = wavfile.read(f_name)
        if (data.ndim>1):
            fich= data[:,0]
        else:
            fich = data
        infoM6a(dat,fich,pas,alf , 2, f_name,0)
        print("")
    
    #ex6c
    for f_name in nomes3: #----------//----------//---------- 
        f_name = os.getcwd() + "/data/" + f_name
        print(f_name+" ----------//----------//----------")
        [fs, data] = wavfile.read(f_name)
        if (data.ndim>1):
            fich= data[:,0]
        else:
            fich = data
        infoM6a(dat,fich,pas,alf , 3, f_name, [])
        print("")

if __name__== "__main__" :
    main()