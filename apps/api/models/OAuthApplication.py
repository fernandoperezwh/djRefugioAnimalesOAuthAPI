from oauth2_provider.models import AbstractApplication


class OAuthApplication(AbstractApplication):
    def allows_grant_type(self, *grant_types):
        """
        Sobreescribimos el metodo y permitimos todos los flujos de OAuth2.0.
        Con este cambio, las aplicaciones que se registren no importara si se especifica un grant type en especifico
        :param grant_types:
        :return:
        """
        return bool({self.authorization_grant_type,
                     self.GRANT_CLIENT_CREDENTIALS,
                     self.GRANT_AUTHORIZATION_CODE,
                     self.GRANT_PASSWORD,
                     self.GRANT_IMPLICIT,
                     } & set(grant_types))
