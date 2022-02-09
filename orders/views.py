
import json

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.generic import View

from django.shortcuts import render, redirect
from django.template import Context, Template
from django.forms.models import model_to_dict

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



from django.core import serializers

from .models import Salad, Subs, Pizza, Pasta, Orders, Toppings

session_items = []
new_item = {}

class SendTops(View):
    def get(self, request):
        
        if request.method == "GET":

            toppings_all = Toppings.objects.all()
            toppings = serializers.serialize('json', toppings_all)
            raw_data = json.loads(toppings)
            data = dict()
            for d in raw_data:
                data[d["pk"]] = {
                    "topping": d["fields"]["topping"],
                    "type": d["fields"]["topping_type"]
                    
                    }
        return JsonResponse(data)
    

class GetSession(View):
    def post(self, request):
        if request.method == "POST":
            name = json.loads(request.body).get('name')
            pk = json.loads(request.body).get('pk')
            size = json.loads(request.body).get('size')
            price = json.loads(request.body).get('price')
            options = json.loads(request.body).get('options')
            
            new_item = {
                "name": name,
                "pk": pk,
                "size": size,
                "price": price,
                "options": options
            }
            session_items.append(new_item)
            request.session["allthe_items"] = session_items
            
        return HttpResponse()

class GetPz(View):
   def post(self, request):
        if request.method == "POST":
            size = json.loads(request.body).get('size')
            price = json.loads(request.body).get('price')
            name = json.loads(request.body).get('name')
            pk = json.loads(request.body).get('pk')
                
            new_item = {
                "name": name,
                "price": price,
                "size": size.lower(),
                "pk": pk,
                "options": []
            }
            request.session["current"] = new_item
        return HttpResponse() 
        
class SendSession(View):
    def get(self, request):
        
        if request.method == "GET" and request.session["current"]:

            data = request.session["current"] 
        return JsonResponse(data)

class GetFd(View):
    def post(self, request):
        if request.method == "POST":
            name = json.loads(request.body).get('name')
            price = json.loads(request.body).get('price')
            size = json.loads(request.body).get('size')
            pk = json.loads(request.body).get('pk')
            if size is None:
                new_item = {
                    "name": name,
                    "price": price,
                    "pk": pk
                }
                session_items.append(new_item)
                request.session["allthe_items"] = session_items
            else:
                new_item = {
                    "name": name,
                    "price": price,
                    "size": size.lower(),
                    "pk": pk
                }
                session_items.append(new_item)
                request.session["allthe_items"] = session_items
            
            
        return HttpResponse()


#TEST TEST TEST TEST TEST
def test(request):
    request.session["allthe_items"] 
    request.session["thing"] 

    test1 = request.session["allthe_items"] 
    test2 = request.session["current"]


    context = {
        "test1": test1,
        "test2": test2,
        

        }
    
    return render(request, "orders/test.html", context)
#TEST TEST TEST TEST TEST



# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def home(request):
    return render(request, "orders/index.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "nzielln":
                        
            return redirect("orders")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["username"] = request.user.username
            request.session["name"] = request.user.first_name
            return redirect("profile")
        
    return render(request, "orders/signin.html")

def signup(request):
    
    if request.method == "GET":
        logout(request)
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        if password == re_password:

            user = User.objects.create_user(username, email, password)
            user.save()
            request.session["username"] = username    
            
            return redirect("info")        

        
    return render(request, "orders/signup.html")


def info(request):
    username = request.session["username"]
    user_get = User.objects.get(username=username)


    if request.method == "POST":
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        user_get.first_name = firstname
        user_get.last_name = lastname
        user_get.save()
        request.session["name"] = firstname
        return redirect("pizza")
        
    return render(request, "orders/info.html")

def logout_user(request):
    if request.method == "GET":
        logout(request)
        allthe_items = []
        session_items = []
        request.session["allthe_items"] = session_items
    return render(request, "orders/index.html")

@login_required(login_url='login')
def profile(request):
    username = "None"
    if request.method == "GET":
        username = request.session["username"]
        name = request.session["name"]
        if request.user.is_authenticated:
            username = request.user.username
            name = request.user.first_name
    
        orders = Orders.objects.all()
        
    something = request.session["username"]
        
    context = {
        "name": name,
        "username": username,

        "orders": orders
    }
        
    return render(request, "orders/profile.html", context)

@login_required(login_url='login')
def success(request):
    allthe_items = request.session["allthe_items"]
    order_price = []
    order_items = []
    order_list = []
    
    
    if request.method == "GET":
        for d in allthe_items:
            order_price.append(int(float(d["price"][1:])))
            order_items.append(d)
        username = request.session["username"]
        order = {
            "items": order_items,
            "price": sum(order_price)
                
        }
        
        new_order = Orders.objects.create(username=username, order=order, status="Not Complete")
        new_order.save()
        order_list.append(order_price)
        order_list.append(order_items)
        allthe_items = []
        session_items = []
        request.session["allthe_items"] = session_items

    return render(request, "orders/success.html")
    
def options(request, item_name, item_id):
    #add toppings
    meat = list()
    veg = list()
    other = list()
    item = Toppings.objects.all()
    
    for i in item:
        if i.topping_type == "Meat":
            meat.append(i)
        elif i.topping_type == "Other":
            other.append(i)
        else:
            veg.append(i)
    
    main_item = Pizza.objects.get(pk=item_id)
        
                
    context = {
        "meat": meat,
        "veg": veg,
        "other": other,
        "main": main_item,

    }
            
    return render(request, "orders/options.html", context)
#send_pizza

def pizza_menu(request):
    data = Pizza.objects.all()
    """ items = dict()

    for d in data:
        items[d.name] = d """

    items = serializers.serialize('json', data)
    the_data = json.loads(items)
    datas = json.dumps(the_data)
        
    context = {
        "pizzas": Pizza.objects.all(),
        "data": datas
    }
    return render(request, "orders/pizza_menu.html", context)

def subs_menu(request):
    context = {
        "subs": Subs.objects.all(),
    }
    return render(request, "orders/subs_menu.html", context)

def pasta_menu(request):
    context = {
        "pastas": Pasta.objects.all(),
    }
    return render(request, "orders/pasta_menu.html", context)

def salad_menu(request):
    context = {
        "salads": Salad.objects.all(),
    }
    return render(request, "orders/salad_menu.html", context)

def order(request, order_pk):
    the_order = Orders.objects.get(pk=order_pk)
    
    the_items = the_order.order["items"]
    the_price = the_order.order["price"]
    
    context = {
        "orders": the_order
    }
        
        
    return render(request, "orders/order.html", context)

def cart(request): 
    request.session.modified = True
 
    prices = []
    new_prices = []
    new_price = int()
    
    if request.session["allthe_items"]:
            for item in request.session["allthe_items"]:
            #pasta and salads, no sizes
                if item["name"] == "Regular" or item["name"] == "Sicilian":
                    get_item = Pizza.objects.get(pk=item["pk"])
                    if item["size"] == "small":
                        new_price = get_item.small
                    elif item["size"] == "large":
                        new_price = get_item.large
                    new_prices.append(new_price)
                elif item["name"] == "Antipasto" or "Salad" in item["name"]:
                    get_item = Salad.objects.get(pk=item["pk"])
                    new_price = get_item.price
                    new_prices.append(new_price)
                elif "Baked" in item["name"]:
                    get_item = Pasta.objects.get(pk=item["pk"])
                    new_price = get_item.price
                    new_prices.append(new_price)
                else:
                    get_item = Subs.objects.get(name=item["name"])
                    if item["size"] == "small":
                        new_price = get_item.small
                    elif item["size"] == "large":
                        new_price = get_item.large
                    new_prices.append(new_price)
                all_items = request.session["allthe_items"]
    if not request.session["allthe_items"]:
        all_items = None
        return redirect("pizza")

    context = {
        "items" : all_items,
        "sum" : sum(new_prices),
       
    } 
    
    return render(request, "orders/cart.html", context)

def remove(request, item_name, item_id):
    request.session.modified = True

    new_prices = []
    new_price = int()
    all_items = request.session["allthe_items"]
    theid = item_id
    
    
    for item in range(len(all_items)):
        if all_items[item]["name"] == item_name:
            del all_items[item]
            break
            request.session["allthe_items"] = all_items
            
        if all_items[item]["name"] == item_name and all_items[item]["pk"] == item_id:
            del all_items[item]
            break
            request.session["allthe_items"] = all_items
                

                    
    if request.session["allthe_items"]:
            for item in all_items:
            #pasta and salads, no sizes
                if item["name"] == "Regular" or item["name"] == "Sicilian":
                    get_item = Pizza.objects.get(pk=item["pk"])
                    if item["size"] == "small":
                        new_price = get_item.small
                    elif item["size"] == "large":
                        new_price = get_item.large
                    new_prices.append(new_price)
                elif item["name"] == "Antipasto" or "Salad" in item["name"]:
                    get_item = Salad.objects.get(pk=item["pk"])
                    new_price = get_item.price
                    new_prices.append(new_price)
                elif "Baked" in item["name"]:
                    get_item = Pasta.objects.get(pk=item["pk"])
                    new_price = get_item.price
                    new_prices.append(new_price)
                else:
                    get_item = Subs.objects.get(name=item["name"])
                    if item["size"] == "small":
                        new_price = get_item.small
                    elif item["size"] == "large":
                        new_price = get_item.large
                    new_prices.append(new_price)
    
                    
    
    context = {
        "items" : all_items,
        "sum" : sum(new_prices)
    }
    
    return redirect('cart')

@login_required(login_url='login')
def orders(request):
    if request.method == "GET":
        orders = Orders.objects.all()
                
    context = {
        "orders": orders
    }
        
    return render(request, "orders/orders.html", context)

class Status(View):
    def post(self, request):
        if request.method == "POST":
            status = json.loads(request.body).get("status")
            pk = json.loads(request.body).get("pk")
            
            order = Orders.objects.get(pk=pk)
            order.status = "Complete"
            order.save()
            
            
            return HttpResponse()
