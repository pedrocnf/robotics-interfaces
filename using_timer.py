from machine import Pin, I2C, ADC, Timer
from ssd1306 import SSD1306_I2C
import random
import time

# Configuração do display OLED (ajuste o endereço e os pinos conforme necessário)
i2c = I2C(1, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)


# Configuração do potenciômetro
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)  # Faixa de 0 a 3.3V
pot.width(ADC.WIDTH_10BIT)  # Resolução de 10 bits (0-1023)

# Variáveis globais para armazenar os valores
value_50ms = 0
value_2s = 0

# Função executada a cada 50ms
def task_50ms(timer):
    global value_50ms
    value_50ms = random.randint(0, 100)  # Gera um valor aleatório entre 0 e 100

# Função executada a cada 2s
def task_2s(timer):
    global value_2s
    value_2s = random.randint(100, 200)  # Gera um valor aleatório entre 100 e 200

# Função para atualizar o display conforme o valor do potenciômetro
def update_display():
    while True:
        pot_value = pot.read()  # Lê o valor do potenciômetro (0 a 1023)
        oled.fill(0)  # Limpa o display

        # Verifica se o potenciômetro está abaixo ou acima de 512 (metade do range)
        if pot_value < 512:
            oled.text(f"Value 50ms: {value_50ms}", 0, 0)
        else:
            oled.text(f"Value 2s: {value_2s}", 0, 0)

        oled.show()
        time.sleep(0.1)  # Atualiza a cada 100ms

# Configuração dos timers
timer_50ms = Timer(0)
timer_2s = Timer(1)

# Executa task_50ms a cada 50ms
timer_50ms.init(period=50, mode=Timer.PERIODIC, callback=task_50ms)

# Executa task_2s a cada 2s (2000ms)
timer_2s.init(period=2000, mode=Timer.PERIODIC, callback=task_2s)

# Inicia a atualização do display
update_display()
