from sounddevice import play

try:
    from morshu import Morshu
except ImportError:
    from .morshu import Morshu


def main():
    morshu = Morshu()

    print("Type the text you would like Morshu to speak")
    print("Leave blank and press enter to exit")

    try:
        while True:
            text = input("> ")
            if len(text) == 0:
                exit(0)
            else:
                audio = morshu.load_text(text)
                play(audio.get_array_of_samples(), audio.frame_rate)

    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
