import json
import os
from models import User, ItemType, Item

class Database:
    """数据库管理类"""
    def __init__(self, db_file='database.json'):
        self.db_file = db_file
        self.data = {
            'users': [],
            'item_types': [],
            'items': []
        }
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                pass
    
    def save_data(self):
        """保存数据"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # 用户相关操作
    def add_user(self, user):
        """添加用户"""
        self.data['users'].append(user.to_dict())
        self.save_data()
    
    def get_user(self, username):
        """获取用户"""
        for user in self.data['users']:
            if user['username'] == username:
                return user
        return None
    
    def update_user(self, username, updated_data):
        """更新用户信息"""
        for i, user in enumerate(self.data['users']):
            if user['username'] == username:
                self.data['users'][i].update(updated_data)
                self.save_data()
                return True
        return False
    
    def get_pending_users(self):
        """获取待审核用户"""
        return [user for user in self.data['users'] if not user['is_approved']]
    
    # 物品类型相关操作
    def add_item_type(self, item_type):
        """添加物品类型"""
        self.data['item_types'].append(item_type.to_dict())
        self.save_data()
    
    def get_item_types(self):
        """获取所有物品类型"""
        return self.data['item_types']
    
    def get_item_type(self, name):
        """获取特定物品类型"""
        for item_type in self.data['item_types']:
            if item_type['name'] == name:
                return item_type
        return None
    
    def update_item_type(self, old_name, new_type):
        """更新物品类型"""
        for i, item_type in enumerate(self.data['item_types']):
            if item_type['name'] == old_name:
                self.data['item_types'][i] = new_type.to_dict()
                self.save_data()
                return True
        return False
    
    # 物品相关操作
    def add_item(self, item):
        """添加物品"""
        self.data['items'].append(item.to_dict())
        self.save_data()
    
    def get_items(self, item_type=None, keyword=None):
        """获取物品列表"""
        items = self.data['items']
        
        if item_type:
            items = [item for item in items if item['item_type'] == item_type]
        
        if keyword:
            items = [item for item in items 
                     if keyword.lower() in item['name'].lower() 
                     or keyword.lower() in item['description'].lower()]
        
        return items
    
    def get_item(self, item_id):
        """获取特定物品"""
        for item in self.data['items']:
            if item['id'] == item_id:
                return item
        return None
    
    def delete_item(self, item_id):
        """删除物品"""
        for i, item in enumerate(self.data['items']):
            if item['id'] == item_id:
                del self.data['items'][i]
                self.save_data()
                return True
        return False