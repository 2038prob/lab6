#if (ARDUINO >= 100)
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif

#include <Servo.h>
#include <ros.h>
#include <std_msgs/UInt16.h>
#include <geometry_msgs/Twist.h>
#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>
ros::NodeHandle nh;
geometry_msgs::Twist msg;
sensor_msgs::Range range_msg;
ros::Publisher pub_range( "/ultrasound", &range_msg);
const int adc_pin = 0;

char frameid[] = "/ultrasound";

Servo servo;
Servo servo2;
uint16_t turn = 0;
uint16_t sped = 0;
float getRange_Ultrasound(int pin_num){
  int val = 0;
  for(int i=0; i<4; i++) val += analogRead(pin_num);
  float range =  val;
  return range /322.519685;   // (0.0124023437 /4) ; //cvt to meters
}
void servo_cb( const geometry_msgs::Twist& cmd_vel){
  float pressed = cmd_vel.angular.z;
  int throttle = cmd_vel.linear.x;
  turn = round(pressed*45);
// if (pressed == 2){
//  turn = 45;
//  }
// if(pressed == -2){
//  turn = 135;
// }
 if (throttle > 1){
  sped = 80;
  }
  else if (throttle < -1){
  sped = 100;
  }
 servo.write(turn);
 servo2.write(sped);
 digitalWrite(13, HIGH-digitalRead(13));
}

ros::Subscriber <geometry_msgs::Twist> sub("/cmd_vel_mux/input/teleop",servo_cb);

void setup(){
   pinMode(13,OUTPUT);
   nh.initNode();
   nh.subscribe(sub);
   servo.attach(9);
   servo2.attach(10);

   range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg.header.frame_id =  frameid;
  range_msg.field_of_view = 0.1;  // fake
  range_msg.min_range = 0.0;
  range_msg.max_range = 6.47;
  nh.advertise(pub_range);
  pinMode(7,OUTPUT);
  digitalWrite(7, LOW);
}

long range_time;

void loop(){
  if ( millis() >= range_time ){
    int r =0;

    range_msg.range = getRange_Ultrasound(5);
    range_msg.header.stamp = nh.now();
    pub_range.publish(&range_msg);
    range_time =  millis() + 50;
  }
 nh.spinOnce();
 delay(1);
}
