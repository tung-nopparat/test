from django.urls import path
from blogs import views
urlpatterns = [
    path('',views.index),
    path('bloglist/',views.bloglist,name="bloglist"),
    path('backoffice/',views.dashboard,name="dashboard"),
    path('add/',views.add,name="add"),
    path('insert/',views.insert,name="insert"),
    path('editdata/<int:id>',views.editdata,name="editdata"),
    path('updatedata/<int:id>',views.updatedata,name="updatedata"),
    path('deletedata/<int:id>',views.deletedata,name="deletedata"),
    path('blogdetail/<int:id>',views.blogdetail,name="blogdetail"),
    path('submit_review/<int:id>',views.submit_review,name="submit_review"),
    path('search/',views.search,name="search"),

]