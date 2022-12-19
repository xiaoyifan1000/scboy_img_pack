import shutil
import main
import time
import datetime
import DateTime
import zipfile
import os
import excel


RUN_Version = "1.1v"
main.SAVE_FILE = '.'
main.DEBUG["RUNNING_TIME"] = 1
main.DEFAULT["MIN_LIST_IMG"] = 3
main.cookies = {}

while True:
    # nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    # if nowtime == '03:30:00' or nowtime == '03:30:00':
    run = main.Run()
    run.first_run()
    run.down_scboy_biaoche()
    run.save_img_html()
    ex = excel.EXCEL()
    ex.write_in()
    del run
    time.sleep(1800)



