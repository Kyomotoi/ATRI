from rich.console import Console as C


class Console(C):
    def __init__(self, console: C, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = console

    def info(self, content: str, *args, **kwargs):
        text = "[blue][¡][/blue] " + content
        self.console.print(text, *args, **kwargs)

    def success(self, content: str, *args, **kwargs):
        text = "[green][√][/green] " + content
        self.console.print(text, *args, **kwargs)

    def warn(self, content: str, *args, **kwargs):
        text = "[yellow][!][/yellow] " + content
        self.console.print(text, *args, **kwargs)

    def error(self, content: str, *args, **kwargs):
        text = "[red][×][/red] " + content
        self.console.print(text, *args, **kwargs)

    def input(
        self,
        prompt: str,
        default_return=str(),
        assign_type=None,
        reject_message=str(),
        *args,
        **kwargs,
    ) -> str:
        self.console.print(f"[gray][?][/gray] [white]{prompt}[/white]")
        while True:
            text = self.console.input("> ", *args, **kwargs)
            if not text:
                self.info(f"已使用默认设置: {default_return if default_return else '空'}")
                return default_return

            if not assign_type:
                return text

            try:
                return assign_type(text)
            except Exception:
                self.warn(reject_message)
