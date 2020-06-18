from sys import stdout,platform
from os import path,geteuid
from time import sleep
from subprocess import Popen, PIPE, STDOUT, run , check_output ,CalledProcessError
from collections import Counter
from re import *
from platform import *


 
class GeneralGui:

 def __init__(self,):
 
   #Renk Tanımlamalarını Yap.
   self.CRED  = '\33[31m' # Hata Test Renk Stili
   self.CEND  = '\33[0m' # Default Text Renk Stili.
   self.GREEN = '\033[0;32m' # Başarılı Text Renk Stili.
   self.CURL  = '\33[4m'  #  Alt Çizgili Dikkatli Renk Stili.

   
   
   self.system_required()
   self.progress_bar()
   self.usr_intput()
   self.main_progress()
   
   
 def system_required(self,):
  try:
     
    if geteuid() == 0:
       stdout.write(self.GREEN)
       print(' Sistem Gereksinimleri Kontrol Ediliyor\n')
       sleep(1)
       self.output = ''
       if linux_distribution()[0].lower()    == 'centos':      

         check_output( "systemctl status ufw",stderr=STDOUT,shell=True)
         self.output = 'centos'

       elif  linux_distribution()[0].lower() == 'centos linux':

         check_output( "systemctl status ufw",stderr=STDOUT,shell=True)
         self.output = 'centos linux'

       elif linux_distribution()[0].lower()  == 'red hat enterprise linux server':
          check_output( "systemctl status ufw",stderr=STDOUT,shell=True)
          self.output = 'red hat enterprise linux serve'
       else:
          print('Kullanmış Olduğunuz İşletim Sistemi :'+linux_distribution()[0]+' Desteklenmemektedir...\nÇıkış Yapılıyor...')
          exit()

    else:
        stdout.write(self.CRED)
        print('Fms Waf Root Yetkisi ile çalışmadıktadır lütfen root yetkisi ile çalıştırın. !/n')
        sleep(0.5)
        print('Çıkış yapılıyor...')
        sleep(0.5)
        exit()

  except CalledProcessError as exc:
          
           if self.output in 'centos' or 'centos linux' or 'red hat enterprise linux server':
            print(self.CRED,exc.output.decode("utf-8"))
            print(self.GREEN,"Ufw Firewall Yükleniyor...")
            sleep(1)
            ufw_install = run(['yum','install','ufw','-y'],stderr=stdout)          
            ufw_enabled = run(['systemctl','enable','ufw'],stderr=stdout)
            ufw_start   = run(['systemctl','start','ufw'],stderr=stdout)
            clear_scr   = run(['clear','-x'],stderr=stdout)
            stdout.write(self.GREEN)

    
   
 def usr_intput(self,domain=...,time=...,delay=...):
  try:
   while(True):
    
   
      stdout.write(self.GREEN)
      print('  ____            _       __          __    __  __      ____  ')         
      print(' |  _ \          (_)      \ \        / /   / _| \ \    / /_ | ')
      print(' | |_) | __ _ ___ _  ___   \ \  /\  / /_ _| |_   \ \  / / | | ')
      print(' |  _ < / _` / __| |/ __|   \ \/  \/ / _` |  _|   \ \/ /  | | ')
      print(' | |_) | (_| \__ \ | (__     \  /\  / (_| | |      \  /   | | ')
      print(' |____/ \__,_|___/_|\___|     \/  \/ \__,_|_|       \/    |_| ')  
      print('')   
      sleep(0.01)

      self.domain   = (str(input(" Lütfen Domain Adresi Giriniz : ")))
      self.pattern  = '^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$'
      self.path     = "/usr/local/apache/domlogs/"
      self.status   = {}
      self.http_path  = self.path+self.domain
      self.https_path = self.path+self.domain+'-ssl_log'
   
      if match(self.pattern,self.domain) and (path.exists(self.http_path)): 
        try:
          self.status = {
          '1':'Http',
          '2':'Https',
          }
          self.inp = input(' Lütfen Websitenizin ziyaret edilen protokolü Seçiniz Rakam İle;\n 1)Http  2)Https \n Seçiminiz: ')
          self.main_progress()
        except  :
          print(self.CRED,"\n Hatalı Değer Girildi.. Lütfen Tekrar Deneyiniz...")

      else:
        print(self.CRED,"Böyle bir alan adı yok veya yanlış domain sytax girildi...")

  except KeyboardInterrupt:
          print(self.CRED,"CTRL + C ile Çıkış Yapıldı...")
          stdout.write(self.CEND)
          exit()
         
  except EOFError:
          print(self.CRED,"CTRL + D ile Çıkış Yapıldı...")
          stdout.write(self.CEND)
          exit()



#**********  *********  *********  *********  *********  *********  *********  *********  *********          
 def progress_bar(self):
    for self.i in range(100+1):
      sleep(0.01)
      stdout.write(('#'*self.i)+(''*(100-self.i))+("\r [%d"%self.i+"%]"+("Tamamlandı:")))
      stdout.flush()
    print('\n')
#**********  *********  *********  *********  *********  *********  *********  *********  *********    

 
  
 def main_progress(self):
   while(True):
    mylist = list()
    if self.status.get(self.inp).lower() in 'http':
      deneme = Popen (['tail','-f',self.http_path], universal_newlines=True, stdout=PIPE)
      cnc = Counter()
      for line in deneme.stdout:    
        line =  line[::1]
        print(self.GREEN,line)
        seperated = line.split() 
        seperated.append(line)  
        mylist = list()
        mylist.append(seperated[0])
        sleep(1)
        for i in mylist:
          i=(str(i))
          cnc[i] += 1            
          if (int(cnc[i])) > 5:           
              print(self.CRED,i,"- - İp adresi Engellenmiştir..")       
              engelle = run(['sudo','ufw','deny','from',i], check=False,stdout=PIPE)
              print('')
    else:
      deneme = Popen (['tail','-f',self.https_path], universal_newlines=True, stdout=PIPE)
      cnc = Counter()
      for line in deneme.stdout:    
        line =  line[::1]
        print(self.GREEN,line)
        seperated = line.split() 
        seperated.append(line)  
        mylist = list()
        mylist.append(seperated[0])
        sleep(1)
        for i in mylist:
          i=(str(i))
          cnc[i] += 1            
          if (int(cnc[i])) > 5:           
              print(self.CRED,i,"- - İp adresi Engellenmiştir..")       
              engelle = run(['sudo','ufw','deny','from',i], check=False,stdout=PIPE)
              print('')

    

          
 

if __name__ == "__main__":
 self.general = GeneralGui() # Main Class Çağır.
 self.general.usr_intput() # User Fonksiyonlarını Çağır.
 self.general.progress_bar()
 self.general.main_progress()
