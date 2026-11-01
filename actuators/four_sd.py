try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import threading

class FourSD(object):
    def __init__(self, settings):
        self.segments = settings['segments']
        self.digits = settings['digits']
        
        GPIO.setmode(GPIO.BCM)
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
            
        self.num = {' ': (0,0,0,0,0,0,0),
                    '0': (1,1,1,1,1,1,0),
                    '1': (0,1,1,0,0,0,0),
                    '2': (1,1,0,1,1,0,1),
                    '3': (1,1,1,1,0,0,1),
                    '4': (0,1,1,0,0,1,1),
                    '5': (1,0,1,1,0,1,1),
                    '6': (1,0,1,1,1,1,1),
                    '7': (1,1,1,0,0,0,0),
                    '8': (1,1,1,1,1,1,1),
                    '9': (1,1,1,1,0,1,1)}
        
        # inic stanje
        self.current_text = "    " 
        self.is_blinking = False
        self.is_blank = False # Koristi se da ugasi cifre dok treperi
        self.running = True
        
        # nit za osvezavanje ekrana
        self.thread = threading.Thread(target=self._refresh_display)
        self.thread.start()
        
        # nit koja kontrolise treperenje
        self.blink_thread = threading.Thread(target=self._blink_loop)
        self.blink_thread.start()

    def _refresh_display(self):
        while self.running:
            # ako je u ciklusu treperenja "ugaseno", preskocimo crtanje
            if self.is_blank:
                time.sleep(0.01)
                continue
                
            # Uklanjamo dvotacku iz vremena "0230"
            s = self.current_text.replace(":", "").rjust(4, ' ')
            
            for digit in range(4):
                if digit >= len(s):
                    continue
                    
                char = s[digit]
                if char not in self.num:
                    char = ' ' # ako stigne neki nepoznat znak, stavi razmak

                for loop in range(0, 7):
                    GPIO.output(self.segments[loop], self.num[char][loop])
                    
                GPIO.output(self.digits[digit], 0) # pali cifru
                time.sleep(0.001)
                GPIO.output(self.digits[digit], 1) # gasi cifru

    def _blink_loop(self):
        while self.running:
            if self.is_blinking:
                self.is_blank = not self.is_blank # upaljeno/ugaseno
                time.sleep(0.5) # treperi svakih pola sekunde
            else:
                self.is_blank = False
                time.sleep(0.1)

    # poziva pi2
    def display_text(self, text):
        self.is_blinking = False
        self.current_text = str(text)

    def blink(self, text="00:00"):
        self.current_text = str(text)
        self.is_blinking = True

    def clear(self):
        self.is_blinking = False
        self.current_text = "    "

    def stop(self):
        self.running = False
        self.thread.join()
        self.blink_thread.join()