from collections.abc import Iterator


class SequenceIterator(Iterator):
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __next__(self):
        if self._index < len(self._sequence):
            square = self._sequence[self._index] ** 2
            self._index += 1
            return square
        else:
            raise StopIteration


class FibonacciIterator:
    def __init__(self):
        self._index = 0
        self._current = 0
        self._next = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        self._index += 1
        fib_number = self._current
        self._current, self._next = (
            self._next,
            self._current + self._next,
        )
        return fib_number


def sequence_generator(sequence):
    for item in sequence:
        yield item
