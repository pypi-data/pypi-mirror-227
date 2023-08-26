import argparse
import os
import pprint
import sys
from collections.abc import Callable
from typing import Optional

from .constants import DEEPL_AUTH_KEY, SOURCE_LANGS, TARGET_LANGS
from .core import configuration, histogram, translator


def translate(
    auth_key: str,
    text: str,
    config_file: str,
    source_lang: Optional[str],
    target_lang: Optional[str],
    count_lang: Optional[str],
    swap: bool,
    func: Callable,
    **kwargs: dict,
) -> None:
    config = configuration.Config.load(config_file)
    if not auth_key:
        auth_key = os.getenv(DEEPL_AUTH_KEY, "")
    if text == "-":
        text = sys.stdin.read()
    if not source_lang:
        source_lang = config.source_lang
    if not target_lang:
        target_lang = config.target_lang
    if not count_lang:
        count_lang = config.count_lang

    if swap:
        source_lang, target_lang = target_lang, source_lang

    result = translator.DeepLTranslator(auth_key).translate(
        text,
        config_file,
        source_lang,
        target_lang,
        count_lang,
        **kwargs,
    )
    print(f"input text({result.source_lang})")
    print(result.source_text)
    print("")

    print(f"output text({result.target_lang})")
    print(result.result_text)
    print("")


def hist(
    config_file: str, min_count: int, num_words: Optional[int], func: Callable
) -> None:
    counts = histogram.Histogram.load(configuration.Config.load(config_file)).counts
    pprint.pprint([i for i in counts.most_common(num_words) if i[1] >= min_count])


def configure(
    config_file: str,
    ignore_add: list[str],
    ignore_delete: list[str],
    min_length: Optional[int],
    source_lang: Optional[str],
    target_lang: Optional[str],
    count_lang: Optional[str],
    show: bool,
    func: Callable,
) -> None:
    configuration.update(
        config_file,
        ignore_add,
        ignore_delete,
        min_length,
        source_lang,
        target_lang,
        count_lang,
    )
    if show:
        print(configuration.Config.load(config_file).dump())


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    translate_parser = subparsers.add_parser("translate")
    translate_parser.add_argument(
        "--auth-key",
        default="",
    )
    translate_parser.add_argument(
        "--text",
        default="-",
    )
    translate_parser.add_argument(
        "--config-file",
        default="",
    )
    translate_parser.add_argument(
        "--source-lang",
        choices=SOURCE_LANGS + [lang.lower() for lang in SOURCE_LANGS],
        default=None,
    )
    translate_parser.add_argument(
        "--target-lang",
        choices=TARGET_LANGS + [lang.lower() for lang in TARGET_LANGS],
        default=None,
    )
    translate_parser.add_argument(
        "--count-lang",
        default=None,
        choices=TARGET_LANGS
        + [lang.lower() for lang in TARGET_LANGS]
        + SOURCE_LANGS
        + [lang.lower() for lang in SOURCE_LANGS],
    )
    # translate_parser.add_argument(
    #     "--split-sentences",
    #     default="1",
    #     choices=[1, 0, "nonewlines"],
    # )
    # translate_parser.add_argument(
    #     "--preserve-formatting",
    #     action="store_true",
    #     default=False,
    # )
    # translate_parser.add_argument(
    #     "--formality",
    #     default=None,
    #     choices=["less", "more"],
    # )
    translate_parser.add_argument("--swap", default=False, action="store_true")
    translate_parser.set_defaults(func=translate)

    hist_parser = subparsers.add_parser("hist")
    hist_parser.add_argument(
        "--config-file",
        default="",
    )
    hist_parser.add_argument(
        "--min-count",
        default=0,
        type=int,
    )
    hist_parser.add_argument(
        "--num-words",
        default=None,
        type=int,
    )
    hist_parser.set_defaults(func=hist)

    config_parser = subparsers.add_parser("configure")
    config_parser.add_argument("--ignore-add", default=[], nargs="+", type=str)
    config_parser.add_argument("--ignore-delete", default=[], nargs="+", type=str)
    config_parser.add_argument("--min-length", default=None, type=int)
    config_parser.add_argument(
        "--source-lang",
        default=None,
        choices=SOURCE_LANGS + [lang.lower() for lang in SOURCE_LANGS],
    )
    config_parser.add_argument(
        "--target-lang",
        default=None,
        choices=TARGET_LANGS + [lang.lower() for lang in TARGET_LANGS],
    )
    config_parser.add_argument(
        "--count-lang",
        default=None,
        choices=TARGET_LANGS
        + [lang.lower() for lang in TARGET_LANGS]
        + SOURCE_LANGS
        + [lang.lower() for lang in SOURCE_LANGS],
    )
    config_parser.add_argument("--show", default=False, action="store_true")
    config_parser.add_argument(
        "--config-file",
        default="",
    )
    config_parser.set_defaults(func=configure)

    known, unknown = parser.parse_known_args()
    known.func(**vars(known))


if __name__ == "__main__":
    main()
