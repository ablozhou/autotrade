params = {"symbol": "", "limit": 100}

proxy = "http://127.0.0.1:1087"


class config(dict):
    def __init__(self, *args, **kwargs):
        """
        Create the config instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from Huobi.
            secret_key: The private key applied from Huobi.
            url: The URL name like "https://api.huobi.pro".
            init_log: Init logger, default is False, True will init logger handler
        """
        super().__init__(*args, **kwargs)

    def setBaseUrl(self, base_url: str):
        self['base_url'] = base_url

    def updateParams(self, params: dict):
        self.params.update(params)

    def setParams(self, params: dict):
        self.params = params


c = config(url="http://b.com", proxy='127.0.0.1')
# c.setDefaultUrl("http://b.com/api")

c['pproxy'] = '127.0.0.2'
print(f"{c['url']},{c['proxy']},{c.get('pproxy')}")
