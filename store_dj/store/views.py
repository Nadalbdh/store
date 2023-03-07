from ast import Or
from http.client import HTTPResponse
from unicodedata import category
from django.shortcuts import HttpResponse
from itertools import product
from multiprocessing import context
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
import json
import datetime
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from store.forms import  CommentForm, CreateUserForm
from store.models import *

# Create your views here.

def store(request):
	if request.user.is_authenticated:
		customer=request.user
		order , created = Order.objects.get_or_create ( customer=customer , complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_items':0,'get_cart_total':0,'shipping':False}
		cartItems = order['get_cart_items']
	products=Product.objects.all()
	context= {'products':products,'cartItems':cartItems}
	return render(request,'store/store.html',context )

def home(request):
	if request.user.is_authenticated:
		customer=request.user
		order , created = Order.objects.get_or_create ( customer=customer , complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_items':0,'get_cart_total':0,'shipping':False}
		cartItems = order['get_cart_items']
	products=Product.objects.all()[:4]
	articles=Post.objects.all()[:3]
	context= {'articles':articles,'products':products,'cartItems':cartItems}
	return render(request,'store/home.html',context)

def product(request,slug):
	#te3 product detaillé
	print('Product slug',slug)
	product=get_object_or_404(Product,slug=slug)
	related_products=Product.objects.filter(category=product.category)[:4]
	context={'product':product,'related_products':related_products}
	return render (request,'store/product.html',context)

def blog_article(request,slug):
	#te3 post detaillé
	print('post slug',slug)
	post=get_object_or_404(Post,slug=slug)
	form = CommentForm(request.POST,instance=post)
	if (request.method == 'POST'): 
		if (form.is_valid):
			body=form.cleaned_data['body']
			print(body)
			c = Comment(post=post,body=body,date_commented=datetime.now())
			c.save()
			return redirect ('store/blog_article.html')
		else:
			print('form is invalid')

	context={'post':post ,'form':form}
	return render (request,'store/blog_article.html',context)

def blog(request):
	posts=Post.objects.all()
	context= {'posts':posts}
	return render(request,'store/blog.html',context)

def contact(request):
	return render(request,'store/contact.html')
def cart(request):
	#cart o payement wkol maysyro ken b customer is already connected sinn yatl3o 0
	if request.user.is_authenticated:
		customer=request.user
		order , created = Order.objects.get_or_create ( customer=customer , complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_items':0,'get_cart_total':0,'shipping':False}
		cartItems = order['get_cart_items']
	context= {'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/cart.html',context )

def checkout(request):
	if request.user.is_authenticated:
		customer=request.user
		order , created = Order.objects.get_or_create ( customer=customer , complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items=[]
		order={'get_cart_items':0,'get_cart_total':0,'shipping':False}
		cartItems = order['get_cart_items']
	context= {'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/checkout.html',context )

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print ('Action : ',action)
	print ('productId : ',productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order , created = Order.objects.get_or_create ( customer=customer , complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
	if (action== 'add'):
		orderItem.quantity = (orderItem.quantity + 1)
	elif (action == 'remove'):
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added',safe=False)

def processOrder(request):
	print('Data',request.body)
	transaction_id=datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user
		order , created = Order.objects.get_or_create ( customer=customer , complete=False)
		total = float(data['form']['total'])
		order.transaction_id=transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
	
	else:
		print ('User is not logged in.. ')
	return JsonResponse('Payment complete !',safe=False)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'auth/login.html', context)
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')
			

		context = {'form':form}
		return render(request, 'auth/register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

