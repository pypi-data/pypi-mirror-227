
class AtScaleExtrasDependencyImportError(Exception):
    def __init__(self, extras_type: str, nested_error: str):
        message = (f'{nested_error}\nYou may need run pip '
                   f'install \'atscale[{extras_type}]\'')
        super().__init__(message)

class UserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class DependentMeasureException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

