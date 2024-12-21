Title = 'Symphony No. 9'
Composer = 'Ludwig van Beethoven'
staff = 'Bass'
clef = 'F'
time_signature = '3/4'
key_signature = '@D Minor'

def MainTheme():
    pattern = []
    pattern.append({'note': 'D4', 'duration': 'half'})
    pattern.append({'note': 'F4', 'duration': 'quarter'})
    repeat_result_0 = []
    pattern.append({'note': 'A4', 'duration': 'quarter'})
    for _ in range(3):
        repeat_result_0.append({'note': 'D4', 'duration': 'eighth'})
        repeat_result_0.append({'note': 'F4', 'duration': 'eighth'})
    pattern.extend(repeat_result_0)
    return pattern
cached_MainTheme = MainTheme()

def Bridge():
    pattern = []
    pattern.append({'note': 'G4', 'duration': 'quarter'})
    repeat_result_1 = []
    pattern.append({'note': 'B4', 'duration': 'quarter'})
    repeat_result_1.extend(cached_MainTheme)
    pattern.extend(repeat_result_1)
    return pattern
cached_Bridge = Bridge()

def High():
    pattern = []
    pattern.append({'note': 'C4', 'duration': 'quarter'})
    repeat_result_2 = []
    pattern.append({'note': 'D3', 'duration': 'quarter'})
    repeat_result_2.extend(cached_Bridge)
    pattern.extend(repeat_result_2)
    repeat_result_3 = []
    repeat_result_3.extend(cached_MainTheme)
    pattern.extend(repeat_result_3)
    return pattern
cached_High = High()
fullPiece = cached_MainTheme + (cached_Bridge + (cached_MainTheme + cached_High))