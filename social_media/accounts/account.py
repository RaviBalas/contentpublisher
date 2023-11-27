class Account(object):
    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

    def generate_public_url(self, social_media_url):
        pass

    def publish_content(self, identifier, **kwargs):
        pass
