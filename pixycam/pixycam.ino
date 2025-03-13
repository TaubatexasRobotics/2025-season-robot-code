#include <Pixy2.h>

Pixy2 pixy;

void setup()
{
  Serial.begin(115200);
  pixy.init();
}

void loop()
{ 
  int i; 
  pixy.ccc.getBlocks();
  
  if (pixy.ccc.numBlocks && Serial.available())
  {
    for (i = 0; i < pixy.ccc.numBlocks; i++)
      pixy.ccc.blocks[i].print();
  }
  delay(50);
}
