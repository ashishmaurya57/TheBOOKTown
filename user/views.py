from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import datetime
from django.db import connection


# Create your views here.


def about(req):
    noofitemsincart = addtocart.objects.all().count()
    return render(req, 'user/about.html', {"noofitemsincart":noofitemsincart})


def contactus(request):
    noofitemsincart = addtocart.objects.all().count()
    status = False
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Message = request.POST.get("msg", "")
        x = contact(name=Name, email=Email, mobile=Mobile, message=Message)
        x.save()
        status = True
        # return HttpResponse("<script>alert('Thanks for enquiry...');window.location.href='/user/contactus/'</script>")

    return render(request, 'user/contactus.html', {'S': status,"noofitemsincart":noofitemsincart})


def services(req):
    return render(req, 'user/services.html')


def myorders(request):
    userid = request.session.get('userid')
    oid = request.GET.get('oid')
    noofitemsincart = addtocart.objects.all().count()
    orderdata = ""
    if userid:
        cursor = connection.cursor()
        cursor.execute(
            "select o.*,p.* from user_order o,user_product p where o.pid=p.id and o.userid='" + str(userid) + "'")
        orderdata = cursor.fetchall()
        if oid:
            result = order.objects.filter(id=oid, userid=userid)
            result.delete()
            return HttpResponse(
                "<script>alert('your order has been cancelled');window.location.href='/user1/myorders'</script>")

    return render(request, 'user/myorders.html', {"pendingorder": orderdata ,"noofitemsincart":noofitemsincart})


def myprofile(request):
    user = request.session.get('userid')
    pdata = profile.objects.filter(email=user)
    noofitemsincart = addtocart.objects.all().count()
    if user:
        if request.method == 'POST':
            name = request.POST.get("name", "")
            DOB = request.POST.get("dob", "")
            mobile = request.POST.get("mobile", "")
            password = request.POST.get("passwd", "")
            address = request.POST.get("address", "")
            picname = request.FILES['ppic']
            profile(email=user, name=name, dob=DOB, passwd=password, mobile=mobile, ppic=picname,
                    address=address).save()
            return HttpResponse(
                "<script>alert('Your profile updated successfully..');window.location.href='/user1/myprofile/'</script>")
    return render(request, 'user/myprofile.html', {"profile": pdata ,"noofitemsincart":noofitemsincart})


def prod(request):
    cdata = category.objects.all().order_by('-id')
    noofitemsincart = addtocart.objects.all().count()
    x = request.GET.get('abc')
    # pdata=""
    if x is not None:
        pdata = product.objects.filter(category=x)
    else:
        pdata = product.objects.all().order_by('-id')
    return render(request, 'user/products.html', {"cat": cdata, "products": pdata ,"noofitemsincart":noofitemsincart})


def signup(req):
    noofitemsincart = addtocart.objects.all().count()
    if req.method == "POST":
        name = req.POST.get("name", "")
        DOB = req.POST.get("dob", "")
        email = req.POST.get("email", "")
        mobile = req.POST.get("mobile", "")
        password = req.POST.get("passwd", "")
        address = req.POST.get("address", "")
        picname = req.FILES['ppic']
        d = profile.objects.filter(email=email)

        if d.count() > 0:
            return HttpResponse("<script>alert('Already registered..');window.location.href='/user1/signup/'</script>")
        else:
            profile(name=name, dob=DOB, mobile=mobile, email=email, passwd=password, address=address,
                    ppic=picname).save()
            return HttpResponse(
                "<script>alert('Registered successfully..');window.location.href='/user1/signup/'</script>")
        # return  HttpResponse("<script>alert('Registered successfully..');window.location.href='/user1/signup/';</script>")
    return render(req, 'user/signup.html', {"noofitemsincart":noofitemsincart})


def home(req):
    cdata = category.objects.all().order_by('-id')[0:6]
    pdata = product.objects.all().order_by('-id')[0:12]
    noofitemsincart = addtocart.objects.all().count()

    return render(req, 'user/index.html', {"data": cdata, "products": pdata, "noofitemsincart": noofitemsincart})


def signin(req):
    noofitemsincart = addtocart.objects.all().count()
    if req.method == 'POST':
        uname = req.POST.get('email', "")
        pwd = req.POST.get('passwd', "")
        checkuser = profile.objects.filter(email=uname, passwd=pwd)
        if (checkuser):
            req.session["userid"] = uname

            return HttpResponse(
                "<script>alert('Logged In Successfully..');window.location.href='/user1/signin/';</script>")
        else:
            return HttpResponse(
                "<script>alert('User Id or Password is incorrect');window.location.href='/user1/signin/';</script>")
    return render(req, 'user/signin.html',{"noofitemsincart":noofitemsincart})


def viewdetails(request):
    noofitemsincart = addtocart.objects.all().count()
    a = request.GET.get('msg')
    data = product.objects.filter(id=a)


    return render(request, 'user/viewdetails.html', {"d": data,"noofitemsincart":noofitemsincart})


def process(request):

    userid = request.session.get('userid')
    pid = request.GET.get('pid')
    btn = request.GET.get('bn')
    print(userid, pid, btn)
    if userid is not None:
        if btn == 'cart':
            checkcartitem = addtocart.objects.filter(pid=pid, userid=userid)
            if checkcartitem.count() == 0:
                addtocart(pid=pid, userid=userid, status=True, cdate=datetime.datetime.now()).save()
            else:
                return HttpResponse(
                    "<script>alert('Your item is successfully added to cart..');window.location.href='/user1/cart/'</script>")

        elif btn == 'order':
            order(pid=pid, userid=userid, remarks="pending", status=True, odate=datetime.datetime.now()).save()
            return HttpResponse(
                "<script>alert('your order has confirmed...');window.location.href='/user1/myorders/'</script>")

        elif btn == 'orderfromcart':
            res = addtocart.objects.filter(pid=pid, userid=userid)
            res.delete()
            order(pid=pid, userid=userid, remarks="pending", status=True, odate=datetime.datetime.now()).save()
            return HttpResponse(
                "<script>alert('your order has confirmed...');window.location.href='/user1/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True})

    else:
        return HttpResponse("<script>window.location.href='/user1/signin/'</script>")


def logout(request):
    del request.session['userid']
    # return render(request,'user/logout.html')
    return HttpResponse("<script>window.location.href='/user1/home/'</script>")


def cart(request):
    noofitemsincart = addtocart.objects.all().count()
    if request.session.get('userid'):
        userid = request.session.get('userid')
        cursor = connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_product p where p.id=c.pid")
        cartdata = cursor.fetchall()
        pid = request.GET.get('pid')
        if request.GET.get('pid'):
            res = addtocart.objects.filter(id=pid, userid=userid)
            res.delete()
            return HttpResponse(
                "<script>alert('Your product has been removed successfully');window.location.href='/user1/cart/'</script>")

    return render(request, 'user/cart.html',{"cart":cartdata,"noofitemsincart":noofitemsincart})
