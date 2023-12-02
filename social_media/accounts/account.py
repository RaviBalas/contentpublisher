from social_media.models import Credentials, Category


class Account(object):
    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

    @staticmethod
    def get_credential_using_identifier(identifier):
        return Credentials.objects.get(identifier=identifier)

    @staticmethod
    def get_category_obj(category):
        return Category.objects.get(name=category)

    def list_of_social_media_listing(self, category, identifier, **kwargs):
        pass

    def generate_public_url(self, social_media_url):
        pass

    def publish_content(self, identifier, **kwargs):
        pass
