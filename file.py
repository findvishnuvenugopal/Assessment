#Task 1

def registration(request):
    if request.method=='POST':
        name=request.POST['name']
        address=request.POST['address']
        phno=request.POST['number']
        email=request.POST['email']
        password=request.POST['password']
        confpassword=request.POST['confirm password']
        emailExist=customer.objects.filter(email=email)
        phnoExist=customer.objects.filter(phno=phno)
        if emailExist:
            messages.info(request,'email already exist')
            return render(request,'registration.html') 
        elif phnoExist:
            messages.info(request,'this phno is already exist')
            return render(request,'registration.html')
        elif password!=confpassword:
            messages.info(request,'your password and confirm password is incorrect')
            return render(request,'registration.html')
        else:
            customer(name=name,address=address,phno=phno,email=email,password=password,confpassword=confpassword).save()
            
    return render(request,'registration.html')
def login(request):
    if request.method=='POST':
        try:
            customerdetails=customer.objects.get(email=request.POST['email'],password=request.POST['password'])
            request.session['email']=customerdetails.email
            return redirect('/')
        except customer.DoesNotExist as e:
            messages.info(request,'your email and password is incorrect')
            return render(request,'login.html')
    return render(request,'login.html')



#Task2

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    products=get_object_or_404(product,id=product_id)
    item_already_in_cart=Cart.objects.filter(products=product_id,user=user)
    if item_already_in_cart:
        cp=get_object_or_404(Cart,products=product_id,user=user)
        cp.quantity +=1
        cp.save()
    else:
        Cart(user=user,products=products).save()
    return redirect('shopingcart')


@login_required
def shopingcart(request):
    user=request.user
    cart_products=Cart.objects.filter(user=user)
    amount=decimal.Decimal(0)
    shipping_amount=decimal.Decimal(10)
    cp=[p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount=(p.quantity*p.products.price)
            amount += temp_amount

    context={
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount+shipping_amount,
    }
    return render(request,'shoping-cart.html',context)

#task3

@login_required
def pluscart(request,cart_id):
    if request.method=='GET':
        cp=get_object_or_404(Cart,id=cart_id)
        cp.quantity +=1
        if cp.quantity>=cp.products.productStock:
            cp.quantity -=1
        cp.save()
    return redirect('shopingcart')

@login_required
def minuscart(request,cart_id):
    if request.method=='GET':
        cp=get_object_or_404(Cart,id=cart_id)
        if cp.quantity==1:
            cp.delete()
        else:
            cp.quantity-=1
            cp.save()
    return redirect('shopingcart')
@login_required
def delete(request,cart_id):
    if request.method=='GET':
        cp=get_object_or_404(Cart,id=cart_id)
        cp.delete()
    return redirect('shopingcart')
