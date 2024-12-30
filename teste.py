import time
from machine import Pin, ADC, I2C, Timer
from ssd1306 import SSD1306_I2C
import dht


# Configuração da I2C e display OLED
i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # Ajustar os pinos conforme necessário
display = SSD1306_I2C(128, 64, i2c)

# Configuração do ADC para ler o microfone
adc = ADC(Pin(27))  # Ajustar conforme o pino usado
adc.width(ADC.WIDTH_10BIT)

# Sensor de umidade e temperatura
dht_sensor = dht.DHT22(Pin(13))

# Configuração do potenciômetro
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)  # Faixa de 0 a 3.3V
pot.width(ADC.WIDTH_10BIT)  # Resolução de 10 bits (0-1023)

db = 0
temperature = 0
humidity = 0

def dht_read(timer):
    global temperature
    global humidity
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

def noise_read(timer):
    global db
    sampleWindow = 50  # Janela de amostragem em ms
    signalMin = 1024
    signalMax = 0
    startMillis = time.ticks_ms()
    peakToPeak = 0
    signalMin = 1024
    signalMax = 0
    # Coleta de dados durante 50ms
    while (time.ticks_ms() - startMillis) < sampleWindow:
        sample = adc.read()
        if sample < 1024:
            if sample > signalMax:
                signalMax = sample
            elif sample < signalMin:
                signalMin = sample

    # Calcular amplitude de pico-a-pico e converter para dB
    peakToPeak = signalMax - signalMin
    db = ((peakToPeak - 20) * (90 - 49.5) / (900 - 20) + 49.5)-20 #20 é minha calibração
    return db

def thermic_comfort(temperatura, humidity):
    if 20 <= temperature <= 30 and 70 <= humidity >=30:
        conforto = True
    else:
        conforto = False
    return conforto
        
def noise_screen():
    display.fill(0)
    display.text(f"Noise Meter", 10, 0)
    display.text(f"{db:.2f} dB", 20, 15)
    for x in range(5, 114, 6):
        display.line(x, 32, x, 27, 1)
    display.rect(0, 32, 120, 20, 1)
    r = int((db / 120) * 120)
    display.fill_rect(1, 33, r, 18, 1)
    display.show()

      
def temperature_screen():
    display.fill(0)
    display.text("TEMPERATURE", 10, 5)
    display.text(f"{temperature:.2f} oC", 20, 25)
    display.show()
    
def humidity_screen():
    display.fill(0)
    display.text("HUMIDITY", 20, 5)
    display.text(f"{humidity:.2f} %Rh", 25, 25)
    display.show()
    
    
def confort_screen():
    None
    

def update_display():
    while True:
        pot_value = pot.read()  # Lê o valor do potenciômetro (0 a 1023)
        display.fill(0)  # Limpa o display
        print(db)
        # Verifica se o potenciômetro está abaixo ou acima de 512 (metade do range)
        if pot_value < 333:
            noise_screen()
        elif pot_value >= 334 and pot_value < 666:
            temperature_screen()
        else:
            humidity_screen()

        display.show()
        time.sleep(0.1)  # Atualiza a cada 100ms

"""
# Função principal
def loop():
    global signalMin, signalMax
    startMillis = time.ticks_ms()
    peakToPeak = 0
    signalMin = 1024
    signalMax = 0

    # Coleta de dados durante 50ms
    while (time.ticks_ms() - startMillis) < sampleWindow:
        sample = adc.read()
        if sample < 1024:
            if sample > signalMax:
                signalMax = sample
            elif sample < signalMin:
                signalMin = sample

    # Calcular amplitude de pico-a-pico e converter para dB
    peakToPeak = signalMax - signalMin
    db = ((peakToPeak - 20) * (90 - 49.5) / (900 - 20) + 49.5)-20 #20 é minha calibração

    # Atualizar display OLED com valor de dB
    display.fill(0)
    display.text(f"Noise Meter", 10, 0)
    display.text(f"{db:.2f} dB", 20, 15)
    for x in range(5, 114, 6):
        display.line(x, 32, x, 27, 1)
    display.rect(0, 32, 120, 20, 1)
    r = int((db / 120) * 120)
    display.fill_rect(1, 33, r, 18, 1)
    display.show()

    time.sleep(0.15)

# Executar o programa
setup()
while True:
    loop()
"""

# Configuração dos timers
timer_50ms = Timer(0)
timer_2s = Timer(1)

# Executa task_50ms a cada 50ms
timer_50ms.init(period=50, mode=Timer.PERIODIC, callback=noise_read)

# Executa task_2s a cada 2s (2000ms)
timer_2s.init(period=2000, mode=Timer.PERIODIC, callback=dht_read)


update_display()