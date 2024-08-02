import asyncio
import utils

from telethon.tl.custom.dialog import Dialog
from typing import List

from dialog_filter import DialogFilter


# archives or displays dialogs for a specified period of time
class TimedDialogArchiver:


    def __init__(self, message_display_time: int = 10, dialog_filter: DialogFilter = DialogFilter()) -> None:
        self.__message_display_time = message_display_time
        self.__dialog_filter = dialog_filter
        self.__dialogs_to_archive = dict()
        self.__dialogs_to_show = list[Dialog]()



    async def processDialogs(self, dialogs: List[Dialog]) -> None:
        for dialog in dialogs:
            archived = dialog.archived
            should_be_archived = self.__dialog_filter.check_if_should_be_archived(dialog)

            if archived and should_be_archived:
                continue

            if (not archived) and (not should_be_archived):
                continue

            if (not archived) and should_be_archived:
                self.__add_to_archived(dialog)
                continue

            if archived and (not should_be_archived):
                self.__add_to_showed(dialog)
                continue

        await self.__update()


    def __add_to_archived(self, dialog: Dialog):
        if dialog.id not in self.__dialogs_to_archive:
            current_date = utils.get_current_date()
            self.__dialogs_to_archive[dialog.id] = (current_date, dialog)


    def __add_to_showed(self, dialog: Dialog):
        if dialog.id in self.__dialogs_to_archive:
            del self.__dialogs_to_archive[dialog.id]
        self.__dialogs_to_show.append(dialog)


    def __get_expired_dialogs_ids(self) -> List[int]:
        current_date = utils.get_current_date()
        ids_to_archive = []
        for dialog_id, values in self.__dialogs_to_archive.items():
            date, _ = values
            duration = (current_date - date).total_seconds()

            if duration >= self.__message_display_time:
                ids_to_archive.append(dialog_id)

        return ids_to_archive


    async def __update(self):

        ids_to_archive = self.__get_expired_dialogs_ids()

        async with asyncio.TaskGroup() as tg:

            for dialog_id in ids_to_archive:
                _, dialog = self.__dialogs_to_archive.pop(dialog_id)
                tg.create_task(dialog.archive())

            for dialog in self.__dialogs_to_show:
                tg.create_task(dialog.archive(0))

        self.__dialogs_to_show.clear()
