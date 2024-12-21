# Generated Python Code
# Automatically translated from Harmonix_PLT language
Title = 'Simple Melody'
Composer = 'Angela Peng'
staff = 'Treble'
clef = 'G'
time_signature = '4/4'
key_signature = '@C Major'
def MainMelody():
    pattern = []
    pattern.append({'note': 'C4', 'duration': 'quarter'})
    return pattern
repeat_result_0 = []
for _ in range(2):
    repeat_result_0.extend(MainMelody())
a = (repeat_result_0 + (MainMelody() + (MainMelody() + (MainMelody() + MainMelody()))))