﻿from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        """Khởi tạo giỏ hàng"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Nếu chưa có giỏ hàng, tạo giỏ hàng trống
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Thêm sản phẩm vào giỏ hàng hoặc cập nhật số lượng"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Lưu giỏ hàng vào session"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """Xóa sản phẩm khỏi giỏ hàng"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Duyệt qua các sản phẩm trong giỏ hàng"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Đếm tổng số lượng sản phẩm trong giỏ hàng"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Tính tổng giá tiền của giỏ hàng"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Xóa toàn bộ giỏ hàng"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
