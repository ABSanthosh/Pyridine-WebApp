from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import urllib.request
import requests
from bs4 import BeautifulSoup
from re import sub

global s
s = '''- structure, chemical names, physical and chemical properties, classification, patents, literature, biological activities, safety/hazards/toxicity information, supplier lists, and more.'''

def molecularweight(CID):
    mwlink="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+CID+"/property/MolecularWeight/txt"
    mwdata=requests.get(mwlink)
    mw= BeautifulSoup(mwdata.text, "html.parser")
    mw=str(mw).lstrip().rstrip()
    return mw

def molecularname(CID):
    mnlink="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+CID+"/property/IUPACName/txt"
    mndata=requests.get(mnlink)
    mn= BeautifulSoup(mndata.text, "html.parser")
    mn=str(mn).lstrip().rstrip()
    mn=mn.capitalize()
    return mn

def molecularformula(CID):
    mflink="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+CID+"/property/MolecularFormula/txt"
    mfdata=requests.get(mflink)
    mf= BeautifulSoup(mfdata.text, "html.parser")
    mf=str(mf).lstrip().rstrip()
    return mf

def molecularstructure(CID):
    mslink="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+CID+"/PNG?record_type=2d"
    return mslink    

def getinfo(comm):
    global s
    basepage = "https://pubchem.ncbi.nlm.nih.gov/compound/"+comm
    pagehtmldata = requests.get(basepage)
    soup = BeautifulSoup(pagehtmldata.text, "html.parser")
    name_formula = soup.find("meta", {"name": "description"})["content"]
    name_formula = name_formula.replace(s, "")
    name_formula = name_formula.split('|')
    try:
        x = name_formula[2].lstrip().rstrip().split(" ")
        CID=x[1]
        mcn = molecularname(x[1])
        mcw = molecularweight(x[1])
        mcf = molecularformula(x[1])
        mcs = molecularstructure(x[1])
    except:
        pass
    try:
        skx = (mcn, mcw, mcf, mcs,CID) 
    except UnboundLocalError as lclerr:
        pass
    return skx


@csrf_exempt
def home(request):
    return render(request, "ChemicalStructurer.html")


@csrf_exempt
def putdata(request):
    com = str(request.POST.get("Compname"))
    if com != None:
        try:
            mcinfo = getinfo(com)
            mmn=mcinfo[0]
            mmw=mcinfo[1]
            mmf=mcinfo[2]
            mms=mcinfo[3]
            Cid=mcinfo[4]
        except Exception as err:
            print("")
    else :
        print("")
    try:
        return render(request, "ChemicalStructurerw3d.html",{'cp':com,'mn':mcinfo[0],'mw':mcinfo[1],'mf':mcinfo[2],'CID':Cid,'d2d':mcinfo[3]})
    except UnboundLocalError as err1:
        return render(request, "ChemicalStructurerw3d.html")

