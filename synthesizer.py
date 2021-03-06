import random
import wave

import ffmpeg
import thinkdsp
from pydub import AudioSegment
from pydub.playback import play

note_freqs = {
    'C0': 16.35, 'Db0': 17.32, 'D0': 18.35, 'Eb0': 19.45,
    'E0': 20.60, 'F0': 21.83, 'Gb0': 23.12, 'G0': 24.50,
    'Ab0': 25.96, 'A0': 27.50, 'Bb0': 29.14, 'B0': 30.87,
    'C1': 32.70, 'Db1': 34.65, 'D1': 36.71, 'Eb1': 38.89,
    'E1': 41.20, 'F1': 43.65, 'Gb1': 46.25, 'G1': 49.00,
    'Ab1': 51.91, 'A1': 55.00, 'Bb1': 58.27, 'B1': 61.74,
    'C2': 65.41, 'Db2': 69.30, 'D2': 73.42, 'Eb2': 77.78,
    'E2': 82.41, 'F2': 87.31, 'Gb2': 92.50, 'G2': 98.00,
    'Ab2': 103.83, 'A2': 110.00, 'Bb2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'Db3': 138.59, 'D3': 146.83, 'Eb3': 155.56,
    'E3': 174.81, 'F3': 174.61, 'Gb3': 185.00, 'G3': 196.00,
    'Ab3': 207.65, 'A3': 220.00, 'Bb3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'Db4': 277.18, 'D4': 293.66, 'Eb4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'Gb4': 369.99, 'G4': 392.00,
    'Ab4': 415.30, 'A4': 440.00, 'Bb4': 446.16, 'B4': 493.88,
    'C5': 523.25, 'Db5': 554.37, 'D5': 587.33, 'Eb5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'Gb5': 739.99, 'G5': 783.99,
    'Ab5': 830.61, 'A5': 880.00, 'Bb5': 932.33, 'B5': 987.77,
}

# Generates random set of coefficients to be used for Fourier Sound Synthesis
random_coeffs = []
for i in range(0, 8):
    random_coeffs.append(random.uniform(-1, 1))

fourier_coefficients = {
    'sine': [0, 1, 0, 0, 0, 0, 0, 0],
    'sawtooth': [0, 0.6366, 0, -0.2122, 0, 0.1273, 0, -0.0909],
    'trumpet': [0.1155, 0.3417, 0.1789, 0.1232, 0.0678, 0.0473, 0.0260, 0.0045, 0.0020],
    'random': random_coeffs,
}


def create_note(note_name='A4', type='sine', amp=0.5, beats=1.0, filter=None, cutoff=None, filename='defaultFilename.wav'):
    frequency = note_freqs[note_name]
    duration = beats / 2
    signal = thinkdsp.SinSignal(freq=0)

    for i in range(0, 8):
        signal += thinkdsp.SinSignal(freq=frequency * i, amp=amp * fourier_coefficients[type][i], offset=0)

    wave = signal.make_wave(duration=duration, start=0, framerate=44100)
    wave.write(filename=filename)
    audio = AudioSegment.from_wav(filename)

    print(f'Creating note {note_name} at {frequency} for {beats} beats with the synthesizer')

    if filter == 'lowPass':
        audio = audio.low_pass_filter(cutoff)
    if filter == 'highPass':
        audio = audio.high_pass_filter(cutoff)
    return audio


def create_chord(note_values=['A4, E4'], type='sine', amp=0.5, beats=1.0, filter=None, cutoff=None, filename='defaultFilename.wav'):
    note1 = []
    note2 = []
    note1.append(create_note(note_values[0], type, beats))
    note2.append(create_note(note_values[1], type, beats))
    return mix2tracks(note1, note2)


# Sample note; Writes the notes resulting wav to the specified file
trumpet = create_note(note_name='A4', type='trumpet', amp=1.0, beats=4.0, filter=None, cutoff=None,
                      filename='wav files/testtt.wav')


def create_space(track, attack=100, release=100):
    for i in range(0, len(track) - 1):
        if track[i][0:2] == track[i + 1][0:2]:
            track[i] = track[i].fade_out(duration=release)


def mix2tracks(track1, track2):
    create_space(track1, attack=50, release=50)
    create_space(track2, attack=50, release=50)
    song = AudioSegment.empty()
    for i in range(len(track1)):
        note1 = track1[i]
        note2 = track2[i]
        song += note1[:len(note1)].overlay(note2[:len(note2)])
    return song


G3_long = create_note('G3', 'sine', beats=2.0)
C4 = create_note('C4', 'sine')
C4_long = create_note('C4', 'sine', beats=2.0)
D4 = create_note('D4', 'sine')
D4_long = create_note('D4', 'sine', beats=2.0)
Eb4 = create_note('Eb4', 'sine')
Eb4_long = create_note('Eb4', 'sine', beats=2.0)
E4 = create_note('E4', 'sine')
E4_long = create_note('E4', 'sine', beats=2.0)
F4_long = create_note('F4', 'sine', beats=2.0)
Gb4 = create_note('Gb4', 'sine')
Gb4_medium = create_note('Gb4', 'sine', beats=2.0)
G4 = create_note('G4', 'sine')
G4_long = create_note('Gb4', 'sine', beats=2.0)
Ab4 = create_note('Ab4', 'sine')
A4 = create_note('A4', 'sine')
A4_long = create_note('A4', 'sine', beats=2.0)
B4 = create_note('B4', 'sine')
B4_long = create_note('B4', 'sine', beats=2.0)
C5 = create_note('C4', 'sine')
D5 = create_note('D5', 'sine')
D5_long = create_note('D5', 'sine', beats=2.0)
G5_long = create_note('G5', 'sine')

track1 = [B4, B4, B4_long, B4, B4, B4_long, B4, D5, G4, A4, B4_long, B4_long,
          C5, C5, C5, C5, C5, B4, B4, B4, B4, A4, A4, B4, A4_long, D5_long,
          B4, B4, B4_long, B4, B4, B4_long, B4, D5, G4, A4, B4_long, B4_long,
          C5, C5, C5, C5, C5, B4, B4, B4, D5, D5, C5, A4, G4_long, G5_long]
track2 = [G4, B4, D4_long, G4, B4, D4_long, G4, D5, D4, Gb4, G4_long, F4_long,
          E4, G4, Eb4, G4, D4, G4, E4, Ab4, A4, E4, C4, E4, D4_long, Gb4_medium,
          G4, B4, D4_long, G4, B4, D4_long, G4, B4, D4, Gb4, G4_long, F4_long,
          E4, G4, Eb4, G4, D4, G4, E4, Ab4, A4, E4, D4, Gb4, G4_long, G3_long]

song = mix2tracks(track1, track2)
print(type(song))
song.export('testArray.wav', format='wav')

A3_long = create_note('A3', 'trumpet', beats=2.0)
B3_long = create_note('B3', 'trumpet', beats=2.0)
D3_long = create_note('D3', 'trumpet', beats=2.0)
Db3_long = create_note('D3', 'trumpet', beats=2.0)
Db4_short = create_note('Db4', 'trumpet', beats=0.25)
Db4 = create_note('Db4', 'trumpet', beats=0.5)
D4 = create_note('D4', 'trumpet', beats=0.5)
D4_long = create_note('D4', 'trumpet', beats=2.0)
E4_short = create_note('E4', 'trumpet', beats=0.5)
E4 = create_note('E4', 'trumpet', beats=0.5)
E4_medium = create_note('E4', 'trumpet', beats=1.0)
E4_long = create_note('E4', 'trumpet', beats=3.0)
Gb4 = create_note('Gb4', 'trumpet', beats=0.5)
Gb4_short = create_note('Gb4', 'trumpet', beats=0.25)
Gb4_medium = create_note('Gb4', 'trumpet', beats=1.0)
G4_long = create_note('G4', 'trumpet', beats=1.5)
D4_Gb4_chord = create_chord(['D4', 'Gb4'], 'trumpet', amp=0.25, beats=1.0)
E4_Db4_chord = create_chord(['Db4', 'E4'], 'trumpet', beats=0.5)
E4_A4_chord = create_chord(['A4', 'E4'], 'trumpet', beats=1.0)
B4_Gb4_chord = create_chord(['B4', 'Gb4'], 'trumpet', beats=0.25)
Db4_E4_chord_short = create_chord(['Db4', 'E4'], 'trumpet', beats=0.5)

track1 = [D4, E4, Gb4_medium, D4_Gb4_chord, D4_Gb4_chord, D4, E4, Gb4_medium, D4_Gb4_chord, D4_Gb4_chord,
          D4, E4, Gb4_medium, D4_Gb4_chord, G4_long, Gb4, E4_long,
          Db4, D4, E4_medium, E4_Db4_chord, E4_Db4_chord, Db4, D4, E4_medium, E4_Db4_chord, E4_Db4_chord,
          Db4, D4, E4_A4_chord, E4_Db4_chord, B4_Gb4_chord, E4_short, Db4_short, Gb4_short, D4_long]

#track2 = [D4, E4, D3_long, Db3_long, B3_long, A3_long, D3_long, A3_long, B3_long, A3_long]

song = AudioSegment.empty()
for i in range(len(track1)):
    note1 = track1[i]
    song += note1[:len(note1)]

#song = mix2tracks(track1, track1)
song.export('Route1.wav', format='wav')
