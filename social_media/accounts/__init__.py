from .instagram import Instagram
from .youtube import Youtube


class AccountManager(object):
    account_dict = {
        "instagram": Instagram(),
        "youtube": Youtube()
    }

    def __init__(self, name):
        self.account_obj = None
        if name in self.account_dict:
            self.account_obj = self.account_dict.get(name)

    @property
    def get_account_object(self):
        return self.account_obj
