#!/usr/bin/env python3
"""
Замер скорости интернета.
Последовательно выполняет N запросов к указанному URL,
измеряет время, объём данных и вычисляет среднюю скорость.
"""

import argparse
import sys
import time
from dataclasses import dataclass

import requests


@dataclass
class Attempt:
    index: int
    bytes_downloaded: int
    elapsed: float  # секунды

    @property
    def speed_mbps(self) -> float:
        """Скорость в Мбит/с (как обычно измеряют провайдеры)."""
        if self.elapsed <= 0:
            return 0.0
        return (self.bytes_downloaded * 8) / (self.elapsed * 1_000_000)

    @property
    def speed_mb_per_s(self) -> float:
        """Скорость в Мегабайтах в секунду (MB/s)."""
        if self.elapsed <= 0:
            return 0.0
        return self.bytes_downloaded / (self.elapsed * 1_000_000)


def download_once(url: str, index: int, timeout: float = 60.0) -> Attempt:
    """Один запрос с замером времени и объёма."""
    # stream=True чтобы можно было посчитать реально скачанные байты
    start = time.perf_counter()
    with requests.get(url, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        size = 0
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            size += len(chunk)
    elapsed = time.perf_counter() - start
    return Attempt(index=index, bytes_downloaded=size, elapsed=elapsed)


def format_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} TB"


def run(url: str, count: int, timeout: float) -> int:
    print(f"URL: {url}")
    print(f"Запросов: {count}")
    print("-" * 60)

    attempts: list[Attempt] = []
    for i in range(1, count + 1):
        try:
            attempt = download_once(url, i, timeout)
        except requests.RequestException as e:
            print(f"[{i:02d}/{count}] Ошибка: {e}", file=sys.stderr)
            continue

        attempts.append(attempt)
        print(
            f"[{i:02d}/{count}] "
            f"{format_bytes(attempt.bytes_downloaded):>10}  "
            f"{attempt.elapsed:6.3f} с  "
            f"{attempt.speed_mbps:8.2f} Мбит/с  "
            f"({attempt.speed_mb_per_s:6.2f} МБ/с)"
        )

    if not attempts:
        print("\nНе удалось выполнить ни одного запроса.", file=sys.stderr)
        return 1

    total_bytes = sum(a.bytes_downloaded for a in attempts)
    total_time = sum(a.elapsed for a in attempts)
    avg_time = total_time / len(attempts)
    avg_speed_mbps = (total_bytes * 8) / (total_time * 1_000_000)
    avg_speed_mb_s = total_bytes / (total_time * 1_000_000)

    print("-" * 60)
    print("ИТОГИ")
    print(f"  Успешных запросов:     {len(attempts)}/{count}")
    print(f"  Всего скачано:         {format_bytes(total_bytes)}")
    print(f"  Общее время:           {total_time:.3f} с")
    print(f"  Среднее время запроса: {avg_time:.3f} с")
    print(f"  Средняя скорость:      {avg_speed_mbps:.2f} Мбит/с "
          f"({avg_speed_mb_s:.2f} МБ/с)")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Замер скорости интернета через повторные скачивания URL."
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://speed.hetzner.de/100MB.bin",
        help="URL тяжёлого ресурса (по умолчанию тестовый файл Hetzner 100MB)",
    )
    parser.add_argument(
        "-n", "--count", type=int, default=1,
        help="Количество запросов (по умолчанию 1)",
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=60.0,
        help="Таймаут одного запроса в секундах (по умолчанию 60)",
    )
    args = parser.parse_args()

    if args.count <= 0:
        print("Количество запросов должно быть > 0", file=sys.stderr)
        return 2

    return run(args.url, args.count, args.timeout)


if __name__ == "__main__":
    sys.exit(main())