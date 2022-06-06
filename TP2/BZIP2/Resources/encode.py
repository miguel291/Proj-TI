#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Dec 14 20:31:44 2020
@author: thomasfresco
"""

import bz2
import itertools
import threading
import time
import sys
import os 
from pathlib import Path

#chamada para sair
def sair():
    print("\n  __________________________________________________________________")
    print(" |                                                                  |")
    print(" | Python Script por Diogo Cleto, Miguel Pedroso e Thomas Fresco.   |")
    print(" | Créditos biblioteca BZIP2: Nadeem Vawda (nadeem.vawda@gmail.com) |")
    print(" |__________________________________________________________________|")
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.exit()
   
#chamada depois de executar 1 conversão
def nova_conversão():
    i = 0 #contar vezes opção inválida
    
    while(True):
        time.sleep(0.2)
        opcao = input("\n  Deseja efetuar nova compressão? ")    
        opcao = opcao.lower()
        if opcao == "sim":
            main()
        elif opcao == "não" or opcao == "nao" or opcao == "sair":
            sair()
        else:
            print("  Opção inválida!")
            i+=1
            if i>=3:
                sair()
            time.sleep(1)

def main(): #------------------------------------------------------------------
    dir_path = os.path.dirname(os.path.realpath(__file__))
    done = False
    
    #função para a animação de loading
    def animate():
        for c in itertools.cycle(["■□□□□□□□□□","■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□", "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□", "■■■■■■■■□□", "■■■■■■■■■□", "■■■■■■■■■■"]):
            if done:
                break
            sys.stdout.write('\r  Processando ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r  CONCLUÍDO! ---------------------------")
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.2)
            
        #escrita do cabeçalho gráfico
        print("\n ---------------------------------------------------------------------------------------------------")
        print("| ██████  ███████ ██ ██████  ██████      ███████ ███    ██  ██████  ██████  ██████  ███████ ██████  |")
        print("| ██   ██    ███  ██ ██   ██      ██     ██      ████   ██ ██      ██    ██ ██   ██ ██      ██   ██ |")
        print("| ██████    ███   ██ ██████   █████      █████   ██ ██  ██ ██      ██    ██ ██   ██ █████   ██████  |")
        print("| ██   ██  ███    ██ ██      ██          ██      ██  ██ ██ ██      ██    ██ ██   ██ ██      ██   ██ |")
        print("| ██████  ███████ ██ ██      ███████     ███████ ██   ████  ██████  ██████  ██████  ███████ ██   ██ |")
        print(" ---------------------------------------------------------------------------------------------------")
        print(' -- Para sair, escreva "sair" ----------------------------------------------------------------------')
        
        #pedir nome do ficheiro
        f_name = input("\n  Nome do ficheiro: ")
        #registar diretorio de leitura
        read_dir = os.path.join(Path(dir_path).parent,"Original",f_name)
            
        #se for lido "sair"
        if f_name.lower() == "sair":
            sair()
             
        #leitura do ficheiro
        with open(read_dir,"rb") as f:   
            a = f.read()

        #registar diretorio de escrita
        nome = f_name.partition(".")[2]+"_"+f_name.partition(".")[0]+".bz2"
        write_dir_bz2 = os.path.join(Path(dir_path).parent,"Encoded",nome)
        
        #registar diretorio de escrita2
        write_dir = os.path.join(Path(dir_path).parent,"Decoded",f_name)
        
        #cabeçalho compressão
        print("\n  ______________________________________")
        print(" |                                      |")
        print(" |------------- COMPRESSÃO -------------|")
        print(" |______________________________________|\n")
        
        time.sleep(0.5)

        #executar animação loading
        t = threading.Thread(target=animate)
        t.start()
        
        #iniciar "cronómetro"
        start = time.time()
    
        #compressão propriamente dita
        dat_out=bz2.compress(a)
        with bz2.open(write_dir_bz2,"w") as f:
            f.write(dat_out)
        
        #parar "cronómetro"
        end = time.time()   
            
        #parar loading
        done = True
        time.sleep(1)
            
        #informação tamanho do ficheiro original e comprimido, bem como o tempo de compressão
        print("\n  ______________________________________")
        print(" |                                      |")
        print("   Tamanho Original: " +str(round(len(a)/1000000,2))+ " MB")
        print(" |______________________________________|")
        print(" |                                      |")
        print("   Tamanho Comprimido: " + str(round(len(dat_out)/1000000,2)) + " MB") 
        print(" |______________________________________|")
        print(" |                                      |")
        print("   Tempo Compressão: " + str(round(end-start,2)) + " s") 
        print(" |______________________________________|")
            
        time.sleep(0.5)
        
        #informação do local onde é escrito o ficheiro comprimido
        print("\n  Ficheiro comprimido (.bz2) guardado em " + write_dir_bz2)
        
        time.sleep(1.5)
        
         #reset loading
        done = False
        
        #cabeçalho compressão
        print("\n  ______________________________________")
        print(" |                                      |")
        print(" |------------ DESCOMPRESSÃO -----------|")
        print(" |______________________________________|\n")
        
        time.sleep(0.5)
        
        #executar animação loading
        t = threading.Thread(target=animate)
        t.start()
        
        #iniciar "cronómetro"
        start = time.time()
        
        #descompressão propriamente dita
        dat_back=bz2.decompress(dat_out)
        with open(write_dir,"wb") as f:
            f.write(dat_back)
            
        #parar "cronómetro"
        end = time.time()   
            
        #parar loading
        done = True  
        time.sleep(1)
            
        #informação tamanho do ficheiro descomprimido, bem como o tempo de compressão
        print("\n  ______________________________________")
        print(" |                                      |")
        print("   Tamanho Comprimido: " +str(round(len(dat_out)/1000000,2))+ " MB")
        print(" |______________________________________|")
        print(" |                                      |")
        print("   Tamanho Descomprimido: " + str(round(len(dat_back)/1000000,2)) + " MB") 
        print(" |______________________________________|")
        print(" |                                      |")
        print("   Tempo Descompressão: " + str(round(end-start,2)) + " s") 
        print(" |______________________________________|")
        
        time.sleep(0.5)
        
        #informação do local onde é escrito o ficheiro descomprimido
        print("\n  Ficheiro descomprimido (." + f_name.partition(".")[2] + ") guardado em " + write_dir)
        
        time.sleep(1.5)
        if len(a) == len(dat_back):
            print("\n  ______________________________________")
            print(" |                                      |")
            print(" |   Conversão realizada sem perdas!    |")
            print(" | (tam. original = tam. descomprimido) |")
            print(" |______________________________________|")
            time.sleep(2)

        #confirmar se o utilizador quer sair ou executar nova compressão
        nova_conversão() 
        
    #caso um ficheiro com o nome inserido não exista
    except Exception: 
        print("\n  ______________________________________")
        print(" |                                      |")
        print(" |  Ficheiro ou diretório não existe!   |") 
        print(" |______________________________________|")
        time.sleep(2)
        main()
        
if __name__ == "__main__":
    main()
