import base64
import datetime
import os

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from eonapp.chatbot_file import get_Response
from eonapp.models import *


static_path=r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\\"

def log(request):
    return render(request,"login_new.html")
def login_post(request):
    un=request.POST['u']
    ps=request.POST['p']
    request.session['login']=1
    res=login.objects.filter(username=un,password=ps)

    image_data = request.POST.get('image')  # Base64 encoded image

    # Save the captured image
    if image_data:
        image_data = image_data.split(",")[1]  # Remove Base64 header
        image_path = os.path.join(r"C:\Users\hilus\PycharmProjects\eon\\", f'{un}_login_image.png')
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(image_data))



    if res.exists():
        res = res[0]
        request.session['lid']=res.id
        if res.usertype=='admin':
            return HttpResponse('<script>window.location="/admin_index"</script>')
        if res.usertype=='pending':
            return HttpResponse('<script>alert("admin has not yet approved your account");window.location="/"</script>')
        if res.usertype=='seller':
            request.session['lid'] = res.id
            request.session['sid'] = seller.objects.get(LOGIN=res.id).id
            return HttpResponse('<script>window.location="/seller_index"</script>')
        if res.usertype == 'customer':
            request.session['lid'] = res.id
            request.session['cid'] =customer.objects.get(LOGIN=res.id).id
            print("cid", request.session['cid'])

            return HttpResponse('<script>window.location="/cust_index"</script>')
    else:
        return HttpResponse('<script>alert("unauthorised user");window.location="/"</script>')

def logout(request):
    request.session['login']=0
    return HttpResponse('<script>window.location="/"</script>')


def admin_index(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/index.html")

def chpass(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/changepass.html")

def chpass_post(request):
    curps=request.POST['textfield']
    nwps=request.POST['textfield2']
    cnfmps=request.POST['textfield3']
    # user = request.session['lid']


    data = login.objects.filter(id = request.session['lid'],password=curps)
    if data.exists():
        if (nwps == cnfmps):
            login.objects.filter(id=request.session['lid']).update(password=cnfmps)
            return HttpResponse('<script>alert("password changed!");window.location="/admin_index"</script>')

        else:
            return HttpResponse('<script>alert("password not same");window.location="/chpass"</script>')
    else:
        return HttpResponse('<script>alert("user not found");window.location="/chpass"</script>')

def add_cat(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/addcat.html")

def addcat_post(request):
    catname=request.POST['textfield']
    description=request.POST['textarea']

    obj=category()
    obj.categoryname=catname
    obj.discription=description
    obj.save()

    return HttpResponse("<script>alert('Category added');window.location='/view_cat#aa'</script>")


def view_cat(request):
    res=category.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/viewcat.html",{'data':res})

def edit_cat(request,id):
    view=category.objects.get(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/editcat.html",{"view":view})
def editcat_post(request,id):
    catname = request.POST['textfield']
    description = request.POST['textarea']
    category.objects.filter(id=id).update(categoryname=catname,discription=description)
    return HttpResponse('<script>alert(" category edited!");window.location="/view_cat#aa"</script>')

def delete_cat(request,id):
    category.objects.get(id=id).delete()
    return HttpResponse('<script>window.location="/view_cat#aa"</script>')

def onlinebookadd(request):
    data = category.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/onlinebook.html",{'data':data})

def onlinebookadd_post(request):
    bookname=request.POST['textfield']
    author=request.POST['textfield2']
    type=request.POST['select1']
    description=request.POST['textfield5']
    book_content = request.FILES['textfield19']
    image=request.FILES['image']

    pgno=request.POST['textfield14']
    lang=request.POST['textfield15']
    filesize=request.POST['textfield16']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
    path = "/static/image/" + d + ".jpg"

    # fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\certificate\\"+d+".pdf", book_content)
    path1 = "/static/certificate/"+d+".pdf"
    obj=online_book()
    obj.book_name=bookname
    obj.author=author
    obj.type=type
    if type == "academic":
        obj.subject = request.POST['select2']
        obj.GENRE_id = category.objects.filter()[0].id
    if type== "non-academic":
        obj.GENRE_id = request.POST['select']
        obj.emotion =1

    obj.description=description
    obj.image=path
    obj.content=path1
    obj.language=lang
    obj.filesize=filesize
    obj.no_ofpage=pgno
    obj.save()
    return HttpResponse('<script>window.location="/onlinebkview_frontview#aa"</script>')

def onlinebkview_frontview(request):
    res=online_book.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/onlinebkview_interface.html",{'data':res})

def onlinebkview_frontview_post(request):
    res=online_book.objects.filter(type = request.POST['select2'])
    return render(request,"admin/onlinebkview_interface.html",{'data':res})

def onlinebkview(request,id):
    data = online_book.objects.filter(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/onlinebookview.html",{'data':data})

def onlinebookedit(request,id):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')
    data = online_book.objects.get(id=id)
    data1 = category.objects.all()


    return render(request,"admin/edit_onlinebook.html",{"data":data,"data1":data1})

def onlinebookedit_post(request,id):
        description = request.POST['textfield5']
        type = request.POST['select1']
        filesize = request.POST['textfield16']
        language = request.POST['textfield15']
        print("disss",description)
        print("type",type)
        print("filesize",filesize)
        print("lang",language)
        # print("pgnoo",pgno)
        pgno = request.POST['textfield14']
        online_book.objects.filter(id=id).update(description=description, filesize=filesize, language=language,
                                                 type=type, no_ofpage=pgno)

        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            d = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
            path = "/static/image/" + d + ".jpg"

            online_book.objects.filter(id=id).update(image=path)
            return HttpResponse('<script>alert(" edit successfully");window.location="/onlinebkview_frontview"</script>')

        if type == "academic":
            subject1 = request.POST['select2']
            online_book.objects.filter(id=id).update(subject=subject1)
            return HttpResponse('<script>alert(" edit successfully");window.location="/onlinebkview_frontview"</script>')
        elif type == "non-academic":
            genre1 = request.POST['select']
            online_book.objects.filter(id=id).update(GENRE=genre1)
            return HttpResponse('<script>alert(" edit successfully");window.location="/onlinebkview_frontview"</script>')
        else:
            online_book.objects.filter(id=id).update(description=description,filesize=filesize,language=language,type=type, no_ofpage=pgno)
            return HttpResponse('<script>alert(" edit successfully");window.location="/onlinebkview_frontview"</script>')


def onlinebkdelete(request,id):
    online_book.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/onlinebkview_frontview#aa"</script>')

def seller_mngt(request):
    res=seller.objects.filter(LOGIN__usertype='pending')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/seller_mngt.html",{'data':res})

def sellerapprove(request,id):
    login.objects.filter(id = id).update(usertype = 'seller')
    return HttpResponse('<script>alert("Approved successfully");window.location="/seller_approval#aa"</script>')

def rejectseller(request,id):
    login.objects.filter(id=id).update(usertype='reject')
    return HttpResponse('<script>alert("Rejected successfully");window.location="/seller_mngt#aa"</script>')

def seller_approval(request):
    res=seller.objects.filter(LOGIN__usertype='seller')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/viewapprovedseller.html",{'data':res})

def ordhist(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')
    return render(request,"admin/type_orderhist.html")

def orderhist_post(request):
    type=request.POST['select']
    if type == 'seller':
        res=order_sub.objects.all()
        print(res,"resssssssssss")
        return render(request,"admin/orderhist.html",{'data':res})
    else:
        res=customer_order_sub.objects.all()
        return render(request,"admin/view_user_orderhist.html",{'data':res})

def reviw(request):
    res=review.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/reviewman.html",{'data':res})

def dltreview(request,id):
    review.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/onlinebk_reviw#aa"</script>')

def onlinebk_reviw(request):
    res=onlinebk_review.objects.all()

    # next
    res2=review.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/onlinebk_review.html",{'data':res, 'data2':res2})

def dlt_onlinebk_review(request,id):
    onlinebk_review.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/onlinebk_reviw#aa"</script>')

def view_user(request):
    res=customer.objects.filter(LOGIN__usertype = 'customer')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/viewcust.html",{'data':res})

def blockuser(request,id):
    login.objects.filter(id=id).update(usertype='blocked')
    return HttpResponse('<script>alert("Blocked sccessfully");window.location="/view_user#aa"</script>')

def blockeduser(request):
    res = customer.objects.filter(LOGIN__usertype='blocked')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "admin/blockuser.html", {'data': res})

def unblockuser(request,id):
    login.objects.filter(id=id).update(usertype='customer')
    return HttpResponse('<script>alert("unblocked sccessfully");window.location="/blockeduser#aa"</script>')

def view_allthoughtwave_frontview(request):
    res=cust_thoughtwaves.objects.all()
    return render(request,"admin/all_thoughtwave_frontview.html",{'data':res})

# def cust_tw(request):
#     res=cust_thoughtwaves.objects.all()
#     if request.session['login'] == 0:
#         return HttpResponse('<script>alert("session expired");window.location="/"</script>')
#
#     return render(request,"admin/cust_TW.html",{'data':res})

def view_thoughtwaves(request,id):
    res=cust_thoughtwaves.objects.filter(id=id)

    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/thoughtwaves_view.html",{'data':res})

def dlt_thoughtwave(request,id):
    cust_thoughtwaves.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/cust_tw#aa"</script>')

def view_comment(request,id):
    res=comment.objects.all()
    res1 = comment.objects.filter(THOUGHTNAME=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"admin/view_twcomment.html",{'data':res,'data1':res1})



###################################################################################################################


def reg_seller(request):
    return render(request,"seller/reg.html")


def reg_seller_post(request):
    seller_name=request.POST['textfield']
    email=request.POST['textfield2']
    phno=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield6']
    pin=request.POST['textfield7']
    password=request.POST['textfield8']
    confirm_password=request.POST['textfield5']
    cert = request.FILES['fileField']
    fs=FileSystemStorage()
    d=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\certificate\\" +d+ ".pdf",cert)
    path="/static/certificate/" +d+ ".pdf"

    if password == confirm_password:
        obj1=login()
        obj1.username=email
        obj1.usertype="pending"
        obj1.password=password
        obj1.save()

        obj=seller()
        obj.sellername=seller_name
        obj.email=email
        obj.phonenumber=phno
        obj.place=place
        obj.post=post
        obj.pincode=pin
        obj.certificate=path
        obj.LOGIN_id=obj1.id
        obj.save()
    else:
        return HttpResponse('<script>alert("PASSWORD DOESNT MATCH");window.location="/reg_seller"</script>')
    return HttpResponse('<script>alert("success");window.location="/"</script>')

def seller_chpass(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/seller_chpass.html")

def seller_chpass_post(request):
    curps=request.POST['textfield']
    nwps=request.POST['textfield2']
    cnfmps=request.POST['textfield3']
    # user = request.session['lid']


    data = login.objects.filter(id = request.session['lid'],password=curps)
    if data.exists():
        if (nwps == cnfmps):
            login.objects.filter(id=request.session['lid']).update(password=cnfmps)
            return HttpResponse('<script>alert("password changed!");window.location="/seller_index"</script>')

        else:
            return HttpResponse('<script>alert("password not same");window.location="/seller_chpass"</script>')
    else:
        return HttpResponse('<script>alert("user not found");window.location="/seller_chpass"</script>')

def seller_index(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/index.html")

def seller_view(request):
    data = seller.objects.get(LOGIN=request.session['lid'])
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/profile_view.html",{"data":data})

def edit_profile(request,id):
    data = seller.objects.get(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/seller_edit.html",{"data":data,"id":id})

def edit_profile_post(request,id):
    name = request.POST['textfield']
    phno=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield6']
    pin=request.POST['textfield7']
    seller.objects.filter(id=id).update(sellername=name,phonenumber=phno,place=place,post=post,pincode=pin)
    return HttpResponse('<script>alert("edited");window.location="/seller_view#aa"</script>')

def bookadd(request):
    data = category.objects.all
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/book/add.html",{'data':data})

def bookadd_post(request):
    bookname=request.POST['textfield']
    author=request.POST['textfield2']
    genre=request.POST['select']
    description=request.POST['textfield5']
    price=request.POST['textfield6']
    discount=request.POST['textfield7']
    image=request.FILES['fileField']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
    path = "/static/image/" + d + ".jpg"
    availability=request.POST['textfield13']
    pgno=request.POST['textfield14']
    obj=book()
    obj.book_name=bookname
    obj.author=author
    obj.GENRE_id=genre
    obj.description=description
    obj.price=price
    obj.discount=discount
    obj.image=path
    obj.LOGIN_id = request.session['lid']
    obj.type='seller'
    obj.availability=availability
    obj.numberofpages=pgno
    obj.SELLER = seller.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse('<script>alert("added");window.location="/bkview_frontview"</script>')

def bookedit(request,id):
    data = book.objects.get(id=id)
    print(data.id, " cc")
    data1 = category.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/book/edit.html",{"data2":data,"data1":data1})

def bookedit_post(request,id):
        description = request.POST['textfield5']
        price = request.POST['textfield6']
        discount = request.POST['textfield7']
        genre = request.POST['cat']
        type = request.POST['textfield12']
        availability = request.POST['textfield13']
        pgno = request.POST['textfield14']
        if 'fileField' in request.FILES:
            image = request.FILES['fileField']
            fs = FileSystemStorage()
            d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
            path = "/static/image/" + d + ".jpg"

            book.objects.filter(id=id).update(description=description, price=price, discount=discount,GENRE=genre, image=path, type=type,  availability=availability, numberofpages=pgno)
            return HttpResponse('<script>alert(" edit successfully");window.location="/bkview_frontview"</script>')
        else:
            book.objects.filter(id=id).update(description=description, price=price, discount=discount, type=type,
                                              availability=availability, numberofpages=pgno,GENRE=genre)
            return HttpResponse('<script>alert(" edit successfully");window.location="/bkview_frontview"</script>')

def bkview(request,id):
    print(request.session['lid'])
    data = book.objects.filter(id = id, type = 'seller')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')
    return render(request,"seller/book/bookview.html",{'data':data})

def bkview_frontview(request):
    res=book.objects.filter(LOGIN=request.session['lid'],LOGIN__usertype = 'seller')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')
    return render(request,"seller/bookview.html",{'data':res})

def bkview_frontview_post(request):
    res=book.objects.filter(LOGIN=request.session['lid'],LOGIN__usertype = 'seller', book_name__icontains=request.POST['ttt'])
    return render(request,"seller/bookview.html",{'data':res})


def bkdelete(request,id):
    book.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/bkview_frontview"</script>')

def seller_view_order(request):
    print( request.session['lid'])
    res = seller_order.objects.filter(SELLER__LOGIN = request.session['lid'],orderstatus='pending')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/ordermngt.html",{'data':res})

def orderapprove(request,id):
    seller_order.objects.filter(id = id).update(orderstatus = 'approved')
    return HttpResponse('<script>alert("Approved successfully");window.location="/seller_view_order"</script>')

def rejectorder(request,id):
    seller_order.objects.filter(id=id).update(orderstatus='reject')
    return HttpResponse('<script>alert("Rejected successfully");window.location="/seller_view_order"</script>')

def orderapproved(request):
    res=seller_order.objects.filter(orderstatus__in=['approved','orderplaced','dispatched','shipped','out for delivery','delayed','delivered','cancelled','returned'],SELLER__LOGIN = request.session['lid'])
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/approvedorder.html",{'data':res})

def seller_order_sub(request,id):
    res=order_sub.objects.filter(SELLER_ORDER=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/suborder.html",{'data':res})


def update_order_status(request,id):

    return render(request,"seller/orderstatus.html",{'id':id})

def update_order_status_post(request,id):
    status=request.POST['ord']
    print("status",status)

    print("idddddddddd",id)
    if status == 'dispatched' or status == 'shipped' or status == 'delayed':
        return render(request, "seller/delivery.html",{'id':id,'status':status})
    else:
        res = seller_order.objects.filter(id=id).update(orderstatus=status)
        print(res,"ressssssss")
        return HttpResponse('<script>alert("Updated successfully");window.location="/orderapproved#aa"</script>')

def update_delivery_post(request,id,status):
    delivery=request.POST['textfield']
    seller_order.objects.filter(id = id).update(deliverydate =delivery ,orderstatus = status)
    return HttpResponse('<script>window.location="/orderapproved#aa"</script>')

def review_book(request,id):
    res=review.objects.filter(BOOK_id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"seller/review.html",{'data':res})

#################################################################################


def reg_cust(request):
    return render(request,"customer/register_interface.html")

def reg_cust_post(request):
    image = request.FILES['fileField']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
    path = "/static/image/" + d + ".jpg"
    first_name=request.POST['textfield']
    last_name = request.POST['textfield9']
    email=request.POST['textfield2']
    phno=request.POST['textfield3']
    dob=request.POST['textfield4']
    age=request.POST['textfield6']
    gender=request.POST['radio']
    place = request.POST['textfield7']
    post = request.POST['textfield10']
    pin = request.POST['textfield11']
    password=request.POST['textfield8']
    confirm_password=request.POST['textfield5']

    data = login.objects.filter(username=email)
    if data.exists():

        return HttpResponse('<script>alert("Username al exist");window.location="/reg_cust"</script>')

    else:
        if password == confirm_password:
            obj1=login()
            obj1.username=email
            obj1.usertype="customer"
            obj1.password=password
            obj1.save()

            obj=customer()
            obj.image=path
            obj.firstname=first_name
            obj.lastname = last_name
            obj.email=email
            obj.phonenumber=phno
            obj.dob=dob
            obj.age=age
            obj.gender=gender
            obj.place=place
            obj.post=post
            obj.pin=pin
            obj.LOGIN_id=obj1.id
            obj.save()
        else:
            return HttpResponse('<script>alert("PASSWORD DOES NOT MATCH!!");window.location="/reg_cust"</script>')
        return HttpResponse('<script>alert("success");window.location="/"</script>')

def cust_index(request):
    return render(request,"customer/index.html")

def cust_chpass(request):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/cust_chpass.html")

def cust_chpass_post(request):
    curps=request.POST['textfield']
    nwps=request.POST['textfield2']
    cnfmps=request.POST['textfield3']

    data = login.objects.filter(id = request.session['lid'],password=curps)
    if data.exists():
        if (nwps == cnfmps):
            login.objects.filter(id=request.session['lid']).update(password=cnfmps)
            return HttpResponse('<script>alert("password changed!");window.location="/cust_index"</script>')

        else:
            return HttpResponse('<script>alert("password not same");window.location="/cust_chpass"</script>')
    else:
        return HttpResponse('<script>alert("user not found");window.location="/cust_chpass"</script>')

def cust_view(request):
    data = customer.objects.get(LOGIN=request.session['lid'])
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/viewprofile.html",{"data":data})


def edit_csprofile(request,id):
    data = customer.objects.get(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/edit.html",{"data":data,"id":id})

def edit_csprofile_post(request,id):
    first_name = request.POST['textfield']
    last_name = request.POST['textfield9']
    email = request.POST['textfield2']
    phno = request.POST['textfield3']
    dob = request.POST['textfield4']
    age = request.POST['textfield6']
    # gender = request.POST['radio']
    place = request.POST['textfield7']
    post = request.POST['textfield10']
    pin = request.POST['textfield11']
    if 'fileField' in request.FILES:
        image = request.FILES['fileField']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
        path = "/static/image/" + d + ".jpg"

        customer.objects.filter(id=id).update(image=path,firstname=first_name,lastname=last_name,email=email,phonenumber=phno,dob=dob,age=age,place=place,post=post,pin=pin)
        return HttpResponse('<script>alert(" edit successfully");window.location="/cust_view#aa"</script>')
    else:
        customer.objects.filter(id=id).update(firstname=first_name,lastname=last_name,email=email,phonenumber=phno,dob=dob,age=age,place=place,post=post,pin=pin)
        return HttpResponse('<script>alert(" edit successfully");window.location="/cust_view#aa"</script>')

def csbookadd(request):
    data = category.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/book/add.html",{'data':data})

def csbookadd_post(request):
    bookname=request.POST['textfield']
    author=request.POST['textfield2']
    genre=request.POST['select']
    description=request.POST['textfield5']
    price=request.POST['textfield6']
    discount=request.POST['textfield7']
    image=request.FILES['fileField']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
    path = "/static/image/" + d + ".jpg"
    condition=request.POST['textfield11']
    availability=request.POST['textfield13']
    pgno=request.POST['textfield14']

    obj=book()
    obj.book_name=bookname
    obj.author=author
    obj.GENRE_id=genre
    obj.description=description
    obj.price=price
    obj.discount=discount
    obj.image=path
    obj.bookcondition=condition
    obj.type='customer'
    obj.availability=availability
    obj.numberofpages=pgno
    obj.LOGIN_id = request.session['lid']
    obj.save()
    return HttpResponse('<script>window.location="/csbkview_frontview"</script>')

def csbkview(request,id):
    res=book.objects.filter(id = id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/book/bookview.html",{'data':res})

def csbkview_frontview(request):
    res=book.objects.filter(LOGIN=request.session['lid'],LOGIN__usertype = 'customer')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/bkview_interface.html",{'data':res})

def csbkview_frontview_post(request):
    res=book.objects.filter(LOGIN=request.session['lid'],LOGIN__usertype = 'customer', book_name__icontains=request.POST['ttt'])
    return render(request,"customer/bkview_interface.html",{'data':res})

def csbookedit(request,id):
    data = book.objects.get(id = id)
    data1 = category.objects.all()
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/book/edit.html",{"data2":data,"data1":data1})

def csbookedit_post(request,id):
        description = request.POST['textfield5']
        price = request.POST['textfield6']
        discount = request.POST['textfield7']
        genre = request.POST['select']
        condition = request.POST['textfield11']
        availability = request.POST['textfield13']
        pgno = request.POST['textfield14']
        if 'fileField' in request.FILES:
            image = request.FILES['fileField']
            fs = FileSystemStorage()
            d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image)
            path = "/static/image/" + d + ".jpg"

            book.objects.filter(id=id).update(description=description, price=price, discount=discount,GENRE=genre, image=path, bookcondition=condition,  availability=availability, numberofpages=pgno)
            return HttpResponse('<script>alert(" edit successfully");window.location="/csbkview_frontview"</script>')
        else:
            book.objects.filter(id=id).update(description=description, price=price, discount=discount,
                                              GENRE=genre,
                                              availability=availability, bookcondition=condition, numberofpages=pgno)
            return HttpResponse('<script>window.location="/csbkview_frontview"</script>')

def csbkdelete(request,id):
    book.objects.get(id=id).delete()
    return HttpResponse('<script>window.location="/csbkview_frontview"</script>')

def view_review_bout_mybk(request):
    res = review.objects.filter(BOOK__LOGIN=request.session['lid'])
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/review_bout_mybk.html", {'data':res})

def view_customer_book_frontview(request):
    res=book.objects.filter(~Q(LOGIN = request.session['lid']),type="customer")
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/bookinterface_sell.html",{'data':res})

def view_customer_book(request,id):
    res=book.objects.filter(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/otherbook.html", {'data': res})

def view_seller_book_frontview(request):
    res=book.objects.filter(~Q(LOGIN = request.session['lid']),type="seller")
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/sellerbook_interface.html",{'data':res})


def view_seller_book(request,id):
    res=book.objects.filter(id=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/details_sellerbk.html", {'data': res})

def add_cart(request,id):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/quantity_cart.html", {"id": id})

def add_cart_post(request,id):
    quantity=request.POST['select']
    q1 = request.POST['select']
    availability1 = book.objects.get(id=id).availability
    print("avvaaill", availability1)

    if int(q1) <= int(availability1):

        obj=cart()
        obj.quantity=quantity
        obj.BOOK_id = id
        obj.CUSTOMER_id = request.session['cid']
        obj.save()
        final_quantity = int(availability1) - int(q1)
        book.objects.filter(id = id).update(availability = final_quantity)
        return HttpResponse('<script>window.location="/view_seller_book_frontview"</script>')

    else:
        return HttpResponse('<script>alert("out of stock");window.location="/view_seller_book_frontview"</script>')


def view_cart(request):
    res = cart.objects.filter(CUSTOMER=request.session['cid'])
    total = 0

    for i in res:
        i.total = int(i.quantity) * float(i.BOOK.price) * (1 - float(i.BOOK.discount) / 100)
        total += i.total

    type="seller"
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/cartview.html", {'data': res,'type':type,'total':total})

def rmv_cart(request,id):
    cart.objects.get(id=id).delete()
    return HttpResponse('<script>window.location="/view_cart"</script>')

def place_orderfromcart(request,id,cslid,type,amt):
    request.session['typee'] = type
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/view_cart"</script>')

    return render(request,"customer/place_quantitycart.html",{"id": id,'cslid':cslid,'amt':amt})

def place_orderfromcart_post(request,id,cslid,amt):
    pin = request.POST['textfield']
    city = request.POST['textfield4']
    state = request.POST['textfield5']
    house = request.POST['textfield2']
    colony = request.POST['textfield3']
    q1 = request.POST['select']
    discount1 = book.objects.get(id=id).discount
    print("discount", discount1)
    total_amount_withoutdis = float(amt) * int(q1)
    discount_amount = float((total_amount_withoutdis) * float(discount1)) / 100

    final_amount = float(total_amount_withoutdis) - float(discount_amount)
    if str(request.session['typee']) == 'customer':
        obj = customer_order()
        obj.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj.CUSTOMER_se_id = cslid
        obj.date = datetime.datetime.now()
        obj.orderstatus = 'pending'
        obj.paymentstatus = 'pending'
        obj.paymentmethod = 'pending'
        obj.totalamount = final_amount
        obj.discount = book.objects.get(id=id).discount

        obj.pin = pin
        obj.city = city
        obj.state = state
        obj.colony = colony
        obj.house = house
        obj.deliverydate = 'pending'
        # obj.return_or_refund = 'pending'
        # obj.ordernotes = 'pending'
        obj.ordercancellationreason = 'NA'
        obj.save()

        obj1 = customer_order_sub()
        obj1.CUSTOMER_ORDER_id = obj.id
        obj1.BOOK_id = id
        obj1.quantity = q1
        obj1.save()
    else:
        obj2=seller_order()
        obj2.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
        obj2.SELLER_id = cslid
        obj2.date = datetime.datetime.now()
        obj2.orderstatus = 'pending'
        obj2.paymentstatus = 'pending'
        obj2.paymentmethod = 'pending'
        obj2.totalamount = 'pending'
        obj2.discount = book.objects.get(id=id).discount
        obj2.pin = pin
        obj2.city = city
        obj2.state = state
        obj2.colony = colony
        obj2.house = house
        # obj2.deliverydate = 'pending'
        # obj2.return_or_refund = 'pending'
        # obj2.ordernotes = 'pending'
        obj2.ordercnclreason = 'NA'
        obj2.save()
        obj3=order_sub()
        obj3.SELLER_ORDER = obj2
        obj3.BOOK_id = id
        obj3.quantity = q1
        obj3.save()
    cart.objects.get(BOOK=id,CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid'])).delete()
    return HttpResponse('<script>alert("order plaved!");window.location="/view_cart#aa"</script>')


def cs_order_view(request):
    res =  customer_order.objects.filter(CUSTOMER_se=request.session['cid'],orderstatus = 'pending')
    print(res,'aaaaaaaaaaa')
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request, "customer/customer_order_ view.html", {'data': res})

def view_ordersed_books(request,id):
    res=customer_order_sub.objects.filter(CUSTOMER_ORDER=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,'customer/bookitems.html',{'data':res})

def cs_order_sub(request,id):
    res=customer_order_sub.objects.filter(CUSTOMER_ORDER=id)
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/cs_suborder.html",{'data':res})


def csorderapprove(request,id):
    customer_order.objects.filter(id = id).update(orderstatus = 'approved')
    return HttpResponse('<script>window.location="/cs_order_view"</script>')

def csrejectorder(request,id):
    customer_order.objects.filter(id=id).update(orderstatus='reject')
    return HttpResponse('<script>window.location="/cs_order_view"</script>')

def csorderapproved(request):
    res=customer_order.objects.filter(~Q(CUSTOMER  = request.session['lid']),orderstatus__in=['approved','orderplaced','dispatched','shipped','out for delivery','delayed','delivered','returned'])
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/csapprovedorder.html",{'data':res})

def csupdate_status(request,id):
    if request.session['login'] == 0:
        return HttpResponse('<script>alert("session expired");window.location="/"</script>')

    return render(request,"customer/csorderstatus.html",{'id':id})

def csupdate_status_post(request,id):
    status=request.POST['ord']
    print("status",status)
    if status == 'dispatched' or status == 'shipped' or status == 'delayed':
        return render(request, "customer/delivery.html",{'id':id,'status':status})
    else:
        customer_order.objects.filter(id=id).update(orderstatus=status)
        return HttpResponse('<script>window.location="/csorderapproved#aa"</script>')

def csupdate_delivery_post(request,id,status):
    delivery=request.POST['textfield']
    customer_order.objects.filter(id = id).update(deliverydate =delivery ,orderstatus = status)
    return HttpResponse('<script>window.location="/csorderapproved#aa"</script>')

def place_orderfrombook(request,id,cslid,amt):
    return render(request,"customer/quantity_place.html",{"id": id,'cslid':cslid,'amt':amt})

def place_orderfrombook_post(request,id,cslid,amt):
    pin = request.POST['textfield']
    city = request.POST['textfield4']
    state = request.POST['textfield5']
    house = request.POST['textfield2']
    colony = request.POST['textfield3']
    q1 = request.POST['select']
    print("cslid",cslid)
    availability1 = book.objects.get(id=id).availability
    print("avvaaill", availability1)

    if int(q1) <= int(availability1):


        discount1 = book.objects.get(id=id).discount

        print("discount", discount1)
        total_amount_withoutdis = int(amt) * int(q1)
        discount_amount = float((total_amount_withoutdis) * float(discount1)) / 100
        final_amount = float(total_amount_withoutdis) - (float(discount_amount))

        print(final_amount,"Final amounttttttttttttttttttt")

        obj = customer_order()
        obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
        obj.CUSTOMER_se_id = customer.objects.get(LOGIN = cslid).id
        obj.date = datetime.datetime.now()
        obj.orderstatus = 'pending'
        obj.paymentstatus = 'pending'
        obj.paymentmethod = 'pending'
        obj.totalamount = final_amount
        obj.discount = book.objects.get(id=id).discount
        obj.pin = pin
        obj.city = city
        obj.state = state
        obj.colony = colony
        obj.house = house
        obj.deliverydate = 'pending'
        # obj.return_or_refund = 'pending'
        # obj.ordernotes = 'pending'
        obj.ordercancellationreason = 'NA'
        obj.save()

        obj1 = customer_order_sub()
        obj1.CUSTOMER_ORDER = obj
        obj1.BOOK_id = id
        obj1.quantity = q1
        obj1.save()

        final_quantity = int(availability1)-int(q1)
        book.objects.filter(id = id).update(availability = final_quantity)
        return HttpResponse('<script>window.location="/view_customer_book_frontview"</script>')

    else:
        return HttpResponse('<script>alert("out of stock");window.location="/view_customer_book_frontview"</script>')


def place_orderfrombookseller(request,id,slid,amt):

    return render(request,"customer/placeorder_sellerbook.html",{"id": id,'slid':slid,'amt':amt})

def place_orderfrombookseller_post(request,id,slid,amt):
    pin = request.POST['textfield']
    city = request.POST['textfield4']
    state = request.POST['textfield5']
    house = request.POST['textfield2']
    colony = request.POST['textfield3']
    q1 = request.POST['select']

    availability1 = book.objects.get(id = id).availability
    print("avvaaill",availability1)

    if int(q1) <=  int(availability1) :

        discount1 = book.objects.get(id=id).discount

        print("discount", discount1)

        total_amount_withoutdis = int(amt) * int(q1)

        discount_amount = float((total_amount_withoutdis) * float(discount1)) / 100

        final_amount = float(total_amount_withoutdis) - float(discount_amount)

        obj2 = seller_order()
        obj2.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj2.SELLER_id = seller.objects.get(LOGIN=slid).id
        obj2.date = datetime.datetime.now()
        obj2.orderstatus = 'pending'
        obj2.paymentstatus = 'pending'
        obj2.paymentmethod = 'pending'
        obj2.totalamount = final_amount
        obj2.discount = book.objects.get(id=id).discount
        obj2.pin = pin
        obj2.city = city
        obj2.state = state
        obj2.colony = colony
        obj2.house = house
        obj2.deliverydate = 'pending'
        # obj2.return_or_refund = 'pending'
        # obj2.ordernotes = 'pending'
        obj2.ordercnclreason = 'NA'
        obj2.save()

        obj3 = order_sub()
        obj3.SELLER_ORDER = obj2
        obj3.BOOK_id = id
        obj3.quantity = q1
        obj3.save()
        final_quantity = int(availability1) - int(q1)
        book.objects.filter(id=id).update(availability=final_quantity)

        return HttpResponse('<script>alert("Order Placed!!");window.location="/view_seller_book_frontview"</script>')



    else:
        return HttpResponse('<script>alert("out of stock");window.location="/view_customer_book_frontview"</script>')

def view_my_order(request):
    res=customer_order.objects.filter(CUSTOMER = request.session['cid'],orderstatus__in = [ 'approved', 'orderplaced', 'dispatched', 'shipped', 'out for delivery', 'delayed',
                           'delivered', 'cancelled', 'returned'])
    data=seller_order.objects.filter(CUSTOMER = request.session['cid'],orderstatus__in = [ 'approved', 'orderplaced', 'dispatched', 'shipped', 'out for delivery', 'delayed',
                           'delivered', 'cancelled', 'returned'])
    return render(request, "customer/myorder.html", {'res': res,'data1':data})

def view_my_order_post(request):

    select1 = request.POST['select']

    res = customer_order.objects.filter(CUSTOMER=request.session['cid'],
                                        orderstatus__in=[ 'approved', 'orderplaced', 'dispatched', 'shipped',
                                                         'out for delivery', 'delayed',
                                                         'delivered', 'cancelled', 'returned'],)
    data = seller_order.objects.filter(CUSTOMER=request.session['cid'],orderstatus__in = [ 'approved', 'orderplaced', 'dispatched', 'shipped', 'out for delivery', 'delayed',
                           'delivered', 'cancelled', 'returned'])
    return render(request, "customer/myorder.html", {'res': res, 'data1': data,'select1':select1})


def my_order_sub(request,id):
    res=customer_order_sub.objects.filter(CUSTOMER_ORDER=id)
    return render(request,"customer/myordersub.html",{'data':res})

def my_seller_order_sub(request,id):
    res = order_sub.objects.filter(SELLER_ORDER=id)
    return render(request,"customer/seller_sub_order.html",{'data':res})

def my_cust_order_cancel(request,id):
    return render(request, "customer/cancellation_reason.html",{'id':id})

def my_cust_order_cancel_post(request,id):
    reason=request.POST['textarea']
    customer_order.objects.filter(id=id).update(ordercancellationreason=reason, orderstatus='cancelled')
    return HttpResponse('<script>alert("Order Cancelled!!");window.location="/view_my_order#aa"</script>')


def my_seller_order_cancel(request,id):
    return render(request, "customer/seller_order_cancellation.html", {'id':id})

def my_seller_order_cancel_post(request,id):
    reason=request.POST['textarea']
    seller_order.objects.filter(id=id).update(ordercnclreason=reason, orderstatus='cancelled')
    return HttpResponse('<script>alert("Order Cancelled!!");window.location="/view_my_order#aa"</script>')

def cs_onlinebkview_frontview(request):
    res=online_book.objects.filter(type="non-academic")
    return render(request,"customer/onlinebook_interface.html",{'data':res})

def studymaterial_frontview(request):
    res=online_book.objects.filter(type="academic")
    return render(request,"customer/studymaterial_frontview.html",{'data':res})


def studymaterial_frontview_post(request):
    res=online_book.objects.filter(type="academic",subject = request.POST['select2'])
    return render(request,"customer/studymaterial_frontview.html",{'data':res})

def cs_academicbk_view(request,id):
    res=online_book.objects.filter(type="academic",id=id )
    return render(request,"customer/cs_academicbk_view.html",{'data':res})

def cs_onlinebkview_frontview_post(request):
    res=online_book.objects.filter(type="non-academic",subject__contains = request.POST['select2'])
    return render(request,"customer/onlinebook_interface.html",{'data':res})

def cs_onlinebkview(request,id):
    res=online_book.objects.filter(type="non-academic" ,id = id)
    return render(request,"customer/nonacademic_bkview.html",{'data':res})

def cs_onlinebkview_post(request):
    # btn = request.POST['button']
    search1 = request.POST['select2']
    newres = []
    res = online_book.objects.filter(type="non-academic",book_name__contains=search1)
    for i in res:
        if str(search1) in i.book_name:
            newres.append(i)
    return render(request, "customer/nonacademic_bkview.html", {'data': res})

def add_review(request,id):
    return render(request,"customer/send_review.html",{'id':id})

def add_review_post(request,id):
    revw=request.POST['textfield3']
    rating=request.POST['star']
    obj=review()
    obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
    obj.revw=revw
    obj.date = datetime.datetime.now()
    obj.BOOK_id= id
    obj.rating=rating
    obj.save()
    return HttpResponse("<script>alert('review send successfully');window.location='/cust_index'</script>")

def view_allreview(request,id):
    res = review.objects.filter(BOOK_id=id)
    cur_cust = customer.objects.get(LOGIN = request.session['lid'])
    return render(request, "customer/view_allreview.html", {'data':res,'id':cur_cust})

def view_own_review(request):
    data = review.objects.filter(CUSTOMER=request.session['cid'])
    return render(request,'customer/csreview.html',{'data':data})

def edit_review(request,id):
    view=review.objects.get(id=id)
    return render(request,"customer/edit_review.html",{"view":view})

def edit_review_post(request,id):
    revw1 = request.POST['textfield3']
    rating1 = request.POST['textfield5']
    review.objects.filter(id=id).update(revw=revw1, rating=rating1, date=datetime.datetime.now())
    return HttpResponse('<script>alert(" edited successfully");window.location="/view_own_review#aa"</script>')

def cs_dlt_review(request,id):
    review.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/view_own_review#aa"</script>')

def add_onlinebk_review(request,id):
    return render(request,"customer/send_onlinebkreview.html",{'id':id})

def add_onlinebkreview_post(request,id):
    revw=request.POST['textfield3']
    rating=request.POST['star']

    obj=onlinebk_review()
    obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
    obj.revw=revw
    obj.date = datetime.datetime.now()
    obj.ONLINE_BOOK_id= id
    obj.rating=rating
    obj.save()
    return HttpResponse("<script>alert('review send successfully');window.location='/cs_onlinebkview_frontview'</script>")

def view_all_onlinebk_review(request,id):
    res = onlinebk_review.objects.all()
    cur_cust = customer.objects.get(LOGIN = request.session['lid'])
    return render(request, "customer/view_all_onlinebk_review.html", {'data':res,'id':cur_cust})

def view_own_onlinebk_review(request):
    data = onlinebk_review.objects.filter(CUSTOMER=request.session['cid'])
    return render(request,'customer/cs_own_onlinebk_review.html',{'data':data})

def edit_onlinebk_review(request,id):
    view=onlinebk_review.objects.get(id=id)
    return render(request,"customer/edit_onlinebk_review.html",{"view":view})

def edit_onlinebk_review_post(request,id):
    revw1 = request.POST['textfield3']
    rating1 = request.POST['textfield5']
    onlinebk_review.objects.filter(id = id).update(revw = revw1,rating = rating1,date = datetime.datetime.now())
    return HttpResponse('<script>alert(" edited successfully");window.location="/view_own_onlinebk_review#aa"</script>')

def cs_dlt_onlinebk_review(request,id):
    onlinebk_review.objects.get(id=id).delete()
    return HttpResponse('<script>alert("delete successfully");window.location="/view_own_onlinebk_review#aa"</script>')

def add_qtn(request,id):
    return render(request, "customer/question_add.html", {'id': id})

def add_qtn_post(request,id):
    qtn=request.POST['textfield']
    opt_a=request.POST['textfield2']
    opt_b=request.POST['textfield3']
    opt_c=request.POST['textfield4']
    opt_d=request.POST['textfield5']
    ans=request.POST['select']


    if ans == 'OPTION A':
        obj = question()
        obj.ONLINE_BOOK_id = id
        obj.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj.questions = qtn
        obj.option_a = opt_a
        obj.option_b = opt_b
        obj.option_c = opt_c
        obj.option_d = opt_d
        obj.answers = opt_a
        obj.save()

    elif ans == 'OPTION B':
        obj = question()
        obj.ONLINE_BOOK_id = id
        obj.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj.questions = qtn
        obj.option_a = opt_a
        obj.option_b = opt_b
        obj.option_c = opt_c
        obj.option_d = opt_d
        obj.answers = opt_b
        obj.save()

    elif ans == 'OPTION C':
        obj = question()
        obj.ONLINE_BOOK_id = id
        obj.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj.questions = qtn
        obj.option_a = opt_a
        obj.option_b = opt_b
        obj.option_c = opt_c
        obj.option_d = opt_d
        obj.answers = opt_c
        obj.save()

    else:
        obj = question()
        obj.ONLINE_BOOK_id = id
        obj.CUSTOMER_id = customer.objects.get(LOGIN=request.session['lid']).id
        obj.questions = qtn
        obj.option_a = opt_a
        obj.option_b = opt_b
        obj.option_c = opt_c
        obj.option_d = opt_d
        obj.answers = opt_d
        obj.save()

    return HttpResponse('<script>alert("added");window.location="/cs_academicbk_view/'+str(id)+'#aa"</script>')


def view_question(request,id):
    request.session['qid'] = id
    res=question.objects.filter(CUSTOMER=request.session['cid'],ONLINE_BOOK = id)
    return render(request,"customer/question_vw.html",{'data':res})

def edit_question(request,id):
    view=question.objects.get(id=id)
    qid = request.session['qid']
    return render(request,"customer/edit_qtn.html",{"view":view,'qid':qid})

def edit_question_post(request,id,qid):
    request.session['qid']=qid

    print("qid",qid)
    qtn = request.POST['textfield']
    opt_a = request.POST['textfield2']
    opt_b = request.POST['textfield3']
    opt_c = request.POST['textfield4']
    opt_d = request.POST['textfield5']
    ans = request.POST['select']

    if ans == 'OPTION A':
        question.objects.filter(id =id).update(answers = opt_a)

    elif ans == 'OPTION B':
        question.objects.filter(id=id).update(answers=opt_b)

    elif ans == 'OPTION C':
        question.objects.filter(id=id).update(answers=opt_c)

    else:
        question.objects.filter(id=id).update(answers=opt_d)

    question.objects.filter(id=id).update(questions=qtn, option_a=opt_a, option_b=opt_b, option_c=opt_c, option_d=opt_d,)

    return HttpResponse(f'<script>alert("Edited successfully");window.location="/view_question/'+str(qid)+'#aa"</script>')

def delete_qtn(request,id):
    qid = request.session['qid']
    question.objects.get(id=id).delete()

    return HttpResponse('<script>alert("deleted successfully");window.location="/view_question/'+str(qid)+'#aa"</script>')

def score(request,id):
    try:
        res=result.objects.get(ONLINE_BOOK =id,CUSTOMER = request.session['cid'])
        return render(request,"customer/score.html",{'data':res})
    except:
        return HttpResponse('<script>alert("you have not attended any questions");window.location="/cs_academicbk_view/' + str(id) + '#cc"</script>')

def attend_qtn(request, id):
    try:
        res = question.objects.filter(Q(ONLINE_BOOK_id=id),
                                      ~Q(CUSTOMER=customer.objects.get(LOGIN_id=request.session['lid'])))[0]
        request.session['cnt'] = 0
        request.session['score'] = 0
        return render(request, "customer/attend_qtn.html", {'data': res, 'score': request.session['score'], 'id': id})
    except:
        return HttpResponse('<script>alert("No one has entered questions for this book");window.location="/cs_academicbk_view/'+str(id)+'#cc"</script>')


def attend_qtn_post(request, id):
    res=question.objects.filter(ONLINE_BOOK_id=id)
    corr_ans = request.POST['ans']
    ans = request.POST['radio']
    if corr_ans == ans:
        scr=request.session['score']
        request.session['score']=int(scr)+1
    request.session['cnt']=int(request.session['cnt'])+1
    if int(request.session['cnt'])<len(res):
        return render(request, "customer/attend_qtn.html",
                      {'data': res[int(request.session['cnt'])], 'score': request.session['score'], 'id': id})
    else:
        res2=result.objects.filter(ONLINE_BOOK_id=id, CUSTOMER__LOGIN_id=request.session['lid'])
        if res2.exists():
            res2=res2[0]
        else:
            res2=result()
        res2.date=datetime.datetime.now().date()
        res2.marks=request.session['score']
        res2.ONLINE_BOOK_id=id
        res2.CUSTOMER=customer.objects.get(LOGIN_id=request.session['lid'])
        res2.save()
        return HttpResponse('<script>alert("Score updated");window.location="/cs_academicbk_view/'+str(id)+'#cc"</script>')


def view_mythoughtwaves(request,id):
    res=cust_thoughtwaves.objects.filter(CUSTOMER=request.session['cid'],id=id)
    for i in res:
        i.like = like.objects.filter(THOUGHTNAME=i.id).count()
    return render(request,"customer/mythoughtwaves_view.html",{'data':res})

def add_mythoughtwaves(request):
    return render(request,"customer/mythoughtwaves_add.html")

def add_mythoughtwaves_post(request):
    title=request.POST['textfield']
    content=request.POST['textarea']
    category=request.POST['select']
    image1 = request.FILES['image']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image1)
    path = "/static/image/" + d + ".jpg"

    obj=cust_thoughtwaves()
    obj.thoughtname=title
    obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
    obj.content=content
    obj.image = path
    obj.publish_date = datetime.datetime.now()
    obj.category=category
    obj.save()
    return HttpResponse("<script>alert('uploaded');window.location='/mythoughtwave_frontview'</script>")

def edit_mythoughtwaves(request,id):
    view=cust_thoughtwaves.objects.get(id=id)
    return render(request,"customer/mythoughtwave_edit.html",{"view":view})
def edit_mythoughtwaves_post(request,id):
    try:
        title = request.POST['textfield']
        content = request.POST['textarea']
        category = request.POST['select']
        image1 = request.FILES['image']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\image\\" + d + ".jpg", image1)
        path = "/static/image/" + d + ".jpg"
        cust_thoughtwaves.objects.filter(id=id).update(thoughtname = title,content = content,category=category,publish_date = datetime.datetime.now(),image=path)
        return HttpResponse('<script>alert(" edit successfully");window.location="/mythoughtwave_frontview"</script>')
    except Exception as e:
        title = request.POST['textfield']
        content = request.POST['textarea']
        category = request.POST['select']
        cust_thoughtwaves.objects.filter(id=id).update(thoughtname = title,content = content,category=category,publish_date = datetime.datetime.now())
        return HttpResponse('<script>alert(" edit successfully");window.location="/mythoughtwave_frontview"</script>')


def delete_mythoughtwaves(request,id):
    cust_thoughtwaves.objects.get(id=id).delete()
    return HttpResponse('<script>alert("deleted successfully");window.location="/mythoughtwave_frontview"</script>')

def mythoughtwave_frontview(request):
    res=cust_thoughtwaves.objects.filter(CUSTOMER__LOGIN_id=request.session['lid'])
    return render(request,"customer/mythoughtwave_frontview.html",{'data':res})

def all_thoughtwaves(request,id):
    res = cust_thoughtwaves.objects.filter(id=id)
    cur_cust = customer.objects.get(LOGIN=request.session['lid'])
    for i in res:
        i.like = like.objects.filter(THOUGHTNAME=i.id).count()
        like_new = like.objects.filter(THOUGHTNAME=i.id,CUSTOMER = request.session['cid'])
        if like_new.exists():
            i.flag = 1
        else:
            i.flag = 0

    return render(request, "customer/view_allthoughtwave.html", {'data': res, 'id': cur_cust})

def allthoughtwave_frontview(request):
    res=cust_thoughtwaves.objects.all()
    return render(request,"customer/all_thoughtwave_frontview.html",{'data':res})

def add_comment(request,id):
    request.session['tid'] = id
    res = comment.objects.filter(THOUGHTNAME_id=id)
    data1 = comment.objects.filter(CUSTOMER = request.session['cid'],THOUGHTNAME_id=id)
    if data1.exists():
        flag = 1
    else:
        flag = 0
    return render(request, "customer/tw_comment_add.html",{'res':res,'id':id,'flag':flag})

def add_comment_post(request,id):
    tid = request.session['tid']
    cmt=request.POST['textarea']

    obj=comment()
    obj.THOUGHTNAME_id = id
    obj.cmts=cmt
    obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
    obj.date = datetime.datetime.now()
    obj.save()
    return HttpResponse(f'<script>alert("added successfully");window.location="/add_comment/{tid}#aa";</script>')

def delete_comment(request,id):
    tid = request.session['tid']
    comment.objects.get(id=id).delete()
    return HttpResponse(f'<script>alert("deleted successfully");window.location="/add_comment/{tid}#aa";</script>')

def tw_like(request,id):
    obj=like()
    obj.THOUGHTNAME_id = id
    obj.CUSTOMER_id = customer.objects.get(LOGIN = request.session['lid']).id
    obj.date = datetime.datetime.now()
    obj.save()
    return HttpResponse(f'<script>alert("liked");window.location="/all_thoughtwaves/{id}#cc";</script>')

def chatbott(request):
    return render(request, "customer/chatbot.html")

def chatsnd(request):
        m=request.POST['msg']
        obj=chatbot()
        obj.type="user"
        obj.date=datetime.datetime.now().strftime("%Y-%m-%d")
        obj.chat=m
        obj.CUSTOMER_id=request.session['cid']
        obj.save()
        resp=get_Response(m)
        print("Chatbot : ", resp)
        obj = chatbot()
        obj.type = "chatbot"
        obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
        obj.chat = resp
        obj.CUSTOMER_id = request.session['cid']
        obj.save()
        print("DDDDDD")
        return JsonResponse({'status':'ok'})

def chatrply(request):
        res = chatbot.objects.filter(CUSTOMER = request.session['cid'])
        data=[]
        for i in res:
            data.append({'id':i.id, 'message':i.chat, 'date':i.date, 'type':i.type})
        print(data)
        return JsonResponse({'status':"ok", "data":data})

def turn_pages(request,c):
    c= online_book.objects.get(id=c).content
    print(c)

    # # Open the PDF file
    # c = "C:\\Users\\hilus\\PycharmProjects\\eon\\eonapp\\static\\certificate\\"+str(c)
    # import PyPDF2
    #
    # with open(c, 'rb') as f:
    #     reader = PyPDF2.PdfReader(f)
    #     for page in reader.pages:
    #         text = page.extract_text()
    #         print(text)
    #
    #         print()
    #         import pyttsx3
    #
    #         engine = pyttsx3.init()
    #         engine.say(text)
    #         engine.runAndWait()
    return render(request,"customer/pdf_turn_pages.html",{'c':c})
#
#
# # def save_image(request):
# #     if request.method == 'POST' and request.FILES.get('image'):
# #         image = request.FILES['image']
# #         upload_path = os.path.join(r"C:\Users\hilus\PycharmProjects\eon\\", 'captures')
# #         os.makedirs(upload_path, exist_ok=True)
# #         image_path = os.path.join(upload_path, image.name)
# #
# #         with open(image_path, 'wb') as f:
# #             for chunk in image.chunks():
# #                 f.write(chunk)
# #         emotion()
# #         return JsonResponse({"message": "Image saved successfully!", "path": image_path})
# #     return JsonResponse({"error": "Invalid request"}, status=400)
# import cv2
# def emot_rec(request):
#     cam=cv2.VideoCapture(0)
#     ok, frame=cam.read()
#     em=""
#     res=""
#     if ok:
#         cv2.imwrite(r"C:\Users\hilus\PycharmProjects\eon\captures\webcam_capture.png", frame)
#         em=emotion()
#         print(em)
#         cam.release()
#         res=online_book.objects.filter(emotion=em, type="non-academic")
#     return render(request, "customer/recommendation.html", {'em':em, "data":res})
#
#
# def emotion():
#     from tensorflow.keras.models import Sequential
#     from tensorflow.keras.layers import Dense, Dropout, Flatten
#     from tensorflow.keras.layers import Conv2D
#     from tensorflow.keras.optimizers import Adam
#     from tensorflow.keras.layers import MaxPooling2D
#     from tensorflow.keras.preprocessing.image import ImageDataGenerator
#     import os
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#
#     import cv2
#     ####emotion finding
#     import requests
#
#     import cv2
#     model = Sequential()
#
#     model.add(
#         Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
#     model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#
#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#
#     model.add(Flatten())
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(7, activation='softmax'))
#
#     model.load_weights(r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\model.h5')
#
#     # prevents openCL usage and unnecessary logging messages
#     cv2.ocl.setUseOpenCL(False)
#
#     # dictionary which assigns each label an emotion (alphabetical order)
#     emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral",
#                     5: "Sad",
#                     6: "Surprised"}
#
#     frame = cv2.imread( r"C:\Users\hilus\PycharmProjects\eon\captures\webcam_capture.png")
#
#     facecasc = cv2.CascadeClassifier(r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#     print("Faces", len(faces))
#
#     import numpy as np
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
#         roi_gray = gray[y:y + h, x:x + w]
#         cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
#         prediction = model.predict(cropped_img)
#         print(prediction, "prediction")
#         maxindex = int(np.argmax(prediction))
#         res_emo = emotion_dict[maxindex]
#         print(res_emo, max(prediction[0]), "eeeeeeeeeeeeeeeeee")
#
#         return res_emo
#
#
#
# def emotion2():
#     import os
#     import cv2
#     import numpy as np
#     from tensorflow.keras.models import Sequential
#     from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
#
#     # Suppress TensorFlow logging and OpenCL usage
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#     cv2.ocl.setUseOpenCL(False)
#
#     # Initialize the emotion recognition model
#     model = Sequential()
#
#     # Model architecture
#     model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
#     model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#
#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#
#     model.add(Flatten())
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(7, activation='softmax'))
#
#     # Load pre-trained weights
#     model_path = r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\model.h5'
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"Model file not found at: {model_path}")
#     model.load_weights(model_path)
#
#     # Emotion dictionary
#     emotion_dict = {
#         0: "Angry",
#         1: "Disgusted",
#         2: "Fearful",
#         3: "Happy",
#         4: "Neutral",
#         5: "Sad",
#         6: "Surprised"
#     }
#
#     # Haar cascade file path
#     haar_cascade_path = r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\haarcascade_frontalface_default.xml'
#     if not os.path.exists(haar_cascade_path):
#         raise FileNotFoundError(f"Haar Cascade XML file not found at: {haar_cascade_path}")
#     face_cascade = cv2.CascadeClassifier(haar_cascade_path)
#
#     # Input image path
#     image_path = r"C:\Users\hilus\PycharmProjects\eon\captures\webcam_capture.png"
#     frame = cv2.imread(image_path)
#     if frame is None:
#         raise FileNotFoundError(f"Image not found or could not be loaded at: {image_path}")
#
#     # Convert image to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#
#     # Process each face
#     for (x, y, w, h) in faces:
#         # Draw rectangle around the face
#         cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
#
#         # Crop and preprocess the face region
#         roi_gray = gray[y:y + h, x:x + w]
#         cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
#
#         # Predict emotion
#         prediction = model.predict(cropped_img)
#         maxindex = int(np.argmax(prediction))
#         res_emo = emotion_dict[maxindex]
#
#         # Display the detected emotion
#         print(f"Detected Emotion: {res_emo}")
#         return res_emo
#
#         # Display the output (optional)
#         # cv2.imshow('Emotion Detection', frame)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()

def payment(request,id,amt):
    request.session['oid']=id
    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount = float(amt)*100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],

    }

    if customer_order.objects.filter(id = id).exists():
        customer_order.objects.filter(id=id).update(paymentmethod="online", paymentstatus="paid")

    else:

        seller_order.objects.filter(id=id).update(paymentmethod="online", paymentstatus="paid")




    return render(request, 'customer/payment.html',{'razorpay_api_key': razorpay_api_key,
                                            'amount': order_data['amount'],
                                            'currency': order_data['currency'],
                                            'order_id': order['id']})