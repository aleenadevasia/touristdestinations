from rest_framework import generics
from .models import State, Category, TouristDestination
from .serializers import StateSerializer, CategorySerializer, TouristDestinationCreateSerializer
from rest_framework.permissions import AllowAny
from . forms import *
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseServerError
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination



# Views for State model


class StateCreateAPIView(generics.CreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateRetrieveAPIView(generics.RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateUpdateAPIView(generics.UpdateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class StateDestroyAPIView(generics.DestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

# Views for Category model


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Views for TouristDestination model


class TouristDestinationCreateAPIView(generics.CreateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer


class TouristDestinationListAPIView(generics.ListAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer


class TouristDestinationRetrieveAPIView(generics.RetrieveAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer


class TouristDestinationUpdateAPIView(generics.UpdateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer


class TouristDestinationDestroyAPIView(generics.DestroyAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer


class DestinationSearchViewSet(generics.ListAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationCreateSerializer
    def get_queryset(self):
        place_name = elf.kwargs.get('place_name')
        return TouristDestination.objects.filter(place_name__icontains=place_name)


def create_state(request):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('state_list')  # Redirect to the state list view
    else:
        form = StateForm()
    return render(request, 'state_form.html', {'form': form})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the category list view
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


def create_tourist_destination(request):
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                main_image = request.FILES.get('main_image')  # Use get() method to avoid MultiValueDictKeyError
                if main_image:  # Check if main_image exists
                    form.instance.main_image = main_image
                form.save()

                api_url = 'http://127.0.0.1:8000/destinations/'
                data = form.cleaned_data
                response = requests.post(api_url, data=data, files={'main_image': main_image})
                if response.status_code == 201:
                    messages.success(request, 'Destination inserted successfully')
                else:
                    messages.error(request, f'Error {response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
        # Redirect to the same page after form submission
        return redirect('destination_list')
    else:
        form = TouristDestinationForm()
    return render(request, 'create_destination.html', {'form': form})


def detail_destination(request, id):
    api_url = f'http://127.0.0.1:8000/destinations/{id}/detail/'
    response = requests.get(api_url)

    if response.status_code == 200:
        destination_data = response.json()

        destination = TouristDestination.objects.get(id=id)

        state_name = destination.state.name
        category_name = destination.category.name


        destination_data['state_name'] = state_name
        destination_data['category_name'] = category_name
        destination_data['main_image_url'] = destination.main_image.url


        return render(request, 'destination_detail.html', {'destination': destination_data})
    else:
        return render(request, 'error_page.html')




def update_destination(request, id):
    if request.method == 'POST':
        destination = TouristDestination.objects.get(pk=id)
        form = TouristDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination updated successfully')
            return redirect(reverse('detail_destination', kwargs={'id': id}))
        else:
            messages.error(request, 'Error updating destination. Please check the form.')
    else:
        destination = TouristDestination.objects.get(pk=id)
        form = TouristDestinationForm(instance=destination)
    return render(request, 'update_destination.html', {'form': form, 'id': id})

def index(request):
    if request.method == 'POST':
        # Handle search functionality if needed
        pass
    else:
        # Fetch tourist destinations data from the database
        tourist_destinations = TouristDestination.objects.all()[:3]
        more_destinations_available = TouristDestination.objects.count() > 3


        # Add state_name and main_image_url dynamically to each destination
        for destination in tourist_destinations:
            destination.state_name = destination.state.name
            destination.main_image_url = destination.main_image.url

        # Pass the tourist destinations data to the template context
        context = {'tourist_destinations': tourist_destinations}
        return render(request, 'index.html', context)


def destination_fetch(request,id):
    api_url = f'http://127.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        description = data['description'].split('_')
        return render(request,'destination_fetch.html',{'destinations':data,'description':description})
    return render(request,'destination_fetch.html')

def destination_list(request):
    # Fetch tourist destinations data from the database
    tourist_destinations = TouristDestination.objects.all()

    # Pass the tourist destinations data to the template context
    context = {'tourist_destinations': tourist_destinations}
    return render(request, 'destination_list.html', context)

class DestinationListPagination(PageNumberPagination):
    page_size = 3 # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

def destination_list(request):
    # Fetch tourist destinations data from the database
    tourist_destinations = TouristDestination.objects.all()

    # Configure pagination
    paginator = Paginator(tourist_destinations, 3)  # Show 10 items per page

    page = request.GET.get('page')
    try:
        tourist_destinations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tourist_destinations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tourist_destinations = paginator.page(paginator.num_pages)

    # Pass the paginated tourist destinations data to the template context
    context = {'tourist_destinations': tourist_destinations}

    return render(request, 'destination_list.html', context)

def destination_delete(request, id):
    # Get the destination object or return a 404 error if not found
    destination = get_object_or_404(TouristDestination, pk=id)

    try:
        # Delete the destination
        destination.delete()
        print(f'Destination with id {id} has been deleted')
        return redirect('destination_list')  # Redirect to the homepage after successful deletion
    except Exception as e:
        print(f'Failed to delete destination with id {id}. Error: {str(e)}')
        # Render an error page if deletion fails
        return HttpResponseServerError('Failed to delete the destination. Please try again later.')