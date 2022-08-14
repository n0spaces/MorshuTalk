from sounddevice import play

from morshutalk.morshu import Morshu
from morshutalk.cli_progress import CliProgress


def main():
    morshu = Morshu()
    progress = CliProgress()

    print("Type the text you would like Morshu to speak")
    print("Leave blank and press enter to exit")

    try:
        while True:
            text = input("> ")
            if len(text) == 0:
                exit(0)
            else:
                audio = morshu.load_text(text, progress.update_progress)
                play(audio.get_array_of_samples(), audio.frame_rate)

    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
