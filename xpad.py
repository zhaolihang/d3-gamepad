# 需安裝的套件 pypiwin32 pynput==1.6.8
# 0009A : 把程式改成兼容 PoE2 WASD 輸入的搖桿設定，並修正一個小Bug(有時進到遊戲時程式會閃退，用try ... except pass的笨方法避掉此問題)

XPAD_VERSION="XPAD-2026-10-27"

from time import sleep
from Modules.XInput import DEADZONE_TRIGGER,set_deadzone,get_connected
import Modules.mouse_api as Mouse
from pynput.keyboard import Key, Controller
from datetime import datetime
from Modules.WindowMgr import *
from traceback import extract_tb
from sys import argv,exc_info,exit
from msvcrt import kbhit,getch
from math import pi,sin,cos,atan2
from Modules.LoopTimer import LoopTimer
from Modules.InputTiming import tick_interval, cursor_settings, CursorMotion, DirectionKeys


def wait_for_controller(notified=False):
    while not get_connected()[0]:
        if not notified:
            print("未偵測到控制器，請接上支援的遊戲搖桿。", flush=True)
            notified = True
        if kbhit() and getch() == chr(8).encode():
            exit(0)
        sleep(0.1)
    print("已偵測到控制器，手柄已連接。", flush=True)


if __name__ == "__main__":
    try:
        ini_filename="xinput.ini"
        if len(argv)>1 and argv[1]!="" and (argv[1]).split(".")[1]=="ini":
            ini_filename=argv[1]
        #讀取 xinput.ini參數
        with open(ini_filename,"r",encoding="utf-8") as f:
            tmp_content=f.read()
        f.close()
        exec(tmp_content)
        interval = tick_interval(globals())
        cursor_speed, cursor_slow_button, cursor_slow_multiplier = cursor_settings(globals())

        set_deadzone(DEADZONE_TRIGGER,int(XY_OFFSET_UNIT))
        
        print("-----------------------------------------")
        print(f"{ACTIVE_WIN_TITLE} Gamepad 程式運作")
        print("在此視窗中按下 [←Backspace] 可關閉程式")
        print("或在遊戲中同時按住控制器:")
        print("LEFT_SHOULDER+RIGHT_SHOULDER+X一秒關閉程式")
        print("程式版本:"+XPAD_VERSION)
        print("監控視窗:"+ACTIVE_WIN_TITLE)
        print("-----------------------------------------")
        w=WindowMgr()
        #全域變數區.START
        from Modules.IniVariable import *
        keyboard = Controller()
        global_var=IniVariable()
        global_var.cx,global_var.cy=Mouse.get_pos()
        global_var.xy_offset=XY_OFFSET_UNIT
        global_var.deg_dict=global_var.gent_degree_dict(360,int(XY_OFFSET_UNIT))
        global_var.active_win_title=ACTIVE_WIN_TITLE
        global_var.key_config=KEY_CONFIG
        global_var.cursor_slow_button=cursor_slow_button
        global_var.set_left_controller_move_and_click=SET_LEFT_CONTROLLER_MOVE_AND_CLICK
        global_var.left_controller_click_val =LEFT_CONTROLLER_CLICK_VAL
        global_var.xy_offset_unit =XY_OFFSET_UNIT
        global_var.delay_second =interval
        global_var.y_center_offset =Y_CENTER_OFFSET
        global_var.btn_dict =BTN_DICT
        global_var.btn2_dict =BTN2_DICT
        global_var.onoff_list=[]
        global_var.debug_mode =DEBUG_MODE
        global_var.key_onoff_mode=KEY_ONOFF_MODE
        global_var.keys_stat_last=[False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        global_var.current_onoff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        global_var.in_active_win=False
        global_var.stick_info=[{"val":0},{"val":0}]
        #全域變數區.END
        from Modules.MyHandler import *
        handler = MyHandler(0,global_var_obj=global_var) # initialize handler object
        direction_keys = DirectionKeys(keyboard, LSTICK_DICT)
        cursor_motion = CursorMotion(cursor_speed)
        def tick(context):
            global_var.tick = context
            handler.global_var.in_active_win = ((ACTIVE_WIN_TITLE != "" and ACTIVE_WIN_TITLE in w.active_window_title())
                                               or ACTIVE_WIN_TITLE == "")
            handler.poll(context)
            if not global_var.controller_connected:
                return False
            if {"X", "LEFT_SHOULDER", "RIGHT_SHOULDER"}.issubset(handler.global_var.buttons_down):
                #按下LEFT_SHOULDER+RIGHT_SHOULDER+X 強制結束程式，結束前要先把已經按下的key全都release
                for i in range(0,len(handler.global_var.keys_stat_last)):
                    if handler.global_var.keys_stat_last[i]==True: #目前是按下狀態
                        #取得value
                        handler.kb_release_eval_key(KEY_CONFIG[BTN2_DICT[i]])
                exit(0)
            if kbhit() and getch() == chr(8).encode():
                exit(0)
            #判斷當前視窗完整標題文字是否包含 ACTIVE_WIN_TITLE 設定之文字，若是才繼續後續處理...
            if handler.global_var.in_active_win:
                handler.global_var.win_pos_size=w.get_window_pos_size() #[x,y,w,h]
                handler.global_var.x_center=int(handler.global_var.win_pos_size[0]+(handler.global_var.win_pos_size[2]/2))
                handler.global_var.y_center=int(handler.global_var.win_pos_size[1]+(handler.global_var.win_pos_size[3]/2)+(Y_CENTER_OFFSET))
                #if DEBUG_MODE: print("LEFT STICK:",handler.global_var.stick_info[0])
                try:
                    if handler.global_var.stick_info[0]["val"]!=0: #左小搖桿
                        deg=int(atan2(handler.global_var.stick_info[0]["x"],handler.global_var.stick_info[0]["y"])/pi*180)
                        if deg<0: deg=180+(180+deg)
                        if DEBUG_MODE: print(f"LeftStickDeg:{deg}")
                        direction_keys.update(deg)
                        handler.global_var.stick_degree[0]=deg
                        # 處理滑鼠遊標是否移至畫面中心再隨LSTICK方向移動
                        if SET_LFET_CONTROLLER_BIND_CURSOR:
                            xx,yy=handler.deg_to_xy(handler.global_var.deg_dict,deg)
                            target_pos = (handler.global_var.x_center+xx*handler.global_var.xy_offset_unit,
                                          handler.global_var.y_center+yy*handler.global_var.xy_offset_unit)
                            if Mouse.get_pos() != target_pos:
                                Mouse.set_pos(*target_pos)
                            if SET_LEFT_CONTROLLER_MOVE_AND_CLICK:
                                handler.kb_press_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                                handler.kb_release_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                            #if DEBUG_MODE: print("LEFT STICK:",xx,yy)
                    else:
                        direction_keys.update(None)
                except:
                    pass
                try:
                    if handler.global_var.stick_info[1]["val"]!=0: #右小搖桿
                        speed_multiplier = cursor_slow_multiplier if cursor_slow_button in handler.global_var.buttons_down else 1.0
                        move_x, move_y = cursor_motion.step(handler.global_var.stick_info[1]["dir"], context.dt, speed_multiplier)
                        if move_x or move_y:
                            Mouse.move_to(move_x, move_y)
                    else:
                        cursor_motion.reset()
                except:
                    pass
                if len(handler.global_var.onoff_list)>0:
                    for i in handler.global_var.onoff_list:
                        handler.kb_press_eval_key(i)
                        handler.kb_release_eval_key(i)
            else:
                direction_keys.update(None)
                cursor_motion.reset()
            return True

        waiting_notified = False
        while True:
            wait_for_controller(notified=waiting_notified)
            global_var.controller_connected = True
            loop_timer = LoopTimer(interval)
            while tick(loop_timer.wait()):
                pass
            direction_keys.update(None)
            cursor_motion.reset()
            waiting_notified = True
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = exc_info() #取得Call Stack
        lastCallStack = extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        with open('runtime_error.log','a+',encoding='utf-8') as f:
            f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\t'+errMsg+'\n')
        print(errMsg)
        exit(0)
