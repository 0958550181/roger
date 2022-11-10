def 左轉優先():
    global 地圖資料, 找到終點
    執行動作("直走")
    if 路口型態 == 9:
        執行動作("停止")
        地圖資料 = "" + 地圖資料 + "E"
        找到終點 += 1
    elif 路口型態 % 2 == 1:
        地圖資料 = "" + 地圖資料 + "L"
        執行動作("左轉")
    elif 路口型態 == 6:
        地圖資料 = "" + 地圖資料 + "S"
    elif 路口型態 == 0:
        地圖資料 = "" + 地圖資料 + "B"
        執行動作("迴轉")
    elif 路口型態 == 4:
        地圖資料 = "" + 地圖資料 + "R"
        執行動作("右轉")
def 判斷十字T字路口():
    global 路口, 路口型態, 路口判斷結束
    if 紅外線IR1 < 1000 and (紅外線IR5 < 1000 and 右轉紅外線狀態 + 左轉紅外線狀態 == 2):
        if 中間紅外線狀態 == 1:
            路口 = "十字"
            路口型態 = 7
            路口判斷結束 = 1
        else:
            路口 = "T字"
            路口型態 = 5
            路口判斷結束 = 1
def 判斷終點():
    global 終點時間, 路口, 路口型態, 路口判斷結束
    if 紅外線IR1 > 3000 and (紅外線IR3 == 3000 and 紅外線IR5 < 3000):
        終點時間 = 1
        if 終點時間 >= 40:
            終點時間 = 0
            路口 = "終點"
            路口型態 = 9
            路口判斷結束 = 1
    else:
        終點時間 = 0
def 設定旋轉速度(右輪速: number, 左輪速: number):
    BitRacer.motor_run(BitRacer.Motors.M_R, 右輪速)
    BitRacer.motor_run(BitRacer.Motors.M_R, 左輪速)
def 左轉終止():
    global 吸線狀態, 停止動作
    BitRacer.LED(BitRacer.LEDs.LED_L, BitRacer.LEDswitch.ON)
    while 停止動作 == 0:
        if BitRacer.read_ir(BitRacer.IR_Sensors.IR3) < 2000 and BitRacer.read_ir(BitRacer.IR_Sensors.IR2) > 2000:
            吸線狀態 = 0
            吸線()
            停止動作 = 1
    BitRacer.LED(BitRacer.LEDs.LED_L, BitRacer.LEDswitch.OFF)
def 記憶碰到路口():
    global 停止動作
    while 停止動作 == 0:
        PD控制(200, 250, 210)
        讀取紅外線()
        if 紅外線IR1 >= 1500 or (紅外線IR5 >= 1500 or 紅外線IR3 <= 1500):
            BitRacer.motor_run(BitRacer.Motors.ALL, 150)
            路口判斷()
            停止動作 = 1
def 判斷左卜左彎():
    global 路口, 路口型態, 路口判斷結束
    if 紅外線IR1 < 1000 and (右轉紅外線狀態 == 0 and 左轉紅外線狀態 == 1):
        if 中間紅外線狀態 == 1:
            路口 = "左卜"
            路口型態 = 3
            路口判斷結束 = 1
        else:
            路口 = "左彎"
            路口型態 = 1
            路口判斷結束 = 1

def on_button_pressed_a():
    global 地圖資料
    music.play_tone(988, music.beat(BeatFraction.WHOLE))
    basic.pause(1000)
    地圖資料 = ""
    while 找到終點 == 0:
        左轉優先()
    簡化路徑()
    music.play_tone(988, music.beat(BeatFraction.WHOLE))
    basic.show_icon(IconNames.SQUARE)
    basic.pause(1000)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def 簡化路徑():
    global 地圖資料
    while 地圖資料.includes("B"):
        music.play_tone(988, music.beat(BeatFraction.HALF))
        serial.write_line(地圖資料)
        地圖資料 = 替換地圖資料(地圖資料, "LBL", "S")
        地圖資料 = 替換地圖資料(地圖資料, "LBS", "R")
        地圖資料 = 替換地圖資料(地圖資料, "SBL", "R")
        地圖資料 = 替換地圖資料(地圖資料, "LBR", "B")
        地圖資料 = 替換地圖資料(地圖資料, "RBL", "B")
        地圖資料 = 替換地圖資料(地圖資料, "SBS", "B")
def 右轉終止():
    global 吸線狀態, 停止動作
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.ON)
    while 停止動作 == 0:
        if BitRacer.read_ir(BitRacer.IR_Sensors.IR3) < 2000 and BitRacer.read_ir(BitRacer.IR_Sensors.IR4) > 2000:
            吸線狀態 = 0
            吸線()
            停止動作 = 1
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.OFF)
def 替換地圖資料(地圖: str, 簡化路口: str, 替換資料: str):
    global Path, 簡化indesx
    Path = 地圖
    while Path.includes(簡化路口):
        簡化indesx = Path.index_of(簡化路口)
        Path = "" + Path.substr(0, 簡化indesx) + 替換資料 + Path.substr(簡化indesx + len(簡化路口), len(Path) - (簡化indesx + len(簡化路口)))
    serial.write_line(Path)
    basic.pause(10)
    return Path
def 判斷死路():
    global 路口, 路口型態, 路口判斷結束
    if 紅外線IR2 < 1000 and (紅外線IR3 < 1000 and 右轉紅外線狀態 + 左轉紅外線狀態 == 0):
        路口 = "死路"
        路口型態 = 0
        路口判斷結束 = 1
def 碰到路口():
    global 停止動作
    while 停止動作 == 0:
        PD控制(200, 250, 210)
        讀取紅外線()
        if 紅外線IR1 >= 1500 or (紅外線IR5 >= 1500 or 紅外線IR3 <= 1500):
            BitRacer.motor_run(BitRacer.Motors.ALL, 150)
            路口判斷()
            停止動作 = 1

def on_button_pressed_ab():
    BitRacer.calibrate_begin()
    music.play_tone(988, music.beat(BeatFraction.WHOLE))
    BitRacer.motor_run(BitRacer.Motors.ALL, 300)
    basic.pause(1000)
    BitRacer.motor_run(BitRacer.Motors.ALL, 0)
    music.play_tone(988, music.beat(BeatFraction.HALF))
    music.rest(music.beat(BeatFraction.WHOLE))
    music.play_tone(988, music.beat(BeatFraction.HALF))
    BitRacer.calibrate_end(BitRacer.LineColor.WHITE)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def 執行動作(動作: str):
    global 停止動作
    停止動作 = 0
    if 動作 == "右轉":
        設定旋轉速度(1, 1)
        右轉終止()
    elif 動作 == "左轉":
        設定旋轉速度(1, 1)
        左轉終止()
    elif 動作 == "迴轉":
        設定旋轉速度(1, 1)
        迴轉終止()
    elif 動作 == "直走":
        碰到路口()
    elif 動作 == "直走加速":
        記憶碰到路口()
    elif 動作 == "停止":
        BitRacer.motor_run(BitRacer.Motors.ALL, 0)
        music.play_tone(988, music.beat(BeatFraction.WHOLE))

def on_button_pressed_b():
    global 動作2
    music.play_tone(988, music.beat(BeatFraction.WHOLE))
    basic.pause(1000)
    index = 0
    while index <= len(地圖資料) - 1:
        執行動作("直走加速")
        動作2 = 地圖資料.char_at(index)
        if 動作2 == "R":
            執行動作("右轉")
        elif 動作2 == "L":
            執行動作("左轉")
        elif 動作2 == "E":
            執行動作("停止")
        index += 1
input.on_button_pressed(Button.B, on_button_pressed_b)

def 讀取紅外線():
    global 紅外線IR1, 紅外線IR2, 左轉紅外線狀態, 紅外線IR3, 中間紅外線狀態, 紅外線IR4, 紅外線IR5, 右轉紅外線狀態
    紅外線IR1 = BitRacer.read_ir(BitRacer.IR_Sensors.IR1)
    紅外線IR2 = BitRacer.read_ir(BitRacer.IR_Sensors.IR2)
    if 紅外線IR1 > 3000:
        左轉紅外線狀態 = 1
    紅外線IR3 = BitRacer.read_ir(BitRacer.IR_Sensors.IR3)
    if 紅外線IR3 > 3000:
        中間紅外線狀態 = 1
    else:
        中間紅外線狀態 = 0
    紅外線IR4 = BitRacer.read_ir(BitRacer.IR_Sensors.IR4)
    紅外線IR5 = BitRacer.read_ir(BitRacer.IR_Sensors.IR5)
    if 紅外線IR5 > 3000:
        右轉紅外線狀態 = 1
def 判斷右卜右彎():
    global 路口, 路口型態, 路口判斷結束
    if 紅外線IR5 < 1000 and (右轉紅外線狀態 == 1 and 左轉紅外線狀態 == 0):
        if 中間紅外線狀態 == 1:
            路口 = "右卜"
            路口型態 = 6
            路口判斷結束 = 1
        else:
            路口 = "右彎"
            路口型態 = 4
            路口判斷結束 = 1
def 路口判斷():
    global 右轉紅外線狀態, 左轉紅外線狀態, 路口判斷結束
    右轉紅外線狀態 = 0
    左轉紅外線狀態 = 0
    路口判斷結束 = 0
    while 路口判斷結束 == 0:
        讀取紅外線()
        判斷終點()
        判斷十字T字路口()
        判斷左卜左彎()
        判斷右卜右彎()
        判斷死路()
def PD控制(基礎速度: number, kp: number, kd: number):
    global 線位置, Error_P, Error_D, Error_P_old, PID_Val
    線位置 = BitRacer.read_line()
    Error_P = 0 - 線位置
    Error_D = Error_P - Error_P_old
    Error_P_old = Error_P
    PID_Val = Error_P * kp + Error_D * kd
    BitRacer.motor_run(BitRacer.Motors.M_R,
        Math.constrain(基礎速度 + PID_Val, -1000, 1000))
    BitRacer.motor_run(BitRacer.Motors.M_R,
        Math.constrain(基礎速度 - PID_Val, -1000, 1000))
def 迴轉終止():
    global 吸線狀態, 停止動作
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.ON)
    while 停止動作 == 0:
        if BitRacer.read_ir(BitRacer.IR_Sensors.IR3) < 2000 and BitRacer.read_ir(BitRacer.IR_Sensors.IR4) > 2000:
            吸線狀態 = 0
            吸線()
            停止動作 = 1
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.OFF)
def 吸線():
    global 轉彎時間, 吸線狀態
    while 吸線狀態 == 0:
        PD控制(0, 轉彎kp, 轉彎kd)
        if 線位置 <= 0.3 and 線位置 >= -0.3:
            轉彎時間 += 1
        else:
            轉彎時間 = 0
        if 轉彎時間 >= 轉彎延遲:
            BitRacer.motor_run(BitRacer.Motors.ALL, 0)
            吸線狀態 = 1
轉彎時間 = 0
PID_Val = 0
Error_P_old = 0
Error_D = 0
Error_P = 0
線位置 = 0
紅外線IR4 = 0
動作2 = ""
紅外線IR2 = 0
簡化indesx = 0
Path = ""
吸線狀態 = 0
停止動作 = 0
終點時間 = 0
紅外線IR3 = 0
路口判斷結束 = 0
路口 = ""
中間紅外線狀態 = 0
左轉紅外線狀態 = 0
右轉紅外線狀態 = 0
紅外線IR5 = 0
紅外線IR1 = 0
地圖資料 = ""
路口型態 = 0
找到終點 = 0
轉彎延遲 = 0
轉彎kd = 0
轉彎kp = 0
轉彎速度 = 500
轉彎kp = 250
轉彎kd = 210
轉彎延遲 = 3
找到終點 = 0
吸線幅度 = 0.3