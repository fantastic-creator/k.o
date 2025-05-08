| 源设备        | 源引脚     | 目标设备        | 目标引脚号/符号 | 信号/功能             | 备注                                       |
| :-------------- | :--------- | :-------------- | :-------------- | :-------------------- | :----------------------------------------- |
| **Arduino UNO** |            |                 |                 |                       |                                            |
|                 | D2         | **ULN2003 #1**  | **IN1**         | Step Signal 1 Input   | **驱动 Motor 1**                           |
|                 | D3         | **ULN2003 #1**  | **IN2**         | Step Signal 2 Input   | **驱动 Motor 1**                           |
|                 | D4         | **ULN2003 #1**  | **IN3**         | Step Signal 3 Input   | **驱动 Motor 1**                           |
|                 | D5         | **ULN2003 #1**  | **IN4**         | Step Signal 4 Input   | **驱动 Motor 1**                           |
|                 | **D6**     | **CD4052BE #1** | **13 (ZA)**     | **Step Signal 1 (Mux)** | 公共输入 A (芯片 #1)                       |
|                 | **D7**     | **CD4052BE #1** | **3 (ZB)**      | **Step Signal 2 (Mux)** | 公共输入 B (芯片 #1)                       |
|                 | **D8**     | **CD4052BE #2** | **13 (ZA)**     | **Step Signal 3 (Mux)** | 公共输入 A (芯片 #2)                       |
|                 | **D9**     | **CD4052BE #2** | **3 (ZB)**      | **Step Signal 4 (Mux)** | 公共输入 B (芯片 #2)                       |
|                 | D10        | CD4052BE #1     | 10 (A0)         | Select Bit 0          | **并联**到芯片 #2 的 Pin 10                |
|                 | D10        | CD4052BE #2     | 10 (A0)         | Select Bit 0          | **并联**到芯片 #1 的 Pin 10                |
|                 | D11        | CD4052BE #1     | 9 (A1)          | Select Bit 1          | **并联**到芯片 #2 的 Pin 9                 |
|                 | D11        | CD4052BE #2     | 9 (A1)          | Select Bit 1          | **并联**到芯片 #1 的 Pin 9                 |
|                 | D12        | CD4052BE #1     | 6 (E_bar)       | Enable (Active Low)   | **并联**到芯片 #2 的 Pin 6                 |
|                 | D12        | CD4052BE #2     | 6 (E_bar)       | Enable (Active Low)   | **并联**到芯片 #1 的 Pin 6                 |
|                 | 5V (来自UNO) | CD4052BE #1     | 16 (VDD)        | +5V Logic Power       | **并联**到芯片 #2 的 Pin 16                |
|                 | 5V (来自UNO) | CD4052BE #2     | 16 (VDD)        | +5V Logic Power       | **并联**到芯片 #1 的 Pin 16                |
|                 | GND        | CD4052BE #1     | 8 (VSS)         | Ground                | **共地**                                   |
|                 | GND        | CD4052BE #1     | 7 (VEE)         | Ground                | **共地**                                   |
|                 | GND        | CD4052BE #2     | 8 (VSS)         | Ground                | **共地**                                   |
|                 | GND        | CD4052BE #2     | 7 (VEE)         | Ground                | **共地**                                   |
| **CD4052BE #1** |            |                 |                 |                       | **(切换信号 1 和 2)**                      |
|                 | 12 (Y0A)   | **ULN2003 #2**  | **IN1**         | Step Signal 1 Input   | A1=0, A0=0 选择 Motor 2                    |
|                 | 1 (Y0B)    | **ULN2003 #2**  | **IN2**         | Step Signal 2 Input   | A1=0, A0=0 选择 Motor 2                    |
|                 | 14 (Y1A)   | **ULN2003 #3**  | **IN1**         | Step Signal 1 Input   | A1=0, A0=1 选择 Motor 3                    |
|                 | 5 (Y1B)    | **ULN2003 #3**  | **IN2**         | Step Signal 2 Input   | A1=0, A0=1 选择 Motor 3                    |
|                 | 15 (Y2A)   | **ULN2003 #4**  | **IN1**         | Step Signal 1 Input   | A1=1, A0=0 选择 Motor 4                    |
|                 | 2 (Y2B)    | **ULN2003 #4**  | **IN2**         | Step Signal 2 Input   | A1=1, A0=0 选择 Motor 4                    |
|                 | 11 (Y3A)   | **ULN2003 #5**  | **IN1**         | Step Signal 1 Input   | A1=1, A0=1 选择 Motor 5                    |
|                 | 4 (Y3B)    | **ULN2003 #5**  | **IN2**         | Step Signal 2 Input   | A1=1, A0=1 选择 Motor 5                    |
| **CD4052BE #2** |            |                 |                 |                       | **(切换信号 3 和 4)**                      |
|                 | 12 (Y0A)   | **ULN2003 #2**  | **IN3**         | Step Signal 3 Input   | A1=0, A0=0 选择 Motor 2                    |
|                 | 1 (Y0B)    | **ULN2003 #2**  | **IN4**         | Step Signal 4 Input   | A1=0, A0=0 选择 Motor 2                    |
|                 | 14 (Y1A)   | **ULN2003 #3**  | **IN3**         | Step Signal 3 Input   | A1=0, A0=1 选择 Motor 3                    |
|                 | 5 (Y1B)    | **ULN2003 #3**  | **IN4**         | Step Signal 4 Input   | A1=0, A0=1 选择 Motor 3                    |
|                 | 15 (Y2A)   | **ULN2003 #4**  | **IN3**         | Step Signal 3 Input   | A1=1, A0=0 选择 Motor 4                    |
|                 | 2 (Y2B)    | **ULN2003 #4**  | **IN4**         | Step Signal 4 Input   | A1=1, A0=0 选择 Motor 4                    |
|                 | 11 (Y3A)   | **ULN2003 #5**  | **IN3**         | Step Signal 3 Input   | A1=1, A0=1 选择 Motor 5                    |
|                 | 4 (Y3B)    | **ULN2003 #5**  | **IN4**         | Step Signal 4 Input   | A1=1, A0=1 选择 Motor 5                    |
| **ULN2003 #1**  |            |                 |                 |                       | **(驱动 Motor 1, 使用标准ULN2003模块，连接IN1-IN4)** |
|                 | OUT1       | Motor 1         | (橙色线)        | Step Signal 1 Output  |                                            |
|                 | OUT2       | Motor 1         | (黄色线)        | Step Signal 2 Output  |                                            |
|                 | OUT3       | Motor 1         | (粉色线)        | Step Signal 3 Output  |                                            |
|                 | OUT4       | Motor 1         | (蓝色线)        | Step Signal 4 Output  |                                            |
|                 | + (5-12V)  | 独立 5V 电源    | +5V             | Power Input           |                                            |
|                 | - (GND)    | 独立 5V 电源    | GND             | Ground                | **共地**                                   |
| **ULN2003 #2**  |            |                 |                 |                       | **(驱动 Motor 2, 使用标准ULN2003模块，连接IN1-IN4)** |
|                 | OUT1       | Motor 2         | (橙色线)        | Step Signal 1 Output  |                                            |
|                 | OUT2       | Motor 2         | (黄色线)        | Step Signal 2 Output  |                                            |
|                 | OUT3       | Motor 2         | (粉色线)        | Step Signal 3 Output  |                                            |
|                 | OUT4       | Motor 2         | (蓝色线)        | Step Signal 4 Output  |                                            |
|                 | + (5-12V)  | 独立 5V 电源    | +5V             | Power Input           |                                            |
|                 | - (GND)    | 独立 5V 电源    | GND             | Ground                | **共地**                                   |
| **ULN2003 #3**  |            |                 |                 |                       | **(驱动 Motor 3, 使用标准ULN2003模块，连接IN1-IN4)** |
|                 | OUT1       | Motor 3         | (橙色线)        | Step Signal 1 Output  |                                            |
|                 | OUT2       | Motor 3         | (黄色线)        | Step Signal 2 Output  |                                            |
|                 | OUT3       | Motor 3         | (粉色线)        | Step Signal 3 Output  |                                            |
|                 | OUT4       | Motor 3         | (蓝色线)        | Step Signal 4 Output  |                                            |
|                 | + (5-12V)  | 独立 5V 电源    | +5V             | Power Input           |                                            |
|                 | - (GND)    | 独立 5V 电源    | GND             | Ground                | **共地**                                   |
| **ULN2003 #4**  |            |                 |                 |                       | **(驱动 Motor 4, 使用标准ULN2003模块，连接IN1-IN4)** |
|                 | OUT1       | Motor 4         | (橙色线)        | Step Signal 1 Output  |                                            |
|                 | OUT2       | Motor 4         | (黄色线)        | Step Signal 2 Output  |                                            |
|                 | OUT3       | Motor 4         | (粉色线)        | Step Signal 3 Output  |                                            |
|                 | OUT4       | Motor 4         | (蓝色线)        | Step Signal 4 Output  |                                            |
|                 | + (5-12V)  | 独立 5V 电源    | +5V             | Power Input           |                                            |
|                 | - (GND)    | 独立 5V 电源    | GND             | Ground                | **共地**                                   |
| **ULN2003 #5**  |            |                 |                 |                       | **(驱动 Motor 5, 使用标准ULN2003模块，连接IN1-IN4)** |
|                 | OUT1       | Motor 5         | (橙色线)        | Step Signal 1 Output  |                                            |
|                 | OUT2       | Motor 5         | (黄色线)        | Step Signal 2 Output  |                                            |
|                 | OUT3       | Motor 5         | (粉色线)        | Step Signal 3 Output  |                                            |
|                 | OUT4       | Motor 5         | (蓝色线)        | Step Signal 4 Output  |                                            |
|                 | + (5-12V)  | 独立 5V 电源    | +5V             | Power Input           |                                            |
|                 | - (GND)    | 独立 5V 电源    | GND             | Ground                | **共地**                                   |
| **独立 5V 电源**|            |                 |                 |                       |                                            |
|                 | +5V        | Motor 1-5       | (红色线)        | Motor Power           | 所有电机红线并联到此                     |
|                 | +5V        | ULN2003 #1-5    | + (5-12V)       | Driver Power          | 所有驱动板电源并联到此                   |
|                 | GND        | Arduino UNO     | GND             | Common Ground         | **必须连接**                             |
|                 | GND        | CD4052BE #1/2   | VSS/VEE         | Common Ground         | **必须连接**                             |
|                 | GND        | ULN2003 #1-5    | - (GND)         | Common Ground         | **必须连接**                             |

明白！你需要分别列出CD4052BE #1 和 #2 两块芯片的接线表，并且每个表都按照1-16号引脚顺序，且保留“源设备-源引脚-目标设备-目标引脚号/符号-信号/功能-备注”六列表头。这样查线和排查更直观。

下面是区分后的两块芯片的接线表（每块芯片一张表，均按1-16号引脚顺序）：

---

### CD4052BE #1 接线表

| 源设备        | 源引脚     | 目标设备        | 目标引脚号/符号 | 信号/功能             | 备注                       |
| :------------ | :--------- | :-------------- | :-------------- | :-------------------- | :------------------------- |
| ULN2003 #2    | IN2        | CD4052BE #1     | 1 (Y0B)         | 通道B输出0            | A1=0, A0=0 选通            |
| ULN2003 #4    | IN2        | CD4052BE #1     | 2 (Y2B)         | 通道B输出2            | A1=1, A0=0 选通            |
| Arduino UNO   | D7         | CD4052BE #1     | 3 (ZB)          | 公共输入B             | 步进信号2                  |
| ULN2003 #5    | IN2        | CD4052BE #1     | 4 (Y3B)         | 通道B输出3            | A1=1, A0=1 选通            |
| ULN2003 #3    | IN2        | CD4052BE #1     | 5 (Y1B)         | 通道B输出1            | A1=0, A0=1 选通            |
| Arduino UNO   | D12        | CD4052BE #1     | 6 (E_bar)       | 使能（低有效）        | 并联CD4052BE #2的Pin 6     |
| 电源/地       | GND        | CD4052BE #1     | 7 (VEE)         | 电源/地               | 共地                       |
| 电源/地       | GND        | CD4052BE #1     | 8 (VSS)         | 电源/地               | 共地                       |
| Arduino UNO   | D11        | CD4052BE #1     | 9 (A1)          | 选择位1               | 并联CD4052BE #2的Pin 9     |
| Arduino UNO   | D10        | CD4052BE #1     | 10 (A0)         | 选择位0               | 并联CD4052BE #2的Pin 10    |
| ULN2003 #5    | IN1        | CD4052BE #1     | 11 (Y3A)        | 通道A输出3            | A1=1, A0=1 选通            |
| ULN2003 #2    | IN1        | CD4052BE #1     | 12 (Y0A)        | 通道A输出0            | A1=0, A0=0 选通            |
| Arduino UNO   | D6         | CD4052BE #1     | 13 (ZA)         | 公共输入A             | 步进信号1                  |
| ULN2003 #3    | IN1        | CD4052BE #1     | 14 (Y1A)        | 通道A输出1            | A1=0, A0=1 选通            |
| ULN2003 #4    | IN1        | CD4052BE #1     | 15 (Y2A)        | 通道A输出2            | A1=1, A0=0 选通            |
| 电源/5V       | 5V         | CD4052BE #1     | 16 (VDD)        | +5V                   | 并联CD4052BE #2的Pin 16    |

---

### CD4052BE #2 接线表

| 源设备        | 源引脚     | 目标设备        | 目标引脚号/符号 | 信号/功能             | 备注                       |
| :------------ | :--------- | :-------------- | :-------------- | :-------------------- | :------------------------- |
| ULN2003 #2    | IN4        | CD4052BE #2     | 1 (Y0B)         | 通道B输出0            | A1=0, A0=0 选通            |
| ULN2003 #4    | IN4        | CD4052BE #2     | 2 (Y2B)         | 通道B输出2            | A1=1, A0=0 选通            |
| Arduino UNO   | D9         | CD4052BE #2     | 3 (ZB)          | 公共输入B             | 步进信号4                  |
| ULN2003 #5    | IN4        | CD4052BE #2     | 4 (Y3B)         | 通道B输出3            | A1=1, A0=1 选通            |
| ULN2003 #3    | IN4        | CD4052BE #2     | 5 (Y1B)         | 通道B输出1            | A1=0, A0=1 选通            |
| Arduino UNO   | D12        | CD4052BE #2     | 6 (E_bar)       | 使能（低有效）        | 并联CD4052BE #1的Pin 6     |
| 电源/地       | GND        | CD4052BE #2     | 7 (VEE)         | 电源/地               | 共地                       |
| 电源/地       | GND        | CD4052BE #2     | 8 (VSS)         | 电源/地               | 共地                       |
| Arduino UNO   | D11        | CD4052BE #2     | 9 (A1)          | 选择位1               | 并联CD4052BE #1的Pin 9     |
| Arduino UNO   | D10        | CD4052BE #2     | 10 (A0)         | 选择位0               | 并联CD4052BE #1的Pin 10    |
| ULN2003 #5    | IN3        | CD4052BE #2     | 11 (Y3A)        | 通道A输出3            | A1=1, A0=1 选通            |
| ULN2003 #2    | IN3        | CD4052BE #2     | 12 (Y0A)        | 通道A输出0            | A1=0, A0=0 选通            |
| Arduino UNO   | D8         | CD4052BE #2     | 13 (ZA)         | 公共输入A             | 步进信号3                  |
| ULN2003 #3    | IN3        | CD4052BE #2     | 14 (Y1A)        | 通道A输出1            | A1=0, A0=1 选通            |
| ULN2003 #4    | IN3        | CD4052BE #2     | 15 (Y2A)        | 通道A输出2            | A1=1, A0=0 选通            |
| 电源/5V       | 5V         | CD4052BE #2     | 16 (VDD)        | +5V                   | 并联CD4052BE #1的Pin 16    |

---

如需插入到你的文档或进一步调整，请告知！