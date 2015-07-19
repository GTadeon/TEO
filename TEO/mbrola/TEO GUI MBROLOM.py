# -*- coding: cp1250 -*-
#terapija euthyroxom tj TEO skraceno-KORISTECI MBROLU!
#sadrzaj baze azuriram na temelju podataka formulara (novi korisnici) ili na temelju vec postojecih podatka iz baze (stari korisnici)
import sqlite3
from Tkinter import*
import re
import datetime
import tkMessageBox 
import winsound
import os

global ulaz,brojac_tableta
brojac_tableta=100
ulaz=0


#--------------------------------------------------funkcije:----------------------------------------------------------
def POSTAVI_IZBORNIK(): 
        def info(): #info o programu
            tkMessageBox.showinfo(title="Help->TEO info ", message="info: TEO je program namjenjen svim oboljelima od hipo/hipertireoze, te onima koji uzimaju Euthyrox iz nekih drugih razloga.(npr. pacijenti kojima je izvadena stitnjaca),koji nemaju vremena gledati dane na kalendaru\n\nGUI+algoritmi+baza+glasovne snimke: Ivan Grobenski\n\nkontakt: ivgroben@ffzg.hr\n")
            return
    
        moj_meni=Menu(root)
        
        #help izbornik
        help_izbornik=Menu(moj_meni,tearoff=0)
        help_izbornik.add_command(label="TEO info",command=info)
        moj_meni.add_cascade(label="Help",menu=help_izbornik)  
        root.config(menu=moj_meni)
        return
    
def REGISTRACIJA_KORISNIKA():
    global brojac_tableta,ulaz #resetiramo vrijednosti->sve ispocetka za novog korisnika!
    brojac_tableta=100
    ulaz=0
        
    kanvas=Canvas(root,width=1300,height=600,bg="#F0F0F0").place(x="0",y="0")#prekriva prosli gumb promjeni_pacijenta 
    try:kanvas.destroy() #kada dode do stvaranja novog korinika! :)
    except:tkMessageBox.showwarning(title="Registracijski formular", message="formular ispunjavaju svi novi korisnici/pacijenti.")

           
    IspuniFormular=Label(root,text="Nemam vas u bazi pacijenata. Molim vas ispunite ovaj registracijski formular: ",font=("Helvetica",12),pady=5,padx=320,fg="white",bg="black").place(x="0",y="0")
    ime=Label(root,text="Unesite svoje ime: ").place(x="10",y="40") 
    kontrola=Label(root,text="Datum posljednjeg kontrolnog pregleda (dd.mm.gggg):").place(x="10",y="70")
    rok=Label(root,text="Rok trajanja vasih novih Euthyrox tableta (dd.mm.gggg):").place(x="10",y="100")

    global ime_pacijenta,datum_pregleda,ROK_trajanja
    ime_pacijenta=StringVar()
    datum_pregleda=StringVar()
    ROK_trajanja=StringVar()
        
    entry_ime=Entry(root,textvariable=ime_pacijenta).place(x="400",y="40")
    entry_datum=Entry(root,textvariable=datum_pregleda).place(x="400",y="70")
    entry_rok=Entry(root,textvariable=ROK_trajanja).place(x="400",y="100")


    def DropMenu(): 
        global dani
        dani=["ponedeljak","utorak","srijeda","cetvrtak","petak","subota","nedelja"]
        x_k=10
        terapija=Label(root,text="Unesite koliko miligrama (te koliko tableta) Euthyroxa koji dan pijete. Ovu informaciju ste dobili od vaseg endokrinologa na zadnjoj kontroli.",fg="white",bg="black",padx=300,pady=5).place(x="0",y="140") #isto pustit preko ikonice zvucnika hahha :)
        for dan in dani:
            Dan=Label(root,text=dan,font=("Helvetica",12),fg="white",bg="black").place(x=x_k,y="180")
            x_k+=185 #odmak za 185

        #drop menu:
        global pon1,pon2,uto1,uto2,sri1,sri2,cet1,cet2,pet1,pet2,sub1,sub2,ned1,ned2
        pon1=StringVar()
        pon2=StringVar()
        pon1.set("25mg") #po defaultu
        pon2.set("2.tableta?")

        uto1=StringVar()
        uto2=StringVar()
        uto1.set("25mg") #po defaultu
        uto2.set("2.tableta?")

        sri1=StringVar()
        sri2=StringVar()
        sri1.set("25mg") #po defaultu
        sri2.set("2.tableta?")

        cet1=StringVar()
        cet2=StringVar()
        cet1.set("25mg") #po defaultu
        cet2.set("2.tableta?")

        pet1=StringVar()
        pet2=StringVar()
        pet1.set("25mg") #po defaultu
        pet2.set("2.tableta?")

        sub1=StringVar()
        sub2=StringVar()
        sub1.set("25mg") #po defaultu
        sub2.set("2.tableta?")

        ned1=StringVar()
        ned2=StringVar()
        ned1.set("25mg") #po defaultu
        ned2.set("2.tableta?")

        tableta1=OptionMenu(root,pon1,"25mg","50mg","100mg","200mg").place(x="10",y="210")
        tableta2=OptionMenu(root,pon2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="10",y="250")
        
        tableta1=OptionMenu(root,uto1,"25mg","50mg","100mg","200mg").place(x="195",y="210")
        tableta2=OptionMenu(root,uto2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="195",y="250")

        tableta1=OptionMenu(root,sri1,"25mg","50mg","100mg","200mg").place(x="380",y="210")
        tableta2=OptionMenu(root,sri2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="380",y="250")

        tableta1=OptionMenu(root,cet1,"25mg","50mg","100mg","200mg").place(x="565",y="210")
        tableta2=OptionMenu(root,cet2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="565",y="250")

        tableta1=OptionMenu(root,pet1,"25mg","50mg","100mg","200mg").place(x="750",y="210")
        tableta2=OptionMenu(root,pet2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="750",y="250")

        tableta1=OptionMenu(root,sub1,"25mg","50mg","100mg","200mg").place(x="935",y="210")
        tableta2=OptionMenu(root,sub2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="935",y="250")

        tableta1=OptionMenu(root,ned1,"25mg","50mg","100mg","200mg").place(x="1120",y="210")
        tableta2=OptionMenu(root,ned2,"ne uzimam drugu","25mg","50mg","100mg","200mg").place(x="1120",y="250")


        def provjera():
            odgovor=tkMessageBox.askquestion("Provjera","Jete li sigurni da zelite podatke iz formulara unjeti u bazu?")
            if odgovor=="yes":
                #global korisnik
                korisnik="novi korisnik"
                POZOVI_TEA(korisnik) #zove drugi dio programa,tj onaj najbitnj s bazom i snimaka ako kaze da se unesu
            else:pass
            return
        unesi_TEO=Button(root,command=provjera,text="Unesi u bazu!").place(x="580",y="400") #jeste li sigurni da zelite...bla bla
        return

    
    #-----pozivanje funkcija funkcije REGISTRACIJA_KORISNIKA:-----
    DropMenu()
   





#--------------------Najbitnija funkcija programa->rad sa snimkama+baza+algoritmi; -------------------------
    
def POZOVI_TEA(korisnik):
    def sakri_formular_kanvasom():
        #dodajem prazan kanvas preko onog proslog formulara
        global kanvas,dani,brojac_tableta, ime_pacijenta,datum_pregleda,ROK_trajanja
        kanvas=Canvas(root,width=1400,height=600,bg="#F0F0F0")
        kanvas.place(x="0",y="0")

        dani=["ponedeljak","utorak","srijeda","cetvrtak","petak","subota","nedelja"] 
        
        
        if korisnik=="novi korisnik": #dohvaca podatke iz forme samo putem globalnih varijabli, nema veze s bazom!
            kanvas_ime=kanvas.create_text(120,20)
            kanvas.itemconfig(kanvas_ime,text=("Ime pacijenta: "+ime_pacijenta.get()))
            kanvas_dani=kanvas.create_text(90,50)
            kanvas.itemconfig(kanvas_dani,text=("Danas je: "+dani[datetime.datetime.today().weekday()]))
            
        
        if korisnik=="stari korisnik":#ime pacijenta cupam iz baze onda u tom slucaju:
            
            conn=sqlite3.connect("TEO.db")
            c=conn.cursor()
            sql="SELECT Ime FROM Pacijent"

            kanvas_ime=kanvas.create_text(90,20)
            for sadrzaj in c.execute(sql):
                ime=sadrzaj[0] #vraca unicode, a ne str!
                
            kanvas.itemconfig(kanvas_ime,text=("Ime pacijenta: "+ime))
            kanvas_dani=kanvas.create_text(90,50)
            kanvas.itemconfig(kanvas_dani,text=("Danas je: "+dani[datetime.datetime.today().weekday()]))
        
        return
    
    #ubacivanje u bazu TEO.db svih unesenih podataka iz forme,koje cemo ustvari onda vuci iz baze!!:
    def TEO_BAZA(korisnik):
        
        conn=sqlite3.connect("TEO.db")
        c=conn.cursor()

        """ #ovo pozivam samo jednom!;
        def kreirajTABLICE():
            c.execute("CREATE TABLE Pacijent(ID INT, Ime TEXT,DatumPregleda TEXT,PravoKoristenja TEXT,DatumZadnjegPristupa TEXT)")
            c.execute("CREATE TABLE Terapija(ID INT,PON1 TEXT,PON2 TEXT,UTO1 TEXT,UTO2 TEXT,SRI1 TEXT,SRI2 TEXT,CET1 TEXT,CET2 TEXT,PET1 TEXT,PET2 TEXT,SUB1 TEXT,SUB2 TEXT,NED1 TEXT,NED2 TEXT)")
            c.execute("CREATE TABLE Tablete (ID INT,PreostaleTablete INT,RokTrajanja TEXT)")
            
            return
        kreirajTABLICE()
        """
        
        def UnosPodatakaForme(): #INICIJALNO POSTAVLJANJE BAZE-> OVO JE ZA SVE KOJI PRVI PUT PRISTUPAJU PROGRAMU!(nove korisnike)
            global ime_pacijenta,datum_pregleda,ROK_trajanja
            global pon1,pon2,uto1,uto2,sri1,sri2,cet1,cet2,pet1,pet2,sub1,sub2,ned1,ned2
            global brojac_tableta

            global ID,Ime,DatumPregleda,PON1,PON2,UTO1,UTO2,SRI1,SRI2,CET1,CET2,PET1,PET2,SUB1,SUB2,NED1,NED2,PreostaleTablete,RokTrajanja

            #-----------VARIJABLE ZA BAZU-OVO VRIJEDI SAMO ZA PRVO KORISTENJE,inace citamo iz baze:
            ID=1 #s obzirom da imam samo jedan redak svugdje
            #dohvat spremljenih vrijednosti IZ FORME:
            Ime=ime_pacijenta.get()
            DatumPregleda=datum_pregleda.get()
            PON1=pon1.get()
            PON2=pon2.get()
            UTO1=uto1.get()
            UTO2=uto2.get()
            SRI1=sri1.get()
            SRI2=sri2.get()
            CET1=cet1.get()
            CET2=cet2.get()
            PET1=pet1.get()
            PET2=pet2.get()
            SUB1=sub1.get()
            SUB2=sub2.get()
            NED1=ned1.get()
            NED2=ned2.get()
            PreostaleTablete=brojac_tableta #Jedini podatak koji se stalno mijenja u bazi kod jednog pacijenta...
            RokTrajanja=ROK_trajanja.get()
            PravoKoristenja="True" #true je samo za koristenje jednom dnevno,cim se iskoristi odma je false,a resetira se novim  danom
            DatumZadnjegPristupa=str(datetime.datetime.now().day-1)+"."+str(datetime.datetime.now().month)+"."+str(datetime.datetime.now().year)

            #reset baze-> tj brisem stare podatke ako postoje slucajno:
            c.execute("DELETE FROM Pacijent")
            c.execute("DELETE FROM Terapija;")
            c.execute("DELETE FROM Tablete;")
            #---brisanje zavrseno----

            #unos podataka forme u bazu :
            c.execute("INSERT INTO Pacijent(ID,Ime,DatumPregleda,PravoKoristenja,DatumZadnjegPristupa) VALUES(?,?,?,?,?)",(ID,Ime,DatumPregleda,PravoKoristenja,DatumZadnjegPristupa))
            c.execute("INSERT INTO Terapija(ID,PON1,PON2,UTO1,UTO2,SRI1,SRI2,CET1,CET2,PET1,PET2,SUB1,SUB2,NED1,NED2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(ID,PON1,PON2,UTO1,UTO2,SRI1,SRI2,CET1,CET2,PET1,PET2,SUB1,SUB2,NED1,NED2))
            c.execute("INSERT INTO Tablete(ID,PreostaleTablete,RokTrajanja) VALUES(?,?,?)",(ID,PreostaleTablete,RokTrajanja))
            
            conn.commit()#Konfirmacija za unos promjenjenih podataka u bazu
        
            return
                
        #samo novi korisnici ispunjavaju taj formular,stari se oslanjaju na bazu ...
        if korisnik=="novi korisnik":
            UnosPodatakaForme()
      
        return
    
    def saznaj_dozu(): #klikom na taj gumb pacijent slusa snimke temeljene na info iz formulara (novi k.) ili baze (stari k)
        global korisnik
        
        def ProcitajDozuNaTemeljuFormulara():
            global ulaz,brojac_tableta,ROK_trajanja #poziv globalnih var koje sam koristio za podatke formulara
            ulaz+=1 # samo ova i dolje funkcija imau ovu liniju ,provjera pristupa se ionako vrsi kroz bazu u donjoj
            def pravoNaTerapiju_FORMULAR():
                rj_jesam_li_pio={datetime.datetime.now():ulaz} #tj. ako je na danasnji dan  pokrenuto vise od jednom,nisam danas pio postaje false
                if rj_jesam_li_pio[datetime.datetime.now()]>1:
                    nisam_danas_pio=False
                else:nisam_danas_pio=True
                return nisam_danas_pio
            pravoNaTerapiju_FORMULAR()

            def rokTrajanjaTableta_FORMULAR():
                rok_trajanja=ROK_trajanja.get().split(".")
                sadasnji_dan=datetime.datetime.now().day #npr 4
                trenutni_mjesec=datetime.datetime.now().month #npr 8
                trenutna_godina=datetime.datetime.now().year #npr 2015

                #ako je rok prosao,ili ako je jednak danasnjem datumu: 
                if datetime.date(int(rok_trajanja[2]),int(rok_trajanja[1]),int(rok_trajanja[0]))<=datetime.date(trenutna_godina,trenutni_mjesec,sadasnji_dan):
                    rok_trajanja=False #lista postaje booleansada, znaci da je istekao rok trajanja!
                else: rok_trajanja=True
                
                return rok_trajanja
            rokTrajanjaTableta_FORMULAR()


            #tekst za mbrolu koji pretvaramo u znakove i dodjeljujemo trajanje prema pravilu iz rjecnika:
            tekst_dani={0:"danas je ponedjeljak.",1:"danas je utorak.",2:"danas je srijeda.",3:"danas je cetvrtak.",4:"danas je petak.",5:"danas je subota.",6:"danas je nedelja."}

            
            danasnji_dan=datetime.datetime.today().weekday() #npr2 za srijedu...
            

            
            #-----------------POTREBNI UVJETI ZA CITANJE PODATAKA na temelju formulara:-----------------
            if brojac_tableta<=0:
                
                
                poredani_tekstovi=[teskt_dani[danasnji_dan]," nemate vise tableta."]
                    #-----------citanje tekstova umetnutih u listu-> generiranje .wav fajla: -------------
                    
                          # đ -> W
                          # dž -> X
                          # ć -> Y
                          # č -> Q
                          # lj -> L
                          # nj -> N
                        
                glasovi = {
                          "a": "a 61",
                          "b": "b 65",
                          "c": "ts 113",
                          "Q": "tS 90",
                          "Y": "tS' 98",
                          "d": "d 54",
                          "X": "dZ 56",
                          "W": "dZ' 61",
                          "e": "e 53",
                          "f": "f 86",
                          "g": "g 56",
                          "h": "x 68",
                          "i":  "i 49",
                          "j":  "j 53",
                          "k":  "k 81",
                          "l":  "l 35",
                          "L": "L 59",
                          "m":  "m 56",
                          "n":  "n 45",
                          "N": "J 60",
                          "o":  "o 54",
                          "p":  "p 85",
                          "r":  "r 25",
                          "s":  "s 91",
                          "S":  "S 99",
                          "t":  "t 76",
                          "u":  "u 50",
                          "v":  "v 40",
                          "z": "z 68",
                          "Z": "Z 74",
                          ".": "_ 200",
                          " ": "_ 100" }
                          # T -> razmak
                          # đ -> W
                          # dž -> X
                          # ć -> Y
                          # č -> Q
                          # lj -> L
                          # nj -> N
                          # š -> S
                          # ž -> Z
                fajl=open("ProcitajTerapiju.txt","w")
                for element in poredani_tekstovi:
                    for znak in element:
                        znak=glasovi[znak]+"\n" #Mora bit u novom redu za mbrolu...
                        fajl.write(znak.encode("utf8"))
                fajl.close()
                        
                os.system("mbrola cr1 ProcitajTerapiju.txt ProcitajTerapiju.wav")
                winsound.PlaySound("ProcitajTerapiju.wav",winsound.SND_ALIAS)

            else:
                if rok_trajanja==True and nisam_danas_pio==True:
                    conn=sqlite3.connect("TEO.db")
                    c=conn.cursor()
                    for sadrzaj in c.execute("SELECT PON1,UTO1,SRI1,CET1,PET1,SUB1,NED1 FROM Terapija"):
                        doze_tuple_1=sadrzaj #TABLETE 1 za pon-ned

                    for sadrzaj in c.execute("SELECT PON2,UTO2,SRI2,CET2,PET2,SUB2,NED2 FROM Terapija"):
                        doze_tuple_2=sadrzaj #TABLETE 2 za pon-ned

                    RJ_DOZE_1={'25mg':"uzmite jednu od dvadesetipet.",'50mg':"uzmite jednu od pedeset.",'100mg':"uzmite jednu od sto.",'200mg':"uzmite jednu od dvjesto."}
                    RJ_DOZE_2={'25mg':"i jednu od dvadesetpet.",'50mg':"i jednu od pedeset.",'100mg':"i jednu od sto.",'200mg':"i jednu od dvjesto.",'2.tableta?':' ',"ne uzimam drugu":' '}#ZA 2. TABLETU


                    DOZA1=RJ_DOZE_1[doze_tuple_1[danasnji_dan]] 
                    DOZA2=RJ_DOZE_2[doze_tuple_2[danasnji_dan]]
                    
                    poredani_tekstovi=[tekst_dani[danasnji_dan],DOZA1,DOZA2] 

                    conn.commit()
                    
                elif rok_trajanja==False and nisam_danas_pio==True:
                    poredani_tekstovi=[teskt_dani[danasnji_dan],"rok trajanja tableta je istekao. posjetite najbliZu ljekarnu."]

                elif nisam_danas_pio==False:
                    poredani_tekstovi=[teskt_dani[danasnji_dan],"danas ste veY uzeli svoju dozu. pripazite."]
                    
            #-----------citanje tekstova umetnutih u listu-> generiranje .wav fajla: -------------
                
                      # đ -> W
                      # dž -> X
                      # ć -> Y
                      # č -> Q
                      # lj -> L
                      # nj -> N
                    
            glasovi = {
                      "a": "a 61",
                      "b": "b 65",
                      "c": "ts 113",
                      "Q": "tS 90",
                      "Y": "tS' 98",
                      "d": "d 54",
                      "X": "dZ 56",
                      "W": "dZ' 61",
                      "e": "e 53",
                      "f": "f 86",
                      "g": "g 56",
                      "h": "x 68",
                      "i":  "i 49",
                      "j":  "j 53",
                      "k":  "k 81",
                      "l":  "l 35",
                      "L": "L 59",
                      "m":  "m 56",
                      "n":  "n 45",
                      "N": "J 60",
                      "o":  "o 54",
                      "p":  "p 85",
                      "r":  "r 25",
                      "s":  "s 91",
                      "S":  "S 99",
                      "t":  "t 76",
                      "u":  "u 50",
                      "v":  "v 40",
                      "z": "z 68",
                      "Z": "Z 74",
                      ".": "_ 200",
                      " ": "_ 100" }
                      # T -> razmak
                      # đ -> W
                      # dž -> X
                      # ć -> Y
                      # č -> Q
                      # lj -> L
                      # nj -> N
                      # š -> S
                      # ž -> Z
            fajl=open("ProcitajTerapiju.txt","w")
            for element in poredani_tekstovi:
                for znak in element:
                    znak=glasovi[znak]+"\n" #Mora bit u novom redu za mbrolu...
                    fajl.write(znak.encode("utf8"))
            fajl.close()
                    
            os.system("mbrola cr1 ProcitajTerapiju.txt ProcitajTerapiju.wav")
            winsound.PlaySound("ProcitajTerapiju.wav",winsound.SND_ALIAS)
            
                
                


            #Azuriranje Baze da bude spremna za sutrasnjeg "starog korisnika" koji je danasnji "novi" lol:
            def AzurirajBazuTEO_na_temelju_formulara():
                conn=sqlite3.connect("TEO.db")
                c=conn.cursor()
                
                brojac_tableta-=1 #oduzima 1 od ovih inicijalnih 100, ova funkcija se poziva jednom i to samo kod novih korisnika,tj onih koji su ispunili formular
                
                c.execute("UPDATE Tablete SET PreostaleTablete=?",[(brojac_tableta)])
                c.execute("UPDATE Pacijent SET DatumZadnjegPristupa=?"),[(str(datetime.datetime.now().day)+"."+str(datetime.datetime.now().month)+"."+str(datetime.datetime.now().year))] #datum zadnjeg pristupa,u formatu 5.5.2015.,u slijedecem pokretanju,tj donjoj funkciji provjeravamo jel on jednak danasnjem datumu i ako je kolona pravo pristupa dobiva vrijednost false!

                conn.commit()
            AzurirajBazuTEO_na_temelju_formulara()

            #lejbli:
            rok_tabletama_lejbl=Label(root,text=("rok trajanja tableta: "+ROK_trajanja.get())).place(x="35",y="90")
            tablete=Label(root,text=("preostali broj tableta: "+str(brojac_tableta))).place(x="35",y="70")
            
            return
        


        def ProcitajDozuNaTemeljuBaze():
            
            conn=sqlite3.connect("TEO.db")
            c=conn.cursor()

            #podatke doznajemo iz baze TEO kod postojeceg/starog korisnika:
            def provjeraDatumaPristupa_TEO():
                for datum in c.execute("SELECT DatumZadnjegPristupa FROM Pacijent"):
                    if datum[0]==str(datetime.datetime.now().day)+"."+str(datetime.datetime.now().month)+"."+str(datetime.datetime.now().year):
                        c.execute("UPDATE Pacijent SET PravoKoristenja='False'") #znaci ako je datum zadnjeg pristupa jednak danasnjem,onda je pravo pristupa false,tj zabranjeno je davanje terapije u tom slucaju!
                        conn.commit()
                    else:
                        c.execute("UPDATE Pacijent SET PravoKoristenja='True'") #ako zadnji pristup nije bio danas dr rijecima...
                        conn.commit()
                return
            provjeraDatumaPristupa_TEO() #kod svakog starog korisnika,tj onog iz baze,provjeravamo jel ima pravo na danasnju terapiju ili je vec uzeo.SAMO OVU funkciju pozivam u kodu jer se ona uvijek mora izvrsit.
            
                
            def RokTrajanjaTableta_TEO(): 
                for sadrzaj in c.execute("SELECT RokTrajanja FROM Tablete"):
                    rok_trajanja_baza=sadrzaj[0] #vraca unicode datum u obliku npr 15.5.2015.
                    conn.commit()
                rok_tabletama_lejbl=Label(root,text=("rok trajanja tableta: "+rok_trajanja_baza)).place(x="35",y="90")

                rok_trajanja=str(rok_trajanja_baza).split(".") #vraca npr ['15', '5', '2015', '']
                sadasnji_dan=datetime.datetime.now().day #npr 4
                trenutni_mjesec=datetime.datetime.now().month #npr 8
                trenutna_godina=datetime.datetime.now().year #npr 2015

                #ako je rok prosao,ili ako je jednak danasnjem datumu: 
                if datetime.date(int(rok_trajanja[2]),int(rok_trajanja[1]),int(rok_trajanja[0]))<=datetime.date(trenutna_godina,trenutni_mjesec,sadasnji_dan):
                    rok_trajanja=False #lista postaje boolean sada, znaci da je istekao rok trajanja!
                    
                else:
                    rok_trajanja=True
                return rok_trajanja

            
            def PreostaleTablete_TEO():
                for sadrzaj in c.execute("SELECT PreostaleTablete FROM Tablete"): #kada sam uopce dodao tablete u bazu?? JESAM U GORNJOJ FUNKCIJI ZA FORMULAR!
                    brojac_tableta_baza=sadrzaj[0] #vraca broj tableta iz baze ,tj int
                    conn.commit()
                return brojac_tableta_baza
            

            danasnji_dan=datetime.datetime.today().weekday() #npr2 za srijedu...       
            

            #tekst za mbrolu koji pretvaramo u znakove i dodjeljujemo trajanje prema pravilu iz rjecnika:
            tekst_dani={0:"danas je ponedjeljak.",1:"danas je utorak.",2:"danas je srijeda.",3:"danas je cetvrtak.",4:"danas je petak.",5:"danas je subota.",6:"danas je nedelja."}
            
            def procitajUputu():
                #-----------citanje tekstova umetnutih u listu-> generiranje .wav fajla: -------------
                glasovi = {
                      "a": "a 61",
                      "b": "b 65",
                      "c": "ts 113",
                      "Q": "tS 90",
                      "Y": "tS' 98",
                      "d": "d 54",
                      "X": "dZ 56",
                      "W": "dZ' 61",
                      "e": "e 53",
                      "f": "f 86",
                      "g": "g 56",
                      "h": "x 68",
                      "i":  "i 49",
                      "j":  "j 53",
                      "k":  "k 81",
                      "l":  "l 35",
                      "L": "L 59",
                      "m":  "m 56",
                      "n":  "n 45",
                      "N": "J 60",
                      "o":  "o 54",
                      "p":  "p 85",
                      "r":  "r 25",
                      "s":  "s 91",
                      "S":  "S 99",
                      "t":  "t 76",
                      "u":  "u 50",
                      "v":  "v 40",
                      "z": "z 68",
                      "Z": "Z 74",
                      ".": "_ 200",
                      " ": "_ 100" }
                fajl=open("ProcitajTerapiju.txt","w")
                for element in poredani_tekstovi:
                    for znak in element:
                        znak=glasovi[znak]+"\n" #Mora bit u novom redu za mbrolu...
                        fajl.write(znak.encode("utf8"))
                fajl.close()
                    
                os.system("mbrola cr1 ProcitajTerapiju.txt ProcitajTerapiju.wav")
                winsound.PlaySound("ProcitajTerapiju.wav",winsound.SND_ALIAS)
                return
            #-----------------konacni uvjeti za pustanje snimki:----------------
            
            if PreostaleTablete_TEO()<=0:
                poredani_tekstovi=[tekst_dani[danasnji_dan]," nemate viSe tableta. posjetite najbliZu Lekarnu."]
                
                procitajUputu() #poziv funkcije za citanje terapije

                
            else:
                #za doze:
                for sadrzaj in c.execute("SELECT PON1,UTO1,SRI1,CET1,PET1,SUB1,NED1 FROM Terapija"):
                    doze_tuple_1=sadrzaj #1.TABLETA za pon-ned
                    conn.commit()

                for sadrzaj in c.execute("SELECT PON2,UTO2,SRI2,CET2,PET2,SUB2,NED2 FROM Terapija"):
                    doze_tuple_2=sadrzaj #2.TABLETA za pon-ned
                    conn.commit()

                RJ_DOZE_1={'25mg':"uzmite jednu od dvadesetipet.",'50mg':"uzmite jednu od pedeset.",'100mg':"uzmite jednu od sto.",'200mg':"uzmite jednu od dvjesto."}
                RJ_DOZE_2={'25mg':"i jednu od dvadesetpet.",'50mg':"i jednu od pedeset.",'100mg':"i jednu od sto.",'200mg':"i jednu od dvjesto.",'2.tableta?':' ',"ne uzimam drugu":' '}#ZA 2. TABLETU

                
                DOZA1=RJ_DOZE_1[doze_tuple_1[danasnji_dan]] #npr 2 za srijedu,pa dohvaca vrijednost pod 2 iz tuplea pa iz rijecnika
                DOZA2=RJ_DOZE_2[doze_tuple_2[danasnji_dan]]
                
                if RokTrajanjaTableta_TEO()==True:
                    for PravoKoristenja in c.execute("SELECT PravoKoristenja FROM Pacijent"):
                        if PravoKoristenja[0]=='True':
                            poredani_tekstovi=[tekst_dani[danasnji_dan],DOZA1,DOZA2] #DOZA1 i DOZA2 se citaju iz baze...
                            conn.commit()
                            
                            #Oduzimanje od ukupnog broja i u bazi:
                            def AzurirajPreostaliBrojTabletaTEO():
                                c.execute("UPDATE Tablete SET PreostaleTablete=?",[(PreostaleTablete_TEO()-1)])
                                conn.commit()

                                return
                            AzurirajPreostaliBrojTabletaTEO()
                            
                                                         
                elif RokTrajanjaTableta_TEO()==False:
                    for PravoKoristenja in c.execute("SELECT PravoKoristenja FROM Pacijent"):
                        if PravoKoristenja[0]=='True':
                            poredani_tekstovi=[tekst_dani[danasnji_dan],"rok trajanja tableta je istekao. posjetite najbliZu ljekarnu."]
                            conn.commit()
    
                try:#ukoliko gornji uvjeti nisu zadovoljeni (nije rjesivo elsom zbog for petlje donje i nemogucnosti uporabe logickog operatora) :
                    for PravoKoristenja in c.execute("SELECT PravoKoristenja FROM Pacijent"):
                        if PravoKoristenja[0]=='False':
                            poredani_tekstovi=[tekst_dani[danasnji_dan],"danas ste veY uzeli svoju dozu. pripazite"]
                            conn.commit()
                except:pass
                                                     
                procitajUputu() #poziv funkcije za citanje terapije
                
                

                
            

            def AzurirajBazuTEO(): #poziva se samo ako su podaci procitani jednom! ako je vise od jednom onda necu imat tocne podatke u bazi
                
                def AzurirajDatumZadnjegPristupaTEO():
                    #dodavanje DANASNJEG datuma kao datuma zadnjeg pristupa kako bi se onemogucila visestruka uporaba u jednom danu!:
                    c.execute("UPDATE Pacijent SET DatumZadnjegPristupa=?",[(str(datetime.datetime.now().day)+"."+str(datetime.datetime.now().month)+"."+str(datetime.datetime.now().year))])
                    conn.commit()
                    return
                AzurirajDatumZadnjegPristupaTEO() #uvijek se datum zadnjeg pristupa mora azurirati !!!
                
                return
            AzurirajBazuTEO()

            #ispis preostalog broja tableta iz baze na gornji lijevi rub ekrana:
            for preostaleTablete in c.execute("SELECT PreostaleTablete FROM Tablete"):
                tablete=Label(root,text=("Preostali broj tableta: "+str(preostaleTablete[0]))).place(x="35",y="70")
            
            return


        #------poziv funkcija ovisno otome jel stari (citam iz baze) ili novi korisnik (podaci iz formulara)-----------:
        if korisnik=="stari korisnik":
            ProcitajDozuNaTemeljuBaze()
            
        elif korisnik=="novi korisnik":
            ProcitajDozuNaTemeljuFormulara()
        #------------------------------------------------------------------------------
        return

    #----------------------------------Poziv glavnih funkcija:--------------------------
    sakri_formular_kanvasom()
    TEO_BAZA(korisnik)
    #---------------------------------------------------------
    
    #--dodavanje gumbiju preko kanvasa:--
    saznajDozu=Button(root,text="Saznaj danasnju dozu!",command=saznaj_dozu).place(x="500",y="300")
    #u slucaju da netko zeli promjenit korisnika,tj ako neko drugi zeli koristitit aplikaciju:
    novi_pacijent=Button(root,text="Promjena pacijenta?",command=REGISTRACIJA_KORISNIKA).place(x="507",y="350")
    
    
    return






#---------------------------------------------GLAVNI PROGRAM:----------------------------------------------------

root=Tk()
root.title("TEO")
root.geometry("1300x600+30+30")


#------------pozivanje napisanih funkcija ovisno o tome jel korisnik prvi put pristupa ili je vec postojeci----------------:

POSTAVI_IZBORNIK()

conn=sqlite3.connect("TEO.db")
c=conn.cursor()

#problem je ako apsolutno nistan e sadrzi baza :/ onda javlja error...ZATO JER NISAM STAVIO DA JE ID AUTOINCREMENT!!!! ccc

for sadrzaj in c.execute("SELECT ID FROM Pacijent"):
    duljina_provjera=len(sadrzaj) #tj duljina tuplea,sadrzaj je tuple kao tip podatka.
    conn.commit()

if duljina_provjera==0: #TJ Ako nema ID 1 onda je ovo prvi pristup bazi
    #global korisnik
    korisnik="novi korisnik"
    REGISTRACIJA_KORISNIKA()
else:
    #global korisnik
    korisnik="stari korisnik"
    POZOVI_TEA(korisnik) #ovo je za vec registrirane korisnike!! tj za one koji su vec u bazi tj kojima je ID==1...


root.mainloop()
