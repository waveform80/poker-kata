import re
from itertools import product, groupby
from random import shuffle
from functools import total_ordering
from operator import attrgetter


@total_ordering
class Card:
    values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    suits = {
        'S': '\N{PLAYING CARD ACE OF SPADES}',
        'H': '\N{PLAYING CARD ACE OF HEARTS}',
        'D': '\N{PLAYING CARD ACE OF DIAMONDS}',
        'C': '\N{PLAYING CARD ACE OF CLUBS}',
    }
    _regex = re.compile(r'^(?P<value>[AJQK2-9]|10)\s*(?P<suit>[HDSC])$')

    def __init__(self, s):
        match = Card._regex.match(s)
        if not match:
            raise ValueError("%s is not a valid card spec" % s)
        self._value = Card.values.index(match.group('value'))
        self._suit = match.group('suit')

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return 'Card(%r)' % (self.value + self.suit)

    def __str__(self):
        return chr(ord(Card.suits[self.suit]) + {
            # NOTE: Offset by 2 because of the "knight" card (C?!)
            10: 12, # Q
            11: 13, # K
            12: 0,  # A
        }.get(self.score, self.score + 1))

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return Card.values[self.score]

    @property
    def score(self):
        return self._value


@total_ordering
class Hand:
    values = (
        'high card',
        'pair',
        'two pair',
        'three of a kind',
        'straight',
        'flush',
        'full house',
        'four of a kind',
        'straight flush',
        'royal flush',
    )

    def __init__(self, cards):
        if isinstance(cards, Deck):
            cards = cards.deal(5)
        elif isinstance(cards, str):
            cards = [Card(s) for s in cards.split()]
        else:
            cards = [card if isinstance(card, Card) else Card(card)
                     for card in cards]
        if len(cards) != 5:
            raise ValueError('hand must consist of 5 cards')
        self._cards = sorted(cards)

    def __repr__(self):
        return 'Hand([%s])' % ', '.join(repr(card) for card in self)

    def __str__(self):
        return '%s  \N{RIGHTWARDS DOUBLE ARROW} %s' % (
            ' '.join(str(card) for card in self),
            self.hand
        )

    def __iter__(self):
        return iter(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __len__(self):
        return 5

    def __contains__(self, card):
        # NOTE: this checks *identity* rather than equality
        return any(c is card for c in self)

    def __eq__(self, other):
        return self.score == other.score and all(
            sc.score == oc.score for sc, oc in zip(self, other)
        )

    def __lt__(self, other):
        if self.score < other.score:
            return True
        elif self.score == other.score:
            for sc, oc in reversed(list(zip(self, other))):
                if sc.score < oc.score:
                    return True
                elif sc.score > oc.score:
                    break
        return False

    @property
    def hand(self):
        scores = [card.score for card in self]
        is_straight = (
            # special case: 2 3 4 5 A
            scores == [0, 1, 2, 3, 12] or
            # general case
            scores == list(range(self[0].score, self[0].score + 5))
        )
        if all(c.suit == self[0].suit for c in self[1:]):
            if scores == [8, 9, 10, 11, 12]:
                return 'royal flush'
            elif is_straight:
                return 'straight flush'
            else:
                return 'flush'
        else:
            value_runs = tuple(sorted(
                len(list(group))
                for key, group in groupby(self, attrgetter('value'))
            ))
            return {
                (1, 4): 'four of a kind',
                (2, 3): 'full house',
                (1, 1, 3): 'three of a kind',
                (1, 2, 2): 'two pair',
                (1, 1, 1, 2): 'pair',
                (1, 1, 1, 1, 1): 'straight' if is_straight else 'high card',
            }[value_runs]

    @property
    def score(self):
        return Hand.values.index(self.hand)

    def exchange(self, deck, *cards):
        # XXX Should check all cards are in self before redrawing any
        for card in cards:
            self._cards.remove(card)
            deck.discard(card)
            self._cards.append(deck.draw())
        self._cards.sort()


class Deck:
    def __init__(self):
        self._cards = [
            Card(value + suit)
            for value, suit in product(Card.values, Card.suits)
        ]
        self._discard = []
        shuffle(self._cards)

    def __repr__(self):
        return '<Deck cards=%d discard=%d>' % (
            len(self._cards), len(self._discard)
        )

    def __iter__(self):
        return iter(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __len__(self):
        return len(self._cards)

    def __contains__(self, card):
        # NOTE: this checks *identity* rather than equality (see discard())
        return any(c is card for c in self)

    def draw(self):
        try:
            return self._cards.pop()
        except IndexError:
            raise ValueError('cannot draw from empty deck')

    def deal(self, n=5):
        if len(self) < n:
            raise ValueError('insufficient cards left to deal')
        return [self.draw() for i in range(n)]

    def discard(self, card):
        assert card not in self
        self._discard.append(card)

    def reshuffle(self):
        self._cards.extend(self._discard)
        self._discard = []
        shuffle(self._cards)
