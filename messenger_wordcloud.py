"""Word cloud of everything you have ever written on Messenger.

Reads every conversation in a facebook data export (JSON format) and draws
the most used words.
"""
import argparse

from wordcloud import WordCloud

from common import find_message_files, load_messenger_text, load_stopwords


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", help="facebook export folder, messages/inbox folder or a single message_*.json")
    parser.add_argument("--out", default="wordclouds/messenger_all.png")
    parser.add_argument("--colormap", default="viridis", help="any matplotlib colormap")
    parser.add_argument("--background", default="#040916")
    parser.add_argument("--max-words", type=int, default=350)
    parser.add_argument("--width", type=int, default=400)
    parser.add_argument("--height", type=int, default=200)
    parser.add_argument("--scale", type=float, default=3, help="output resolution multiplier")
    args = parser.parse_args()

    paths = find_message_files(args.export)
    print("reading", len(paths), "conversation files")
    text = load_messenger_text(paths)

    wordcloud = WordCloud(
        max_words=args.max_words,
        width=args.width,
        height=args.height,
        scale=args.scale,
        stopwords=load_stopwords(),
        background_color=args.background,
        colormap=args.colormap,
        collocation_threshold=30,
        min_font_size=8,
        font_step=1,
    ).generate(text)

    wordcloud.to_file(args.out)
    print("saved", args.out)


if __name__ == "__main__":
    main()
