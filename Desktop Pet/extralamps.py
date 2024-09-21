from phue import Bridge

b = Bridge('Hue Bridge IP')
b.connect()

user_input_ToF = False

def update_lights():
    global user_input_ToF
    b.set_light([1, 4], 'on', user_input_ToF)
