/*******************************************************
 5线步进电机Arduino控制程序 (28BYJ-48) - 5路控制版
 Platform: Arduino UNO + 2x CD4052BE

 接线方式 (基于提供的 CD4052BE 数据手册):
 电机1 (直连):
   Orange -> D2, Yellow -> D3, Pink -> D4, Blue -> D5, Red -> +5V (独立电源)
 电机2~5 (通过 2x CD4052BE):
   信号源 (Arduino -> CD4052BE 公共输入):
     D6 -> Chip#1 ZA (Pin 13)
     D7 -> Chip#1 ZB (Pin 3)
     D8 -> Chip#2 ZA (Pin 13)
     D9 -> Chip#2 ZB (Pin 3)
   控制线 (Arduino -> CD4052BE 控制/电源):
     D10 -> Chip#1 A0 (Pin 10) & Chip#2 A0 (Pin 10) [并联]
     D11 -> Chip#1 A1 (Pin 9)  & Chip#2 A1 (Pin 9)  [并联]
     D12 -> Chip#1 E_bar(Pin 6) & Chip#2 E_bar(Pin 6) [并联]
     5V  -> Chip#1 VDD (Pin 16)& Chip#2 VDD (Pin 16) [并联]
     GND -> Chip#1 VSS (Pin 8) & Chip#2 VSS (Pin 8) [共地]
     GND -> Chip#1 VEE (Pin 7) & Chip#2 VEE (Pin 7) [共地]
   信号输出 (CD4052BE -> 电机信号线):
     Chip#1 Y0A(12)/Y0B(1) -> Motor2 Orange/Yellow (A1=0,A0=0)
     Chip#2 Y0A(12)/Y0B(1) -> Motor2 Pink/Blue     (A1=0,A0=0)
     Chip#1 Y1A(14)/Y1B(5) -> Motor3 Orange/Yellow (A1=0,A0=1)
     Chip#2 Y1A(14)/Y1B(5) -> Motor3 Pink/Blue     (A1=0,A0=1)
     Chip#1 Y2A(15)/Y2B(2) -> Motor4 Orange/Yellow (A1=1,A0=0)
     Chip#2 Y2A(15)/Y2B(2) -> Motor4 Pink/Blue     (A1=1,A0=0)
     Chip#1 Y3A(11)/Y3B(4) -> Motor5 Orange/Yellow (A1=1,A0=1)
     Chip#2 Y3A(11)/Y3B(4) -> Motor5 Pink/Blue     (A1=1,A0=1)
   电机电源:
     所有电机 Red -> +5V (独立电源)
   共地:
     Arduino GND, Chip#1 GND, Chip#2 GND, 独立电源 GND -> 必须全部连接

 串口命令格式: M<电机号>:<角度>\n (例如: M1:90, M3:-45)
 *******************************************************/

// --- 引脚定义 ---
// 电机1 (直连)
const int motor1_Pin1 = 2; // Orange
const int motor1_Pin2 = 3; // Yellow
const int motor1_Pin3 = 4; // Pink
const int motor1_Pin4 = 5; // Blue
const int motor1_Pins[4] = {motor1_Pin1, motor1_Pin2, motor1_Pin3, motor1_Pin4};

// 电机2-5 (多路复用信号源)
const int mux_SignalPin1 = 6; // To Chip#1 ZA
const int mux_SignalPin2 = 7; // To Chip#1 ZB
const int mux_SignalPin3 = 8; // To Chip#2 ZA
const int mux_SignalPin4 = 9; // To Chip#2 ZB
const int mux_SignalPins[4] = {mux_SignalPin1, mux_SignalPin2, mux_SignalPin3, mux_SignalPin4};

// CD4052BE 控制引脚
const int mux_A0_Pin = 10; // Select Bit 0 (To Both Chips Pin 10)
const int mux_A1_Pin = 11; // Select Bit 1 (To Both Chips Pin 9)
const int mux_Enable_Pin = 12; // Enable, Active Low (To Both Chips Pin 6)

// --- 电机参数 ---
const float STEP_ANGLE = 5.625;    // 步进电机物理步距角
const int REDUCTION_RATIO = 64;     // 减速比
// 注意: 28BYJ-48 通常是 4 步或 8 步模式完成一个电周期，不是直接用物理步距角算
// 8 步模式下，一个完整旋转需要的步数约为 (360 / (STEP_ANGLE / 8)) * REDUCTION_RATIO = 4096
const int STEPS_PER_REVOLUTION = 4096; // 8步模式下，电机轴旋转一圈的总步数
const float ANGLE_PER_STEP = 360.0 / STEPS_PER_REVOLUTION; // 每一步对应的输出轴角度

// --- 校准与调试 ---
const float CALIBRATION_FACTOR = 1.0; // 角度校准系数 (根据实际情况调整, 1.0为不校准)
const bool DEBUG_MODE = true;      // 调试模式开关

// --- 全局变量 ---
String inputString = "";         // 存储串口输入的字符串
bool stringComplete = false;     // 串口字符串接收完成标志

// 8步模式相序表 (对应信号线 1, 2, 3, 4)
const byte phaseSequence[8] = {
  0b1000, // Step 1
  0b1100, // Step 2
  0b0100, // Step 3
  0b0110, // Step 4
  0b0010, // Step 5
  0b0011, // Step 6
  0b0001, // Step 7
  0b1001  // Step 8
};

// --- 初始化 ---
void setup() {
  // 设置电机1引脚为输出
  for (int i = 0; i < 4; i++) {
    pinMode(motor1_Pins[i], OUTPUT);
  }
  // 设置多路复用信号源引脚为输出
  for (int i = 0; i < 4; i++) {
    pinMode(mux_SignalPins[i], OUTPUT);
  }
  // 设置CD4052BE控制引脚为输出
  pinMode(mux_A0_Pin, OUTPUT);
  pinMode(mux_A1_Pin, OUTPUT);
  pinMode(mux_Enable_Pin, OUTPUT);

  // 初始状态：禁用多路复用器，停止所有电机信号
  disableMux();
  motorStop(1); // 停止电机1
  setMuxMotorPhase(0); // 停止电机2-5的信号

  // 初始化串口通信
  Serial.begin(9600);
  inputString.reserve(200); // 预分配字符串内存

  if (DEBUG_MODE) {
    Serial.println("系统初始化完成，等待命令...");
  }
  delay(50); // 短暂延时等待稳定
}

// --- 主循环 ---
void loop() {
  // 处理串口接收到的完整命令
  if (stringComplete) {
    parseAndMoveMotor(inputString);
    // 清理，准备下一次接收
    inputString = "";
    stringComplete = false;
  }
}

// --- 串口事件处理 ---
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar; // 追加字符
    // 如果接收到换行符，标记字符串接收完成
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// --- 命令解析与执行 ---
void parseAndMoveMotor(String cmd) {
  cmd.trim(); // 去除首尾空白
  if (DEBUG_MODE) {
    Serial.print("收到命令: ");
    Serial.println(cmd);
  }

  // 检查命令格式是否为 M<num>:<angle>
  if (!cmd.startsWith("M")) {
    Serial.println("错误: 命令必须以 'M' 开头");
    return;
  }
  int colonPos = cmd.indexOf(':');
  if (colonPos <= 1) {
    Serial.println("错误: 命令格式错误 (应为 M<num>:<angle>)");
    return;
  }

  // 解析电机编号和角度
  int motorIdx = cmd.substring(1, colonPos).toInt();
  float angle = cmd.substring(colonPos + 1).toFloat();

  // 检查电机编号是否有效
  if (motorIdx < 1 || motorIdx > 5) {
    Serial.print("错误: 无效的电机编号 (应为 1-5): ");
    Serial.println(motorIdx);
    return;
  }

  // 执行移动
  moveToAngle(motorIdx, angle);
}

// --- CD4052BE 控制 ---
// 根据电机编号 (2-5) 选择对应的通道 (0-3) 并使能芯片
void setMuxChannel(int motorIdx_2_to_5) {
  if (motorIdx_2_to_5 < 2 || motorIdx_2_to_5 > 5) return; // 安全检查
  int channelIdx = motorIdx_2_to_5 - 2; // 转换为 0-3

  // 设置选择位 A0 和 A1
  digitalWrite(mux_A0_Pin, (channelIdx & 0b01) ? HIGH : LOW); // A0 = channelIdx bit 0
  digitalWrite(mux_A1_Pin, (channelIdx & 0b10) ? HIGH : LOW); // A1 = channelIdx bit 1

  // 使能芯片 (低电平有效)
  digitalWrite(mux_Enable_Pin, LOW);
  delayMicroseconds(10); // 短暂延时确保芯片状态切换
  if (DEBUG_MODE) {
    Serial.print("选择通道: "); Serial.print(channelIdx);
    Serial.print(" (A1="); Serial.print(digitalRead(mux_A1_Pin));
    Serial.print(", A0="); Serial.print(digitalRead(mux_A0_Pin));
    Serial.println("), 使能芯片");
  }
}

// 禁用 CD4052BE 芯片
void disableMux() {
  digitalWrite(mux_Enable_Pin, HIGH); // 高电平禁用
  if (DEBUG_MODE) {
    // Serial.println("禁用芯片"); // 避免过多打印
  }
}

// --- 步进电机控制 ---
// 设置多路复用电机的相位 (通过 D6-D9 输出)
void setMuxMotorPhase(byte phase) {
  digitalWrite(mux_SignalPin1, (phase & 0b1000) ? HIGH : LOW); // 信号1
  digitalWrite(mux_SignalPin2, (phase & 0b0100) ? HIGH : LOW); // 信号2
  digitalWrite(mux_SignalPin3, (phase & 0b0010) ? HIGH : LOW); // 信号3
  digitalWrite(mux_SignalPin4, (phase & 0b0001) ? HIGH : LOW); // 信号4
}

// 设置直连电机 (电机1) 的相位 (通过 D2-D5 输出)
void setDirectMotorPhase(byte phase) {
  digitalWrite(motor1_Pin1, (phase & 0b1000) ? HIGH : LOW); // 信号1
  digitalWrite(motor1_Pin2, (phase & 0b0100) ? HIGH : LOW); // 信号2
  digitalWrite(motor1_Pin3, (phase & 0b0010) ? HIGH : LOW); // 信号3
  digitalWrite(motor1_Pin4, (phase & 0b0001) ? HIGH : LOW); // 信号4
}

// 停止指定电机的信号输出
void motorStop(int motorIdx) {
  if (motorIdx == 1) {
    setDirectMotorPhase(0); // 关闭电机1所有相位
  } else if (motorIdx >= 2 && motorIdx <= 5) {
    // 对于多路复用电机，停止是通过 setMuxMotorPhase(0) 和 disableMux() 实现
    // 这里可以额外确保信号线为低，但主要靠 disableMux
    setMuxMotorPhase(0);
    disableMux();
  }
}

// --- 角度与步数转换 ---
// 校准角度
float calibrateAngle(float requestedAngle) {
  return requestedAngle * CALIBRATION_FACTOR;
}

// 将角度转换为需要的 8 步模式步数
int angleToSteps(float angle) {
  float calibratedAngle = calibrateAngle(angle);
  // 计算需要的总步数 (四舍五入)
  int steps = round(calibratedAngle / ANGLE_PER_STEP);
  if (DEBUG_MODE) {
    Serial.print("请求角度: "); Serial.print(angle);
    Serial.print(", 校准后角度: "); Serial.print(calibratedAngle);
    Serial.print(", 计算步数: "); Serial.println(steps);
  }
  return steps;
}

// --- 核心移动函数 ---
void moveToAngle(int motorIdx, float angle) {
  if (DEBUG_MODE) {
    Serial.print("开始移动 电机#"); Serial.print(motorIdx);
    Serial.print(" 到角度: "); Serial.println(angle);
  }

  int totalSteps = angleToSteps(angle); // 获取需要移动的总步数 (8步模式)
  if (totalSteps == 0) {
    Serial.println("步数为 0，无需移动。");
    return;
  }

  bool clockwise = (totalSteps > 0); // 判断旋转方向
  int stepsToTake = abs(totalSteps); // 获取要移动的绝对步数

  // --- 根据电机编号选择控制方式 ---
  if (motorIdx == 1) {
    // --- 控制直连电机 (电机1) ---
    for (int i = 0; i < stepsToTake; i++) {
      // 计算当前步对应的相位索引
      int phaseIndex = clockwise ? (i % 8) : (7 - (i % 8));
      setDirectMotorPhase(phaseSequence[phaseIndex]);
      delay(2); // 控制转动速度，值越小速度越快 (最小约 1-2ms)
    }
    motorStop(1); // 移动完成后停止电机1

  } else if (motorIdx >= 2 && motorIdx <= 5) {
    // --- 控制多路复用电机 (电机2-5) ---
    setMuxChannel(motorIdx); // 选择并使能对应的通道

    for (int i = 0; i < stepsToTake; i++) {
      // 计算当前步对应的相位索引
      int phaseIndex = clockwise ? (i % 8) : (7 - (i % 8));
      setMuxMotorPhase(phaseSequence[phaseIndex]);
      delay(2); // 控制转动速度
    }
    motorStop(motorIdx); // 移动完成后停止多路复用信号并禁用芯片

  } else {
    // 理论上不会执行到这里，因为前面有检查
    Serial.println("错误: moveToAngle 内部电机编号无效");
    return;
  }

  if (DEBUG_MODE) {
    Serial.print("电机#"); Serial.print(motorIdx);
    Serial.println(" 转动完成");
  }
}