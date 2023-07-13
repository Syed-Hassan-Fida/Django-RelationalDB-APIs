from django.shortcuts import render
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .api.serializers import *
from books.models import Publisher, Author, Book, Customer, MyBook, Comment
from rest_framework.generics import *
from .permissions import IsadminOrStaffReadOnly, IscommentOwnerorReadOnly
from .api.pagination import SmallPagination
from django.db.models import Sum


# ------------------ Login / Register Api View ------------------------------
@api_view(['post'])
def login_view(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info' : {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token
    })

@api_view(['post'])
def registerApi(request):   
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info' : {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token
    })

# ------------------ Book Class Api View ------------------------------
class GetAllBooksAPIView(ListAPIView):
    queryset = Book.objects.order_by("-id")
    serializer_class = BookSerializer
    pagination_class = SmallPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CreateBooksAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

class UpdateBooksAPIview(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

class SearchBookAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
class DeleteBookAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

# ------------------ Customer Class Api View ------------------------------
class GetAllCustomerAPIView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CreateCustomerAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.data 
            book_price = 0

            try:
                if data['books'] != None:
                    book_price = Book.objects.filter(id=data['books'][0]).first().price
            except Exception as e:
                return Response({"error": "Server Error", "status": False}, status=500)
            
            total_price = int(data['total_book']) * int(book_price)

            data['total_price'] = total_price

            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data saved successfully.", "status": True}, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"message": "Unauthenticated."}, status=401)

class UpdateCustomerAPIView(UpdateAPIView):

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_id = self.kwargs.get("pk")
            try:
                customer = Customer.objects.filter(id=order_id).first()
            except Customer.DoesNotExist:
                return Response({"message": "Customer not found."}, status=404)
            
            data = request.data
            book_price = 0
            
            try:
                if data['books'] is not None:
                    book_price = Book.objects.filter(id=data['books'][0]).first().price
            except Exception as e:
                return Response({"error": "Server Error", "status": False}, status=500)
            
            total_price = int(data['total_book']) * int(book_price)
            data['total_price'] = total_price

            serializer = CustomerSerializer(customer, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data updated successfully.", "status": True}, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"message": "Unauthenticated."}, status=401)


    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_id = self.kwargs.get("pk")
            try:
                customer = Customer.objects.filter(id=order_id).first()
            except Customer.DoesNotExist:
                return Response({"message": "Customer not found."}, status=404)
            
            data = request.data
            book_price = 0
            
            try:
                if data['books'] is not None:
                    book_price = Book.objects.filter(id=data['books'][0]).first().price
            except Exception as e:
                return Response({"error": "Server Error", "status": False}, status=500)
            
            total_price = int(data['total_book']) * int(book_price)
            data['total_price'] = total_price

            serializer = CustomerSerializer(customer, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data updated successfully.", "status": True}, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"message": "Unauthenticated."}, status=401)

class DeleteCustomerAPIView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
        

# ------------------ Author Class Api View ------------------------------
class GetAllAuthorAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CreateAuthorAPIView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

class UpdateAuthorAPIView(UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
        
class DeleteAuthorAPIView(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
        

# ------------------ Book Publisher Class Api View ------------------------------
class GetAllPublisherAPIView(ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CreatePublisherAPIView(CreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

class UpdatePublisherAPIView(UpdateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
        
class DeletePublisherAPIView(DestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
     
# ------------------ Book and Comments ------------------------------
class BookApiView(ListCreateAPIView):
    queryset = MyBook.objects.all()
    serializer_class = MyBookSerializer
    # permission_classes = [IsadminOrStaffReadOnly]


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.list(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
            
    
    def post(self, request, *args,**kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MyBook.objects.all()
    serializer_class = MyBookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})
        
class CreateCommentAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')
        serializer.save(book_id=book_id, owner=self.request.user)

class CommentAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IscommentOwnerorReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "UnAuthenticated"})

# ------------------ Custom API ------------------------------
@api_view(['get'])
def GetAllBookData(request, id):
    book_obj = Book.objects.filter(pk=id).first()
    author_obj = Author.objects.filter(book=book_obj).first()
    publisher_obj = Publisher.objects.filter(book=book_obj).first()
    customer_obj = Customer.objects.filter(books=book_obj)
    dicts = {}

    # for direct aggregation query if needed
    # total_price = Customer.objects.filter(books=book_obj).aggregate(total_price=Sum('total_price')).get('total_price')
    # total_book = Customer.objects.filter(books=book_obj).aggregate(total_book=Sum('total_book')).get('total_book')

    try: 
        
        if customer_obj != None:
            for i in customer_obj:
                username = i.client.username
                email = i.client.email
                total_price = i.total_price
                total_books = i.total_book

                if username not in dicts:
                    dicts[username] = {
                        'email': email,
                        'total_price': total_price,
                        'total_books': total_books
                    }
                else:
                    dicts[username]['email'] = email
                    dicts[username]['total_price'] += total_price
                    dicts[username]['total_books'] += total_books
        else:
            dicts = {}

        if book_obj != None:
            context = {
                "book": book_obj.name,
                "Uploaded_by": book_obj.users.username,
                "year": book_obj.year,
                "title": book_obj.title,
                "price": float(book_obj.price),
                "author details": {
                    "name": author_obj.name if author_obj else None,
                    "books written": author_obj.books_written if author_obj else None,
                    "Uploaded Book": author_obj.book.name if author_obj else None
                },
                "publisher Details": {
                    "name": publisher_obj.name if publisher_obj else None,
                    "phone": publisher_obj.phone if publisher_obj else None,
                    "Uploaded Book": publisher_obj.book.name if publisher_obj else None
                },
                "customer Details": dicts,
            }
        else:
            context = {
                "Data": "Book not found..."
            }


        return Response(context, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# ------------------ Test Api View ------------------------------
@api_view(['get'])
def get_client_data(request):
    client = Customer.objects.filter(client=request.user.id).first() 
    customer = client.client
    book = client.book
    user = request.user

    if customer.is_authenticated:
        return Response({
            'Client_info' : {
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
            },
            'books': {
                'title': book.title,
                'price': book.price,
                'year': book.year
            }
        })
    return Response({'errror': 'User not authenticated'}, status=400)