class ATRIError(BaseException):
    pass


class InvalidConfigError(ATRIError):
    """配置文件有问题"""


class InvalidPluginError(ATRIError):
    """插件有问题"""


class InvalidRequestError(ATRIError):
    """网络请求有问题"""
