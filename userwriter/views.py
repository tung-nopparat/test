from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "" or password == "":
            messages.warning(request,"กรุณาป้อนข้อมูลให้ครบ")
            return redirect("/login/")
        else :
            # ตรวจสอบเข้าสู่ระบบ
            user = auth.authenticate(username=username,password=password)
            if user is not None :
                auth.login(request,user)
                return redirect("/backoffice/")
            else:
                messages.warning(request,"ไม่พบบัญชีนี้ในระบบ")
                return redirect("/login/")

    else:

        return render(request,"backend/login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login/")




def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        repassword = request.POST["repassword"]
        if username == "" or password == "" or repassword == "":
            messages.warning(request,"กรุณาป้อนข้อมูลให้ครบ")
            return redirect("/login/")
        else:
            if password == repassword:
                # ตรวจสอบว่า user มีผู้ใช้รึยัง
                if User.objects.filter(username=username).exists():
                    messages.warning(request,"User นี้มีคนใช้แล้ว ")
                    return redirect("/login/")
                elif User.objects.filter(email=email).exists():
                    messages.warning(request,"Email นี้มีคนใช้แล้ว ")
                    return redirect("/login/")

                else :
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        #first_name="สมงิ"
                    )
                    user.save()
                    messages.success(request,"สร้างบัญชีเรียบร้อย")
                    return redirect("/login/")
            else:
                messages.warning(request,"รหัสผ่านไม่ตรงกัน")
                return redirect("/login/")
    else :
        return render(request,"login.html")