from os import path
import numpy as np
import random
import warnings
from pydub import AudioSegment
from g2p_en import G2p
from typing import List, Union, Tuple

g2p = G2p()

morshu_wav_fp = path.join(path.dirname(__file__), 'morshu.wav')
morshu_wav = AudioSegment.from_wav(morshu_wav_fp)

# Record that contains each recognizable phoneme in the morshu audio file,
# along with the time that phoneme ends in milliseconds.
morshu_rec = np.rec.array(
    [
        # typos in comments are intentional
        ('', 160), ('L', 250), ('AE', 348), ('M', 420), ('P', 510), ('OY', 700), ('L', 835), ('', 1090),  # lamp oil
        ('R', 1180), ('OW', 1300), ('', 1390), ('P', 1490), ('', 1850),  # rope
        ('B', 1895), ('AA', 2090), ('M', 2235), ('Z', 2390), ('', 2780), ('Y', 2840), ('UW', 2960),  # bombs you
        ('W', 3030), ('AA', 3110), ('N', 3150), ('IH', 3240), ('T', 3370), ('', 3810),  # won it
        ('IH', 3960), ('T', 4070), ('Y', 4260), ('UH', 4400), ('R', 4510), ('Z', 4600),  # it yours
        ('M', 4675), ('AY', 4810), ('', 4885),  # my
        ('F', 4930), ('R', 4980), ('EH', 5100), ('N', 5240), ('D', 5300), ('', 5520),  # friend
        ('AE', 5630), ('Z', 5740), ('L', 5870), ('AO', 6000), ('NG', 6140), ('AE', 6170), ('Z', 6265),  # as long as
        ('Y', 6300), ('UW', 6380), ('HH', 6450), ('AE', 6510), ('V', 6580),  # you have
        ('IH', 6640), ('N', 6670), ('AH', 6747), ('F', 6855),  # enough
        ('R', 6960), ('UW', 7060), ('B', 7170), ('IY', 7340), ('Z', 7520), ('', 8236),  # rubies

        ('S', 8407), ('AA', 8495), ('R', 8570), ('IY', 8630),  # sorry
        ('L', 8740), ('IH', 8811), ('NG', 8942), ('K', 9014), ('', 9251),  # link
        ('AY', 9384), ('', 9467), ('K', 9512), ('AE', 9640), ('N', 9716), ('', 9844),  # i can
        ('G', 9894), ('IH', 9985), ('V', 10060), ('', 10149),  # give
        ('K', 10256), ('R', 10297), ('EH', 10383), ('IH', 10482), ('', 10564), ('T', 10617),  # cre-it
        ('', 10962), ('K', 11019), ('AH', 11100), ('M', 11229), ('B', 11246), ('AE', 11369),  # come ba-
        ('', 11511), ('W', 11590), ('EH', 11622), ('N', 11705),  # when
        ('Y', 11755), ('UH', 11808), ('R', 11864), ('AH', 11959),  # you're a
        ('L', 12095), ('IH', 12202), ('L', 12386),  # lil
        ('', 12596), ('M', 12748), ('M', 12888), ('M', 13037), ('M', 13196), ('', 13426),  # MMMMMMMMMMMMMM
        ('R', 13494), ('IH', 13589), ('', 13632), ('CH', 13773), ('ER', 13991), ('', 13992)  # richer
    ], names=('phoneme', 'timing'))

# substitutes to phonemes that morshu doesn't say (some of these are tentative
similar_phonemes = {
    'AW': ['AE', 'UW'],
    'DH': ['D'],
    'EY': ['EH', 'IY'],
    'JH': ['CH'],
    'SH': ['CH'],
    'TH': ['D'],
    'ZH': ['CH'],
}


class Morshu:
    def __init__(self):
        self.input_str = ""
        self.input_phonemes = []

        self.space_length = 20
        self.stop_length = 100

        self.out_audio = AudioSegment.empty()

        # TODO: output more data with audio segment

    def load_text(self, text: str = None) -> AudioSegment:
        if text is not None:
            self.input_str = text
        text = self.input_str.replace('\n', ',,,')

        phonemes = g2p(text)
        segments = []
        phoneme_segment = []
        while len(phonemes) > 0:
            p = phonemes.pop(0)
            if p in g2p.phonemes:
                phoneme_segment.append(p)
            if p not in g2p.phonemes or len(phonemes) == 0:
                segments.append(self.get_best_morshu_phoneme_segment(phoneme_segment))
                phoneme_segment = []
            if p == ' ':
                segments.append(AudioSegment.silent(self.space_length))
            elif p in '.,?!:;()':
                segments.append(AudioSegment.silent(self.stop_length))

        full = AudioSegment.empty().set_frame_rate(morshu_wav.frame_rate)
        for segment in segments:
            full += segment

        if len(full) == 0:
            warnings.warn('returned audio segment is empty', UserWarning)

        self.out_audio = full
        return full

    @staticmethod
    def substitute_similar_phonemes(phonemes: List[str]):
        i = 0
        while i < len(phonemes):
            # remove emphasis number
            if phonemes[i].endswith('0') or phonemes[i].endswith('1') or phonemes[i].endswith('2'):
                phonemes[i] = phonemes[i][:len(phonemes[i]) - 1]

            if phonemes[i] in similar_phonemes.keys():
                phonemes = phonemes[0:i] + similar_phonemes[phonemes[i]] + phonemes[i + 1:]
            i += 1
        return phonemes

    @staticmethod
    def get_morshu_phoneme(phoneme: str, random_choice=True) -> Union[AudioSegment, None]:
        phoneme = phoneme.upper()
        phoneme_indices = np.where(morshu_rec['phoneme'] == phoneme)[0]

        if len(phoneme_indices) == 0:
            return None

        if len(phoneme_indices) == 1 or not random_choice:
            index = phoneme_indices[0]
        else:
            index = random.choice(phoneme_indices)

        segment = morshu_wav[morshu_rec['timing'][index - 1]: morshu_rec['timing'][index]]
        return segment

    @staticmethod
    def get_phoneme_sequence_occurrences(phonemes: List[str]) -> List[Tuple[int, int]]:
        occurrences = []
        for i in range(len(morshu_rec) - len(phonemes)):
            if (morshu_rec['phoneme'][i:i + len(phonemes)] == phonemes).all():
                start = morshu_rec['timing'][i - 1]
                end = morshu_rec['timing'][i + len(phonemes) - 1]
                occurrences.append((start, end))
        return occurrences

    @staticmethod
    def get_best_morshu_single_phoneme(phoneme: str, preceding: str = "", succeeding: str = ""):
        # list of phoneme indices of the highest priority
        best_indices = []
        phoneme_indices = np.where(morshu_rec['phoneme'] == phoneme)[0]
        if len(phoneme_indices) == 0:
            return None

        highest_priority = 0
        for i in phoneme_indices:
            # priorities for preceding and succeeding phonemes:
            # exact match: 10
            # compared phonemes both contain vowels: 1
            # no match: 0
            priority = 0

            # check preceding phonemes
            morshu_preceding = morshu_rec['phoneme'][i - 1]
            if morshu_preceding == preceding:
                priority += 10
            # check both phonemes for any vowel
            elif any(c in morshu_preceding for c in "AEIOU") and any(c in preceding for c in "AEIOU"):
                priority += 1

            # check succeeding phonemes
            morshu_succeeding = morshu_rec['phoneme'][i + 1]
            if morshu_succeeding == succeeding:
                priority += 10
            # check both phonemes for any vowel
            elif any(c in morshu_succeeding for c in "AEIOU") and any(c in succeeding for c in "AEIOU"):
                priority += 1

            if priority < highest_priority:
                continue
            if priority > highest_priority:
                highest_priority = priority
                best_indices = []
            best_indices.append(i)

        index = random.choice(best_indices)
        segment = morshu_wav[morshu_rec['timing'][index - 1]: morshu_rec['timing'][index]]
        return segment

    @staticmethod
    def get_best_morshu_phoneme_segment(phonemes: List[str]):
        phonemes = Morshu.substitute_similar_phonemes(phonemes)
        if len(phonemes) == 1:
            return Morshu.get_best_morshu_single_phoneme(phonemes[0])

        # preceding and succeeding phonemes are used if we need to search for a single phoneme
        preceding = ""

        full_segment = AudioSegment.empty()
        while len(phonemes) > 0:
            sequence_length = 1
            segment = AudioSegment.empty()

            while sequence_length <= len(phonemes):
                occurrences = Morshu.get_phoneme_sequence_occurrences(phonemes[:sequence_length])
                if len(occurrences) == 0:
                    break
                start, end = random.choice(occurrences)
                segment = morshu_wav[start:end]
                sequence_length += 1
            sequence_length -= 1

            # find the best single phoneme if a longer segment wasn't found
            if sequence_length == 1:
                if sequence_length + 1 < len(phonemes):
                    succeeding = phonemes[sequence_length + 1]
                else:
                    succeeding = ""
                segment = Morshu.get_best_morshu_single_phoneme(phonemes[0], preceding, succeeding)

            full_segment += segment
            preceding = phonemes[sequence_length - 1]
            del phonemes[:sequence_length]

        return full_segment
