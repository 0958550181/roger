function 左轉優先 () {
    執行動作("直走")
    if (路口型態 == 9) {
        執行動作("停止")
        地圖資料 = "" + 地圖資料 + "E"
        找到終點 += 1
    } else if (路口型態 % 2 == 1) {
        地圖資料 = "" + 地圖資料 + "L"
        執行動作("左轉")
    } else if (路口型態 == 6) {
        地圖資料 = "" + 地圖資料 + "S"
    } else if (路口型態 == 0) {
        地圖資料 = "" + 地圖資料 + "B"
        執行動作("迴轉")
    } else if (路口型態 == 4) {
        地圖資料 = "" + 地圖資料 + "R"
        執行動作("右轉")
    }
}
function 判斷十字T字路口 () {
    if (紅外線IR1 < 1000 && (紅外線IR5 < 1000 && 右轉紅外線狀態 + 左轉紅外線狀態 == 2)) {
        if (中間紅外線狀態 == 1) {
            路口 = "十字"
            路口型態 = 7
            路口判斷結束 = 1
        } else {
            路口 = "T字"
            路口型態 = 5
            路口判斷結束 = 1
        }
    }
}
function 迴轉終止 () {
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.on)
    while (停止動作 == 0) {
        if (BitRacer.readIR(BitRacer.IR_Sensors.IR3) < 2000 && BitRacer.readIR(BitRacer.IR_Sensors.IR4) > 2000) {
            吸線狀態 = 0
            吸線()
            停止動作 = 1
        }
    }
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.off)
}
function 判斷終點 () {
    if (紅外線IR1 > 3000 && (紅外線IR3 == 3000 && 紅外線IR5 < 3000)) {
        終點時間 = 1
        if (終點時間 >= 40) {
            終點時間 = 0
            路口 = "終點"
            路口型態 = 9
            路口判斷結束 = 1
        }
    } else {
        終點時間 = 0
    }
}
function 設定旋轉速度 (右輪速: number, 左輪速: number) {
    BitRacer.motorRun(BitRacer.Motors.M_R, 右輪速)
    BitRacer.motorRun(BitRacer.Motors.M_R, 左輪速)
}
function 碰到路口 () {
    while (停止動作 == 0) {
        PD控制(200, 250, 210)
        讀取紅外線()
        if (紅外線IR1 >= 1500 || (紅外線IR5 >= 1500 || 紅外線IR3 <= 1500)) {
            BitRacer.motorRun(BitRacer.Motors.All, 150)
            路口判斷()
            停止動作 = 1
        }
    }
}
function 記憶碰到路口 () {
    while (停止動作 == 0) {
        PD控制(200, 250, 210)
        讀取紅外線()
        if (紅外線IR1 >= 1500 || (紅外線IR5 >= 1500 || 紅外線IR3 <= 1500)) {
            BitRacer.motorRun(BitRacer.Motors.All, 150)
            路口判斷()
            停止動作 = 1
        }
    }
}
function 判斷左卜左彎 () {
    if (紅外線IR1 < 1000 && (右轉紅外線狀態 == 0 && 左轉紅外線狀態 == 1)) {
        if (中間紅外線狀態 == 1) {
            路口 = "左卜"
            路口型態 = 3
            路口判斷結束 = 1
        } else {
            路口 = "左彎"
            路口型態 = 1
            路口判斷結束 = 1
        }
    }
}
function 左轉終止 () {
    BitRacer.LED(BitRacer.LEDs.LED_L, BitRacer.LEDswitch.on)
    while (停止動作 == 0) {
        if (BitRacer.readIR(BitRacer.IR_Sensors.IR3) < 2000 && BitRacer.readIR(BitRacer.IR_Sensors.IR2) > 2000) {
            吸線狀態 = 0
            吸線()
            停止動作 = 1
        }
    }
    BitRacer.LED(BitRacer.LEDs.LED_L, BitRacer.LEDswitch.off)
}
input.onButtonPressed(Button.A, function () {
    music.playTone(988, music.beat(BeatFraction.Whole))
    basic.pause(1000)
    地圖資料 = ""
    while (找到終點 == 0) {
        左轉優先()
    }
    簡化路徑()
    music.playTone(988, music.beat(BeatFraction.Whole))
    basic.showIcon(IconNames.Square)
    basic.pause(1000)
    basic.clearScreen()
})
function 簡化路徑 () {
    while (地圖資料.includes("B")) {
        music.playTone(988, music.beat(BeatFraction.Half))
        serial.writeLine(地圖資料)
        地圖資料 = 替換地圖資料(地圖資料, "LBL", "S")
        地圖資料 = 替換地圖資料(地圖資料, "LBS", "R")
        地圖資料 = 替換地圖資料(地圖資料, "SBL", "R")
        地圖資料 = 替換地圖資料(地圖資料, "LBR", "B")
        地圖資料 = 替換地圖資料(地圖資料, "RBL", "B")
        地圖資料 = 替換地圖資料(地圖資料, "SBS", "B")
    }
}
function 右轉終止 () {
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.on)
    while (停止動作 == 0) {
        if (BitRacer.readIR(BitRacer.IR_Sensors.IR3) < 2000 && BitRacer.readIR(BitRacer.IR_Sensors.IR4) > 2000) {
            吸線狀態 = 0
            吸線()
            停止動作 = 1
        }
    }
    BitRacer.LED(BitRacer.LEDs.LED_R, BitRacer.LEDswitch.off)
}
function 替換地圖資料 (地圖: string, 簡化路口: string, 替換資料: string) {
    Path = 地圖
    while (Path.includes(簡化路口)) {
        簡化indesx = Path.indexOf(簡化路口)
        Path = "" + Path.substr(0, 簡化indesx) + 替換資料 + Path.substr(簡化indesx + 簡化路口.length, Path.length - (簡化indesx + 簡化路口.length))
    }
    serial.writeLine(Path)
    basic.pause(10)
    return Path
}
function 判斷死路 () {
    if (紅外線IR2 < 1000 && (紅外線IR3 < 1000 && 右轉紅外線狀態 + 左轉紅外線狀態 == 0)) {
        路口 = "死路"
        路口型態 = 0
        路口判斷結束 = 1
    }
}
input.onButtonPressed(Button.AB, function () {
    BitRacer.CalibrateBegin()
    music.playTone(988, music.beat(BeatFraction.Whole))
    BitRacer.motorRun(BitRacer.Motors.All, 300)
    basic.pause(1000)
    BitRacer.motorRun(BitRacer.Motors.All, 0)
    music.playTone(988, music.beat(BeatFraction.Half))
    music.rest(music.beat(BeatFraction.Whole))
    music.playTone(988, music.beat(BeatFraction.Half))
    BitRacer.CalibrateEnd(BitRacer.LineColor.White)
})
function 執行動作 (動作: string) {
    停止動作 = 0
    if (動作 == "右轉") {
        設定旋轉速度(1, 1)
        右轉終止()
    } else if (動作 == "左轉") {
        設定旋轉速度(1, 1)
        左轉終止()
    } else if (動作 == "迴轉") {
        設定旋轉速度(1, 1)
        迴轉終止()
    } else if (動作 == "直走") {
        碰到路口()
    } else if (動作 == "直走加速") {
        記憶碰到路口()
    } else if (動作 == "停止") {
        BitRacer.motorRun(BitRacer.Motors.All, 0)
        music.playTone(988, music.beat(BeatFraction.Whole))
    }
}
input.onButtonPressed(Button.B, function () {
    music.playTone(988, music.beat(BeatFraction.Whole))
    basic.pause(1000)
    while (index <= 地圖資料.length - 1) {
        執行動作("直走加速")
        動作2 = 地圖資料.charAt(index)
        if (動作2 == "R") {
            執行動作("右轉")
        } else if (動作2 == "L") {
            執行動作("左轉")
        } else if (動作2 == "E") {
            執行動作("停止")
        }
        index += 1
    }
})
function 讀取紅外線 () {
    紅外線IR1 = BitRacer.readIR(BitRacer.IR_Sensors.IR1)
    紅外線IR2 = BitRacer.readIR(BitRacer.IR_Sensors.IR2)
    if (紅外線IR1 > 3000) {
        左轉紅外線狀態 = 1
    }
    紅外線IR3 = BitRacer.readIR(BitRacer.IR_Sensors.IR3)
    if (紅外線IR3 > 3000) {
        中間紅外線狀態 = 1
    } else {
        中間紅外線狀態 = 0
    }
    紅外線IR4 = BitRacer.readIR(BitRacer.IR_Sensors.IR4)
    紅外線IR5 = BitRacer.readIR(BitRacer.IR_Sensors.IR5)
    if (紅外線IR5 > 3000) {
        右轉紅外線狀態 = 1
    }
}
function 判斷右卜右彎 () {
    if (紅外線IR5 < 1000 && (右轉紅外線狀態 == 1 && 左轉紅外線狀態 == 0)) {
        if (中間紅外線狀態 == 1) {
            路口 = "右卜"
            路口型態 = 6
            路口判斷結束 = 1
        } else {
            路口 = "右彎"
            路口型態 = 4
            路口判斷結束 = 1
        }
    }
}
function 路口判斷 () {
    右轉紅外線狀態 = 0
    左轉紅外線狀態 = 0
    路口判斷結束 = 0
    while (路口判斷結束 == 0) {
        讀取紅外線()
        判斷終點()
        判斷十字T字路口()
        判斷左卜左彎()
        判斷右卜右彎()
        判斷死路()
    }
}
function PD控制 (基礎速度: number, kp: number, kd: number) {
    線位置 = BitRacer.readLine()
    Error_P = 0 - 線位置
    Error_D = Error_P - Error_P_old
    Error_P_old = Error_P
    PID_Val = Error_P * kp + Error_D * kd
    BitRacer.motorRun(BitRacer.Motors.M_R, Math.constrain(基礎速度 + PID_Val, -1000, 1000))
    BitRacer.motorRun(BitRacer.Motors.M_R, Math.constrain(基礎速度 - PID_Val, -1000, 1000))
}
function 吸線 () {
    while (吸線狀態 == 0) {
        PD控制(0, 轉彎kp, 轉彎kd)
        if (線位置 <= 0.3 && 線位置 >= -0.3) {
            轉彎時間 += 1
        } else {
            轉彎時間 = 0
        }
        if (轉彎時間 >= 轉彎延遲) {
            BitRacer.motorRun(BitRacer.Motors.All, 0)
            吸線狀態 = 1
        }
    }
}
let 轉彎時間 = 0
let PID_Val = 0
let Error_P_old = 0
let Error_D = 0
let Error_P = 0
let 線位置 = 0
let 紅外線IR4 = 0
let 動作2 = ""
let index = 0
let 紅外線IR2 = 0
let 簡化indesx = 0
let Path = ""
let 終點時間 = 0
let 紅外線IR3 = 0
let 吸線狀態 = 0
let 停止動作 = 0
let 路口判斷結束 = 0
let 路口 = ""
let 中間紅外線狀態 = 0
let 左轉紅外線狀態 = 0
let 右轉紅外線狀態 = 0
let 紅外線IR5 = 0
let 紅外線IR1 = 0
let 地圖資料 = ""
let 路口型態 = 0
let 找到終點 = 0
let 轉彎延遲 = 0
let 轉彎kd = 0
let 轉彎kp = 0
let 轉彎速度 = 500
轉彎kp = 250
轉彎kd = 210
轉彎延遲 = 3
找到終點 = 0
let 吸線幅度 = 0.3
