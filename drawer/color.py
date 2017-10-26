def convert_tts_to_pygame(color):
    return (color[0] * 255, color[1] * 255, color[2] * 255)

def convert_pygame_to_tts(color):
    return (float(color[0] / 255), float(color[1] / 255), float(color[2] / 255))