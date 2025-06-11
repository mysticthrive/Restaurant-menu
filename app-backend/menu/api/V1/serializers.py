from rest_framework import serializers
from ...models import MenuItem, Category
from dashboard.admin.api.V1.serializers import GalleryMenuSerializer



class CategorySerializer(serializers.ModelSerializer):

    """Serialize category data for listing and detail views."""

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']



class GetMenuItemSerializer(serializers.ModelSerializer):

    """Serialize menu item for listing and detail, with extra computed fields."""
    
    category = CategorySerializer(many=True, read_only=True)
    detail_link = serializers.SerializerMethodField()
    get_price = serializers.SerializerMethodField()
    is_discounted = serializers.BooleanField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)
    menu_item = GalleryMenuSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'user',
            'category',
            'title',
            'slug',
            'description',
            'image',
            'menu_item',
            'stock',
            'status',
            'price',
            'get_price',
            'discount_percent',
            'views',
            'is_featured',
            'preparation_time',
            'created_date',
            'updated_date',
            'is_discounted',
            'is_published',
            'is_out_of_stock',
            'detail_link',
        ]
        read_only_fields = ['created_date', 'updated_date', 'views']

    def get_detail_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/menu/{obj.slug}/')  

    def get_get_price(self, obj):
        return obj.get_price()  
