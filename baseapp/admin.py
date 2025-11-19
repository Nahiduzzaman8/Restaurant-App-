
from django.contrib import admin
from .models import Category, Items, Aboutus, Feedback, Booktable, SliderImage, Offer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "item_count")
    search_fields = ("category_name",)
    list_filter = ("category_name",)
    ordering = ("category_name",)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Total Items"

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "category", "price", "image")
    list_filter = ("category",)
    search_fields = ("item_name", "description")
    ordering = ("item_name",)
    list_editable = ("price","image")  # optional
    autocomplete_fields = ("category",)

@admin.register(Aboutus)
class AboutusAdmin(admin.ModelAdmin):
    list_display = ("id", "short_description")

    def short_description(self, obj):
        return obj.description[:50] + "..."
    short_description.short_description = "Description"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "rating", "image")
    search_fields = ("username", "description")
    list_editable = ('image',)
    list_filter = ("rating",)
    ordering = ("-rating",)

@admin.register(Booktable)
class BooktableAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "email", "total_person", "booking_data")
    search_fields = ("name", "email")
    list_filter = ("booking_data", "total_person")
    ordering = ("-booking_data",)

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ("id","image",)
    list_editable = ('image',)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("category","percent","image",)
    list_editable = ('image',"percent",)