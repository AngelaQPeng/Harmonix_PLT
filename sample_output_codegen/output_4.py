# Generated Python Code
# Automatically translated from Harmonix_PLT language
Title = 'Error Example'
Composer = 'Nobody'
clef = 'G'
time_signature = '5/4'
key_signature = '@B# Major'
def Bassline():
    pattern = []
    pattern.append({'note': 'D3', 'duration': 'quarter'})
    pattern.append({'note': 'F3', 'duration': 'quarter'})
    pattern.append({'note': 'A3', 'duration': 'quarter'})
    return pattern
def Melody():
    pattern = []
    pattern.append({'note': 'F4', 'duration': 'quarter'})
    repeat_result_0 = []
    for _ in range(3):
        repeat_result_0.extend(Bassline())
    pattern.extend(repeat_result_0)
    return pattern
final = (Bassline() + Melody())