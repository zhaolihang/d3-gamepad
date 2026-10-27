[![watching-on-youtube](watching-on-youtube.png)](https://www.youtube.com/watch?v=jRizX1KbwZ8)

# D3-XPAD

### 更新日期: 2025-10-06 22:00:00 ver.0009A

-----

## 目錄
1. [關於 D3-XPAD :: About](https://github.com/ccutmis/d3-gamepad#1-%E9%97%9C%E6%96%BC-d3-xpad--about)
2. [下載與安裝 :: Download & Install](https://github.com/ccutmis/d3-gamepad#2-%E4%B8%8B%E8%BC%89%E8%88%87%E5%AE%89%E8%A3%9D%E7%A7%BB%E9%99%A4--download--install)
3. [如何使用 :: How to Use](https://github.com/ccutmis/d3-gamepad#3-%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8--how-to-use)
4. [注意事項 :: Notice](https://github.com/ccutmis/d3-gamepad#4-%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A0%85--notice)
5. [特別聲明 :: Statement](https://github.com/ccutmis/d3-gamepad#5-%E7%89%B9%E5%88%A5%E8%81%B2%E6%98%8E--statement)
6. [更新日誌 :: Log](https://github.com/ccutmis/d3-gamepad#6-%E6%9B%B4%E6%96%B0%E6%97%A5%E8%AA%8C--log)
7. [參考資源 :: References](https://github.com/ccutmis/d3-gamepad#7-%E5%8F%83%E8%80%83%E8%B3%87%E6%BA%90--references)

-----

## 1. 關於 D3-XPAD :: About

開發這個小程式的起因是在巴哈暗黑III論壇看到有網友詢問能否用XBOX搖桿玩PC版D3，當時想到可以用Python寫一個小程式獲取搖桿輸入然後模擬鍵盤滑鼠輸入，程式開發大約花了一周把大部份問題處理好，然後有巴友回報他用XBOX ONE手把沒法使用這個小程式，經過一些研究後發現先前寫好的 D3-Gamepad-Mapper，只能用XBOX360手把執行(感謝巴哈網友測試回報)。

為了讓程式能支援更多不同類型手把，這邊把原本的Reposite作廢，重新開一個新的Reposite:D3-Gamepad並用XInput-Python模組為核心獲取搖桿輸入，現在程式可以在Win10環境使用XBOX360及XBOX ONE手把玩D3 (Win7測試可玩但建議OS升到Win10)。
未來或許會加上對PS搖桿的支援(時間未定)

-----

## 2. 下載與安裝移除 :: Download & Install

D3-XPAD 執行目錄為 `XPAD`，可依下方編譯指令產生，裡面需要二個檔案:

* xpad.exe (主程式直接點兩下即可執行)
* xinput.ini (搖桿對應設定檔，建議使用Notepad++編輯)
本軟體無需安裝，將執行目錄放到桌面(或好找的路徑)即完成部署。程式執行時不會修改電腦機碼，若要移除就是直接把主程式跟設定檔刪除即可。

### xinput.ini 設定檔內容

```
#這是一行註解

#設定要啟用搖桿對應的程式標題文字，防止在切換不同視窗程式時可能造成的誤操作
#ACTIVE_WIN_TITLE=" " #雙引號內為單個空白字元時，搖桿對應所有的視窗程式都會有作用，此模式在特殊場景下有妙用。
ACTIVE_WIN_TITLE="暗黑破壞神III"

#key_config字典用來定義按鍵值(設""則該鍵無作用)
KEY_CONFIG={
	"A":"1",
	"B":"2",
	"X":"3",
	"Y":"4",
	"BACK":"t",
	"START":"q",
	"DPAD_UP":"tab",
	"DPAD_DOWN":"m",
	"DPAD_LEFT":"i",
	"DPAD_RIGHT":"s",
	"LEFT_SHOULDER":"esc",
	"RIGHT_SHOULDER":"LM",
	"LEFT_TRIGER":"space",
	"RIGHT_TRIGER":"RM"
}

#設定按鍵改為ON/OFF模式，就是按一下就保持按下狀態，再按一下就取消，
#目前設定所有按鍵關閉此功能，可依自己需求作更改，1為ON，0為OFF，本功能需小心使用。
KEY_ONOFF_MODE={
	"A":0,
	"B":0,
	"X":0,
	"Y":0,
	"BACK":0,
	"START":0,
	"DPAD_UP":0,
	"DPAD_DOWN":0,
	"DPAD_LEFT":0,
	"DPAD_RIGHT":0,
	"LEFT_SHOULDER":0,
	"RIGHT_SHOULDER":0,
	"LEFT_TRIGER":0,
	"RIGHT_TRIGER":0
}

LSTICK_DICT={"up":Key.up,"down":Key.down,"left":Key.left,"right":Key.right}

#設定左小搖桿觸發後滑鼠游標是否連動
SET_LFET_CONTROLLER_BIND_CURSOR = True

#設定左小搖桿在控制滑鼠移動後是否按一下滑鼠左鍵
#設為 True 則在左小搖桿控制滑鼠移動後會在滑鼠所在位置按一下左鍵，要取消則設為 False
SET_LEFT_CONTROLLER_MOVE_AND_CLICK = True
#設定左小搖桿控制滑鼠移動後會點的鍵，假如 SET_LEFT_CONTROLLER_MOVE_AND_CLICK 為 True
LEFT_CONTROLLER_CLICK_VAL = "LM"

#左搖桿光標落點距離的基準單位
XY_OFFSET_UNIT=10
#右搖桿固定光標速度（像素／秒），無持續推桿加速
CURSOR_SPEED=600
#按住 LT 時同時保留空白鍵映射並降低右搖桿光標速度
#LEFT_TRIGER=LT，RIGHT_TRIGER=RT；設為 "" 可停用半速
CURSOR_SLOW_BUTTON="LEFT_TRIGER"
CURSOR_SLOW_MULTIPLIER=0.5

#唯一的 tick 頻率（Hz），輸入、光標、移動點擊與 ON/OFF 連發都在此 tick 執行
#可改為 120、180、240 等正數；滑鼠速度由 dt 換算，不隨頻率變快
TICK_HZ=60

#Y軸中心點修正(基本上勿動)
Y_CENTER_OFFSET=-(XY_OFFSET_UNIT*4)

#勿動BTN_DICT及BTN2_DICT
BTN_DICT={ "A":0, "B":1, "X":2, "Y":3, "BACK":4, "START":5, "DPAD_UP":6, "DPAD_DOWN":7, "DPAD_LEFT":8, "DPAD_RIGHT":9, "LEFT_SHOULDER":10, "RIGHT_SHOULDER":11, "LEFT_TRIGER":12, "RIGHT_TRIGER":13 }
BTN2_DICT={ 0:"A", 1:"B", 2:"X", 3:"Y", 4:"BACK", 5:"START", 6:"DPAD_UP", 7:"DPAD_DOWN", 8:"DPAD_LEFT", 9:"DPAD_RIGHT", 10:"LEFT_SHOULDER", 11:"RIGHT_SHOULDER", 12:"LEFT_TRIGER", 13:"RIGHT_TRIGER" }
#是否啟用degug模式(勿動) 預設值為False
DEBUG_MODE=False


```

![controller-mapping](controller-mapping.png)

修改 xinput.ini 注意事項:
1. 編輯此文件推薦使用Notepad++，如果用記事本編輯在存檔時需注意是否存為"utf-8"文件格式(不可為"Big5"或"utf-8 BOM"格式會出錯)。
2. 只能更改KEY_CONFIG字典裡的值，例如: "A":"1" 改成 "A":"i"，這樣執行程式時按下搖桿A鍵就會模擬按下i鍵，只可修改值不可破壞格式。

程式只有一個 `TICK_HZ`（預設 60，必須為有限正數）。每輪統一讀取單調時鐘，計算 `TickContext(time, dt, raw_dt, index)`，再呼叫 `tick(context)`。事件處理器可透過 `handler.global_var.tick.dt` 取得同一份 dt，其他邏輯直接使用傳入的 context。等待時間會扣除本輪處理耗時，延遲後沿原時間表前進，不累積時間漂移，也不集中補發過期操作。舊設定檔的 `LOOP_HZ` 或 `DELAY_SECOND` 只作為單一頻率的相容輸入，新設定優先使用 `TICK_HZ`。

啟動時先檢查編號 0 的控制器；未連接時顯示一次提示並等待，偵測到連接後才進入 tick，等待期間也可按 Backspace 結束。tick 每輪呼叫一次 `XInputGetState` 同時取得輸入及連接狀態，不再額外查詢在線狀態；讀取時發現斷線會立即停止 tick、釋放按鍵並回到連接監測。重新連接後重置 tick 計時再繼續，等待時間不會算入 dt。連接提示只在狀態改變時輸出，不會每 tick 重複刷屏。

手把狀態在 tick 裡直接輪詢，不建立輸入執行緒。方向鍵、普通按鍵與扳機僅在狀態變化時發送按下／鬆開；連續改變扳機力度不會重複發送按下。左搖桿持續更新光標目標，位置相同時不重複設定光標；持續推桿時，每 tick 執行一次移動點擊／設定的移動按鍵。啟用 ON/OFF 的每個操作也每 tick 執行一次按下＋鬆開，因此它們的頻率隨 `TICK_HZ` 變化，沒有獨立的 60 Hz 設定。

右搖桿以 `CURSOR_SPEED` 指定固定速度（預設 600 像素／秒），超過死區後不隨持續推桿時間或推桿幅度加速，斜向也維持相同總速度；位移只使用 tick 傳入的 `dt` 並保留不足一像素的餘數。回中或切換視窗時清除餘數。tick 統一將 dt 限制為最多 0.1 秒，避免卡頓後光標跳躍；實際未截斷的時間可從 `context.raw_dt` 取得。舊設定檔的 `CURSOR_MOVE_UNIT` 仍可換算為固定速度（乘 20），若同時設定則優先使用 `CURSOR_SPEED`。光標落點半徑與方向判定不需要乘 `dt`。

按住 `CURSOR_SLOW_BUTTON` 時，右搖桿光標速度乘以 `CURSOR_SLOW_MULTIPLIER`（預設 0.5，即 300 像素／秒），鬆開立即恢復正常速度。預設使用 LT（設定檔沿用舊名稱 `LEFT_TRIGER`）：LT 超過原有觸發閾值後照常按住空白鍵，同時進入半速；鬆開時釋放空白鍵並恢復正常光標速度。LB 保留原本的 Esc，M4 與正面 Y 保留原本的數字 4。空字串表示停用半速功能，LT 仍保留空白鍵映射。

可將半速鍵設為 RT（`RIGHT_TRIGER`），扳機作為半速鍵時仍保留 `KEY_CONFIG` 映射；也可指定普通按鈕，如空閒的 L3（`LEFT_THUMB`）、R3（`RIGHT_THUMB`），無需將 L3/R3 加入 `BTN_DICT`，普通按鈕作為半速鍵時會攔截其原映射。倍率必須大於 0 且不大於 1。半速只作用於右搖桿光標，左搖桿角色移動與點擊頻率保持原設定。退出組合鍵 LB+RB+X 仍可使用。

實際 tick 頻率仍受 Windows 排程及處理負載影響。提高 `TICK_HZ` 會提高輸入取樣、光標更新、移動點擊與連發次數，光標每秒移動速度保持不變。

執行原始碼可使用 `python xpad.py`。執行檔輸出至 `XPAD/xpad.exe`，使用同目錄下的 `xinput.ini`，不產生發佈 zip。本機可繼續使用已指向 `XPAD` 目錄的 `D3-XPAD-Start.bat` 啟動。打包部署直接覆蓋，不額外建立備份；部署設定保留本機視窗標題與左搖桿移動鍵。

-----

## 3. 如何使用 :: How to Use

1. 先開啟Diablo III，將畫面顯示設為"全螢幕視窗模式"或"視窗模式"。
2. 確定你的xbox搖桿有接在PC端並正常運作中(可在控制台裡的裝置及印表機項目確認)
3. 執行 xpad.exe 並切換到 Diablo III，拿起搖桿測試看看。
4. 要結束 xpad.exe 很簡單，同時按住控制器的 (LEFT_SHOULDER)+(RIGHT_SHOULDER)+(X) 程式會直接結束。

-----

## 4. 注意事項 :: Notice

### 設備需求:
1. Windows11作業系統(Win10測試可玩但建議OS升到Win11)
2. 目前測試可支援的PC相容搖桿為XBOX360、XBOX ONE、羅技F310，其它搖桿不確定是否可正常運作。

![support-equipments](support-equipments.png)

-----

## 5. 特別聲明 :: Statement

* 本程式無償提供任何人使用，歡迎轉載連結。
* 本程式執行時會依搖桿輸入模擬鍵盤滑鼠動作，若在執行中造成任何非預期之損失概不負責，特此聲明。
* 目前程式基本運作應該是沒問題的，建議在執行xpad.exe的時候先不要開啟 Diablo III以外的任何程式，試試看有沒有問題，當然程式不可能完全沒bugs，未來有修正版會在這邊持續更新。

-----

## 6. 更新日誌 :: Log

### 更新日期: 2025-10-06 22:00:00 ver.0009A
更新內容:
* 把程式改成兼容 PoE2 WASD 輸入的搖桿設定，並修正一個小Bug(有時進到遊戲時程式會閃退，用try ... except pass的笨方法避掉此問題)，經過這次修正，使用Moonlight遠端連PC時使用本程式可以正常遊戲D3了。

### 更新日期: 2020-12-27 22:00:00 ver.0007C
更新內容:
* 重寫左右stick控制滑鼠移動的部份，右stick在長按時會有小加速的效果

### 更新日期: 2020-12-26 14:00:00 ver.0006C
更新內容:
* 優化定時偵測機制(控制滑鼠移動與ONOFF自動施法加上間隔，避免過度連點地面可能造成的遊戲崩潰。

### 更新日期: 2020-12-24 00:30:00 ver.0005C
更新內容:
* 修正R_TRIGER有時會自己重覆施放及監控目標視窗的bug

### 更新日期: 2020-12-21 21:00:00 ver.0003C-Hotfix
更新內容:
* 今天試玩的時候發現在遊戲中LEFT_TRIGER與RIGHT_TRIGER會有不正常的反應，比如說按REFT_TRIGER後會自己不間斷的施放，有點類似系統收到了按下右鍵的訊號，但是放開右鍵的訊號漏掉了。重新檢視原碼並作適當的修正，目前應該能正常運作了。


### 更新日期: 2020-12-20 11:00:00 ver.0003C
更新內容:
* 重整 xpad.py 混亂的代碼 將class整合到Modules裡
* 由於必須改寫XInput.py裡某個class的建構式才能做到class重整，因此將XInput.py整合到Modules裡，未來XInput-Python就不需安裝了
* 追加設定檔功能: 設定按鍵為ON/OFF模式
* 追加用控制器關閉程式的按鍵組合:LEFT_SHOULDER+RIGHT_SHOULDER+X
* 優化判斷當前作用視窗部份(原本在主程式&Class的按鍵搖桿事件裡都會判斷一次，這樣造成重覆運算浪費資源，現在重寫為只在主程式裡判斷

### 更新日期: 2020-12-14 12:30:00 ver.0002C
更新內容:
* 廢除舊版Repo:d3-gamepad-mapper 發佈新版Repo:d3-gamepad 並將主程式 main.py 重新命名為 xpad.py
* 廢除舊版Repo:d3-gamepad-mapper 網址: https://github.com/ccutmis/d3-gamepad-mapper

-----

## 7. 參考資源 :: References

### xpad.py 編譯參考資料

在專案根目錄使用 PowerShell 執行（目前以 Python 3.14 驗證）：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --distpath XPAD --workpath build\pyinstaller xpad.spec
```

`xpad.spec` 使用專案相對路徑，與 `requirements-build.txt` 一起納入版本管理。`xinput.ini` 保持外置，不會被打包指令覆蓋；若執行目錄尚無設定檔，需從根目錄複製並依需求修改。

* resource url: https://github.com/Zuzu-Typ/XInput-Python
* 建置與執行依賴版本見 `requirements-build.txt`；XInput 模組已包含在 `Modules` 中
* 要在win7能正常運作需把XInput.py裡第140~145行註解掉

### D3官網對於家機搖桿的設置參考
https://diablo3.blizzard.com/en-us/game/guide/gameplay/fundamentals

### pygame.joystick(參考頁面里的搖桿分類)
https://www.pygame.org/docs/ref/joystick.html

### get controller event:
https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python

### control mouse action:
https://stackoverflow.com/questions/4263608/ctypes-mouse-events

### simulor keydown:
https://stackoverflow.com/questions/11906925/python-simulate-keydown/11910555

### pynput使用簡單說明
https://www.itread01.com/content/1541887278.html

