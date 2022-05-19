from ops import Ops


class MessageReciever:
    """ Handles operator selection """

    async def do_handle_message(self, message, ops: Ops):
        if message.content.startswith('..en'):
            await ops.do_enhance(message)

        if message.content.startswith('..df'):
            await ops.do_df(message)

        if message.content.startswith('..mag'):
            await ops.do_magik(message)

        if message.content.startswith('..haah'):
            await ops.do_haah(message)

        if message.content.startswith('..waaw'):
            await ops.do_waaw(message)

        if message.content.startswith('..mock'):
            await ops.do_mock(message)

        if message.content.startswith('..tecc'):
            await ops.do_tecc_tip(message)

        if message.content.startswith('..yoi'):
            await ops.do_yoi(message)

        if message.content.startswith('..loud'):
            await ops.do_loud(message)

        if message.content.startswith('..prune'):
            await ops.do_prune(message)
