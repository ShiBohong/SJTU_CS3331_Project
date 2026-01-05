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
                print(f"数据加载成功，用户数: {len(self.data['users'])}, 物品数: {len(self.data['items'])}")
            except Exception as e:
                print(f"加载数据时出错: {e}")
                pass
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("数据保存成功")
        except Exception as e:
            print(f"保存数据时出错: {e}")
    
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
        # 检查是否已存在相同ID的物品
        for existing_item in self.data['items']:
            if existing_item['id'] == item.id:
                print(f"警告: 物品ID {item.id} 已存在，将生成新ID")
                # 生成新ID
                import random
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                random_num = random.randint(1000, 9999)
                item.id = f"{timestamp}{random_num}"
                break
        
        self.data['items'].append(item.to_dict())
        self.save_data()
    
    def get_items(self, item_type=None, keyword=None):
        """获取物品列表"""
        items = self.data['items']
        
        if item_type:
            items = [item for item in items if item['item_type'] == item_type]
        
        if keyword:
            keyword = keyword.lower()
            items = [item for item in items 
                     if keyword in item['name'].lower() 
                     or keyword in item['description'].lower()
                     or keyword in item['address'].lower()]
        
        return items
    
    def get_item(self, item_id):
        """获取特定物品"""
        # 统一处理为字符串比较
        item_id_str = str(item_id)
        for item in self.data['items']:
            if str(item['id']) == item_id_str:
                return item
        return None
    
    def get_item_by_id(self, item_id):
        """根据ID获取物品 - 兼容性方法"""
        return self.get_item(item_id)
    
    def delete_item(self, item_id):
        """删除物品"""
        try:
            item_id_str = str(item_id)
            print(f"正在删除物品 ID: {item_id_str}")
            
            # 检查物品是否存在
            item_found = None
            for item in self.data['items']:
                if str(item['id']) == item_id_str:
                    item_found = item
                    break
            
            if not item_found:
                print(f"物品 {item_id_str} 不存在")
                return False
            
            print(f"找到物品: {item_found['name']}")
            
            # 删除物品
            original_count = len(self.data['items'])
            self.data['items'] = [item for item in self.data['items'] if str(item['id']) != item_id_str]
            new_count = len(self.data['items'])
            
            print(f"删除前物品数: {original_count}, 删除后物品数: {new_count}")
            
            if new_count < original_count:
                self.save_data()
                print(f"物品删除成功: {item_id_str}")
                return True
            else:
                print("删除失败，物品可能不存在")
                return False
            
        except Exception as e:
            print(f"删除物品时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_item(self, item_id, updated_data):
        """更新物品信息"""
        item_id_str = str(item_id)
        for i, item in enumerate(self.data['items']):
            if str(item['id']) == item_id_str:
                self.data['items'][i].update(updated_data)
                self.save_data()
                return True
        return False