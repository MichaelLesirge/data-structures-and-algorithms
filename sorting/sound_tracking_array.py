from typing import Dict, Tuple, Any, Union
import numpy as np
import pygame
import pygame.sndarray
from tracking_array import TrackingArray

class SoundGenerator:
    def __init__(
        self, 
        min_freq: float = 120, 
        max_freq: float = 1200, 
        sample_rate: int = 44100, 
        duration: float = 0.05
    ) -> None:
        self.min_freq: float = min_freq
        self.max_freq: float = max_freq
        self.sample_rate: int = sample_rate
        self.duration: float = duration
        
        pygame.mixer.init(frequency=sample_rate, channels=1)
        self.sounds: Dict[float, pygame.mixer.Sound] = {}  # Cache for generated sounds
        
    def _generate_sine_wave(self, freq: float) -> np.ndarray:
        """Generate a sine wave of given frequency"""
        t: np.ndarray = np.linspace(0, self.duration, int(self.duration * self.sample_rate))
        wave: np.ndarray = np.sin(2 * np.pi * freq * t)
        # Apply fade in/out to avoid clicks
        fade: float = 0.1
        fade_len: int = int(fade * len(wave))
        wave[:fade_len] *= np.linspace(0, 1, fade_len)
        wave[-fade_len:] *= np.linspace(1, 0, fade_len)
        
        # Convert to 16-bit integer and reshape for stereo
        wave = (wave * 32767).astype(np.int16)
        # Make it 2D array for stereo (duplicate mono channel)
        wave = np.column_stack((wave, wave))
        return wave
        
    def get_sound(self, value: float, value_range: Tuple[float, float]) -> pygame.mixer.Sound:
        """Get a sound for a given value within a range"""
        # Normalize value to [0, 1]
        normalized: float = (value - value_range[0]) / (value_range[1] - value_range[0])
        # Map to frequency range (use exponential mapping for more musical results)
        freq: float = self.min_freq * np.exp(normalized * np.log(self.max_freq / self.min_freq))
        
        # Round frequency to nearest semitone for more musical sound
        freq = round(freq * 2) / 2
        
        # Cache sounds to avoid regenerating them
        if freq not in self.sounds:
            wave: np.ndarray = self._generate_sine_wave(freq)
            wave = np.ascontiguousarray(wave)
            sound = pygame.sndarray.make_sound(wave)
            self.sounds[freq] = sound
        
        return self.sounds[freq]
    
    def play_for_value(self, value: float, value_range: Tuple[float, float]) -> None:
        sound = self.get_sound(value, value_range)
        sound.play()

class SoundTrackingArray(TrackingArray):
    def __init__(self, play_sounds = True, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.sound_generator: SoundGenerator = SoundGenerator()
        self.value_range: Tuple[float, float] = (min(self), max(self))
        self.play_sounds = play_sounds
    
    def __getitem__(self, index: int | slice) -> Any:
        value = super().__getitem__(index)
        if isinstance(index, int) and self.play_sounds:
            # Play sound when reading a value
            self.sound_generator.play_for_value(value, self.value_range)
        return value
    
    def __setitem__(self, index: int | slice, value: Any) -> None:
        super().__setitem__(index, value)
        # if isinstance(index, int) and self.play_sounds:
        #     # Play sound when writing a value
        #     self.sound_generator.play_for_value(value, self.value_range)