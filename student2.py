from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
from pymysql import *
import tkinter.messagebox
from tkinter.messagebox import *


def deleted(num):    # 删除列表中第一个元素
    temp = list(num)
    del temp[0]
    return temp


def student1_id():  # 取出数据库所有学生的学号
    list2 = []
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    cursor.execute('select stu_id from student')
    result = cursor.fetchall()
    for i in result:
        temp = ''.join(i)  # 把元组元素转换为字符串
        list2.append(temp)
    cursor.close()
    conn.close()
    return list2


def insert():  # 插入数据
    delButton()
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    list_1 = []
    list_1.append(0)
    list_1.append(student_id.get())
    list_1.append(names.get())
    list_1.append(class1.get())
    list_1.append(age.get())
    list_1.append(serial.get())
    list_1.append(address.get())
    if student_id.get() == '':
        showerror(title='提示', message='输入不能为空')
    elif names.get() == '':
        showerror(title='提示', message='输入不能为空')
    elif class1.get() == '':
        showerror(title='提示', message='输入不能为空')
    elif age.get() == '':
        showerror(title='提示', message='输入不能为空')
    elif serial.get() == '':
        showerror(title='提示', message='输入不能为空')
    elif address.get() == '':
        showerror(title='提示', message='输入不能为空')
        # tkinter.messagebox.showinfo(title=None, message='输入为空')
    else:
        cursor.execute('insert into student values(%s,%s,%s,%s,%s,%s,%s)', tuple(list_1))
        conn.commit()  # 提交数据
        cursor.execute("select * from student")
        result = cursor.fetchall()  # 返回二维元组
        for i in result:
            #row1 = result[i]
            tree.insert('', 'end', values=deleted(i))
        cursor.close()
        conn.close()


def delButton():    # 清除tree所有数据
    x = tree.get_children()
    for item in x:
        tree.delete(item)


def show():  # 显示所有学生信息
    global row1
    delButton()
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    cursor.execute('select * from student ')  # 执行sql语句
    result = cursor.fetchall()   # 返回二维元组
    for i in result:
        #row1 = result[i]
        tree.insert('', 'end', values=deleted(i))
    cursor.close()
    conn.close()


def modify():   # 修改学生年龄
    delButton()
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    if student_id.get() == '':
        showerror(title="提示", message="输入为空")
    else:
        cursor.execute("update student set age='%s' where stu_id='%s'" % (age.get(), student_id.get()) )
        conn.commit()
        cursor.execute("select * from student where stu_id='%s'" % student_id.get())
        result = cursor.fetchone()
        tree.insert('', 'end', values=deleted(result))
        cursor.close()
        conn.close()


def delete_info():    # 删除学生信息
    delButton()
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    if student_id.get() == '':
        showerror(title="提示", message="输入为空")
    elif student_id.get() not in student1_id():
        showerror(title="提示", message="输入有误，请重新输入")
    else:
        cursor.execute('delete from student where stu_id="%s"' % student_id.get())  # 执行sql语句
        conn.commit()  # 提交数据
        cursor.execute('select * from student ')  # 执行sql语句
        result = cursor.fetchall()  # 返回二维元组
        for i in range(len(result)):
            row1 = result[i]
            tree.insert('', 'end', values=deleted(row1))
        cursor.close()
        conn.close()


def search():   # 查询一条学生信息
    delButton()
    conn = connect(host='localhost', port=3306, user='root', password='', database='test')
    cursor = conn.cursor()
    if student_id.get() == '':
        showerror(title="提示", message="输入为空")
    elif student_id.get() not in student1_id():
        showerror(title="提示", message="输入有误，请重新输入")
    else:
        cursor.execute('select * from student where stu_id="%s"' % student_id.get())  # 执行sql语句
        result = cursor.fetchone()  # 返回二维元组
        tree.insert('', 'end', values=deleted(result))
        cursor.close()
        conn.close()


tk = Tk()   # 创建窗体
student_id = StringVar()
names = StringVar()
class1 = StringVar()
age = StringVar()
serial = StringVar()
address = StringVar()

tk.title("学生管理系统")
tk.maxsize(900, 700)    # 设置窗口最大尺寸
Label(tk, text='学生信息管理系统', font=tkfont.Font(size=18), width=70, height=2,
      bg='#00798c').grid(row=0, sticky=W+E)

columns = ('学号', '姓名', '班级', '年龄', '所在系', '联系地址')
tree = ttk.Treeview(tk, height=20, show="headings", columns=columns)
tree.column('学号', width=150, anchor='center')
tree.column('姓名', width=150, anchor='center')
tree.column('班级', width=150, anchor='center')
tree.column('年龄', width=150, anchor='center')
tree.column('所在系', width=150, anchor='center')
tree.column('联系地址', width=150, anchor='center')
tree.column('联系地址', width=150, anchor='center')

tree.heading('学号', text='学号')
tree.heading('姓名', text='姓名')
tree.heading('班级', text='班级')
tree.heading('年龄', text='年龄')
tree.heading('所在系', text='所在系')
tree.heading('联系地址', text='联系地址')
tree.grid(row=1, sticky=W+E)  # 控件左右对齐


frame = Frame(tk)
frame.grid(row=2,pady=10)
Label(frame, text="学号：").grid(row=0, column=0)
Entry(frame, textvariable=student_id).grid(row=0, column=1)
student_id.get()
Label(frame, text="姓名：").grid(row=1, column=0)
Entry(frame, textvariable=names).grid(row=1, column=1)
names.get()
Label(frame, text="班级：").grid(row=2, column=0)
Entry(frame, textvariable=class1).grid(row=2, column=1)
class1.get()
Label(frame, text="年龄：").grid(row=3, column=0)
Entry(frame, textvariable=age).grid(row=3, column=1)
age.get()
Label(frame, text="所在系：").grid(row=4, column=0)
Entry(frame, textvariable=serial).grid(row=4, column=1)
serial.get()
Label(frame, text="联系地址：").grid(row=5, column=0)
Entry(frame, textvariable=address).grid(row=5, column=1, pady=5)
address.get()

Button(frame, text="显示", width=16, command=show).grid(row=0, column=3, padx=20, )
Button(frame, text="修改", width=16, command=modify).grid(row=1, column=3,)
Button(frame, text="插入", width=16, command=insert).grid(row=2, column=3, )
Button(frame, text="删除", width=16, command=delete_info).grid(row=3, column=3, )
Button(frame, text="查询", width=16, command=search).grid(row=4, column=3, )
tk.mainloop()