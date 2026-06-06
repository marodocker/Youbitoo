#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os


def download(url, fmt, output_dir, quality):
    os.makedirs(output_dir, exist_ok=True)

    if fmt == "mp3":
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", quality,
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url,
        ]
    else:
        cmd = [
            sys.executable, "-m", "yt_dlp",
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
    parser = argparse.ArgumentParser(description="Youbitoo")
    parser.add_argument("url")
    parser.add_argument("-f", "--format", choices=["mp4", "mp3"], default="mp4")
    parser.add_argument("-o", "--output", default=".", metavar="DIR")
    parser.add_argument("-q", "--quality", default=None, metavar="QUALITY")

    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        parser.error("the url doesnt work check if you pasted it right")

    quality = args.quality if args.quality is not None else ("0" if args.format == "mp3" else "1080")
    validate_quality(args.format, quality, parser)

    download(args.url, args.format, args.output, quality)


if __name__ == "__main__":
    main()

# Made by MaroDocker on GitHub
