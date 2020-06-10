from commands import Command


class Shell(Command):

    DESCRIPTION = 'Run shell (using IPython if available)'

    def run(self):
        from ask.models import (User, Token, Question, Answer, Comment, Tag, Vote)
        try:
            # trying IPython if installed...
            from IPython import embed
            embed(using=False)
        except ImportError:
            # ... or python default console if not
            try:
                # optional readline interface for history if installed
                import readline  # pylint: disable=possibly-unused-variable
            except ImportError:
                pass
            import code
            variables = globals().copy()
            variables.update(locals())
            shell = code.InteractiveConsole(variables)
            shell.interact()
