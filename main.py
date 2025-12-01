import tkinter as tk
from gui import ItemResurrectionGUI
from database import Database
from models import User, ItemType

def initialize_system():
    """初始化系统"""
    db = Database()
    
    # 如果没有管理员，创建默认管理员
    if not db.get_user('admin'):
        admin = User(
            username='admin',
            password='admin123',
            name='系统管理员',
            address='系统管理',
            phone='12345678901',
            email='admin@example.com',
            is_admin=True,
            is_approved=True
        )
        db.add_user(admin)
    
    # 如果没有物品类型，创建默认类型
    if not db.get_item_types():
        # 添加食品类型
        food_type = ItemType('食品', ['保质期', '数量'])
        db.add_item_type(food_type)
        
        # 添加书籍类型
        book_type = ItemType('书籍', ['作者', '出版社', '出版日期'])
        db.add_item_type(book_type)
        
        # 添加工具类型
        tool_type = ItemType('工具', ['品牌', '使用年限', '功能'])
        db.add_item_type(tool_type)

if __name__ == "__main__":
    initialize_system()
    root = tk.Tk()
    app = ItemResurrectionGUI(root)
    root.mainloop()