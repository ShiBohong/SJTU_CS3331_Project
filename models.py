import json
from datetime import datetime
import random

class User:
    """用户类"""
    def __init__(self, username, password, name, address, phone, email, is_admin=False, is_approved=False):
        self.username = username
        self.password = password
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.is_admin = is_admin
        self.is_approved = is_approved
    
    def to_dict(self):
        """转换为字典"""
        return {
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_approved': self.is_approved
        }

class ItemType:
    """物品类型类"""
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes  # 额外属性列表
    
    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.name,
            'attributes': self.attributes
        }

class Item:
    """物品类"""
    def __init__(self, name, description, address, contact_phone, contact_email, 
                 item_type, user, extra_attributes=None, id=None):
        # 生成更简单的ID：时间戳+随机数
        if id is None:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_num = random.randint(100, 999)
            self.id = f"{timestamp}{random_num}"
        else:
            self.id = id
            
        self.name = name
        self.description = description
        self.address = address
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.item_type = item_type
        self.user = user
        self.extra_attributes = extra_attributes or {}
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'item_type': self.item_type,
            'user': self.user,
            'extra_attributes': self.extra_attributes
        }