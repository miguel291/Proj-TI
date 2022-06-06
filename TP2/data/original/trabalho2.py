#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:20:47 2020

@author: miguelpedroso
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import hufman
import lzma
import bz2


def histograma(f_name,amostra,alf): #----------//----------//---------- 
    leitura = dict.fromkeys(alf)
    
    #inicialização da leitura a 0s
    for i in range(len(alf)):
        leitura[alf[i]] = 0
     
    
   
    #amostra = amostra[:,0]
    #verificação do match alfabeto-amostra (leitura propriamente dita)
    for i in leitura:
        count = np.count_nonzero(amostra == i)
        leitura[i] += count
    
    #colocação plot            
    for i in leitura:
        plt.bar(i, leitura[i],color="blue",width=1)
        plt.title(f_name)
        plt.ylabel("Número de pixeis")
    #cálculo entropia
    
    amostra =amostra.flatten()
    tam = len(amostra)
    entropia(leitura, tam,1) 
    
    #cálculo nº médio bits (Huffman)
    codec = hufman.HuffmanCodec.from_data(leitura) 
    symbols, lenghts = codec.get_code_len()
    num = 0
    count = 0
    e = 0    

    for i in leitura:
       num+=leitura[i]*lenghts[count]  
       e += leitura[i]*(lenghts[count]**2)
       count+=1
    
    
    
    #plt.savefig('texto.png', dpi=199)
    print("Nº médio de bits por símbolo: "+str(num/tam)) #num/tam=nº medio
    

def entropia(leitura,tam,flag): #----------//----------//---------- 
    
    ent = 0

    for i in leitura:
        prob = leitura[i]/tam
        if (prob!= 0):
            ent += prob * np.log2(1/prob)
    if(flag==1):
        print("Entropia: " + str(ent))
    return ent



def main():
    f_name = input("Nome do ficheiro: ")
    fich = mpimg.imread(f_name)
    #histograma(f_name,fich,np.arange(256))
    with open(f_name,"rb") as f:   
       a= f.read()
    
    #LZMA----------//----------//---------- ----------//----------//---------- 
    name1 = f_name.partition(".")[0] + ".xz"
    data_out=lzma.compress(a)
    with lzma.open(name1,"w") as f:
        f.write(data_out)
    data_back=lzma.decompress(data_out)
    print("Compressão LZMA")
    print("Tamanho do ficheiro original: " +str(len(a)/1000000)+ " MB")  
    print("Tamanho do ficheiro comprimido: " + str(len(data_out)/1000000) + " MB") 
    print("Tamanho do ficheiro descomprimido :" + str(len(data_back)/1000000)+ " MB")
    print()
    
    
    #BZIP2 ----------//----------//---------- ----------//----------//---------- 
    dat_out=bz2.compress(a)
    name2 = f_name.partition(".")[0] + ".bz2"
    with bz2.open(name2,"w") as f:
        f.write(dat_out)
    dat_back=bz2.decompress(dat_out)
    print("Compressão BZIP2")
    print("Tamanho do ficheiro original: " +str(len(a)/1000000)+ " MB")
    print("Tamanho do ficheiro comprimido: " + str(len(dat_out)/1000000) + " MB") 
    print("Tamanho do ficheiro descomprimido :" + str(len(dat_back)/1000000)+ " MB")
    
    

if __name__ == "__main__":
    main()