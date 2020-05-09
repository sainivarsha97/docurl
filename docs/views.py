from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Content
import random,string

from django.http import HttpResponse
from django.views.generic import View
from docs.utils import render_to_pdf 
import socket
from bs4 import BeautifulSoup

def GeneratePDF(request,username):
    """to generate pdf""" 

    pdf = render_to_pdf(username)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Document.pdf'
        content = "inline; filename=%s" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def DocumentView(request):
    """To Upload document"""

    template_name='docs.html'

    if request.method=="POST":
        all_urls=Content.objects.all().values_list('url', flat=True)
        
        title=request.POST["title"]
        content=request.POST["content"]
        url=request.POST["url"]
        password=request.POST["edit_password"]

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
       
        all_punctuation=list(string.punctuation)+[" "]
        url_not_allowed=any([True for x in url if x in all_punctuation])
        
        soup = BeautifulSoup(content,'html.parser').text

        if len(soup)<300:
            '''content should be greater tha 300 characters'''

            return render(request,template_name,{"not_data":True,"url":url,"password":password,"title":title})
        
        if url in all_urls or url_not_allowed:
            '''url should be unique and follow all limitations'''

            return render(request,template_name,{"data":content,"url_error":True,"password":password,"title":title})
        
        if len(password)>20 :
            '''pass can be 1-20'''

            return render(request,template_name,{"data":content,"password_error":True,"url":url,"title":title})

        Content.objects.create(content=content,url=url,title=title,password=password,ip=ip_address)
        request.session['password']=password
        return redirect('content',username=url)

    return render(request,template_name)

def EditView(request,username):
    """To Edit Content"""

    template_name='docs.html'

    if request.method=="GET":
       
        content=Content.objects.filter(url=username).first()
        if content:
            data=content.content
            title=content.title
            password=content.password
        return render(request,template_name,{"data":data,"title":title,"password":password,"no_custom_url":True})


    if request.method=="POST":

        title=request.POST["title"]
        content=request.POST["content"]
        if request.POST.get("edit_password",False):
            password=request.POST["edit_password"]
            request.session['password']=password

        url=username
        Content.objects.filter(url=url).update(content=content,title=title,password=password)

        return redirect('content',username=url)


def ContentView(request,username):
    """View Content """
    template_name='page.html'

    try:
        password=request.session['password']
        if password:
            ask_password=False
    except:
        ask_password=True

    content=Content.objects.filter(url=username).first()

    if request.method=="GET":
        
        if content:
            data=content.content
            title=content.title
            content='{% extends "base.html" %}{% block content %}<center><h1 id="main_heading">'+title+'</h1></center>'+data+'{% endblock %}'
            with open("templates/page.html", "w") as file:
                file.write(content)
            file.close()
            return render(request,template_name,{'ask_password':ask_password})
            
        return redirect("document")
        
        
    
    if request.method=="POST":  
        if request.POST.get("download",False)=='':
            """to download as pdf"""

            url=username+"/pdf"
            return redirect(url)
        
        elif request.POST.get("edit_password",False):
            edit_password=request.POST['edit_password']

            if content.password==edit_password:
                """if pass is correct"""
                
                url=username+"/edit"
                return redirect(url)
            else:
                '''wrong pass'''
                return render(request,template_name,{"wrong_password":True,'ask_password':ask_password})
                
        elif request.POST.get("edit",False)=='':
            url=username+"/edit"
            return redirect(url)


    
    
