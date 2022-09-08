#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>


#define LIGHTSEN_OUT 23

volatile int eventCounter = 0;
unsigned char humandetect = 0;

void myInterrupt(void) {
   eventCounter++;
   humandetect = 1;

}


// -------------------------------------------------------------------------
// main
int main(void) 
{
	// sets up the wiringPi library
	if (wiringPiSetup () < 0) 
	{
		fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno));
		return 1;
	}
	
	pinMode(LIGHTSEN_OUT, INPUT);


	if ( wiringPiISR (LIGHTSEN_OUT, INT_EDGE_RISING, &myInterrupt) < 0 ) 
	{
		fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno));
		return 1;
	}

	// display counter value every second.
	while ( 1 ) 
	{
		//printf( "%d\n", eventCounter );
		//eventCounter = 0;
		
		if(digitalRead(LIGHTSEN_OUT) == 0)
			printf("light full ! \n");
		if(digitalRead(LIGHTSEN_OUT) == 1)
			printf("dark \n");		
	
		delay( 200 ); // wait 1 second
	}

	return 0;
}