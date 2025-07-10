from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count, Max, Min
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Transaction
from .forms import InquiryForm, TransactionForm
from .recommendation import get_recommendations

# 🏠 Home View: Handles property search
def home(request):
    query = request.GET.get('q', '').strip()
    properties = Property.objects.filter(city__icontains=query) if query else []

    context = {
        'properties': properties,
        'query': query,
    }
    return render(request, 'listings/home.html', context)


# 🏡 Property Detail View: Shows details and handles inquiry form submission
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    form = InquiryForm()

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property_obj
            inquiry.save()
            return redirect('home')

    return render(request, 'listings/property_detail.html', {
        'property': property_obj,
        'form': form
    })


# 📊 Market Analysis View: Displays property statistics and trends
def market_analysis(request):
    total_properties = Property.objects.count()
    average_price = Property.objects.aggregate(Avg('price'))['price__avg']
    highest_price = Property.objects.aggregate(Max('price'))['price__max']
    lowest_price = Property.objects.aggregate(Min('price'))['price__min']

    listings_count_by_city = (
        Property.objects
        .values('city')
        .annotate(listing_count=Count('id'))
        .order_by('-listing_count')
    )

    avg_price_by_city = (
        Property.objects
        .values('city')
        .annotate(avg_price=Avg('price'))
        .order_by('-avg_price')
    )

    context = {
        'total_properties': total_properties,
        'average_price': average_price,
        'highest_price': highest_price,
        'lowest_price': lowest_price,
        'listings_count_by_city': listings_count_by_city,
        'avg_price_by_city': avg_price_by_city,
    }

    return render(request, 'listings/market_analysis.html', context)


# 📄 Upload Document View: Handles transaction document uploads
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.uploaded_by = request.user
            transaction.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('home')
    else:
        form = TransactionForm()

    return render(request, 'listings/upload_document.html', {'form': form})
# 🤖 Personalized Recommendation View
def recommend_properties(request):
    recommendations = []
    if request.method == 'POST':
        preferences = request.POST.get('preferences', '')
        if preferences:
            recommendations = get_recommendations(preferences).to_dict(orient='records')

    return render(request, 'listings/recommend.html', {
        'recommendations': recommendations
    })
