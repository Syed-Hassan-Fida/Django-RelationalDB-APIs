from django.urls import path
from knox import views as knox_views
from .views import * 

urlpatterns = [
    path('login', login_view, name='login'),
    path('register', registerApi, name="register"),
    path('logout', knox_views.LogoutView.as_view(), name="logout"),
    path('logoutall', knox_views.LogoutAllView.as_view(), name="logout"),

    # ---------------------- My Books ---------------------------------
    path("books", BookApiView.as_view(), name="books"),
    path("books/<int:pk>", BookDetailAPIView.as_view(), name="books"),
    path("books/<int:book_id>/addcomment", CreateCommentAPIView.as_view(), name="books"),
    path("comments/<int:pk>", CommentAPIView.as_view(), name="comments"),

    # --------------------- Books Routes ----------------------------------
    path("all-books", GetAllBooksAPIView.as_view(), name="allbooks"),
    path("create-books", CreateBooksAPIView.as_view(), name="createbooks"),
    path("update-book/<int:pk>", UpdateBooksAPIview.as_view(), name="createbooks"),
    path("search-book/<str:name>", SearchBookAPIView.as_view(), name="serachbooks"),
    path("delete-book/<int:pk>", DeleteBookAPIView.as_view(), name="deletebooks"),

    # --------------------- Customer Routes ----------------------------------
    path("all-customers", GetAllCustomerAPIView.as_view(), name="allcustomers"),
    path("customers-order", CreateCustomerAPIView.as_view(), name="customerorder"),
    path("update-customers/<int:pk>", UpdateCustomerAPIView.as_view(), name="updatecustomers"),
    path("delete-customer/<int:pk>", DeleteCustomerAPIView.as_view(), name="deletecustomer"),

    # --------------------- Author Routes ----------------------------------
    path("all-author", GetAllAuthorAPIView.as_view(), name="allauthor"),
    path("create-author", CreateAuthorAPIView.as_view(), name="createauthor"),
    path("update-author/<int:pk>", UpdateAuthorAPIView.as_view(), name="updateauthor"),
    path("delete-author/<int:pk>", DeleteAuthorAPIView.as_view(), name="deleteauthor"),

    # --------------------- Book Publisher Routes ----------------------------------
    path("all-publisher", GetAllPublisherAPIView.as_view(), name="allapublisher"),
    path("create-publisher", CreatePublisherAPIView.as_view(), name="createpublisher"),
    path("update-publisher/<int:pk>", UpdatePublisherAPIView.as_view(), name="updatepublisher"),
    path("delete-publisher/<int:pk>", DeletePublisherAPIView.as_view(), name="deletepublisher"),

    # --------------------- Custom API Routes ----------------------------------
    path("get-all-book-data/<int:id>", GetAllBookData, name="get-all-book-data"),


]