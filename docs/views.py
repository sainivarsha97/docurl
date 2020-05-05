from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Content
import random,string

from django.http import HttpResponse
from django.views.generic import View
from docs.utils import render_to_pdf 
import socket

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
    template_name='docs.html'

    if request.method=="POST":
        all_urls=Content.objects.all().values_list('url', flat=True)
        
        title=request.POST["title"]
        content=request.POST["content"]
        url=request.POST["url"]
        password=request.POST["edit_password"]

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        if url not in all_urls:
            Content.objects.create(content=content,url=url,title=title,password=password,ip=ip_address)

            request.session['password']=password

            return redirect('content',username=url)

        return render(request,template_name,{"data":content,"url_error":True})
    return render(request,template_name)

def EditView(request,username):
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
            content='{% extends "parent_page.html" %}{% block content %}<center><h1 id="main_heading">'+title+'</h1></center>'+data+'{% endblock %}'
            with open("templates/page.html", "w") as file:
                file.write(content)
            file.close()
            return render(request,template_name,{'ask_password':ask_password})
            
        return redirect("document")
        
        
    
    if request.method=="POST":  
        if request.POST.get("download",False)=='':
            url=username+"/pdf"
            return redirect(url)
        
        elif request.POST.get("edit_password",False)=='':
            edit_password=request.POST['edit_password']

            if content.password==edit_password:
                url=username+"/edit"
                return redirect(url)
            else:
                return render(request,template_name,{"wrong_password":True,'ask_password':ask_password})
                
        elif request.POST.get("edit",False)=='':
            url=username+"/edit"
            return redirect(url)


    
    
