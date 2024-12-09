Title = 'Symphony No. 9'
Composer = 'Ludwig van Beethoven'
staff = 'Bass'
clef = 'F'
time_signature = '3/4'
key_signature = 'D Minor'
def MainTheme():
    pattern = []
    pattern.append({'note': 'D4', 'duration': 'half'})
    pattern.append({'note': 'F4', 'duration': 'quarter'})
    pattern.append({'note': 'A4', 'duration': 'quarter'})
    repeat_result_0 = []
    for _ in range(3):
        repeat_result_0.append({'note': 'D4', 'duration': 'eighth'})
        repeat_result_0.append({'note': 'F4', 'duration': 'eighth'})
    pattern.extend(repeat_result_0)
    return pattern
fullPiece = (MainTheme() + MainTheme())