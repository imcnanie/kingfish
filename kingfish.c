
//#define F_CPU 16000000 

#define RED OCR1A
#define GREEN OCR1B
#define TURN OCR1C
#define WHITE OCR4A
#define FOSC 16000000
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1


#include <avr/io.h> 
#include <util/delay.h> 
#include <avr/interrupt.h>
#include <util/setbaud.h>


#include <stdio.h>


#define sbi(var, mask)   ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)   ((var) &= (uint8_t)~(1 << mask))

#define STATUS_LED 0

#define check_bit(address,bit) ((address & (1<<bit)) == (1<<bit))

#define set_bit(address,bit) (address |= (1<<bit))
#define clear_bit(address,bit) (address &= ~(1<<bit))
#define toggle_bit(address,bit) (address ^= (1<<bit))

//Define functions
//======================

static int uart_putchar(char c, FILE *stream);
uint8_t uart_getchar(void);

static FILE mystdout = FDEV_SETUP_STREAM(uart_putchar, NULL, _FDEV_SETUP_WRITE);

void delay_ms(uint16_t x); // general purpose delay

void pwm_init() { 
  PORTB = 0xFF;
  DDRB |= (1<<7)|(1<<6)|(1<<5);
  ICR1 = 4999;
  //TCCR1A|=0xFF;
  //TCCR1B|=0xFF;
  //TCCR1A = 0b10101010; 
  TCCR1A|=(1<<COM1A1)|(1<<COM1B1)|(1<<COM1C1)|(1<<WGM11);
  //TCCR1A = (COM1A1<<1)|(COM1B1<<1)|(COM1C1<<1)|(WGM11<<1);
  //TCCR1B = 0b00011001;
  TCCR1B|=(1<<WGM13)|(1<<WGM12)|(1<<CS11)|(1<<CS10);
  RED= 0x0000;
  GREEN = 0x0000;
  TURN = 0x0000;
  TC4H = 0x03;
  OCR4C = 0xFF;
  TCCR4A = 0b10000010;
  TCCR4B = 0b00000001;
  //int num = 2000;
  //RED = num;
  //GREEN = num;
  //BLUE = num; 
}       

void adc_init() {
  //Enable prescaler - determined by clock (1,600/5 = 320 to 160/2 = 80)
  ADCSRA |= 1<<ADPS2;
  ADCSRA |= 1<<ADPS1;
  ADCSRA |= 1<<ADPS0;
  
  //Enable interrupts function in ADC
  ADCSRA |= 1<<ADIE;
  
  //8-bit or 10-bit results
  ADMUX |= 1<<ADLAR;
  
  //Set voltage reference
  ADMUX |= 1<<REFS0;
  
  //Turn on ADC
  ADCSRA |= 1<<ADEN;
  
  //Enable global interrupts
  sei();
  
  //Start first conversion
  ADCSRA |= 1<<ADSC;
}

void pwm_set_output(uint8_t duty) 
{ } 

void Wait() {
   uint8_t i;
   for(i=0;i<50;i++)
   {
      _delay_loop_2(0);
      _delay_loop_2(0);
      _delay_loop_2(0);
   }

}

int main(void) { 

  pwm_init();
  adc_init();
  uart_init();
  TURN = 300;
  
  int n;
  int cur_char;
  int cur_char2;
  int state = 0;
  uint8_t cur_pos;

  while(1) {

    //cur_pos = uart_getchar();
    //if (cur_pos>300){
    //OCR1C=cur_pos;
      //Wait();
      //}
    //TURN=300;
    //OCR1C=350;
    // n++;
    // if (n == 3000)
       //    TURN += 1;
    // //OCR1C=400;
       // //Wait();
       //  if (TURN==500)
	//     TURN=350;
      cur_char = uart_getchar();
     // //int ia = (int)cur_char; 
	// //cur_char2 = map(ia, 0x00, 0xFF, 150,400);
      
      if (cur_char == 0x02) {
	state = 2;
      } else if (cur_char == 0x01) {
	state = 1;
      }

      if (cur_char != 0x00 && state == 2) {
	//cur_char2 = cur_char;
	TURN = cur_char+200;
      }

       if (cur_char != 0x00 && state == 1) {
	//cur_char2 = cur_char;
	OCR1A = cur_char+200;
      }
      //if (cur_char2)
     //TURN = 0xFF;
    //} else {
    //TURN=450;
  }
}

void map(int x, long in_min, long in_max, long out_min, long out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void uart_init(void) { 
//DDRD |= (0<<0);
DDRD = 0b11111110; //PORTD (RX on PD0)
UBRR1H = MYUBRR >> 8;
UBRR1L = MYUBRR;
UCSR1B = (1<<RXEN1)|(1<<TXEN1);
} 

static int uart_putchar(char c, FILE *stream)
{
    if (c == '\n') uart_putchar('\r', stream);
  
    loop_until_bit_is_set(UCSR1A, UDRE1);
    UDR1 = c;
    
    return 0;
}

uint8_t uart_getchar(void)
{
    while( !(UCSR1A & (1<<RXC1)) );
    return(UDR1);
}

ISR(ADC_vect)
{

  //global adcResult;
  
  uint8_t theLow = ADCL;
  uint16_t theTenBitResult = ADCH<<8 | theLow;
  
  //String var deceleration
  char adcResult[4];
  
  //Convert ADC conversion result to a string
  itoa(ADCH, adcResult, 10);
  
  //Print to serial
  
  //Start Next conversion
  ADCSRA |= 1<<ADSC;
}

