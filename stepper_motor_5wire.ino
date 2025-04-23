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

void loop() {
  // 正转500步
  for(int i = 0; i < 500; i++) {
    motorCW();
  }
  motorStop();
  delay(500);
  
  // 反转500步
  for(int i = 0; i < 500; i++) {
    motorCCW();
  }
  motorStop();
  delay(500);
}