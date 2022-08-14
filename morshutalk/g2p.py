# This class addess progress reporting to G2p.
# The majority of this code is borrowed from G2p.__call__().
# https://www.github.com/kyubyong/g2p (Apache-2.0)
from typing import Callable

from g2p_en.g2p import *


class G2pProgress(G2p):
    def __init__(self):
        super().__init__()
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def run_with_progress(self, text, callback: Callable[[int, int], None] = None):
        self.cancelled = False

        # preprocessing
        text = unicode(text)
        text = normalize_numbers(text)
        text = ''.join(char for char in unicodedata.normalize('NFD', text)
                       if unicodedata.category(char) != 'Mn')  # Strip accents
        text = text.lower()
        text = re.sub("[^ a-z'.,?!\-]", "", text)
        text = text.replace("i.e.", "that is")
        text = text.replace("e.g.", "for example")

        # tokenization
        words = word_tokenize(text)
        tokens = pos_tag(words)  # tuples of (word, tag)

        step = 0
        total = len(tokens)

        # steps
        prons = []
        for word, pos in tokens:
            if self.cancelled:
                return

            if callback:
                callback(step, total)
                step += 1

            if re.search("[a-z]", word) is None:
                pron = [word]

            elif word in self.homograph2features:  # Check homograph
                pron1, pron2, pos1 = self.homograph2features[word]
                if pos.startswith(pos1):
                    pron = pron1
                else:
                    pron = pron2
            elif word in self.cmu:  # lookup CMU dict
                pron = self.cmu[word][0]
            else: # predict for oov
                pron = self.predict(word)

            prons.extend(pron)
            prons.extend([" "])

        if callback:
            callback(total, total)

        return prons[:-1]
