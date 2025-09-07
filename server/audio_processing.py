import os
import numpy as np
import subprocess
import parselmouth
from parselmouth.praat import call
import librosa
from scipy.signal import lfilter, butter

############ Audio Handling Functions ############

def change_audio_format(audio_path, target_format='wav'):
    if audio_path.lower().endswith(f".{target_format}"):
        return audio_path
    
    audio_folder = os.path.dirname(audio_path)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    new_audio_path = os.path.join(audio_folder, f"{base_name}.{target_format}")

    ffmpeg_path = r'C:\Users\Asmaa\Desktop\ffmpeg_full_build\bin\ffmpeg.exe'

    result = subprocess.call([ffmpeg_path, '-i', audio_path, new_audio_path])
    if result != 0:
        print(f"Error converting audio format: {result}")
    else:
        print(f"Audio format converted successfully to {new_audio_path}")

    return new_audio_path
    

def calculate_zcr(waveform):
    # Calculer le taux de passage par zéro (ZCR)
    return sum(1 for i in range(1, len(waveform)) if waveform[i] * waveform[i-1] < 0)

def calculate_mfccs(y, sr, n_mfcc=12):
    # Calculer les coefficients cepstraux de fréquence de Mel (MFCCs)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfccs.T, axis=0)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def calculate_band_energy(y, sr, lowcut, highcut):
    # Calculer l'énergie par bande
    y_filtered = butter_bandpass_filter(y, lowcut, highcut, sr, order=6)
    energy = np.sum(y_filtered**2)
    return energy

def extract_audio_features(file_name, **kwargs):
    # Paramètres pour l'extraction des caractéristiques
    Intensity = kwargs.get("Intensity")
    meanF0 = kwargs.get("meanF0")
    stdevF0 = kwargs.get("stdevF0")
    minF0 = kwargs.get("minF0")
    maxF0 = kwargs.get("maxF0")
    f1 = kwargs.get("f1")
    f2 = kwargs.get("f2")
    f3 = kwargs.get("f3")
    f4 = kwargs.get("f4")
    number_of_pulses = kwargs.get("number_of_pulses")
    localJitter = kwargs.get("localJitter")
    localShimmer = kwargs.get("localShimmer")
    localabsoluteJitter = kwargs.get("localabsoluteJitter")
    localdbShimmer = kwargs.get("localdbShimmer")

    sound = parselmouth.Sound(file_name)
    result = []

    # Charger le fichier audio
    y, sr = librosa.load(file_name)

    # Calculer et ajouter les nouvelles caractéristiques
    if kwargs.get("ZCR"):
        zcr = calculate_zcr(y)
        result.append(zcr)

    if kwargs.get("MFCCs"):
        mfccs = calculate_mfccs(y, sr)
        result.extend(mfccs)

    if kwargs.get("BandEnergy"):
        lowcut = kwargs.get("lowcut")
        highcut = kwargs.get("highcut")
        band_energy = calculate_band_energy(y, sr, lowcut, highcut)
        result.append(band_energy)
        
    # Extraction de l'intensité
    if Intensity:
        sound_intensity = call(sound, "To Intensity", 75.0, 0.0, False)
        intensity_value = sound_intensity.get_average(0.0, 0.0)  # Intensité
        result.append(float(intensity_value))

    # Extraction des caractéristiques F0
    pitch = sound.to_pitch()
    if minF0:
        minF0_value = call(pitch, "Get minimum", 0, 0, "hertz", "Parabolic")
        result.append(float(minF0_value))

    if maxF0:
        maxF0_value = call(pitch, "Get maximum", 0, 0, "hertz", "Parabolic")
        result.append(float(maxF0_value))

    if meanF0:
        meanF0_value = call(pitch, "Get mean", 0, 0, "hertz")
        result.append(float(meanF0_value))

    if stdevF0:
        stdevF0_value = call(pitch, "Get standard deviation", 0, 0, "hertz")
        result.append(float(stdevF0_value))

    # Extraction des formants et du nombre de pulsations
    formant = sound.to_formant_burg()

    if f1:
        f1_value = call(formant, "Get mean", float(1), 0.0, 0.0, "Hertz")
        result.append(float(f1_value))

    if f2:
        f2_value = call(formant, "Get mean", float(2), 0.0, 0.0, "Hertz")
        result.append(float(f2_value))

    if f3:
        f3_value = call(formant, "Get mean", float(3), 0.0, 0.0, "Hertz")
        result.append(float(f3_value))

    if f4:
        f4_value = call(formant, "Get mean", float(4), 0.0, 0.0, "Hertz")
        result.append(float(f4_value))

    if number_of_pulses:
        pulses = parselmouth.praat.call([sound, pitch], "To PointProcess (cc)")
        number_of_pulses_value = parselmouth.praat.call(pulses, "Get number of points")
        result.append(float(number_of_pulses_value))

    # Extraction des caractéristiques de qualité
    if localJitter:
        local_jitter_value = call(pulses, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        result.append(float(local_jitter_value))

    if localShimmer:
        local_shimmer_value = call([sound, pulses], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        result.append(float(local_shimmer_value))

    if localabsoluteJitter:
        local_absolute_jitter_value = call(pulses, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        result.append(float(local_absolute_jitter_value))

    if localdbShimmer:
        local_db_shimmer_value = call([sound, pulses], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        result.append(float(local_db_shimmer_value))

    return np.array(result)


def process_audio(audio_path):
    wav_audio_path = change_audio_format(audio_path, target_format='wav')
    audio_features = extract_audio_features(wav_audio_path, Intensity=True, meanF0=True, stdevF0=True, minF0=True, maxF0=True,
                                            f1=True, f2=True, f3=True, f4=True, number_of_pulses=True,
                                            localJitter=True, localShimmer=True, localabsoluteJitter=True,
                                            localdbShimmer=True, ZCR=True, MFCCs=True, BandEnergy=True,
                                            lowcut=20.0, highcut=10000.0)
    return audio_features
