#include <Wire.h>
#include <Servo_Hardware_PWM.h>

// constants
#define ADDR 0x8
#define SDA_PIN 20
#define SCL_PIN 21

#define NUM_MOTORS 3

// default angle to achieve platform height of 11 cm
#define DEFAULT_ANGLE 43

// min and max values of calibration angles (i.e. 0 and 90)
#define MAX_CMD_ANGLE 90
#define MIN_CMD_ANGLE 0

// NOTE: angles provided here only valid for default initialization of servo
// convert to microseconds if not using default initialization and use writeMicroseconds() function instead;
#define UPPER_ANG_S1 146     // S1 angle at 0 deg from horizontal
#define LOWER_ANG_S1 50      // S1 angle at 90 deg from horizontal
#define UPPER_ANG_S2 148     // S2 angle at 0 deg from horizontal
#define LOWER_ANG_S2 51      // S2 angle at 90 deg from horizontal
#define UPPER_ANG_S3 150     // S3 angle at 0 deg from horizontal
#define LOWER_ANG_S3 51      // S3 angle at 90 deg from horizontal

#define S1_PIN 7
#define S2_PIN 8
#define S3_PIN 6

const int ANGLE_LIMITS[3][2] = {{UPPER_ANG_S1, LOWER_ANG_S1}, {UPPER_ANG_S2, LOWER_ANG_S2}, {UPPER_ANG_S3, LOWER_ANG_S3}};

// globals
Servo servos[3] = {};

volatile bool new_data = false;
float motor_angles[NUM_MOTORS] = {};
int last_motor_angles[NUM_MOTORS] = {-1, -1, -1};

// event run when data received on SDA line
void on_receive(int num_bytes)
{
  // analyzing runtime
  // int start = millis();
  
  // sets up temporary byte array to construct float values
  byte b_tmp[4] = {};

  // clears first byte received (contains registry number)
  Wire.read();

  // iterate through remaining bytes available
  for(int i = 0; i < num_bytes-1; i++)
  {
    b_tmp[i%4] = Wire.read();
    
    // every 4 bytes, read into motor_angles array
    if ((i+1)%4 == 0)
    {
      memcpy(&motor_angles[i/4], b_tmp, 4);
    }
  }

  // set new_data flag
  new_data = true;

  // debug, analyze runtime
  /*
  Serial.print("Time to execute: ");
  Serial.println(millis()-start);
  */
}

void move_servos(float angles[3])
{
  // debug, analyzing runtime
    // int start = millis();
    // checking if angles within limits
    for(int i = 0; i < NUM_MOTORS; i++)
    {
      /*
      Serial.print("MOTOR ");
      Serial.print(i);
      Serial.println(":");

      Serial.print("Angle limits: ");
      Serial.print(ANGLE_LIMITS[i][0]);
      Serial.print(" - ");
      Serial.print(ANGLE_LIMITS[i][1]);
      Serial.println(" [deg]");

      Serial.print("Command angle: ");
      Serial.print(motor_cmd_angle);
      Serial.println(" [deg]");
      */

      int motor_act_angle = (int)map(angles[i], MIN_CMD_ANGLE, MAX_CMD_ANGLE, ANGLE_LIMITS[i][0], ANGLE_LIMITS[i][1]);

      /*
      Serial.print("Actual angle: ");
      Serial.print(motor_act_angle);
      Serial.println(" [deg]");
      */

      if(motor_act_angle != last_motor_angles[i])
      {
        last_motor_angles[i] = motor_act_angle;

        if(motor_act_angle > ANGLE_LIMITS[i][0])
        {
          /*
          Serial.print("ERROR: Attempted move is larger than upper limit (would go past 0 deg). Setting to upper limit of ");
          Serial.print(ANGLE_LIMITS[i][0]);
          Serial.println(" [deg] instead.");
          */
          servos[i].write(ANGLE_LIMITS[i][0]);
        }
        else if(motor_act_angle < ANGLE_LIMITS[i][1])
        {
          /*
          Serial.print("ERROR: Attempted move is smaller than lower limit (would go past 90 deg). Setting to lower limit of ");
          Serial.print(ANGLE_LIMITS[i][1]);
          Serial.println(" [deg] instead.");
          */
          servos[i].write(ANGLE_LIMITS[i][1]);
        }
        else
        {
          // Serial.println("Angle okay, executing move");

          servos[i].write(motor_act_angle);
        }

      /*
      Serial.print("Actual angle after move: ");
      Serial.print(servos[i].read());
      Serial.println(" [deg]\n");
      */
      }
      
    }

    // debug, analyze runtime
    /*
    Serial.print("Time to execute: ");
    Serial.println(millis()-start);
    */
}

void setup() 
{
  // begin I2C communications at address specified
  Wire.begin(ADDR);

  // sets up event to run on receiving data
  Wire.onReceive(on_receive);

  // enables pull up resistors required for I2C communication
  pinMode(SDA_PIN, INPUT_PULLUP);
  pinMode(SCL_PIN, INPUT_PULLUP);

  // init servos
  servos[0].attach(S1_PIN);
  servos[1].attach(S2_PIN);
  servos[2].attach(S3_PIN);

  // set all servos to same default angle
  float default_angles[3] = {DEFAULT_ANGLE, DEFAULT_ANGLE, DEFAULT_ANGLE};
  move_servos(default_angles);

  // console for debuggin' purposes
  Serial.begin(9600);
}

void loop()
{
  if(new_data)
  {
    move_servos(motor_angles);
 
    //clear flag after using data
    new_data = false;   
  }

  // small delay before checking for new data (prevents race conditions)
  delay(20);
}
