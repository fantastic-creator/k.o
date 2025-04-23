/*******************************************************
5线步进电机Arduino控制程序 (28BYJ-48)
Platform: Arduino UNO + ULN2003步进电机驱动套件

接线方式:
红线(Red)   ---- +5V
橙线(Orange) ---- D2 (Arduino数字引脚2)
黄线(Yellow) ---- D3 (Arduino数字引脚3)
粉线(Pink)   ---- D4 (Arduino数字引脚4)
蓝线(Blue)   ---- D5 (Arduino数字引脚5)
注意：红线接5V电源，其他四线按顺序接Arduino引脚

电机参数：
步距角: 5.625度/64
减速比: 1:64
额定电压: 5V
*********************/

// 定义步进电机控制引脚
const int motorPin1 = 2;    // Orange
const int motorPin2 = 3;    // Yellow
const int motorPin3 = 4;    // Pink
const int motorPin4 = 5;    // Blue

// 电机参数计算
const float STEP_ANGLE = 5.625;    // 步进角度
const int REDUCTION_RATIO = 64;     // 减速比
const int STEPS_PER_REVOLUTION = 4096;  // 一圈总步数 (360/5.625*64*8)
const float ANGLE_PER_STEP = 360.0 / STEPS_PER_REVOLUTION;  // 每步的角度

// 角度校准系数（基于实际测量，输入角度被放大了约8倍）
const float CALIBRATION_FACTOR = 0.125;  // 1/8，用于补偿角度放大
const bool DEBUG_MODE = true;     // 调试模式开关

String inputString = "";         // 用于存储输入的字符串
bool stringComplete = false;     // 字符串是否完整标志

// 8步模式的相序表
const byte phaseSequence[8] = {
  0b1000,
  0b1100,
  0b0100,
  0b0110,
  0b0010,
  0b0011,
  0b0001,
  0b1001
};

void setup() {
  // 设置电机控制引脚为输出模式
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  
  // 初始状态，所有引脚置低
  motorStop();
  
  // 初始化串口通信，波特率9600
  Serial.begin(9600);
  inputString.reserve(200);
  
  delay(50);  // 等待系统稳定
}

// 正转函数 - 8步模式，提供更平滑的运动
void motorCW() {
  for(int i = 0; i < 8; i++) {
    setMotorPhase(phaseSequence[i]);
    delay(2);  // 转速调节
  }
}

// 反转函数 - 8步模式
void motorCCW() {
  for(int i = 7; i >= 0; i--) {
    setMotorPhase(phaseSequence[i]);
    delay(2);  // 转速调节
  }
}

// 停止函数
void motorStop() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
}

// 设置电机相位
void setMotorPhase(byte phase) {
  digitalWrite(motorPin1, (phase & 0b1000) ? HIGH : LOW);
  digitalWrite(motorPin2, (phase & 0b0100) ? HIGH : LOW);
  digitalWrite(motorPin3, (phase & 0b0010) ? HIGH : LOW);
  digitalWrite(motorPin4, (phase & 0b0001) ? HIGH : LOW);
}

// 角度校准函数
float calibrateAngle(float requestedAngle) {
    return requestedAngle * CALIBRATION_FACTOR;
}

// 角度转换为步数，加入校准
int angleToSteps(float angle) {
    float calibratedAngle = calibrateAngle(angle);
    return (int)(calibratedAngle / ANGLE_PER_STEP);
}

// 移动指定角度
void moveToAngle(float angle) {
    if(DEBUG_MODE) {
        Serial.print("输入角度: ");
        Serial.println(angle);
        Serial.print("校准后角度: ");
        Serial.println(calibrateAngle(angle));
    }
    
    int steps = angleToSteps(angle);
    if (steps > 0) {
        for(int i = 0; i < abs(steps); i++) {
            motorCW();
        }
    } else {
        for(int i = 0; i < abs(steps); i++) {
            motorCCW();
        }
    }
    motorStop();
    
    if(DEBUG_MODE) {
        Serial.print("步数: ");
        Serial.println(abs(steps));
    }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void loop() {
    if (stringComplete) {
        float angle = inputString.toFloat();
        
        // 检查角度是否有效
        if (angle != 0 || inputString.indexOf("0") != -1) {
            if(!DEBUG_MODE) {
                Serial.print("执行角度: ");
                Serial.println(angle);
            }
            
            moveToAngle(angle);
            Serial.println("转动完成");
        } else {
            Serial.println("无效的角度输入");
        }
        
        // 清空输入字符串，准备接收新的数据
        inputString = "";
        stringComplete = false;
    }
}