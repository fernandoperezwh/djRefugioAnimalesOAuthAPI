from oauth2_provider.models import AbstractApplication


class OAuthApplication(AbstractApplication):
    def allows_grant_type(self, *grant_types):
        return bool({self.authorization_grant_type,
                     self.GRANT_CLIENT_CREDENTIALS,
                     self.GRANT_AUTHORIZATION_CODE
                     } & set(grant_types))
