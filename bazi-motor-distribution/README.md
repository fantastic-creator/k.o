# Bazi Motor Distribution Project

## Overview
The Bazi Motor Distribution project combines traditional Chinese astrology with modern technology to control stepper motors based on the Bazi (Four Pillars of Destiny) calculations. This project calculates the distribution of beads representing the Five Elements (Wood, Fire, Earth, Metal, Water) based on a given date and time, and then controls stepper motors to physically represent this distribution.

## Project Structure
```
bazi-motor-distribution
├── arduino
│   └── main.ino          # Arduino code for controlling stepper motors
├── src
│   └── bazi_distribution.py # Python script for Bazi calculation and bead distribution
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

### Arduino Setup
1. Open the `arduino/main.ino` file in the Arduino IDE.
2. Connect the Arduino board to your computer.
3. Upload the code to the Arduino board.
4. Ensure that the stepper motors are connected according to the wiring instructions provided in the code comments.

### Python Environment Setup
1. Ensure you have Python installed on your system.
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage Instructions
1. Run the Python script to calculate the Bazi and bead distribution:
   ```
   python src/bazi_distribution.py
   ```
2. Input the date and time in the format `YYYY.MM.DD.HH` when prompted.
3. The script will output the Bazi, the Five Elements scores, and the bead distribution.
4. The calculated bead distribution will correspond to the stepper motors, where each bead represents a 30-degree rotation of the motor.

## Bazi Calculation
The Bazi calculation is based on the lunar calendar and involves determining the Heavenly Stems and Earthly Branches from the input date and time. The scores for each of the Five Elements are calculated based on these pillars.

## Motor Control Logic
The Arduino code listens for serial commands to move the motors based on the calculated bead distribution. Each motor corresponds to one of the Five Elements, and the number of beads allocated to each element determines how far the motor will rotate.

## Example
For an input date of `2003.12.23.22`, the output might look like:
```
八字: 癸未 甲子 庚午 丁亥
天干: 癸甲庚丁
地支: 未子午亥

=== 五行分数 ===
土: 100分
木: 80分
水: 260分
火: 130分
金: 40分

=== 珠子分配 (共24颗) ===
土: 5颗
木: 5颗
水: 3颗
火: 5颗
金: 6颗
```
This output indicates how many beads to allocate to each motor, which will then rotate accordingly.

## Conclusion
This project serves as an innovative intersection of astrology and robotics, allowing for a tangible representation of Bazi calculations through motor movements.

---

# 八字五行珠子分配项目

## 项目简介
本项目结合了中国传统八字（四柱）命理与现代步进电机控制技术。通过输入出生年月日时，自动计算五行（木、火、土、金、水）分数与珠子分配，并通过步进电机物理展示五行珠子的分布。

## 项目结构
```
bazi-motor-distribution
├── arduino
│   └── main.ino          # Arduino 步进电机控制代码
├── src
│   └── bazi_distribution.py # 八字计算与珠子分配 Python 脚本
├── requirements.txt      # Python 依赖
└── README.md             # 项目文档
```

## 硬件与接线
- Arduino UNO + 2x CD4052BE + 5 个 28BYJ-48 步进电机
- 详细接线方式见 `arduino/main.ino` 文件顶部注释

## 安装与运行
### Arduino 部分
1. 用 Arduino IDE 打开 `arduino/main.ino`。
2. 连接开发板，上传代码。
3. 按注释完成电机与芯片接线。

### Python 部分
1. 确保已安装 Python。
2. （可选）创建虚拟环境：
   ```
   python -m venv venv
   source venv/bin/activate  # Windows 用 venv\Scripts\activate
   ```
3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方法
1. 运行 Python 脚本：(注意配置接口)
   ```
   python src/bazi_distribution.py
   ```
2. 按提示输入出生年月日时（格式：YYYY.MM.DD.HH）。
3. 程序会输出八字、五行分数和珠子分配。
4. 珠子分配结果会通过串口发送给 Arduino，电机自动旋转对应角度（每颗珠子 30 度）。

## 八字与五行计算说明
- 基于农历推算天干地支，计算五行分数。
- 珠子总数为 24，按五行分数比例分配。

## 步进电机控制说明
- Arduino 通过串口接收命令，控制 5 路步进电机。
- 每个电机代表一种五行，珠子数决定电机旋转角度。
- 电机一次只转动一个，顺序执行。

## 示例
输入 `2003.12.23.22`，输出：
```
八字: 癸未 甲子 庚午 丁亥
天干: 癸甲庚丁
地支: 未子午亥

=== 五行分数 ===
土: 100分
木: 80分
水: 260分
火: 130分
金: 40分

=== 珠子分配 (共24颗) ===
土: 5颗
木: 5颗
水: 3颗
火: 5颗
金: 6颗
```

## 结语
本项目是传统命理与现代自动化的创新结合，实现了八字五行的可视化与物理交互。