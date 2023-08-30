"""
    String ends with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class EndsWith(StringCondition):
    """
        Condition for string `self.what` ends with `value`
    """

    def _is_satisfied(self, ) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().endswith(self.delimiter + i.lower()) or i.lower() == self.what.lower():
                            return True
                    else:
                        if self.what.lower().endswith(i.lower()):
                            return True
                else:
                    if self.delimiter:
                        if self.what.endswith(self.delimiter + i) or i == self.what:
                            return True
                    else:
                        if self.what.endswith(i):
                            return True
            return False
        else:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().endswith(self.delimiter + i.lower()) or i.lower() == self.what.lower():
                            pass
                        else:
                            return False
                    else:
                        if not self.what.lower().endswith(i.lower()):
                            return False
                else:
                    if self.delimiter:
                        if self.what.endswith(self.delimiter + i) or i == self.what:
                            pass
                        else:
                            return False
                    else:
                        if not self.what.endswith(i):
                            return False
            return True


class EndsWithSchema(StringConditionSchema):
    """
        JSON schema for ends with string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return EndsWith(**data)
