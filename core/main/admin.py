from django.contrib import admin
from . models import Category,Product,Wishlist,HotDeal,Cart,UserMessage,Pay,Store,Store_img,TopSelling,Product_detail,Product_images,Product_description,Accessories,Slide,Video,All_products,Color,Size
from .forms import ProductDetailAdminForm
from ckeditor.widgets import CKEditorWidget

admin.site.register(Wishlist)
admin.site.register(HotDeal)
admin.site.register(Cart)
admin.site.register(UserMessage)
admin.site.register(Pay)
admin.site.register(Store)
admin.site.register(Store_img)
admin.site.register(TopSelling)
admin.site.register(Accessories)
admin.site.register(Slide)
admin.site.register(Video)
admin.site.register(Color)
admin.site.register(Size)




class ProductImagesInline(admin.TabularInline):
    model = Product_images
    extra = 1
class ProductDetailInline(admin.TabularInline):
    model = Product_detail
    form = ProductDetailAdminForm
    extra = 1



class ProductDescriptionInline(admin.TabularInline):
    model = Product_description
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDetailInline, ProductImagesInline] 
    list_display = ['pr_name', 'category', 'new_price', 'old_price', 'status', 'num_sales']
    search_fields = ['pr_name', 'category__category_name']
    list_filter = ['category', 'status']
    
class ProductDescriptionInline(admin.TabularInline):
    model = Product_description
    extra = 1

admin.site.register(Product_description)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)



