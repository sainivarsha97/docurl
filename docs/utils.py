from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Content

def render_to_pdf(username, context_dict={}):
    """template = get_template(template_src)
    html  = template.render(context_dict)
    print(html)"""
    content=Content.objects.filter(url=username).first()
    title=content.title
    data=content.content

    html='<center><h1>'+title+'</h1></center>'+data
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None