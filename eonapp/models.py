from django.db import models

# Create your models here.
class login(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=50)

class category(models.Model):
    categoryname=models.CharField(max_length=200)
    discription=models.CharField(max_length=500)

class seller(models.Model):
    LOGIN=models.ForeignKey(login,default=1,on_delete=models.CASCADE)
    sellername=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=200)
    place=models.CharField(max_length=200,default=1)
    post=models.CharField(max_length=100,default=1)
    pincode=models.CharField(max_length=200,default=1)
    certificate=models.CharField(max_length=150,default=1)


class book(models.Model):
    book_name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    GENRE=models.ForeignKey(category,default=1,on_delete=models.CASCADE)
    description=models.TextField(max_length=500, blank=True)
    price= models.IntegerField()
    discount=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(login,default=1,on_delete=models.CASCADE)
    image=models.CharField(max_length=100)
    bookcondition=models.CharField(max_length=100)
    type=models.CharField(max_length=100,default=1)
    availability=models.CharField(max_length=300)
    numberofpages=models.CharField(max_length=100)

class online_book(models.Model):
    book_name=models.CharField(max_length=200,default=1)
    author=models.CharField(max_length=200,default=1)
    GENRE=models.ForeignKey(category,default=1,on_delete=models.CASCADE)
    description=models.CharField(max_length=500, blank=True,default=1)
    book_format=models.CharField(max_length=500,default=1)
    image=models.CharField(max_length=100,default=1)
    filesize=models.CharField(max_length=100,default=1)
    language=models.CharField(max_length=100,default=1)
    no_ofpage=models.CharField(max_length=100,default=1)
    upload_date=models.CharField(max_length=200,default=1)
    type=models.CharField(max_length=100,default=1)
    subject=models.CharField(max_length=100,default="")
    content=models.CharField(max_length=3000,default=1)
    emotion=models.CharField(max_length=1000,default="Happy")

class customer(models.Model):
    image=models.CharField(max_length=200,default=1)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    dob = models.CharField(max_length=200)
    age=models.CharField(max_length=200,default=1)
    gender=models.CharField(max_length=200,default=1)
    email=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=200)
    place=models.CharField(max_length=200,default=1)
    post=models.CharField(max_length=200,default=1)
    pin=models.CharField(max_length=200,default=1)
    LOGIN=models.ForeignKey(login,default=1,on_delete=models.CASCADE)

class customer_order(models.Model):
    CUSTOMER=models.ForeignKey(customer,related_name='cs1',default=1,on_delete=models.CASCADE)
    CUSTOMER_se=models.ForeignKey(customer,related_name='cs2',default=1,on_delete=models.CASCADE)
    date=models.CharField(max_length=200)
    orderstatus=models.CharField(max_length=200)
    paymentstatus=models.CharField(max_length=200)
    paymentmethod=models.CharField(max_length=200)
    totalamount=models.CharField(max_length=200)
    discount=models.CharField(max_length=200)
    city = models.CharField(max_length=200, default=1)
    state = models.CharField(max_length=200, default=1)
    colony = models.CharField(max_length=200, default=1)
    house = models.CharField(max_length=200, default=1)
    pin=models.CharField(max_length=200,default=1)
    deliverydate=models.CharField(max_length=200)
    # return_or_refund=models.CharField(max_length=200)
    # ordernotes=models.CharField(max_length=200)
    ordercancellationreason=models.CharField(max_length=200)

class customer_order_sub(models.Model):
    CUSTOMER_ORDER=models.ForeignKey(customer_order, default=1, on_delete=models.CASCADE)
    BOOK=models.ForeignKey(book, default=1, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=100)

class cust_thoughtwaves(models.Model):
    thoughtname=models.CharField(max_length=200)
    content=models.CharField(max_length=20000, default=1)
    CUSTOMER=models.ForeignKey(customer,default=1,on_delete=models.CASCADE)
    category=models.CharField(max_length=20000, default=1)
    publish_date=models.CharField(max_length=200,default=1)
    image= models.CharField(max_length=100)

class appvdseller(models.Model):
    SELLER=models.ForeignKey(seller,default=1,on_delete=models.CASCADE)
    email=models.CharField(max_length=200)
    phno=models.CharField(max_length=200)

class cart(models.Model):
    CUSTOMER = models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
    BOOK= models.ForeignKey(book, default=1, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class like(models.Model):
    THOUGHTNAME=models.ForeignKey(cust_thoughtwaves, default=1, on_delete=models.CASCADE)
    CUSTOMER=models.ForeignKey(customer, default=1, on_delete=models.CASCADE)

class comment(models.Model):
    THOUGHTNAME = models.ForeignKey(cust_thoughtwaves, default=1, on_delete=models.CASCADE)
    CUSTOMER = models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
    # CONTENT = models.ForeignKey(content, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    cmts=models.CharField(max_length=100, default=1)

class seller_order(models.Model):
    CUSTOMER=models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
    SELLER=models.ForeignKey(seller, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=200,default=1)
    orderstatus = models.CharField(max_length=200)
    paymentstatus = models.CharField(max_length=200,default=1)
    paymentmethod = models.CharField(max_length=200,default=1)
    totalamount = models.CharField(max_length=200,default=1)
    discount = models.CharField(max_length=200,default=1)
    city = models.CharField(max_length=200, default=1)
    state = models.CharField(max_length=200, default=1)
    colony = models.CharField(max_length=200, default=1)
    house = models.CharField(max_length=200, default=1)
    pin = models.CharField(max_length=200, default=1)
    deliverydate = models.CharField(max_length=200,default=1)
    # return_or_refund = models.CharField(max_length=200,default=1)
    # ordernotes = models.CharField(max_length=200,default=1)
    # customerfdbck=models.CharField(max_length=200,default=1)
    ordercnclreason=models.CharField(max_length=200,default=1)

class order_sub(models.Model):
    SELLER_ORDER=models.ForeignKey(seller_order, default=1, on_delete=models.CASCADE)
    BOOK=models.ForeignKey(book, default=1, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=100)

class question(models.Model):
    ONLINE_BOOK=models.ForeignKey(online_book,default=1,on_delete=models.CASCADE)
    option_a=models.CharField(max_length=100,default=1)
    option_b=models.CharField(max_length=100,default=1)
    option_c=models.CharField(max_length=100,default=1)
    option_d=models.CharField(max_length=100,default=1)
    questions=models.CharField(max_length=1000)
    answers=models.CharField(max_length=1000)
    CUSTOMER = models.ForeignKey(customer, default=1, on_delete=models.CASCADE)

class chatbot(models.Model):
    chat=models.TextField(max_length=100)
    date=models.CharField(max_length=100, default="")
    CUSTOMER=models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
    type=models.CharField(max_length=100,default=1)

class reply(models.Model):
    rply=models.CharField(max_length=300)

class review(models.Model):
    date = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer,default=1, on_delete=models.CASCADE)
    revw = models.CharField(max_length=200)
    BOOK = models.ForeignKey(book, default=1, on_delete=models.CASCADE)
    rating = models.CharField(max_length=200)

class onlinebk_review(models.Model):
    date = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
    revw = models.CharField(max_length=200)
    ONLINE_BOOK = models.ForeignKey(online_book, default=1, on_delete=models.CASCADE)
    rating = models.CharField(max_length=200)

class result(models.Model):
    ONLINE_BOOK=models.ForeignKey(online_book,default=1,on_delete=models.CASCADE)
    marks=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer, default=1, on_delete=models.CASCADE)
