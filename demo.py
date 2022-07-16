import tkinter as tk
from tkinter import Toplevel, image_types, messagebox
from tkinter import font
from tkinter.constants import FALSE
import cv2
from PIL import Image
import time
import pickle
import os

# 拍照
def openCap():

  cap = cv2.VideoCapture(0)

  width = 640
  height = 480

  # 设置宽度
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  # 设置长度
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)

    cv2.imshow('注册', img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
      now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
      os.makedirs('./photo/', exist_ok=True) # 输出目录
      cv2.imwrite('./photo/' + now + '.jpg', img)
      
      tk.messagebox.showinfo(title='提示', message='注册成功')
      break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

# 实例化object，建立窗口window
window = tk.Tk()

# 给窗口的可视化起名字
window.title('嘿，看镜头😉')

# 设定窗口的大小（长 * 宽）
window.geometry('640x480')

# 在图形界面上设定标签
# 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
var = tk.StringVar()

# 表单控件 文字
tk.Label(window, text='用户名').place(x = 150, y = 200)
tk.Label(window, text='密 码').place(x = 150, y = 250)

# 表单控件 输入框 用户名/密码
username_text = tk.StringVar()
entry_username = tk.Entry(window, textvariable=username_text, width=28)
entry_username.place(x = 200, y = 200)

password_text = tk.StringVar()
entry_password = tk.Entry(window, textvariable=password_text, show="*",width=28)
entry_password.place(x = 200, y = 250)

# 登录注册
def user_login():
  # 获取用户登陆信息
  user_name = username_text.get()
  user_pwd = password_text.get()

  # window_login = Toplevel()
  # window_login.title('登录中...')
  # window_login.geometry('640x480')

  # 将用户信息存入本地
  try:
    with open("user_info.pickle", 'rb') as f:
      user_info = pickle.load(f)
  except Exception as e:
    with open("user_info.pickle", 'wb') as f:
      user_info = {'admin':'123456'}
      pickle.dump(user_info,f)
  pass

  # 验证用户信息是否正确
  if user_name in user_info:
    if (user_pwd == user_info[user_name]):
      tk.messagebox.showinfo(title='欢迎', message='你好，' + user_name + '!')
      # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
      l = tk.Label(window, textvariable=var, fg='white', font=('Arial', 12), width=30, height=2)
      l.pack()

      # 注册
      b_take = tk.Button(window, text='注册', font=('Arial', 12), width=10, height=4, command=openCap)
      b_take.pack()

      # 识别
      r_take = tk.Button(window, text='识别', font=('Arial', 12), width=10, height=4, command=eyeDetect)
      r_take.pack()

    else:
      tk.messagebox.showerror(title='错误', message='密码错误，请重试！')
  else:
    is_sign_up = tk.messagebox.askyesno(title='是否注册', message='您还没有注册，请问是否注册呢？')
    if(is_sign_up):
      user_signup()

# 点击注册按钮后处理的业务逻辑
def user_signup():

  def sign_to_database():

    n_pwd = new_pwd.get()
    nr_pwd = new_pwd_confirm.get()
    n_name = new_name.get()

    # 读取本地用户信息
    with open('user_info.pickle', 'rb') as f:
      exists_user_info = pickle.load(f)

    # 判断两处密码是否一致
    if(n_pwd != nr_pwd):
      tk.messagebox.showerror(title='错误',message='两次密码输入不一致，请重试！')
      pass
    else:
      # 判断该用户是否存在数据库
      if (n_name in exists_user_info):
        tk.messagebox.showerror(title='错误',message='该用户已存在！')
      else:
        # 更新写入本地数据
        exists_user_info[n_name] = nr_pwd
        with open("user_info.pickle", 'wb') as f:
          pickle.dump(exists_user_info,f)
        # 注册成功
        tk.messagebox.showinfo(title='欢迎',message='注册成功！')
        # 关闭窗口
        window_signup.destroy()
  
  window_signup = tk.Toplevel(window)
  window_signup.title('欢迎注册！')
  window_signup.geometry('350x200')

  new_name = tk.StringVar()
  # new_name.set('example@python.com')
  tk.Label(window_signup, text='用户名: ').place(x = 10, y = 10)
  entry_new_name = tk.Entry(window_signup, textvariable=new_name)
  entry_new_name.place(x=150, y=10)

  new_pwd = tk.StringVar()
  tk.Label(window_signup, text='密码：').place(x = 10, y = 50)
  entry_usr_pwd = tk.Entry(window_signup, textvariable=new_pwd, show='*')
  entry_usr_pwd.place(x = 150, y = 50)

  # 再次输入密码框
  new_pwd_confirm = tk.StringVar()
  tk.Label(window_signup, text="确认密码").place(x = 10, y = 90)
  tk.Entry(window_signup, textvariable=new_pwd_confirm, show="*").place(x = 150, y = 90)

  # 确定按钮
  btn_confirm_signup = tk.Button(window_signup, text="注册", command=sign_to_database).place(x = 150, y = 130)
  pass

# 退出函数
def user_sign_out():
  window.destroy()

# 识别
def eyeDetect():
  face_cascade = cv2.CascadeClassifier('./Cascades/haarcascade_frontalface_default.xml')
  eye_cascade = cv2.CascadeClassifier('./Cascades/haarcascade_eye.xml')

  cap = cv2.VideoCapture(0)

  while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = img[y:y+h, x:x+w]
      eyes = eye_cascade.detectMultiScale(roi_gray)
      for (ex, ey, ew, eh) in eyes:
        os.makedirs('./recognize/', exist_ok=True) # 输出目录
        now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        pic = cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
        cv2.imshow('识别', pic)
        if cv2.waitKey(1) & 0xFF == ord('s'):
          cv2.imwrite('./recognize/' + now + '.jpg', pic)
          tk.messagebox.showinfo(title='提示',message='识别成功！')
          break

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

btn_login = tk.Button(window, text="登录", command=user_login)
btn_login.place(x = 200, y = 290)

btn_signup = tk.Button(window, text="注册", command=user_signup)
btn_signup.place(x = 300, y = 290)

btn_logout = tk.Button(window, text="退出", command=user_sign_out)
btn_logout.place(x = 400, y = 290)

# 主窗口循环显示
window.mainloop()