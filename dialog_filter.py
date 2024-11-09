from telethon.tl.custom.dialog import Dialog
from typing import List

TELEGRAM_NOTIFICATIONS_DIALOG_ID = 777000

# filters which dialogs should be archived
class DialogFilter:

    # returns True if dialog should be archived
    def check_if_should_be_archived(self, dialog: Dialog):
       if dialog.is_channel:
           return True

       if dialog.dialog.pinned:
           return False

       if dialog.dialog.unread_mark:
           return False

       if dialog.is_user and dialog.dialog.unread_count > 0:
           return False

       if dialog.dialog.unread_mentions_count > 0:
           return False

       if dialog.dialog.unread_reactions_count > 0:
           return False

       if (not dialog.archived) and dialog.is_group:
            return False

       return True

    # removes Telegram dialog from dialog list
    # this dialog cannot be archived
    def filter_telegram_notifications_dialog(self, dialogs: List[Dialog]):
       return [dialog for dialog in dialogs if dialog.id != TELEGRAM_NOTIFICATIONS_DIALOG_ID]
