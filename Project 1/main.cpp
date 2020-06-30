#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <algorithm>
using namespace std;
ifstream f ("nfa.in");
string cuv;
int q0;
int n, m;
char x;
int l;
int k;
char caractere[100];
int sf[100];
int in[100];
char tr[100];
int fin[100];
int stari_actuale[100], nr_stari_actuale;
int stari_temp[100], nr_stari_temp;
int viz[100];
int matr[100][100];
void DFS(int x)
{
    if(viz[x]==0)
    {
        viz[x]=1;
        for(int i=0; i<n; i++)
        {
            if(matr[x][i]==1 && viz[i]==0)
                DFS(i);
        }
    }
}
void lambda(int (&stari_actuale)[100], int& nr_stari_actuale)
{
    memset(viz, 0, sizeof(viz));
    for(int q=0; q<nr_stari_actuale; q++)///ma uit cu un dfs care sunt taote starile in care pot ajunge cu lambda
    {
        if(viz[stari_actuale[q]]==0)
            DFS(stari_actuale[q]);
    }
    memset(stari_actuale, 0, sizeof(stari_actuale));
    nr_stari_actuale=0;
    for(int i=0; i<n; i++)///apoi mut in stari_actuale toate acele stari in care se poate ajunge cu lambda
    {
        if(viz[i]==1)
        {
            stari_actuale[nr_stari_actuale]=i;
            nr_stari_actuale++;
        }
    }
}
bool evaluare(string cuv)
{
    nr_stari_actuale=1;
    stari_actuale[0]=q0;

    for(int i=0; i<cuv.length(); i++)///pentru fiecare litera din cuvant
    {
        ///adaug la lista de stari actuale toate starile in care se poate ajunge cu lambda
        lambda(stari_actuale, nr_stari_actuale);
        memset(stari_temp, 0, sizeof(stari_temp));
        nr_stari_temp=0;
        for(int q=0; q<nr_stari_actuale; q++)///parcurg lista de stari de la pasul curent
        {
            int st=stari_actuale[q];
            for(int j=0; j<l; j++)///parcurg toate translatarile sa vad unde se poate ajunge din starile curente cu litera curenta
            {
                if(in[j]==st && (tr[j]==cuv[i]))
                 {
                    stari_temp[nr_stari_temp]=fin[j];
                    nr_stari_temp++;
                 }
            }
        }
        ///urmeaza sa mut starile temporare ca stari actuale, si pentru a nu avea duplicate le sortez inainte
        sort(stari_temp, stari_temp+nr_stari_temp);
        memset(stari_actuale, 0, sizeof(stari_actuale));
        nr_stari_actuale=0;
        if(nr_stari_temp==1)
        {
            stari_actuale[0]=stari_temp[0];
            nr_stari_actuale=nr_stari_temp;
        }
        else
        {
            for(int i=1; i<nr_stari_temp; i++)
            {
                if(stari_temp[i]!=stari_temp[i-1])
                    {
                        stari_actuale[nr_stari_actuale]=stari_temp[i-1];
                        nr_stari_actuale++;
                        if(i==nr_stari_temp-1)
                        {
                            stari_actuale[nr_stari_actuale]=stari_temp[i];
                            nr_stari_actuale++;
                        }
                    }
            }
        }
    }
    ///dupa ce am parcurs tot cuvantul mai vad o data unde pot ajunge cu lambda
    lambda(stari_actuale, nr_stari_actuale);
    ///dupa ce stiu toate starile actuiale vad daca vreuna e finala
    for(int i=0; i<k; i++)
    {
        for(int j=0; j<nr_stari_actuale; j++)
        {
            if(stari_actuale[j]==sf[i])
                return true;
        }
    }
    return false;
}
int main()
{
    cout<<"Numarul de stari: ";
    cin>>n;
    cout<<"Numarul de caractere: ";
    cin>>m;
    cout<<"Alfabetul: ";
    for(int i=0; i<m; i++)
    {
        cin>>x;
        caractere[i]=x;
    }
    cout<<"Starea initiala: ";
    cin>>q0;
    cout<<"Numarul de stari finale: ";
    cin>>k;
    cout<<"Starile finale: ";
    for(int i=0; i<k; i++)
    {
        cin>>sf[i];
    }
    cout<<"Numarul de translatari: ";
    cin>>l;
    cout<<"Translatarile: ";
    for(int i=0; i<l; i++)
    {
        cin>>in[i]>>tr[i]>>fin[i];
        if(tr[i]=='$')
        {
            matr[in[i]][fin[i]]=1;
        }
    }
    cout<<"Cuvantul: ";
    getline(cin, cuv);
    cout<<"Rezultatul: ";
    int rez=evaluare(cuv);
    if(rez==1)
    {
        cout<<"DA";
    }
    else cout<<"NU";
    return 0;
}
