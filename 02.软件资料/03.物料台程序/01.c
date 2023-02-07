#include <STC15F2K60S2.H>
#define uint unsigned int
	
sbit h = P5^4;
sbit IN2 = P3^3;
sbit q = P5^5;
sbit IN1 = P3^2;
sbit IN = P3^1;
sbit EN = P3^0;

void delay(uint i)
{
	while(i--);
}
void back()
{
	IN1 = 0;
	IN2 = 0;
	delay(10000);
	IN1 = 0;
	IN2 = 1;
	delay(10000);
	IN1 = 1;
	IN2 = 1;
	delay(10000);
	IN1 = 1;
	IN2 = 0;
	delay(10000);
}
void front()
{
	IN1 = 1;
	IN2 = 0;
	delay(10000);
	IN1 = 1;
	IN2 = 1;
	delay(10000);
	IN1 = 0;
	IN2 = 1;
	delay(10000);
	IN1 = 0;
	IN2 = 0;
	delay(10000);
}
void main()
{
	while(h)
	{
		EN = 1;
		back();
		EN = 0;
	}
	/*while(q)
	{
		EN = 1;
		front();
		EN = 0;
	}
	delay(10000);
	while(h)
	{
		EN = 1;
		back();
		EN = 0;
	}*/
	while(1)
	{
		if(IN == 1)
		{
			while(h)
			{
				EN = 1;
				back();
				EN = 0;
			}
			while(q)
			{
				EN = 1;
				front();
				EN = 0;
			}
			delay(10000);
			while(h)
			{
				EN = 1;
				back();
				EN = 0;
			}
		}
	}
}