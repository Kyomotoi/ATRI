import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_code_runner(app: App):
    from ATRI.plugins.code_runner import code_runner

    Message = make_fake_message()

    async with app.test_matcher(code_runner) as ctx:
        bot = ctx.create_bot()

        msg = Message("/code")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请键入 /code.help 以获取帮助~！", True)

    async with app.test_matcher(code_runner) as ctx:
        bot = ctx.create_bot()

        msg = Message("/code.help")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            /code {语言}
            {代码}
            For example:
            /code python
            print('hello world')
            """.strip(),
            True,
        )

    async with app.test_matcher(code_runner) as ctx:
        bot = ctx.create_bot()

        msg = Message("/code.list")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            咱现在支持的语言如下：
            assembly, bash, c, clojure,
            coffeescript, cpp, csharp,
            erlang, fsharp, go, groovy,
            haskell, java, javascript,
            julia, kotlin, lua, perl,
            php, python, ruby, rust,
            scala, swift, typescript
            """.strip(),
            True,
        )

    async with app.test_matcher(code_runner) as ctx:
        bot = ctx.create_bot()

        msg = Message(
            """
            /code python
            print("hello world")
            """
        )
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "stdout:\nhello world", True)
