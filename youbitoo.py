#!/usr/bin/env python3
import argparse
import subprocess
import sys
import shutil
import os


def check_dependency():
    if shutil.which("yt-dlp") is None:
        print("yt-dlp is not installed run pip install yt-dlp")
        sys.exit(1)


def download(url, fmt, output_dir, quality):
    os.makedirs(output_dir, exist_ok=True)

    if fmt == "mp3":
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", quality,
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url,
        ]
    else:
        cmd = [
            "yt-dlp",
            "-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            "--merge-output-format", "mp4",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url,
        ]

    print(f"Grabbing {fmt.upper()} from: {url}\n")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\nsomething went wrong check the url and try again")
        sys.exit(1)

    print("\nall done")


def validate_quality(fmt, quality, parser):
    if fmt == "mp4" and not quality.isdigit():
        parser.error("mp4 quality should be a number like 720 or 1080")
    if fmt == "mp3" and (not quality.isdigit() or not 0 <= int(quality) <= 9):
        parser.error("mp3 quality should be a number from 0 to 9 where 0 is best")


def main():
    parser = argparse.ArgumentParser(
        description="Youbitoo — Download YouTube videos or audio from the terminal.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-f", "--format",
        choices=["mp4", "mp3"],
        default="mp4",
        help="Output format (default: mp4)",
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        metavar="DIR",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "-q", "--quality",
        default=None,
        metavar="QUALITY",
        help=(
            "Quality setting:\n"
            "  mp4: max resolution, e.g. 1080, 720, 480 (default: 1080)\n"
            "  mp3: audio quality 0-9, 0=best (default: 0)"
        ),
    )

    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        parser.error("the url doesnt work check if you pasted it right")

    check_dependency()

    quality = args.quality if args.quality is not None else ("0" if args.format == "mp3" else "1080")
    validate_quality(args.format, quality, parser)

    download(args.url, args.format, args.output, quality)


if __name__ == "__main__":
    main()

# Made by MaroDocker on GitHub
