import sortedcontainers.sortedset


class HMessage:
    """ Message history data element """

    def __init__(self, message_id, date):
        self.message_id = message_id
        self.date = date


class HistoryData:
    """ Message history data """

    def __init__(self, clock, start_clock, messages, further=None):
        self.clock = clock
        self.start_clock = start_clock
        self.messages = sortedcontainers.SortedSet(messages, lambda x: -x.date)
        self.further = further

    def is_solid(self):
        return self.further is None

    def count_after(self, _from):
        if self.is_solid():
            cnt = 0
            for m in self.messages:
                cnt += (1 if _from < m.date else 0)
            return cnt
        else:
            return -1

    def slice(self, from_date, to_date):
        further = self.further.slice(from_date, to_date) if self.further else None

        if from_date > self.clock:
            return further if further else HistoryData(to_date, from_date, [])
        else:
            return HistoryData(
                clock=min(self.clock, to_date),
                start_clock=max(self.start_clock, from_date),
                messages=[m for m in self.messages if m.date >= from_date and m.date <= to_date],
                further=further
            )


class HistoryDataOps:
    """ History data ops """

    @staticmethod
    def merge(a, b):
        (first, second) = (b, a) if a.clock > b.clock else (a, b)

        if first.clock >= second.start_clock:
            if first.start_clock >= second.start_clock:
                return second
            else:
                visible = HistoryData(
                    clock=second.clock,
                    start_clock=first.start_clock,
                    messages=first.messages | second.messages
                )

                further = None
                if first.further and second.further:
                    further = HistoryDataOps.merge(first.further, second.further)
                elif first.further and not second.further:
                    further = first.further
                elif not first.further and second.further:
                    further = second.further

                return HistoryDataOps.merge(visible, further) if further else visible
        else:
            # further

            return HistoryData(
                clock=first.clock,
                start_clock=first.start_clock,
                messages=first.messages | second.messages,
                further=HistoryDataOps.merge(first.further, second) if first.further else second
            )
