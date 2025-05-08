/*******************************************************
  Bazi Motor Distribution Control Program
  Platform: Arduino UNO

  This program controls stepper motors based on the distribution of beads calculated from Bazi scores.
  Each bead corresponds to a specific angle of rotation for the motors.

  Pin Configuration:
  Motor 1: Directly connected to Arduino
  Motor 2-5: Controlled via CD4052BE multiplexer

  Serial Command Format: M<motor_number>:<angle>\n (e.g., M1:90, M2:-45)
 *******************************************************/

// --- Pin Definitions ---
// Motor 1 (direct connection)
const int motor1_Pin1 = 2; // Orange
const int motor1_Pin2 = 3; // Yellow
const int motor1_Pin3 = 4; // Pink
const int motor1_Pin4 = 5; // Blue
const int motor1_Pins[4] = {motor1_Pin1, motor1_Pin2, motor1_Pin3, motor1_Pin4};

// Motor 2-5 (multiplexed signals)
const int mux_SignalPin1 = 6; // To Chip#1 ZA
const int mux_SignalPin2 = 7; // To Chip#1 ZB
const int mux_SignalPin3 = 8; // To Chip#2 ZA
const int mux_SignalPin4 = 9; // To Chip#2 ZB
const int mux_SignalPins[4] = {mux_SignalPin1, mux_SignalPin2, mux_SignalPin3, mux_SignalPin4};

// CD4052BE control pins
const int mux_A0_Pin = 10; // Select Bit 0
const int mux_A1_Pin = 11; // Select Bit 1
const int mux_Enable_Pin = 12; // Enable, Active Low

// --- Motor Parameters ---
const float STEP_ANGLE = 5.625;    // Stepper motor physical step angle
const int REDUCTION_RATIO = 64;     // Reduction ratio
const int STEPS_PER_REVOLUTION = 4096; // Total steps for one revolution in 8-step mode
const float ANGLE_PER_STEP = 360.0 / STEPS_PER_REVOLUTION; // Angle per step

// --- Global Variables ---
String inputString = "";         // Store serial input string
bool stringComplete = false;     // Serial string reception complete flag

// 8-step mode phase sequence table
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

// --- Initialization ---
void setup() {
  // Set motor 1 pins as output
  for (int i = 0; i < 4; i++) {
    pinMode(motor1_Pins[i], OUTPUT);
  }
  // Set multiplexer signal pins as output
  for (int i = 0; i < 4; i++) {
    pinMode(mux_SignalPins[i], OUTPUT);
  }
  // Set CD4052BE control pins as output
  pinMode(mux_A0_Pin, OUTPUT);
  pinMode(mux_A1_Pin, OUTPUT);
  pinMode(mux_Enable_Pin, OUTPUT);

  // Initial state: disable multiplexer, stop all motor signals
  disableMux();
  motorStop(1); // Stop motor 1
  setMuxMotorPhase(0); // Stop signals for motors 2-5

  // Initialize serial communication
  Serial.begin(9600);
  inputString.reserve(200); // Preallocate string memory
}

// --- Main Loop ---
void loop() {
  // Handle complete serial commands
  if (stringComplete) {
    parseAndMoveMotor(inputString);
    // Clear for next reception
    inputString = "";
    stringComplete = false;
  }
}

// --- Serial Event Handling ---
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar; // Append character
    // If newline character received, mark string reception complete
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// --- Command Parsing and Execution ---
void parseAndMoveMotor(String cmd) {
  cmd.trim(); // Remove whitespace
  if (!cmd.startsWith("M")) {
    Serial.println("Error: Command must start with 'M'");
    return;
  }
  int colonPos = cmd.indexOf(':');
  if (colonPos <= 1) {
    Serial.println("Error: Command format error (should be M<num>:<angle>)");
    return;
  }

  // Parse motor index and angle
  int motorIdx = cmd.substring(1, colonPos).toInt();
  float angle = cmd.substring(colonPos + 1).toFloat();

  // Check if motor index is valid
  if (motorIdx < 1 || motorIdx > 5) {
    Serial.print("Error: Invalid motor index (should be 1-5): ");
    Serial.println(motorIdx);
    return;
  }

  // Execute movement
  moveToAngle(motorIdx, angle);
}

// --- Multiplexer Control ---
void setMuxChannel(int motorIdx_2_to_5) {
  if (motorIdx_2_to_5 < 2 || motorIdx_2_to_5 > 5) return; // Safety check
  int channelIdx = motorIdx_2_to_5 - 2; // Convert to 0-3

  // Set select bits A0 and A1
  digitalWrite(mux_A0_Pin, (channelIdx & 0b01) ? HIGH : LOW);
  digitalWrite(mux_A1_Pin, (channelIdx & 0b10) ? HIGH : LOW);

  // Enable chip (active low)
  digitalWrite(mux_Enable_Pin, LOW);
  delayMicroseconds(10); // Short delay to ensure chip state change
}

// Disable CD4052BE chip
void disableMux() {
  digitalWrite(mux_Enable_Pin, HIGH); // High level disables
}

// --- Stepper Motor Control ---
void setMuxMotorPhase(byte phase) {
  digitalWrite(mux_SignalPin1, (phase & 0b1000) ? HIGH : LOW);
  digitalWrite(mux_SignalPin2, (phase & 0b0100) ? HIGH : LOW);
  digitalWrite(mux_SignalPin3, (phase & 0b0010) ? HIGH : LOW);
  digitalWrite(mux_SignalPin4, (phase & 0b0001) ? HIGH : LOW);
}

// Stop specified motor signal output
void motorStop(int motorIdx) {
  if (motorIdx == 1) {
    setDirectMotorPhase(0); // Stop all phases for motor 1
  } else if (motorIdx >= 2 && motorIdx <= 5) {
    setMuxMotorPhase(0);
    disableMux();
  }
}

// --- Angle to Steps Conversion ---
int angleToSteps(float angle) {
  // Calculate required total steps (rounding)
  int steps = round(angle / ANGLE_PER_STEP);
  return steps;
}

// --- Core Move Function ---
void moveToAngle(int motorIdx, float angle) {
  int totalSteps = angleToSteps(angle); // Get total steps needed
  if (totalSteps == 0) {
    Serial.println("Steps are 0, no movement required.");
    return;
  }

  bool clockwise = (totalSteps > 0); // Determine rotation direction
  int stepsToTake = abs(totalSteps); // Get absolute steps

  if (motorIdx == 1) {
    // Control direct motor (motor 1)
    for (int i = 0; i < stepsToTake; i++) {
      int phaseIndex = clockwise ? (i % 8) : (7 - (i % 8));
      setDirectMotorPhase(phaseSequence[phaseIndex]);
      delay(2); // Control rotation speed
    }
    motorStop(1); // Stop motor 1 after movement

  } else if (motorIdx >= 2 && motorIdx <= 5) {
    // Control multiplexed motors (motor 2-5)
    setMuxChannel(motorIdx); // Select and enable corresponding channel

    for (int i = 0; i < stepsToTake; i++) {
      int phaseIndex = clockwise ? (i % 8) : (7 - (i % 8));
      setMuxMotorPhase(phaseSequence[phaseIndex]);
      delay(2); // Control rotation speed
    }
    motorStop(motorIdx); // Stop multiplexed signals and disable chip

  } else {
    Serial.println("Error: Invalid motor index in moveToAngle");
    return;
  }
  Serial.println("DONE");
}