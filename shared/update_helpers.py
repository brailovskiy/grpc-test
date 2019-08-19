from __future__ import print_function
import time
import threading
from dialog_api import obsolete_pb2


def make_subscribe_to_onlines(id, access_hash):
    return obsolete_pb2.ObsoleteWeakUpdateCommand(
        subscribeToOnlines=obsolete_pb2.ObsoletePeersList(
            peers=[obsolete_pb2.ObsoletePeer(
                type=1,
                id=id,
                access_hash=access_hash
            )]))


def send_my_online():
    return obsolete_pb2.ObsoleteWeakUpdateCommand(
        myOnline=obsolete_pb2.ObsoleteWeakUpdateCommand.ObsoleteMyOnline(
            online=True
        )
    )


def make_subscribe_to_typing(id, access_hash):
    return obsolete_pb2.ObsoleteWeakUpdateCommand(
        subscribeToTypings=obsolete_pb2.ObsoletePeersList(
            peers=[obsolete_pb2.ObsoletePeer(
                type=1,
                id=id,
                access_hash=access_hash
            )]))


def send_my_typing(id, access_hash):
    return obsolete_pb2.ObsoleteWeakUpdateCommand(
        myTyping=obsolete_pb2.ObsoleteWeakUpdateCommand.ObsoleteMyTyping(
            peer=obsolete_pb2.ObsoletePeer(
                type=1,
                id=id,
                access_hash=access_hash
            ),
            type=1,
            start=True
        )
    )


def make_subscribe_to_weak_channel():
    return obsolete_pb2.ObsoleteWeakUpdateCommand()


def generate_messages(message):
    messages = [
        message,
        message,
        message
    ]
    for msg in messages:
        time.sleep(3)
        yield msg


class UpdateHelpers:
    def __init__(self):
        d = threading.Thread(name='daemon', target=self.weak_updates_helper)
        d.setDaemon(True)
        d.start()

    @staticmethod
    def weak_updates_helper(stub, message):
        responses = stub.WeakUpdates(generate_messages(message))
        return responses

    @staticmethod
    def check_update_message(update):
        if update.WhichOneof('update') == 'updateMessage':
            return update.updateMessage
