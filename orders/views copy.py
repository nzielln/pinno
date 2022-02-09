
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from django.shortcuts import render
from django.template import Context, Template
import json
from django.forms.models import model_to_dict



from django.core import serializers


from .models import Salad, Subs, Pizza, Pasta, Orders, Toppings
#AJAX

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
    

session_items = []
new_item = {}
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
    

class GetFd(View):
    def post(self, request):
        
        if request.method == "POST":
            
            name = json.loads(request.body).get('name')
            price = json.loads(request.body).get('price')
            size = json.loads(request.body).get('size')
            pk = json.loads(request.body).get('pk')

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
    request.session["some"] 
    request.session["thing"] 

    test1 = request.session["some"]
    test2 = request.session["thing"]


    context = {
        "test1": test1,
        "test2": test2

        }
    
    return render(request, "orders/test.html", context)
#TEST TEST TEST TEST TEST

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def home(request):
    return render(request, "orders/index.html")

def login(request):
    return render(request, "orders/signin.html")

def signup(request):
    return render(request, "orders/signup.html")

def info(request):
    return render(request, "orders/info.html")

def profile(request):
    return render(request, "orders/profile.html")

def success(request):
    return render(request, "orders/success.html")

class SendSession(View):
    def get(self, request):
        request.session["current"]
        
        if request.method == "GET" and request.session["current"]:

            data = request.session["current"] 
        return JsonResponse(data)
    
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
    
    request.session["pizza"] 
    request.session["sub"] 
    request.session["pasta"] 
    request.session["salad"] 
    
    new = {}
    
    cart_items = request.session["items"]
    pizza_list = request.session["pizza"]
    pasta_list = request.session["pasta"]
    salad_list = request.session["salad"]
    sub_list = request.session["sub"]

    
    if request.method == "GET":
        #pizza
        if item_name == "Regular" or item_name == "Sicilian":
            if item_id not in request.session["pizza"]:
                pizza_list.append(item_id)
                request.session["pizza"] = pizza_list
                main_item = Pizza.objects.get(pk=item_id)
                
            else: 
                request.session["pizza"] = pizza_list
            new = {
                "item_name": item_name,
                "pk": item_id,
                "options": []
            }
            request.session["current_item"] = new
            

        #pasta
        elif "Baked" in item_name:
            if item_id not in request.session["pasta"]:
                pasta_list.append(item_id)
                request.session["pasta"] = pasta_list
            else: 
                request.session["pasta"] = pasta_list 
            new = {
                "item_name": item_name,
                "pk": item_id,
                "options": []
            }
            request.session["current_item"] = new
            

        #salad
        elif "Salad" in item_name or item_name == "Antipasto":
            if item_id not in request.session["salad"]:
                salad_list.append(item_id)
                request.session["salad"] = salad_list
            else: 
                request.session["salad"] = salad_list 
            new = {
                "item_name": item_name,
                "pk": item_id,
                "options": []
            }
            request.session["current_item"] = new
            
        #subs and everything else...
        else:
            if item_id not in request.session["sub"]:
                sub_list.append(item_id)
                request.session["sub"] = sub_list
            else: 
                request.session["sub"] = sub_list
                
            new = {
                "item_name": item_name,
                "pk": item_id,
                "options": []
            }
            request.session["current_item"] = new
            
        #item info
        if item_name == "Regular" or item_name == "Sicilian":
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

def order(request):
    return render(request, "orders/order.html")

def cart(request):  
    c = []
    prices = []
    new_prices = []
    new_price = int()
    cart_items = {}
    session_items = request.session["allthe_items"]
    
        
    #get items and add to list
    for an_id in request.session["pizza"]:
        new_item = Pizza.objects.get(pk=an_id)
        c.append(new_item)
    for an_id in request.session["sub"]:
        new_item = Subs.objects.get(pk=an_id)
        c.append(new_item)
    for an_id in request.session["pasta"]:
        new_item = Pasta.objects.get(pk=an_id)
        c.append(new_item)
    for an_id in request.session["salad"]:
        new_item = Salad.objects.get(pk=an_id)
        c.append(new_item)
            

  # get total price
    for item in c:
        #pasta and salads, no sizes
        if item.name == "Antipasto" or "Salad" in item.name or "Baked" in item.name:
            price = item.price
            prices.append(price)
        #subs and pizza, have sizes
        else:
            price = item.small
            prices.append(price)
            
    cart_items["pasta"] = request.session["pasta"]
    cart_items["salad"] = request.session["salad"]
    cart_items["subs"] = request.session["sub"]
    cart_items["pizza"] = request.session["pizza"]
    request.session["items"] = cart_items

    
    itemss = request.session["items"]
    
    if request.session["allthe_items"]:
            all_items = request.session["allthe_items"]
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
        "sum" : sum(new_prices),
       
    } 
    
    return render(request, "orders/cart.html", context)

def remove(request, item_name, item_id):
    # variables
    ''' ["new_item_pending"] = {
        "item_name":
        "item_pk":
        "price":
        "":
        
    } '''
    c = []
    new_prices = []
    new_price = int()
    session_items = request.session["allthe_items"]

    
    cart_items = request.session["items"]
    pizza_list = request.session["pizza"]
    pasta_list = request.session["pasta"]
    salad_list = request.session["salad"]
    sub_list = request.session["sub"]
    all_items = request.session["allthe_items"]
    
    if request.method == "GET":
        # if pizza
        for item in all_items:
            if item["name"] == item_name and item["pk"] == item_id:
                    all_items.remove(item)
                    request.session["allthe_items"] = all_items
                
    if request.session["allthe_items"]:
            all_items = request.session["allthe_items"]
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
                    
    #double check that ids are correct [this if just for me if i get an error]
    cart_items["pasta"] = request.session["pasta"]
    cart_items["salad"] = request.session["salad"]
    cart_items["subs"] = request.session["sub"]
    cart_items["pizza"] = request.session["pizza"]
    request.session["items"] = cart_items

    itemss = request.session["items"]
    
    
    context = {
        "items" : all_items,
        "sum" : sum(new_prices)
    }

    
    
    return render(request, "orders/cart.html", context)
    
