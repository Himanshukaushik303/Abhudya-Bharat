from AB import settings
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required

# Create your views here.

# Register page for user to sign up
@logindirect()
def registerPage(request):

    form = CreateUserForm()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email-id already exists.")
                return redirect("register")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")
    context = {"form": form}
    return render(request, "website/register.html", context)


# Login page
@logindirect()
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            settings.LOGIN_REDIRECT_URL = "products"
            login(request, user)
        else:
            messages.info(request, "Username OR password is incorrect")
    context = {}
    return render(request, "website/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


# Homepage
def homepage(request):
    return render(request, "website/baselayout.html", context={})


# About page
def about(request):
    return render(request, "website//about.html", context={})


# Register as an Entrepreneur. Page with form.
@login_required(login_url="login")
@allowed_users()
def addEnt(request):
    entform = AddEnterpreneur()
    if request.method == "POST":
        print(entform.errors)
        entform = AddEnterpreneur(request.POST, request.FILES)
        print(entform.errors)
        if entform.is_valid():
            ent = entform.save(commit=False)
            ent.user = request.user
            group = Group.objects.get(name="pending_ents")
            request.user.groups.add(group)
            ent.save()

        return redirect("conf")

    return render(request, "website/entrepreneurs.html", context={"form": entform})


# Edit Page for entrepreneurs to update personal details.
@login_required(login_url="login")
@allowed_roles(roles=["active_ents"])
def edit_ent(request):
    ent = request.user.ent
    entform = AddEnterpreneur(instance=ent)
    if request.method == "POST":
        print(entform.errors)
        entform = AddEnterpreneur(request.POST, request.FILES, instance=ent)
        print(entform.errors)
        if entform.is_valid():
            entform.save()

        return redirect("ent_dash")

    return render(request, "website/entrepreneurs.html", context={"form": entform})


# Register as a Bussiness Partner. Page with form.
@login_required(login_url="login")
@allowed_users()
def addPart(request):
    partform = AddPartner()
    if request.method == "POST":
        partform = AddPartner(request.POST)
        print(partform.errors)
        if partform.is_valid():
            bp = partform.save(commit=False)
            bp.user = request.user
            group = Group.objects.get(name="pending_bps")
            request.user.groups.add(group)
            bp.save()

            return redirect(
                "conf",
            )
    return render(request, "website/partners.html", context={"form": partform})


# Add products to database can only be done by active Bussiness Partners.
@login_required(login_url="login")
@allowed_roles(roles=["active_bps"])
def addProd(request):
    bp = request.user.bp
    prodform = AddProduct()
    image_formset = modelformset_factory(Product_Image, form=Addimages, extra=2)
    faq_formset = modelformset_factory(FAQ, form=Addfaqs, extra=2)
    imageset = image_formset(queryset=Product_Image.objects.none())
    faqset = faq_formset(queryset=FAQ.objects.none())
    if request.method == "POST":
        prodform = AddProduct(request.POST, request.FILES)
        imageset = image_formset(request.POST, request.FILES)
        faqset = faq_formset(request.POST)
        if prodform.is_valid():
            obj = prodform.save(commit=False)
            obj.company = bp
            obj.save()
            prodform.save_m2m()
            for form in imageset:
                if form.is_valid():
                    item = form.save(commit=False)
                    item.product = obj
                    item.save()

            for form in faqset:
                if form.is_valid():
                    item = form.save(commit=False)
                    item.product = obj
                    item.save()

        return redirect("productsdash")
    return render(
        request,
        "website/addproduct.html",
        context={"prodform": prodform, "imageset": imageset, "faqset": faqset},
    )


# Edit products to database can only be done by active Bussiness Partners.
@login_required(login_url="login")
@allowed_roles(roles=["active_bps"])
def editProd(request, pk):
    bp = request.user.bp
    temp = Product.objects.get(id=pk)
    prodform = AddProduct(instance=temp)
    image_formset = modelformset_factory(Product_Image, form=Addimages, extra=0)
    faq_formset = modelformset_factory(FAQ, form=Addfaqs, extra=0)
    imageset = image_formset(queryset=Product_Image.objects.filter(product=temp))
    faqset = faq_formset(queryset=FAQ.objects.filter(product=temp))
    if request.method == "POST":
        prodform = AddProduct(request.POST, request.FILES, instance=temp)
        imageset = image_formset(
            request.POST,
            request.FILES,
            queryset=Product_Image.objects.filter(product=temp),
        )
        faqset = faq_formset(request.POST, queryset=FAQ.objects.filter(product=temp))
        if prodform.is_valid():
            obj = prodform.save(commit=False)
            obj.company = bp
            obj.save()
            prodform.save_m2m()
            for form in imageset:
                if form.is_valid():
                    item = form.save(commit=False)
                    item.product = obj
                    item.save()

            for form in faqset:
                if form.is_valid():
                    item = form.save(commit=False)
                    item.product = obj
                    item.save()
        else:
            print(prodform.errors)
            print(imageset.errors)
            print(faqset.errors)
        return redirect("productsdash")
    return render(
        request,
        "website/addproduct.html",
        context={"prodform": prodform, "imageset": imageset, "faqset": faqset},
    )


# Delete products from the in use products not from the database can only be done by active Bussiness Partners.
@login_required(login_url="login")
@allowed_roles(roles=["active_bps"])
def delprod(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("productsdash")


# Page to show options for registering as BP or Ent.
@login_required(login_url="login")
def registerAs(request):
    return render(request, "website/choose.html", context={})


# Confirmation Page to show the status of the profile of the user.
@login_required(login_url="login")
@allowed_roles(roles=["pending_bps", "pending_ents", "rejected_ents", "rejected_bps"])
def confirmation(request):
    pending = ["pending_bps", "pending_ents"]
    if request.user.groups.exists():
        if request.user.groups.all()[0].name in pending:
            msg = "Thank you for registering. You will be notified when your profile will be approved."
        else:
            msg = "Sorry to inform you that your profile has been rejected by the company."
    return render(request, "website/confirmation.html", context={"msg": msg})


# Pending Bussiness Partners request can only be seen by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def pending_bps(request):
    bps = Bussiness_Partner.objects.filter(status=0)
    return render(request, "website/pending_bps.html", context={"bps": bps})


# Pending Bussiness Partners request can only be seen by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def view_bp(request, pk):
    bp = Bussiness_Partner.objects.get(id=pk)
    return render(request, "website/view_bp.html", context={"bp": bp})


# Pending  Entrepreneurs request can only be seen by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def pending_ents(request):
    ents = Entrepreneurs.objects.filter(status=0)
    return render(request, "website/pending_ents.html", context={"ents": ents})


# Pending  Entrepreneurs request can only be seen by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def view_ent(request, pk):
    ent = Entrepreneurs.objects.get(id=pk)
    return render(request, "website/view_ent.html", context={"ent": ent})


# Accept a Pending Entrepreneur request can only be done by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def accept_ent(request, pk):
    ent = Entrepreneurs.objects.get(id=pk)
    ent.status = 1
    group = Group.objects.get(name="active_ents")
    ent.user.groups.clear()
    ent.user.groups.add(group)
    ent.save()
    return redirect("pen_ents")


# Reject a Pending Entrepreneur request can only be done by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def reject_ent(request, pk):
    ent = Entrepreneurs.objects.get(id=pk)
    ent.status = -1
    group = Group.objects.get(name="rejected_ents")
    ent.user.groups.clear()
    ent.user.groups.add(group)
    ent.save()
    return redirect("pen_ents")


# Accept a Pending Bussiness Partner request can only be done by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def accept_bp(request, pk):
    bp = Bussiness_Partner.objects.get(id=pk)
    bp.status = 1
    group = Group.objects.get(name="active_bps")
    bp.user.groups.clear()
    bp.user.groups.add(group)
    bp.save()
    return redirect("pen_bps")


# reject a Pending Entrepreneur request can only be done by admin.
@login_required(login_url="login")
@allowed_roles(roles=["admin"])
def reject_bp(request, pk):
    bp = Bussiness_Partner.objects.get(id=pk)
    bp.status = -1
    group = Group.objects.get(name="rejected_bps")
    bp.user.groups.clear()
    bp.user.groups.add(group)
    bp.save()
    return redirect("pen_bps")


# Page showing all the categories can be seen by any user
def services(request):
    cats = Categories.objects.all()
    return render(request, "website/services.html", context={"cats": cats})


# Page of all the products of a particular category can be seen by any user
def prodlist(request, pk):
    cat = Categories.objects.get(id=pk)
    prodlist = Product.objects.all().filter(category=cat).exclude(status=1)
    return render(request, "website/productlist.html", context={"prodlist": prodlist})


# Detail page view of a product can be seen by any user
def product(request, pk):
    product = Product.objects.get(id=pk)
    cat = product.category.all()[0]
    images = Product_Image.objects.filter(product=product)
    faqs = FAQ.objects.filter(product=product)
    return render(
        request,
        "website/product.html",
        context={"prod": product, "imgs": images, "faqs": faqs, "cat": cat},
    )


# Entrepreneur Dashboard only for active Entrepreneurs
@login_required(login_url="login")
@allowed_roles(roles=["active_ents"])
def ent_dash(request):
    ent = request.user.ent
    return render(request, "website/ent_dashboard.html", context={"ent": ent})


# Bussiness Partners Dashboard only for active Partners
@login_required()
@allowed_roles(roles=["active_bps"])
def bp_dash(request):
    user = request.user.bp
    products = Product.objects.filter(company=user)
    return render(request, "website/productsdash.html", context={"prodlist": products})


# Admin dashboard for admin only
@login_required()
@allowed_roles(roles=["admin"])
def admin_dash(request):
    return render(request, "website/admin_dash.html", context={})


# Detail page of a product of own company of a Bussiness Partner with edit access
@login_required()
@allowed_roles(roles=["active_bps"])
def productdash(request, pk):
    product = Product.objects.get(id=pk)
    cat = product.category.all()[0]
    images = Product_Image.objects.filter(product=product)
    faqs = FAQ.objects.filter(product=product)
    return render(
        request,
        "website/productdash.html",
        context={"prod": product, "imgs": images, "faqs": faqs, "cat": cat},
    )
