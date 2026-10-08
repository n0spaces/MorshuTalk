"""
Grapheme-to-phoneme tool

This is derived from g2p_en, but with progress reporting and a different
phoneme predictor.

The phoneme predictor is basically a Python port of p5-NRL-TextToPhoneme,
which is in turn a Perl implementation of the Naval Research Laboratory
text-to-phoneme algorithm:
> Elovitz, H., Johnson, R., McHugh, A., & Shore, J. (January 21, 1976).
> Automatic Translation of English Text to Phonetics by Means of
> Letter-to-Sound Rules. NRL Report, Issue 5418, Part 7948.

g2p_en (Apache-2.0): https://github.com/Kyubyong/g2p

p5-NRL-TextToPhoneme (Unlicense): https://github.com/greg-kennedy/p5-NRL-TextToPhoneme
"""

import json
import logging
import re
import unicodedata
from builtins import str as unicode
from collections.abc import Callable
from itertools import chain
from os import path
from typing import NamedTuple

from g2p_en.g2p import (
    G2p,
    normalize_numbers,
    pos_tag,
    word_tokenize,
)

logger = logging.getLogger(__name__)


class Rule(NamedTuple):
    prev: re.Pattern[str] | None
    next: re.Pattern[str]
    length: int
    result: list[str]


def _prepare_nrl_rules() -> list[Rule]:
    """
    Prepare rules for the NRL text-to-phoneme predictor
    """

    # Character classes used by the NRL rules.
    # The NRL paper defines classes for * and $, but these are not actually used
    # by any of the rules, so they are omitted from the IEEE version.
    classes = {
        "#": "[AEIOUY]+",
        # "*": "[BCDFGHJKLMNPQRSTVWXZ]+",
        ".": "[BDVGJLMNRWZ]",
        # "$": "[BCDFGHJKLMNPQRSTVWXZ][EI]",
        "%": "(?:ER|E|ES|ED|ING|ELY)",
        "&": "(?:S|C|G|Z|X|J|CH|SH)",
        "@": "(?:T|S|R|D|L|Z|N|J|TH|CH|SH)",
        "^": "[BCDFGHJKLMNPQRSTVWXZ]",
        "+": "[EIY]",
        ":": "[BCDFGHJKLMNPQRSTVWXZ]*",
    }

    # Regex that matches first group if it is a class above, or the second group if not
    class_regex = re.compile(r"(?P<class>[#.%&@^+:])|(?P<noclass>[^#.%&@^+:]+)")
    line_regex = re.compile(r"^([#.%&@^+: A-Z']*)\[([^]]+)\]([#.%&@^+: A-Z']*)=/(.+)/$")

    rules_dir = path.join(path.dirname(__file__), "rules")

    with open(path.join(rules_dir, "eng_to_ipa.json"), "r") as f:
        eng_to_ipa: dict[str, list[str]] = json.load(f)

    rules: list[Rule] = []

    # Perl code flattens the dictionary into a list because the keys apparently aren't useful.
    # This seems kinda inefficient to possibly run through every regex for each word, but oh well!
    for line in chain(*eng_to_ipa.values()):
        # Parse a rule.
        # Split at equals and brackets into a prev, current, next, and output.
        match = line_regex.match(line)
        if match is None:
            logger.warning("Failed to match regex for rule line: %s", line)
            continue

        groups: tuple[str, str, str, str] = match.groups()  # type: ignore (i'm lazy)
        prev, current, next, result_str = groups

        # Skip the problematic punct lines (I don't think we need them)
        if current == "." or current == "?":
            continue

        # Find class characters and replace them
        # with the partial regex in the classes dict above.
        # Ex: " B#" becomes " B[AEIOUY]+"
        prev = "".join(
            [
                classes[_class] if _class else noclass
                for _class, noclass in class_regex.findall(prev)
            ]
        )

        next = "".join(
            [
                classes[_class] if _class else noclass
                for _class, noclass in class_regex.findall(next)
            ]
        )

        # result is the resulting phonemes to use for this rule.
        # Convert it to a list, and replace the representations that are not in ARPABET.
        # AX => AH (?)
        # NX => NG
        # WH => W (?)
        result = (
            result_str.replace("AX", "AH")
            .replace("NX", "NG")
            .replace("WH", "W")
            .split(" ")
        )

        rules.append(
            Rule(
                re.compile(f"{prev}$", re.IGNORECASE) if prev != "" else None,
                re.compile(f"^{current}{next}", re.IGNORECASE),
                len(current),
                result,
            )
        )

    return rules


class MorshuG2p(G2p):
    def __init__(self):
        super().__init__()
        self.cancelled = False
        self.rules = _prepare_nrl_rules()

    def cancel(self):
        self.cancelled = True

    def run_with_progress(
        self, text, callback: Callable[[int, int], None] | None = None
    ) -> list[str]:
        """
        G2p.__call__(text) but with a callback for reporting progress
        """
        self.cancelled = False

        # preprocessing
        text = unicode(text)
        text = normalize_numbers(text)
        text = "".join(
            char
            for char in unicodedata.normalize("NFD", text)
            if unicodedata.category(char) != "Mn"
        )  # Strip accents
        text = text.lower()
        text = re.sub(r"[^ a-z'.,?!\-]", "", text)
        text = text.replace("i.e.", "that is")
        text = text.replace("e.g.", "for example")

        # tokenization
        words = word_tokenize(text)
        tokens = pos_tag(words)  # tuples of (word, tag)

        step = 0
        total = len(tokens)

        # steps
        prons: list[str] = []
        for word, pos in tokens:
            if self.cancelled:
                return prons

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
            else:  # predict for oov
                pron = self.predict(word)

            prons.extend(pron)
            prons.extend([" "])

        if callback:
            callback(total, total)

        return prons[:-1]

    def predict(self, word) -> list[str]:
        """
        Overrides G2p's neural network-based phoneme predictor
        with our own NRL rule-based predictor.
        """

        prons = []
        text = f" {word} "

        i = 1
        while i < len(text) - 1:
            matched = False
            rest = text[i:]
            # We're basically matching the text at the current position
            # against a ton of regex patterns until we find one
            for rule in self.rules:
                prevmatch = rule.prev is None or rule.prev.match(text, 0, i)
                if prevmatch and rule.next.match(rest):
                    matched = True
                    prons.extend(rule.result)
                    i += rule.length
                    break
            if not matched:
                logger.warning(
                    "RULE ERROR: Failed to match at position %d in '%s'", i, text
                )
                i += 1
                # well we gotta put something here
                prons.append("UH")

        # Add stress number because our code checks G2p.phonemes to see if a phoneme is accurate.
        # We could remove the stress numbers from the G2p.phonemes, but I don't know if that has
        # any side effects (aside from breaking the neural phoneme predictor, which we don't care
        # about)
        prons = [pron + "0" if pron not in self.phonemes else pron for pron in prons]

        return prons
