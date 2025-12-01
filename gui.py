import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import User, ItemType, Item
from database import Database

class ItemResurrectionGUI:
    """物品复活系统GUI"""
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活系统")
        self.root.geometry("800x600")
        
        self.db = Database()
        self.current_user = None
        
        # 创建主界面
        self.create_login_interface()
    
    def create_login_interface(self):
        """创建登录界面"""
        self.clear_interface()
        
        # 登录框架
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text="物品复活系统", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(login_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(login_frame, text="密码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5)
        
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="登录", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="注册", command=self.register).pack(side=tk.LEFT, padx=5)
    
    def create_main_interface(self):
        """创建主界面"""
        self.clear_interface()
        
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 用户菜单
        user_menu = tk.Menu(menubar, tearoff=0)
        user_menu.add_command(label="个人信息", command=self.show_user_info)
        user_menu.add_command(label="退出登录", command=self.logout)
        menubar.add_cascade(label="用户", menu=user_menu)
        
        # 如果是管理员，添加管理员菜单
        if self.current_user and self.current_user.get('is_admin'):
            admin_menu = tk.Menu(menubar, tearoff=0)
            admin_menu.add_command(label="审核用户", command=self.approve_users)
            admin_menu.add_command(label="管理物品类型", command=self.manage_item_types)
            menubar.add_cascade(label="管理", menu=admin_menu)
        
        # 工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="添加物品", command=self.add_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除物品", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        
        # 搜索框架
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="物品类型:").pack(side=tk.LEFT, padx=5)
        self.type_var = tk.StringVar()
        type_names = [t['name'] for t in self.db.get_item_types()]
        type_names.insert(0, "全部")
        self.type_combobox = ttk.Combobox(search_frame, textvariable=self.type_var, values=type_names, width=20)
        self.type_combobox.pack(side=tk.LEFT, padx=5)
        self.type_combobox.current(0)
        
        ttk.Label(search_frame, text="关键字:").pack(side=tk.LEFT, padx=5)
        self.keyword_entry = ttk.Entry(search_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="搜索", command=self.search_items).pack(side=tk.LEFT, padx=5)
        
        # 物品列表
        self.tree = ttk.Treeview(self.root, columns=('ID', '名称', '类型', '联系人', '地址'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('名称', text='物品名称')
        self.tree.heading('类型', text='物品类型')
        self.tree.heading('联系人', text='联系人')
        self.tree.heading('地址', text='地址')
        
        # 设置列宽
        self.tree.column('ID', width=100)
        self.tree.column('名称', width=200)
        self.tree.column('类型', width=100)
        self.tree.column('联系人', width=150)
        self.tree.column('地址', width=200)
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 显示所有物品
        self.load_items()
    
    def clear_interface(self):
        """清空界面"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def login(self):
        """用户登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("警告", "用户名和密码不能为空！")
            return
        
        user = self.db.get_user(username)
        if not user:
            messagebox.showerror("错误", "用户名不存在！")
            return
        
        if user['password'] != password:
            messagebox.showerror("错误", "密码错误！")
            return
        
        if not user['is_approved']:
            messagebox.showinfo("提示", "您的账号正在审核中，请等待管理员批准！")
            return
        
        self.current_user = user
        self.create_main_interface()
        messagebox.showinfo("成功", f"欢迎回来，{user['name']}！")
    
    def register(self):
        """用户注册"""
        username = simpledialog.askstring("注册", "请输入用户名:")
        if not username:
            return
        
        if self.db.get_user(username):
            messagebox.showerror("错误", "用户名已存在！")
            return
        
        password = simpledialog.askstring("注册", "请输入密码:", show="*")
        if not password:
            return
        
        name = simpledialog.askstring("注册", "请输入真实姓名:")
        address = simpledialog.askstring("注册", "请输入地址:")
        phone = simpledialog.askstring("注册", "请输入联系电话:")
        email = simpledialog.askstring("注册", "请输入邮箱:")
        
        if not all([name, address, phone, email]):
            messagebox.showwarning("警告", "所有信息都必须填写！")
            return
        
        user = User(username, password, name, address, phone, email)
        self.db.add_user(user)
        messagebox.showinfo("成功", "注册成功！请等待管理员审核。")
    
    def logout(self):
        """退出登录"""
        self.current_user = None
        self.create_login_interface()
    
    def show_user_info(self):
        """显示个人信息"""
        if not self.current_user:
            return
        
        info_window = tk.Toplevel(self.root)
        info_window.title("个人信息")
        info_window.geometry("400x300")
        info_window.transient(self.root)
        info_window.grab_set()
        
        frame = ttk.Frame(info_window, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="个人信息", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="用户名:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(frame, text=self.current_user['username']).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="姓名:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(frame, text=self.current_user['name']).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="地址:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(frame, text=self.current_user['address']).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="电话:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(frame, text=self.current_user['phone']).grid(row=4, column=1, sticky=tk.W)
        
        ttk.Label(frame, text="邮箱:").grid(row=5, column=0, sticky=tk.W)
        ttk.Label(frame, text=self.current_user['email']).grid(row=5, column=1, sticky=tk.W)
        
        ttk.Button(frame, text="关闭", command=info_window.destroy).grid(row=6, column=0, columnspan=2, pady=20)
    
    def approve_users(self):
        """审核用户"""
        if not self.current_user or not self.current_user['is_admin']:
            return
        
        pending_users = self.db.get_pending_users()
        if not pending_users:
            messagebox.showinfo("提示", "没有待审核的用户！")
            return
        
        approve_window = tk.Toplevel(self.root)
        approve_window.title("审核用户")
        approve_window.geometry("500x400")
        approve_window.transient(self.root)
        approve_window.grab_set()
        
        tree = ttk.Treeview(approve_window, columns=('用户名', '姓名', '电话', '邮箱'), show='headings')
        tree.heading('用户名', text='用户名')
        tree.heading('姓名', text='姓名')
        tree.heading('电话', text='电话')
        tree.heading('邮箱', text='邮箱')
        
        for user in pending_users:
            tree.insert('', tk.END, values=(user['username'], user['name'], user['phone'], user['email']))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def approve_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("警告", "请选择要审核的用户！")
                return
            
            for item in selected:
                username = tree.item(item)['values'][0]
                self.db.update_user(username, {'is_approved': True})
            
            messagebox.showinfo("成功", "用户审核成功！")
            approve_window.destroy()
        
        ttk.Button(approve_window, text="审核通过", command=approve_selected).pack(pady=10)
    
    def manage_item_types(self):
        """管理物品类型"""
        if not self.current_user or not self.current_user['is_admin']:
            return
        
        type_window = tk.Toplevel(self.root)
        type_window.title("管理物品类型")
        type_window.geometry("500x400")
        type_window.transient(self.root)
        type_window.grab_set()
        
        # 类型列表
        tree = ttk.Treeview(type_window, columns=('名称', '属性'), show='headings')
        tree.heading('名称', text='类型名称')
        tree.heading('属性', text='额外属性')
        
        for item_type in self.db.get_item_types():
            attrs = ', '.join(item_type['attributes'])
            tree.insert('', tk.END, values=(item_type['name'], attrs))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 按钮框架
        btn_frame = ttk.Frame(type_window)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        def add_type():
            name = simpledialog.askstring("添加类型", "请输入物品类型名称:")
            if not name:
                return
            
            attrs = simpledialog.askstring("添加属性", "请输入额外属性（逗号分隔）:")
            attributes = [attr.strip() for attr in attrs.split(',')] if attrs else []
            
            item_type = ItemType(name, attributes)
            self.db.add_item_type(item_type)
            
            # 刷新列表
            for item in tree.get_children():
                tree.delete(item)
            for item_type in self.db.get_item_types():
                attrs_str = ', '.join(item_type['attributes'])
                tree.insert('', tk.END, values=(item_type['name'], attrs_str))
        
        ttk.Button(btn_frame, text="添加类型", command=add_type).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="修改类型", command=lambda: self.edit_item_type(tree)).pack(side=tk.LEFT, padx=5)
    
    def edit_item_type(self, tree):
        """编辑物品类型"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要修改的类型！")
            return
        
        item = tree.item(selected[0])
        old_name = item['values'][0]
        old_attrs = item['values'][1]
        
        new_name = simpledialog.askstring("修改类型", "请输入新的类型名称:", initialvalue=old_name)
        if not new_name:
            return
        
        new_attrs = simpledialog.askstring("修改属性", "请输入新的额外属性（逗号分隔）:", initialvalue=old_attrs)
        attributes = [attr.strip() for attr in new_attrs.split(',')] if new_attrs else []
        
        new_type = ItemType(new_name, attributes)
        self.db.update_item_type(old_name, new_type)
        
        # 刷新列表
        for item in tree.get_children():
            tree.delete(item)
        for item_type in self.db.get_item_types():
            attrs_str = ', '.join(item_type['attributes'])
            tree.insert('', tk.END, values=(item_type['name'], attrs_str))
    
    def add_item(self):
        """添加物品"""
        if not self.current_user:
            return
        
        # 获取物品类型
        item_types = self.db.get_item_types()
        if not item_types:
            messagebox.showwarning("警告", "暂无物品类型，请联系管理员添加！")
            return
        
        type_names = [t['name'] for t in item_types]
        selected_type = simpledialog.askstring("选择类型", f"请选择物品类型（{', '.join(type_names)}）:")
        
        if selected_type not in type_names:
            messagebox.showerror("错误", "无效的物品类型！")
            return
        
        # 获取基本信息
        name = simpledialog.askstring("物品名称", "请输入物品名称:")
        if not name:
            return
        
        description = simpledialog.askstring("物品描述", "请输入物品描述:")
        address = simpledialog.askstring("物品地址", "请输入物品所在地址:")
        phone = simpledialog.askstring("联系电话", "请输入联系电话:")
        email = simpledialog.askstring("联系邮箱", "请输入联系邮箱:")
        
        if not all([description, address, phone, email]):
            messagebox.showwarning("警告", "所有信息都必须填写！")
            return
        
        # 获取额外属性
        item_type = self.db.get_item_type(selected_type)
        extra_attributes = {}
        
        for attr in item_type['attributes']:
            value = simpledialog.askstring("额外属性", f"请输入{attr}:")
            if value:
                extra_attributes[attr] = value
        
        # 创建物品
        item = Item(
            name=name,
            description=description,
            address=address,
            contact_phone=phone,
            contact_email=email,
            item_type=selected_type,
            user=self.current_user['username'],
            extra_attributes=extra_attributes
        )
        
        self.db.add_item(item)
        self.load_items()
        messagebox.showinfo("成功", "物品添加成功！")
    
    def delete_item(self):
        """删除物品"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的物品！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的物品吗？"):
            item_id = self.tree.item(selected[0])['values'][0]
            self.db.delete_item(item_id)
            self.load_items()
            messagebox.showinfo("成功", "物品删除成功！")
    
    def search_items(self):
        """搜索物品"""
        item_type = self.type_var.get()
        keyword = self.keyword_entry.get().strip()
        
        if item_type == "全部":
            item_type = None
        
        self.load_items(item_type, keyword)
    
    def load_items(self, item_type=None, keyword=None):
        """加载物品列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取物品数据
        items = self.db.get_items(item_type, keyword)
        
        # 添加到表格
        for item in items:
            self.tree.insert('', tk.END, values=(
                item['id'],
                item['name'],
                item['item_type'],
                item['contact_phone'],
                item['address']
            ))