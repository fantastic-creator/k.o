import serial
import time
import sys
import traceback

PORT = 'COM5'
BAUDRATE = 9600
TIMEOUT = 2  # seconds

def debug_print(msg):
    print(f"[DEBUG] {msg}")

def main():
    debug_print(f"Python version: {sys.version}")
    debug_print(f"pyserial version: {serial.__version__}")
    debug_print(f"Trying to open serial port {PORT} at {BAUDRATE} baud...")
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        debug_print(f"Serial port {PORT} opened successfully.")
    except Exception as e:
        debug_print(f"Failed to open serial port: {e}")
        traceback.print_exc()
        return

    try:
        # 测试命令列表，分别让5个电机正转90度、反转90度
        test_cmds = [
            b'M1:90\n', b'M2:90\n', b'M3:90\n', b'M4:90\n', b'M5:90\n',
            b'M1:-90\n', b'M2:-90\n', b'M3:-90\n', b'M4:-90\n', b'M5:-90\n'
        ]
        for cmd in test_cmds:
            debug_print(f"Sending command: {cmd.strip()}")
            ser.write(cmd)
            debug_print("Command sent. Waiting for response...")
            time.sleep(1.5)  # 等待电机动作和Arduino响应
            resp = b''
            start_time = time.time()
            while time.time() - start_time < 2:
                if ser.in_waiting:
                    resp += ser.read(ser.in_waiting)
                time.sleep(0.1)
            if resp:
                debug_print(f"Received response: {resp}")
            else:
                debug_print("No response received for this command.")
    except Exception as e:
        debug_print(f"Error during serial communication: {e}")
        traceback.print_exc()
    finally:
        ser.close()
        debug_print(f"Serial port {PORT} closed.")

if __name__ == '__main__':
    main()