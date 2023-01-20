from django.urls import path,include
from tutorials import views 
 
urlpatterns = [ 
    path('api/tutorials', views.tutorial_list),
    path('api/tutorials/<pk>', views.tutorial_detail),
    path('api/tutorials/published', views.tutorial_list_published)
#path('api/tutorials',views.TutorialView.as_view()),
#path('api/tutorials/published',views.TutorialPublish.as_view()),
#path('api/tutorials/<int:pk>',views.TutorialDetail.as_view()),

]