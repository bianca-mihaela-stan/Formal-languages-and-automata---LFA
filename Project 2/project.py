import copy
def DFS(x, dict_tranz_lnfa, dict_lambda_inchidere, parinte, viz):
    if viz[x] == 0:
        viz[x] = 1
        dict_lambda_inchidere[parinte].append(x)
        if '$' in dict_tranz_lnfa[x]:
            for nod in dict_tranz_lnfa[x]['$']:
                if viz[nod] == 0:
                    DFS(nod, dict_tranz_lnfa, dict_lambda_inchidere, parinte, viz)


def calculare_lambda_inchidere(dict_tranz_lnfa, dict_lambda_inchidere, nr_stari_lnfa):
    for nod in range(nr_stari_lnfa):
        viz = [0] * nr_stari_lnfa
        dict_lambda_inchidere[nod] = []
        if nod in dict_tranz_lnfa:
            DFS(nod, dict_tranz_lnfa, dict_lambda_inchidere, nod, viz)
        dict_lambda_inchidere[nod].sort()


def calculare_functie_tranzitie_nfa(nr_stari_lnfa, dict_tranz_nfa, dict_tranz_lnfa, lista_caract, dict_lambda_inchidere):
    for i in range(nr_stari_lnfa):#iau toate starile din lnfa
        dict_tranz_nfa[i] = {}
        for ch in lista_caract:
            dict_tranz_nfa[i][ch]=[]
            lista_lambda1 = dict_lambda_inchidere[i]
            lista_ch = []
            lista_lambda2 = []
            for element in lista_lambda1:
                if ch in dict_tranz_lnfa[element]:
                    for nod in dict_tranz_lnfa[element][ch]:
                        lista_ch.append(nod)
            lista_ch = set(lista_ch)
            #print(i, ch, lista_ch)
            for element in lista_ch:
                if element in dict_lambda_inchidere:
                    #print(dict_lambda_inchidere[element])
                    for nod in dict_lambda_inchidere[element]:
                        lista_lambda2.append(nod);
            lista_lambda2 = [*set(lista_lambda2)]
            dict_tranz_nfa[i][ch] = lista_lambda2


def modificare_stari_init_fin_nfa(multime_stari_finale_nfa, multime_stari_finale_lnfa, dict_tranz_nfa, dict_lambda_inchidere):
    for x in multime_stari_finale_lnfa:
        multime_stari_finale_nfa.add(x)  # am o multime de stari finale pentru nfa
    aux = multime_stari_finale_lnfa
    modificari = 1
    for element in aux:
        for nod in dict_tranz_nfa:
            if nod in dict_lambda_inchidere:
                if element in dict_lambda_inchidere[nod]:
                    n1 = len(multime_stari_finale_nfa)
                    multime_stari_finale_nfa.add(nod)
                    n2 = len(multime_stari_finale_nfa)
                    if n2 != n1:
                        modificari = 1


def eliminare_stari_redundante(dict_tranz_nfa, nr_stari_lnfa, multime_stari_finale_nfa):
    lista_tupluri_identice = []
    copie_dict_tranz_nfa={}
    for element in dict_tranz_nfa:
        dict={}
        for ch in dict_tranz_nfa[element]:
            lista=[]
            for nod in dict_tranz_nfa[element][ch]:
                lista.append(nod)
            dict[ch]=lista
        copie_dict_tranz_nfa[element]=dict

    for i in range(nr_stari_lnfa - 1):  # iau perechi de noduri din automat
        for j in range(i + 1, nr_stari_lnfa):
            if (dict_tranz_nfa[i] == dict_tranz_nfa[j]) and (i in multime_stari_finale_nfa) == (
                    j in multime_stari_finale_nfa):
                lista_tupluri_identice.append((i, j))
    for tuplu in lista_tupluri_identice:
        for element in dict_tranz_nfa:
            for ch in dict_tranz_nfa[element]:
                for i in range(len(dict_tranz_nfa[element][ch])):
                    nod=dict_tranz_nfa[element][ch][i]
                    if nod==tuplu[0]:
                        dict_tranz_nfa[element][ch][i]=tuplu[1]
                dict_tranz_nfa[element][ch]=[*set(dict_tranz_nfa[element][ch])]
    for tuplu in lista_tupluri_identice:
        if tuplu[0] in dict_tranz_nfa:
            del dict_tranz_nfa[tuplu[0]]
        if tuplu[0] in multime_stari_finale_nfa:
            multime_stari_finale_nfa.remove(tuplu[0])



def aflare_multime_de_noi_stari(dict_tranz_nfa, multime_stari_dfa):
    for element in dict_tranz_nfa:
        for ch in dict_tranz_nfa[element]:
            if dict_tranz_nfa[element][ch]!=[] and dict_tranz_nfa[element][ch] not in multime_stari_dfa:
                multime_stari_dfa.append(dict_tranz_nfa[element][ch])


def aflare_tranzitii_dfa(stare_init_nfa, lista_caract, dict_tranz_nfa,  dict_tranz_dfa):
    coada=[[stare_init_nfa]]
    lista_stari_vizitate=[{stare_init_nfa}]
    while len(coada)>0:#cat timp coada nu e goala
        lista_stari_vizitate.append({*coada[0]})
        for ch in lista_caract:
            m = set()  # creez multimea care va fi noua stare pt caracterul ch
            for element in coada[0]: #daca coada[0]=[0,1] merg in 0 si in 1
                for nod in dict_tranz_nfa[element][ch]:#ma uit care erau tranzitiile pentru 0, rsepectiv 1, inainte
                    m.add(nod)#fac o singura multime din ele
            if len(m)>0:
                #dupa ce am creat multimea vreau sa verific daca a fost vizitata:
                if m not in lista_stari_vizitate: #si daca nu e vizitat il adaug in coada
                    coada.append([*m])
                #apoi vreau sa adaug tranzitia asta in dict_tranz_dfa
                #fiindca nu pot sa bag decat imutabile in cheia dictionarului si fiindca starea {2,1}
                # trebuie sa fie diferita de strea 21, transform starile in string-uri, cu ',' intre stari
                nr=''
                for nod in sorted(coada[0], reverse=True):
                    nr+=str(nod)
                    nr+=','
                if nr not in dict_tranz_dfa:
                    dict_tranz_dfa[nr]={}
                dict_tranz_dfa[nr][ch]=m
            else:
                nr = ''
                for nod in sorted(coada[0], reverse=True):
                    nr += str(nod)
                    nr += ','
                if nr not in dict_tranz_dfa:
                    dict_tranz_dfa[nr] = {}
        #dupa ce am terminat verficarea pentru elementul curent vreau sa il sterg din coada
        del coada[0]





def calculare_stari_fin_dfa(multime_stari_finale_nfa, multime_stari_finale_dfa, dict_tranz_dfa):
    for element in multime_stari_finale_nfa:#tsarile finale sunt cele care au in componenta stari finale dinainte
        for key in dict_tranz_dfa:
            x=0
            for i in range(0,len(key), 2):
                x=x*10+int(key[i])
            while x>0:
                if x%10==element:
                    multime_stari_finale_dfa.add(key)
                    break
                x//=10




def redenumirea_starilor(lista_tupluri_stare_notatie, dict_tranz_dfa, stare_init_dfa, multime_stari_finale_dfa, nou_dict_tranz_dfa):
    for element in dict_tranz_dfa:#iau toate starile care erau scrise ca multimi si le transform in string-uri
        for ch in dict_tranz_dfa[element]:
            nr=''
            for nod in sorted([*dict_tranz_dfa[element][ch]], reverse=True):
                nr+=str(nod)
                nr+=','
            dict_tranz_dfa[element][ch]=nr
    # fac o lista in care stabilesc o notatie pentru fiecare stare
    # starea initiala va fi notata cu 0
    p=1
    lista_tupluri_stare_notatie.append((str(stare_init_dfa)+',', 0))
    for key in dict_tranz_dfa:
        if key!=str(stare_init_dfa)+',':
            lista_tupluri_stare_notatie.append((key, p))
            p+=1
    #fac un nou dictionar, redenumit
    #redenumesc cheile
    for element in dict_tranz_dfa:
        for ch in dict_tranz_dfa[element]:
            dict_tranz_dfa[element][ch]=str(dict_tranz_dfa[element][ch])
    for tuplu in lista_tupluri_stare_notatie:
        if tuplu[0] in dict_tranz_dfa:
            nou_dict_tranz_dfa[tuplu[1]]=dict_tranz_dfa[tuplu[0]]
    #redenumesc starile pentru fiecare cheie
    for key in nou_dict_tranz_dfa:
        for ch in nou_dict_tranz_dfa[key]:
            for tuplu in lista_tupluri_stare_notatie:
                if nou_dict_tranz_dfa[key][ch]==tuplu[0]:
                    nou_dict_tranz_dfa[key][ch]=str(tuplu[1])
                    break
    #redenumesc starile finale:
    for stare in multime_stari_finale_dfa:
        for tuplu in lista_tupluri_stare_notatie:
            if stare==tuplu[0]:
                multime_stari_finale_dfa.remove(stare)
                multime_stari_finale_dfa.add(tuplu[1])
                break
    for tuplu in lista_tupluri_stare_notatie:
        if tuplu[0]==stare_init_dfa:
            stare_init_dfa=tuplu[1]



def determinarea_starilor_echivalente(multime_stari_finale_dfa, dict_tranz_dfa, dict_tranz_mindfa, lista_caract, lista_grupuri):
    matrice=[[1 for x in range(len(dict_tranz_dfa))] for x in range(len(dict_tranz_dfa))]#matrice stare cu stare, la care adaug si starea de eroare
    #marchez cu 0 toate perechile(stare nefinala, stare finala)
    for i in range (len(matrice)):
        for j in range (len(matrice[i])):
            if i in multime_stari_finale_dfa and j not in multime_stari_finale_dfa:
                matrice[i][j]=0
                matrice[j][i]=0
    schimbari=1
    while schimbari==1:
        schimbari=0
        for i in range(len(matrice)):#pentru fiecare pereche de noduri
            for j in range(len(matrice[i])):
                if matrice[i][j]==1:
                    for ch in lista_caract:#verfic inchiderea la fiecare caracter
                        x=dict_tranz_dfa[i][ch]
                        y=dict_tranz_dfa[j][ch]
                        if matrice[x][y]==0:
                            matrice[i][j]=0
                            matrice[j][i]=0
                            schimbari=1
    for i in range(len(matrice)):
        m=set()
        for j in range(len(matrice[i])):
            if matrice[i][j]==1:
                m.add(j)
        if m not in lista_grupuri:
            lista_grupuri.append(m)



def calculare_tranz_mindfa(dict_tranz_mindfa, lista_grupuri, dict_tranz_dfa, dict_stari):
    #fac un dictionar care sa imi spuna: starea 0 din dfa se duce in starea "0,1," in mindfa
    for element in lista_grupuri:
        nr=''
        for nod in sorted([*element], reverse=True):
            nr+=str(nod)
            nr+=','
        dict_tranz_mindfa[nr]={}
        for nod in element:
            dict_stari[nod]=nr
    for element in dict_tranz_dfa:#iau fiecare stare din dfa
        for ch in dict_tranz_dfa[element]:#cu fiecare nod
            #si ma uit in ce caracter se duce ca sa stiu in ce nou stare se duce
            plecare1=element#in dfa se pleca din plecare1 si cu ch se ajungea in ajungere1
            plecare2=dict_stari[plecare1]#iar in mindfa se pleaca din plecare2 si se ajunge in ajungere2
            ajungere1=dict_tranz_dfa[element][ch]
            ajungere2=dict_stari[ajungere1]
            dict_tranz_mindfa[plecare2][ch]=ajungere2




def calculare_stari_fin_mindfa(dict_stari, multime_stari_finale_dfa, multime_stari_finale_mindfa):
    for nod in multime_stari_finale_dfa:
        multime_stari_finale_mindfa.add(dict_stari[nod])


def DFS2(x, dict_tranz_mindfa, viz):
    if viz[x]==0:
        viz[x]=1
        for ch in dict_tranz_mindfa[x]:
            if viz[dict_tranz_mindfa[x][ch]]==0:
                DFS2(dict_tranz_mindfa[x][ch],  dict_tranz_mindfa, viz)



def eliminare_stari_deadend(dict_tranz_mindfa, multime_stari_finale_mindfa, stare_init_mindfa, nou_dict_tranz_mindfa):
    stari_care_trebuie_eliminate=[]
    for element in dict_tranz_mindfa:
        ok=0
        viz={}
        for e in dict_tranz_mindfa:
            viz[e]=0
        DFS2(element, dict_tranz_mindfa, viz)
        for stare in multime_stari_finale_mindfa:
            if viz[stare]==1:
                ok=1
        if ok==0:
            stari_care_trebuie_eliminate.append(element)
    for element in dict_tranz_mindfa:
        if element not in stari_care_trebuie_eliminate:
            nou_dict_tranz_mindfa[element]={}
            for ch in dict_tranz_mindfa[element]:
                if dict_tranz_mindfa[element][ch] not in stari_care_trebuie_eliminate:
                    nou_dict_tranz_mindfa[element][ch]=dict_tranz_mindfa[element][ch]




def eliminare_stari_inaccesibile(dict_tranz_mindfa, stare_init_mindfa, nou_dict_tranz_mindfa):
    stari_care_trebuie_eliminate=[]
    viz = {}
    for e in dict_tranz_mindfa:
        viz[e] = 0
    DFS2(stare_init_mindfa, dict_tranz_mindfa, viz)
    for e in viz:
        if viz[e]==0:
            stari_care_trebuie_eliminate.append(e)
    for element in dict_tranz_mindfa:
        if element not in stari_care_trebuie_eliminate:
            nou_dict_tranz_mindfa[element] = {}
            for ch in dict_tranz_mindfa[element]:
                if dict_tranz_mindfa[element][ch] not in stari_care_trebuie_eliminate:
                    nou_dict_tranz_mindfa[element][ch] = dict_tranz_mindfa[element][ch]




def adaugarea_starii_de_eroare():
    global stare_eraoare
    stare_eroare=nr_stari_dfa
    for x in range(nr_stari_dfa):
        if x not in dict_tranz_dfa:
            dict_tranz_dfa[x]={}
            for ch in lista_caract:
                dict_tranz_dfa[x][ch]=nr_stari_dfa#adaug si starea de eroare
        for ch in lista_caract:
            if ch not in dict_tranz_dfa[x]:
                dict_tranz_dfa[x][ch]=nr_stari_dfa
    dict_tranz_dfa[stare_eroare]={}
    for ch in lista_caract:
        dict_tranz_dfa[stare_eroare][ch]=nr_stari_dfa




def lNFA_NFA():
    global dict_lambda_inchidere, dict_tranz_nfa, stare_init_nfa, multime_stari_finale_nfa
    dict_lambda_inchidere = {}
    calculare_lambda_inchidere(dict_tranz_lnfa, dict_lambda_inchidere, nr_stari_lnfa)
    dict_tranz_nfa = {}
    calculare_functie_tranzitie_nfa(nr_stari_lnfa, dict_tranz_nfa, dict_tranz_lnfa, lista_caract, dict_lambda_inchidere)
    stare_init_nfa = stare_init_lnfa
    multime_stari_finale_nfa=set()
    modificare_stari_init_fin_nfa(multime_stari_finale_nfa, multime_stari_finale_lnfa, dict_tranz_nfa,
                                  dict_lambda_inchidere)#fac upate la starile finale ca ramaneau in urma si imi elimina prost starile redundante
    eliminare_stari_redundante(dict_tranz_nfa, nr_stari_lnfa, multime_stari_finale_nfa)
    print("Dictionarul NFA-ului este:")
    for element in dict_tranz_nfa:
        print(f"{element}: {dict_tranz_nfa[element]}")
    multime_stari_finale_nfa = set()
    stare_init_nfa = stare_init_lnfa
    modificare_stari_init_fin_nfa(multime_stari_finale_nfa, multime_stari_finale_lnfa, dict_tranz_nfa,
                                  dict_lambda_inchidere)
    print(f"cu starile finale: {multime_stari_finale_nfa} si starea initiala {stare_init_lnfa}")


def NFA_DFA():
    global dict_tranz_dfa, multime_Stari_finale_dfa, stare_init_dfa, multime_stari_finale_dfa, nr_stari_dfa
    dict_tranz_dfa = {}
    aflare_tranzitii_dfa(stare_init_nfa, lista_caract, dict_tranz_nfa,
                         dict_tranz_dfa)
    multime_stari_finale_dfa = set()
    stare_init_dfa = stare_init_nfa
    calculare_stari_fin_dfa(multime_stari_finale_nfa, multime_stari_finale_dfa, dict_tranz_dfa)
    lista_tupluri_stare_notatie=[]
    nou_dict_tranz_dfa={}
    redenumirea_starilor(lista_tupluri_stare_notatie, dict_tranz_dfa, stare_init_dfa, multime_stari_finale_dfa, nou_dict_tranz_dfa)
    dict_tranz_dfa=nou_dict_tranz_dfa
    for element in dict_tranz_dfa:
        for ch in dict_tranz_dfa[element]:
            dict_tranz_dfa[element][ch]=int(dict_tranz_dfa[element][ch].replace(',', ''))
    print("Dictionarul DFA-ului este:")
    for element in dict_tranz_dfa:
        print(f"{element}: {dict_tranz_dfa[element]}")
    print(f"cu starile finale: {multime_stari_finale_dfa} si starea initiala {stare_init_dfa}")
    nr_stari_dfa=len(dict_tranz_dfa)

def DFA_minDFA():
    global dict_tranz_mindfa, stare_init_mindfa, multime_stari_finale_mindfa, nr_stari_dfa
    adaugarea_starii_de_eroare()
    dict_tranz_mindfa = {}
    lista_grupuri=[]
    determinarea_starilor_echivalente(multime_stari_finale_dfa, dict_tranz_dfa, dict_tranz_mindfa, lista_caract, lista_grupuri)
    dict_stari = {}  # fac un dictionar unde vad cum se transforma toate starile vechi in stari noi
    calculare_tranz_mindfa(dict_tranz_mindfa, lista_grupuri, dict_tranz_dfa, dict_stari)
    if stare_init_dfa in dict_stari:
        stare_init_mindfa=dict_stari[stare_init_dfa]
    multime_stari_finale_mindfa=set()
    calculare_stari_fin_mindfa(dict_stari, multime_stari_finale_dfa, multime_stari_finale_mindfa)
    nou_dict_tranz_mindfa = {}
    eliminare_stari_deadend(dict_tranz_mindfa, multime_stari_finale_mindfa, stare_init_mindfa, nou_dict_tranz_mindfa)
    dict_tranz_mindfa=nou_dict_tranz_mindfa
    nou_dict_tranz_mindfa={}
    eliminare_stari_inaccesibile(dict_tranz_mindfa, stare_init_mindfa, nou_dict_tranz_mindfa)
    dict_tranz_mindfa=nou_dict_tranz_mindfa
    print("Dictionarul minDFA-ului este:")
    for element in dict_tranz_mindfa:
        print(f"{element}: {dict_tranz_mindfa[element]}")
    print(f"cu starile finale: {multime_stari_finale_mindfa} si starea initiala {stare_init_mindfa}")



def citire_lNFA():
    global nr_stari_lnfa, nr_caract, lista_caract, stare_init_lnfa, nr_stafi_finale_lnfa, multime_stari_finale_lnfa, nr_stranslatii_lnfa, dict_tranz_lnfa
    f = open("input.in")
    nr_stari_lnfa = int(f.readline())
    nr_caract = int(f.readline())
    lista_caract = f.readline().split()
    stare_init_lnfa = int(f.readline())
    nr_stari_finale_lnfa = int(f.readline())
    multime_stari_finale_lnfa=set();
    for x in f.readline().split():
        multime_stari_finale_lnfa.add(int(x))
    nr_translatii_lnfa = int(f.readline())
    dict_tranz_lnfa = {}
    for line in f:
        line = line.strip()
        nod1 = int(line.split()[0])
        nod2 = int(line.split()[2])
        tranz = line.split()[1]
        if nod1 not in dict_tranz_lnfa:
            dict_tranz_lnfa[nod1] = {tranz: [nod2]}
        else:
            if tranz not in dict_tranz_lnfa[nod1]:
                dict_tranz_lnfa[nod1][tranz] = [nod2]
            else:
                dict_tranz_lnfa[nod1][tranz].append(nod2)
    for i in range(nr_stari_lnfa):
        if i not in dict_tranz_lnfa:
            dict_tranz_lnfa[i]={}
        for ch in lista_caract:
            if ch not in dict_tranz_lnfa[i]:
                dict_tranz_lnfa[i][ch]=[]





def citire_NFA():
    global nr_stari_nfa, nr_caract, lista_caract, stare_init_nfa, nr_stari_finale_nfa, multime_stari_finale_nfa, nr_translatii_nfa, dict_tranz_nfa
    f = open("input.in")
    nr_stari_nfa = int(f.readline())
    nr_caract = int(f.readline())
    lista_caract = f.readline().split()
    stare_init_nfa = int(f.readline())
    nr_stari_finale_nfa = int(f.readline())
    multime_stari_finale_nfa = set()
    for x in f.readline().split():
        multime_stari_finale_nfa.add(int(x))
    nr_translatii_nfa = int(f.readline())
    dict_tranz_nfa = {}
    for line in f:
        line = line.strip()
        nod1 = int(line.split()[0])
        nod2 = int(line.split()[2])
        tranz = line.split()[1]
        if nod1 not in dict_tranz_nfa:
            dict_tranz_nfa[nod1] = {tranz: [nod2]}
        else:
            if tranz not in dict_tranz_nfa[nod1]:
                dict_tranz_nfa[nod1][tranz] = [nod2]
            else:
                dict_tranz_nfa[nod1][tranz].append(nod2)



def citire_DFA():
    global nr_stari_dfa, nr_caract, lista_caract, stare_init_dfa, nr_stari_finale_dfa, multime_stari_finale_dfa, nr_translatii_dfa, dict_tranz_dfa
    f = open("input.in")
    nr_stari_dfa = int(f.readline())
    nr_caract = int(f.readline())
    lista_caract = f.readline().split()
    stare_init_dfa = int(f.readline())
    nr_stari_finale_dfa = int(f.readline())
    multime_stari_finale_dfa = set()
    for x in f.readline().split():
        multime_stari_finale_dfa.add(int(x))
    nr_translatii_dfa = int(f.readline())
    dict_tranz_dfa = {}
    for line in f:
        line = line.strip()
        nod1 = int(line.split()[0])
        nod2 = int(line.split()[2])
        tranz = line.split()[1]
        if nod1 not in dict_tranz_dfa:
            dict_tranz_dfa[nod1] = {tranz: nod2}
        else:
            if tranz not in dict_tranz_dfa[nod1]:
                dict_tranz_dfa[nod1][tranz] = nod2




citire_lNFA()
#citire_NFA()
#citire_DFA()
lNFA_NFA()
NFA_DFA()
DFA_minDFA()

