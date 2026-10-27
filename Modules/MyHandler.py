from Modules.XInput import *
from pynput.keyboard import Key, Controller
import Modules.mouse_api as Mouse
from math import pi,sin,cos,atan2

class MyHandler(EventHandler):
    def poll(self, tick):
        # All events in this tick share one time sample; no input worker thread.
        self.global_var.tick = tick
        for event in get_events(self.controllers):
            if not self.has_controller(event.user_index):
                continue
            if event.type in (EVENT_BUTTON_PRESSED, EVENT_BUTTON_RELEASED):
                self.process_button_event(event)
            elif event.type == EVENT_TRIGGER_MOVED:
                self.process_trigger_event(event)
            elif event.type == EVENT_STICK_MOVED:
                self.process_stick_event(event)
            elif event.type in (EVENT_CONNECTED, EVENT_DISCONNECTED):
                self.process_connection_event(event)

    def process_button_event(self,event):
        # Track physical state even for unmapped buttons or background windows.
        if event.type == EVENT_BUTTON_PRESSED:
            self.global_var.buttons_down.add(event.button)
        else:
            self.global_var.buttons_down.discard(event.button)
        # A speed modifier must not also send its normal keyboard/mouse mapping.
        if event.button == self.global_var.cursor_slow_button:
            return
        key_val = self.global_var.key_config.get(event.button, "")
        if key_val == "":
            return
        pressed = event.type == EVENT_BUTTON_PRESSED
        if self.global_var.key_onoff_mode[event.button]:
            if self.global_var.in_active_win and pressed:
                if key_val in self.global_var.onoff_list:
                    self.global_var.onoff_list.remove(key_val)
                else:
                    self.global_var.onoff_list.append(key_val)
            # The tick sends one repeat; the button event only toggles its state.
            return
        index = self.global_var.btn_dict[event.button]
        if pressed and self.global_var.in_active_win:
            self.kb_press_eval_key(key_val)
            self.global_var.keys_stat_last[index] = True
        elif not pressed and self.global_var.keys_stat_last[index]:
            self.kb_release_eval_key(key_val)
            self.global_var.keys_stat_last[index] = False

    def process_stick_event(self, event):
        #print(event)
        if event.stick == LEFT:
            self.global_var.stick_info[0]={"x":event.x,"y":event.y,"val":event.value,"dir":event.dir}
        else:
            self.global_var.stick_info[1]={"x":event.x,"y":event.y,"val":event.value,"dir":event.dir}

    def process_trigger_event(self, event):
        if event.trigger not in (LEFT, RIGHT):
            return
        button = "LEFT_TRIGER" if event.trigger == LEFT else "RIGHT_TRIGER"
        pressed = int(round(40 * event.value, 0)) > 0
        # Trigger modifiers also retain their ordinary mapping (e.g. LT -> Space).
        if pressed:
            self.global_var.buttons_down.add(button)
        else:
            self.global_var.buttons_down.discard(button)
        key_val = self.global_var.key_config[button]
        if key_val == "":
            return
        if self.global_var.in_active_win:
            if self.global_var.triger_stat[event.trigger] == int(pressed):
                return
            self.global_var.triger_stat[event.trigger] = int(pressed)
            if pressed:
                self.kb_press_eval_key(key_val)
            else:
                self.kb_release_eval_key(key_val)
        elif not pressed and self.global_var.triger_stat[event.trigger]:
            # A release after switching windows must not leave Space held down.
            self.global_var.triger_stat[event.trigger] = 0
            self.kb_release_eval_key(key_val)

    def process_connection_event(self, event):
        if event.type == EVENT_CONNECTED:
            if not self.global_var.controller_connected:
                print("已偵測到控制器，手柄已連接。", flush=True)
            self.global_var.controller_connected = True
        elif event.type == EVENT_DISCONNECTED:
            if self.global_var.controller_connected:
                print("未偵測到控制器，請接上支援的遊戲搖桿。", flush=True)
            self.global_var.controller_connected = False
            for button, index in self.global_var.btn_dict.items():
                if self.global_var.keys_stat_last[index]:
                    self.kb_release_eval_key(self.global_var.key_config[button])
                    self.global_var.keys_stat_last[index] = False
            for index, button in enumerate(("LEFT_TRIGER", "RIGHT_TRIGER")):
                if self.global_var.triger_stat[index]:
                    self.kb_release_eval_key(self.global_var.key_config[button])
                    self.global_var.triger_stat[index] = 0
            self.global_var.buttons_down.clear()
            self.global_var.onoff_list.clear()
            self.global_var.stick_info = [{"val": 0}, {"val": 0}]
        else:
            print("Unrecognized controller event type")

    def gent_degree_dict(self,divisions=360,radius=10):
        #divisions,radius=360,10
        out_dict={}
        # the difference between angles in radians -- don't bother with degrees
        angle = 2 * pi / divisions
        # a list of all angles using a list comprehension
        angles = [i*angle for i in range(divisions)]
        oi=0
        for a in angles:
            out_dict[oi]=[round(radius*sin(a)),(round(radius*cos(a)))]
            oi+=1
        return out_dict

    def deg_to_xy(self,deg_dict,deg):
        #deg_dict must be a dictionary
        xy_list=deg_dict[deg]
        return xy_list[0],-xy_list[1]
    
    def kb_press_eval_key(self,key_val):
        keyboard = Controller()
        if key_val!="": #不是空白才繼續動作
            if key_val not in ["LM","RM"]:
                if len(key_val)==1:
                    keyboard.press(key_val)
                else:
                    keyboard.press(eval("Key."+key_val))
            else:
                cx,cy=Mouse.get_pos()
                if key_val=="LM":
                    Mouse.click("left",cx,cy)
                else:
                    Mouse.click("right",cx,cy)

    def kb_release_eval_key(self,key_val):
        keyboard = Controller()
        if key_val!="": #不是空白才繼續動作
            if key_val not in ["LM","RM"]:
                if len(key_val)==1:
                    keyboard.release(key_val)
                else:
                    keyboard.release(eval("Key."+key_val))
            else:
                cx,cy=Mouse.get_pos()
                if key_val=="LM":
                    Mouse.click("left",cx,cy,0)
                else:
                    Mouse.click("right",cx,cy,0)
