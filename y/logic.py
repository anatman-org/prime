class Proposition:
    def __len__(self):
        """Return the number of propositions, connectors"""
        pass

    def __pos__(self):
        """Implements behavior for unary positive"""
        pass

    def __sub__(self, other):
        """Implements behavior for math.ceil()"""
        pass

    def __neg__(self):
        """Implements behavior for negation"""
        pass

    def __and__(self, other):
        """Implements bitwise and using the & operator."""
        pass

    def __or__(self, other):
        """Implements bitwise or using the | operator."""
        pass

    def __rshift__(self, other):
        """Implements right bitwise shift using the >> operator."""
        pass

    def __add__(self, other):
        """Implements behavior for math.trunc()"""
        pass

    def __mul__(self, other):
        """Implements behavior for math.floor()"""
        pass

    def __floordiv__(self, other):
        """Implements behavior for the built-in round()"""
        pass

    def __div__(self, other):
        """Implements behavior for inversion using the ~ operator."""
        pass

    def __truediv__(self, other):
        """Implements behavior for the built-in abs()"""
        pass

    def __mod__(self, other):
        """Implements behavior for negation"""
        pass

    def __divmod__(self, other):
        """Implements behavior for unary positive"""
        pass

    def __pow__(self, other):
        """Implements behavior for exponents using the ** operator."""
        pass

    def __lshift__(self, other):
        """Implements left bitwise shift using the << operator."""
        pass

    def __xor__(self, other):
        """Implements bitwise xor using the ^ operator."""
        pass

    def __trunc__(self):
        """Implements behavior for math.trunc()"""
        pass

    def __ceil__(self):
        """Implements behavior for math.ceil()"""
        pass

    def __floor__(self):
        """Implements behavior for math.floor()"""
        pass

    def __round__(self, n):
        """Implements behavior for the built-in round()"""
        pass

    def __invert__(self):
        """Implements behavior for inversion using the ~ operator."""
        pass

    def __abs__(self):
        """Implements behavior for the built-in abs()"""
        pass

    def __eq__(self, other):
        """Defines behavior for the equality operator, ==."""
        pass

    def __ne__(self, other):
        """Defines behavior for the inequality operator, !=."""
        pass

    def __lt__(self, other):
        """Defines behavior for the less-than operator, <."""
        pass

    def __gt__(self, other):
        """Defines behavior for the greater-than operator, >."""
        pass

    def __le__(self, other):
        """Defines behavior for the less-than-or-equal-to operator, <=."""
        pass

    def __ge__(self, other):
        """Defines behavior for the greater-than-or-equal-to operator, >=."""
        pass

    def __str__(self):
        """Defines behavior for when str() is called on an instance of your class."""
        pass

    def __repr__(self):
        """To get called by built-int repr() method to return a machine readable representation of a type."""
        pass

    def __unicode__(self):
        """This method to return an unicode string of a type."""
        pass

    def __format__(self, formatstr):
        """return a new style of string."""
        pass

    def __hash__(self):
        """It has to return an integer, and its result is used for quick key comparison in dictionaries."""
        pass

    def __nonzero__(self):
        """Defines behavior for when bool() is called on an instance of your class."""
        pass

    def __dir__(self):
        """This method to return a list of attributes of a class."""
        pass

    def __sizeof__(self):
        """It return the size of the object."""
        pass
