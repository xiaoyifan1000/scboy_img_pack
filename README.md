# scboy_img_pack

说明：对scboy论坛飙车图片下载压制工具

<h5>main.py 主要文件</h5>
<h5>run.py 运行文件</h5>
<h5>excel.py excel文件生成</h5>
<h5>requirements.txt py运行需要的包</h5>

# 环境
<h3>请使用python3.7-3.9,并且运行以下代码构建需要的运行环境</h3>
<code>pip install -r requirements.txt</code>

# 可使用变量说明

<pre>
main.SAVE_FILE = '.'  # 点表示当前目录下，支持绝对路径和相对路径
main.DEBUG["NOT_DOWN_IMG"] = True  # 是否下载图片
main.DEBUG["NOT_DOWN_HOME"] = True  # 是否下载主文件
main.DEBUG["RUNNING_TIME"] = 1  # 是否下载运行间隔
main.DEFAULT["MIN_LIST_IMG"] = 3  # 如果页面少于3则跳过该页面
main.HTML_URL = "https://www.scboy.cc/"  # 论坛目标地址
main.DB_LITE = "scboy_href_img.db"  # 文件db缓存名称
main.cookies = {}  # cookies
</pre>

# 运行
<h4>运行之前，先填写run.py 里面的cookies，论坛飙车区必须登录状态才能访问，否则无法运行</h4>

<h5>cookie 获取自行百度，获取后按字典形式填写</h5>
<h4>配置好需要的设置后，运行run.py即可</h4>

# 文件生成目录

<pre>
---img # 图片生成目录
   ｜-thread-x00xxx.htm
      ｜- 图片
      ｜- 图片
      ｜- 图片
   ｜-scboy_href.xlsx
---Temp # 飙车页面储存页面缓存
   ｜
   thread-x00xxx.htm
---scboy_href_img.db  # 数据库
---scboy.html  # 主页面
---RUNNING.log  # 日志

</pre>

# 运行执行逻辑
<pre>
下载飙车页面
储存db文件，
将不在db文件中的页面地址进行下载进temp文件夹
下载temp文件夹中新加入的帖子中所有图片进img文件夹
更新scboy_href.xlsx文件
run = main.Run()  # 调用主文件，建db环境
run.first_run()  # 初始化
run.down_scboy_biaoche()  # 下载飙车页面
run.save_img_html()  # 缓存所有图片
ex = excel.EXCEL()  # 生成excel记录文件
ex.write_in()  # 写入
</pre>





   
  






