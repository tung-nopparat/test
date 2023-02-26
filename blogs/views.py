from django.shortcuts import render,redirect
from blogs.models import Blog, ReviewRating
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum ,Avg ,Q
from django.core.paginator import Paginator
# inport .forms
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    blog = Blog.objects.all()
    topview = blog.order_by('-view')[:4]
    news = blog.order_by('-id')[:4]
    return render(request, "frontend/index.html",{"blog":blog,"topview":topview,"news":news})

def bloglist(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"frontend/bloglist.html",{"page_obj":page_obj})


def search(request):
    search = request.GET.get("search")
    blog_search = Blog.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
    paginator = Paginator(blog_search, 5)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request,"frontend/searchblogs.html",{"blogs":blogs, "search":search})
   


@login_required(login_url="/login/")
def dashboard(request):
    writer = request.user.username
    blog = Blog.objects.filter(writer=writer)
    blog_id = blog.values_list("id",flat=True)
    total_blog = blog.count()
    total_view = blog.aggregate(Sum("view"))
    review_ = ReviewRating.objects.filter(blog__in=blog_id)
    total_rating = review_.aggregate(Avg("rating"))
    total_review = review_.count()

    return render(request,"backend/dashboard.html",{"blog":blog,"total_blog":total_blog,"total_view":total_view,"total_rating":total_rating,"total_review":total_review})

@login_required(login_url="/login/")
def add(request):
    return render(request,"backend/add.html")

@login_required(login_url="/login/")
def insert(request):
    
    try:
        if request.method == "POST" and request.FILES["cover_img"]:
            dataimage = request.FILES["cover_img"]
            #รับค่าจากฟอม เพิ่มบทความ
            title =request.POST["title"]
            description = request.POST["description"]
            category =request.POST["category"]
            blog_content = request.POST["blog_content"]
            tag = request.POST["tag"]
            publish = request.POST.get("publish",False)
            if publish == 'on' :
                publish=True
            writer = request.user.username
            if str(dataimage.content_type).startswith("image"):
                
                fs = FileSystemStorage()
                #การ upload image
                img_url = "images/"+dataimage.name
                filename = fs.save(img_url,dataimage)
                 #การบันทึกข้อมูล
                blog = Blog(title = title,description=description,cover_img = img_url ,category = category,blog_content = blog_content, tag = tag, publish = publish, writer=writer)
                blog.save()
                
                return redirect("/backoffice/")
            else:
                
                return redirect("/add/") 
            
    except:
        return redirect('/add/')

@login_required(login_url="/login/")
def editdata(request,id):
    blog = Blog.objects.get(id=id)

    return render(request,"backend/edit.html",{"blog":blog})

@login_required(login_url="/login/")
def updatedata(request,id):
    try:
        if request.method == "POST":
        #ดึวข้อมูลบทความเดิม
            blog = Blog.objects.get(id=id)
            #รับค่าจากฟอม เพิ่มบทความ
            title =request.POST["title"]
            description = request.POST["description"]
            category =request.POST["category"]
            blog_content = request.POST["blog_content"]
            tag = request.POST["tag"]
            publish = request.POST.get("publish",False)
            if publish == 'on' :
                publish=True

            #อัพเดทข้อมูล
            blog.title = title
            blog.description = description
            blog.category = category
            blog.blog_content = blog_content
            blog.tag = tag
            blog.publish = publish
            blog.save()

            #อัพเดทภาพปก
            if request.FILES["cover_img"]:
                dataimage = request.FILES["cover_img"]
                if str(dataimage.content_type).startswith("image"):
                    # ลบภาพจริงออกก่อน
                    fs = FileSystemStorage()
                    fs.delete(str(blog.cover_img))

                    #อัพภาพใหม่
                    img_url = "images/"+dataimage.name
                    filename = fs.save(img_url,dataimage)
                    blog.cover_img = img_url
                    blog.save()
            return redirect("/backoffice/")
    except:
        return redirect("/backoffice/")

@login_required(login_url="/login/")
def deletedata(request,id):
    try:
        blog = Blog.objects.get(id=id)
        #ลบรูปภาพ
        fs = FileSystemStorage()
        fs.delete(str(blog.cover_img))
        #ลบข้อมูลในฐานข้อมูล 
        blog.delete()
        return redirect('/backoffice/') 
    except:
        return redirect('/backoffice/')


def blogdetail(request,id):
    blog = Blog.objects.get(id=id)
    blog.view+=1
    blog.save()
    review = ReviewRating.objects.filter(blog=id)
    return render(request,"frontend/blogdetail.html",{"blog":blog,"review":review})


def submit_review(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(blog__id=id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.blog_id = id
                data.save()
                return redirect(url)
        return redirect(url)