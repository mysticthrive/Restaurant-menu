from django.db import models
from django.utils.text import slugify
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name="نامک")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Category.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class ProductStatusType(models.IntegerChoices):
    publish = 1, "نمایش"
    draft = 2, "عدم نمایش"


class MenuItem(models.Model):
    user = models.ForeignKey('accounts.CustomeUser', on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True, verbose_name="کاربر")
    category = models.ManyToManyField(Category, verbose_name="دسته‌بندی‌ها", related_name="categories")
    title = models.CharField(max_length=255, verbose_name="نام آیتم")
    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name="نامک")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='menu_items', verbose_name="تصویر اصلی")

    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.publish.value, verbose_name="وضعیت")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0, verbose_name="قیمت")
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="درصد تخفیف")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    is_featured = models.BooleanField(default=False, verbose_name="آیتم ویژه")
    preparation_time = models.PositiveIntegerField(default=15, verbose_name="مدت زمان آماده‌سازی (دقیقه)")  # اینجا اضافه شد

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم‌های منو"

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and MenuItem.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        return round(self.price - discount_amount)

    def is_discounted(self):
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatusType.publish.value

    @property
    def is_out_of_stock(self):
        return self.stock == 0


class GalleryMenu(models.Model):
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="menu_item")
    image = models.ImageField(upload_to="gallery/menu_items", null=True, blank=True)

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "گالری تصاویر"
