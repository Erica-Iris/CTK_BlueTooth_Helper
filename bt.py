import argparse
import asyncio
import structlog
from bleak import BleakScanner


log = structlog.get_logger()


async def main(args: argparse.Namespace):
    log.info("Scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        log.info(d)
        log.info("-" * len(str(d)))
        log.info(a)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
