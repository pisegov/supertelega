import asyncio
import os

from dialog_filter import DialogFilter
import dotenv
from telethon import TelegramClient

from timed_dialog_archiver import TimedDialogArchiver

dotenv.load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME="session"

# telegram disconnects the account from every client
# without this system version
SYSTEM_VERSION="4.16.30-vxCUSTOM"
UPDATE_PERIOD = 5  # dialogs fetching period in seconds
MESSAGE_DISPLAY_TIME = 10  # display time of the read chat in seconds


async def main(
        telegram_client: TelegramClient,
        dialog_filter: DialogFilter,
        archiver: TimedDialogArchiver,
):

    async with telegram_client as client:

        while True:
            dialogs = dialog_filter.filter_telegram_notifications_dialog(
                await client.get_dialogs(ignore_pinned=True)
            )

            await archiver.processDialogs(dialogs)

            # wait for next update
            await asyncio.sleep(UPDATE_PERIOD)


if __name__ == "__main__":

    telegram_client = TelegramClient(
            session = SESSION_NAME,
            api_id = API_ID,
            api_hash = API_HASH,
            system_version = SYSTEM_VERSION)

    dialog_filter = DialogFilter()

    archiver = TimedDialogArchiver(
        message_display_time = MESSAGE_DISPLAY_TIME,
        dialog_filter = dialog_filter,
    )

    asyncio.run(
        main(
            telegram_client = telegram_client,
            dialog_filter = dialog_filter,
            archiver = archiver,
        )
    )
