#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# only instance variables. Composed property will have access to all
# these variables.
@extendable
class ExampleClass:
    def __init__(self):
        self.public = 42
        self._hidden = 43
        self.__private = 44


# Then we create a class which contains different types of methods that will be
# transferred as a part of the class above. Note that ExampleTrait requires target
# object to contain instance variables, thus it won't work as a stand-alone object.
class ExampleTrait:
    @property
    def trait_property(self):
        return self.public, self._hidden, self.__private

    @trait_property.setter
    def trait_property(self, new_value):
        self.public, self._hidden, self.__private = new_value

    @trait_property.deleter
    def trait_property(self):
        self.public, self._hidden, self.__private = (42, 43, 44)


# Then add the property as a part of our new class simply by referring it.
example_instance = ExampleClass()
example_instance.add_traits(ExampleTrait.trait_property)


# Here are the proofs that composed property works as part of new class.
assert example_instance.trait_property == (42, 43, 44),\
    "Cherry-picked property not working in instance!"

# We also demonstrate that we can alter the values through the property
example_instance.trait_property = (142, 143, 144)
assert example_instance.trait_property == (142, 143, 144),\
    "Cherry-picked property's setter not working in instance!"

# Finally, we can delete property's content
del example_instance.trait_property
assert example_instance.trait_property == (42, 43, 44),\
    "Cherry-picked property's deleter not working in instance!"

# And finally, original class is still unaffected.
assert not hasattr(ExampleClass, "trait_property"),\
    "Cherry-picked property has leaked into class!"
