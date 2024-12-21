Title = 'Simple Melody'
Composer = 'Angela Peng'
staff = 'Treble'
clef = 'G'
time_signature = '4/4'
key_signature = '@C Major'

def MainMelody():
    pattern = []
    pattern.extend([{'note': 'C4', 'duration': 'quarter'}] * 10)
    pattern.extend([{'note': 'C5', 'duration': 'quarter'}] * 2)
    return pattern
cached_MainMelody = MainMelody()
repeat_result_0 = []
repeat_result_0.extend(cached_MainMelody * 2)
a = repeat_result_0 + (cached_MainMelody + (cached_MainMelody + (cached_MainMelody + cached_MainMelody)))