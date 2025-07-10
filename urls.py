from django.contrib import admin
from django.urls import path
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # ✅ Import LoginView

urlpatterns = [
    # 🛠 Admin Panel
    path('admin/', admin.site.urls),

    # 🏠 Home page with search functionality
    path('', views.home, name='home'),

    # 🏡 Property detail page with inquiry form
    path('property/<int:pk>/', views.property_detail, name='property_detail'),

    # 📊 Market Analysis feature
    path('market-analysis/', views.market_analysis, name='market_analysis'),

    # 📄 Upload Transaction Document
    path('upload-document/', views.upload_document, name='upload_document'),

    # 🔐 Login page
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
	
    # 🤖 AI-based Property Recommendation
    path('recommend/', views.recommend_properties, name='recommend_properties'),

]

# ✅ Serve media files in development (for property images & documents)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ (Optional) Serve static files manually if needed
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
