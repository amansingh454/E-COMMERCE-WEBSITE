from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import zerosms
from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
def legal_notice(request):
    return render(request,'contact/legal_notice.html')
def tac(request):
    return render(request,'contact/tac.html')
def contact(request):
    if request.method=="POST":
        message_title=request.POST['message_title']
        message_body=request.POST['message_body']
        message_email=request.POST['message_email']
        send_mail(message_title,message_body,'amankasyapp@gmail.com',[message_email])
        messages.success(request,'email sent successfully')
        return redirect('contact')
    return render(request,'contact/contact.html')
def faq(request):
    return render(request,'contact/faq.html')
def sms(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        sendto= request.POST['sendto']
        msg=request.POST['msg']
        zerosms.sms(phno=username, passwd=password, message=msg, receivernum=sendto)
        return HttpResponse('SEND')
    else:
        return render(request,'contact/email.html')