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







