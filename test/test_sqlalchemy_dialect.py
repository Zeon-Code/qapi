from unittest import TestCase

from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.dialects import mysql

from dialect import SQLAlchemyDialect, NotRegisteredTable
from action import WhereAction, OrderAction, ActionGroup


user = Table(
    "user",
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False)
)


class SQLAlchemyTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dialect = SQLAlchemyDialect()
        cls.dialect.register_table(user)

    def setUp(self):
        self.grouped_action = ActionGroup()

    def test_raise_NotRegisteredTable(self):
        where_action = WhereAction(["[country.name]", "Brazil"])
        self.grouped_action.add(where_action)

        self.assertRaises(NotRegisteredTable, self.dialect.translate, self.grouped_action.actions)

    def test_raise_AttributeError(self):
        where_action = WhereAction(["[user.mobile_number]", "Brazil"])
        self.grouped_action.add(where_action)

        self.assertRaises(AttributeError, self.dialect.translate, self.grouped_action.actions)

    def test_order_action(self):
        order_action = OrderAction(["[0]", "user.id asc"])
        self.grouped_action.add(order_action)

        self.assertEqual({"where": [], "order": ["user.id ASC"]}, self._translate())

    def test_where_action_operator_eq(self):
        where_action = WhereAction(["[user.name]", "[eq]", "Igor"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name = 'Igor'"], "order": []}, self._translate())

    def test_where_action_operator_lt(self):
        where_action = WhereAction(["[user.name]", "[lt]", "Igor"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name < 'Igor'"], "order": []}, self._translate())

    def test_where_action_operator_lte(self):
        where_action = WhereAction(["[user.name]", "[lte]", "Igor"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name <= 'Igor'"], "order": []}, self._translate())

    def test_where_action_operator_gt(self):
        where_action = WhereAction(["[user.name]", "[gt]", "Igor"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name > 'Igor'"], "order": []}, self._translate())

    def test_where_action_operator_gte(self):
        where_action = WhereAction(["[user.name]", "[gte]", "Igor"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name >= 'Igor'"], "order": []}, self._translate())

    def test_where_action_operator_inq(self):
        """Assemble inq operator"""
        where_action = WhereAction(["[user.name]", "[inq]", ["Igor", "Fernando"]])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name IN ('Igor', 'Fernando')"], "order": []}, self._translate())

    def test_where_action_operator_like(self):
        where_action = WhereAction(["[user.name]", "[like]", "%Igor%"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name LIKE '%%Igor%%'"], "order": []}, self._translate())

    def test_where_action_operator_nlike(self):
        where_action = WhereAction(["[user.name]", "[nlike]", "%Igor%"])
        self.grouped_action.add(where_action)

        self.assertEqual({"where": ["user.name NOT LIKE '%%Igor%%'"], "order": []}, self._translate())

    def test_where_action_logical_operator_and(self):
        where_action1 = WhereAction(["[and]", "[0]", "[user.name]", "Igor"])
        where_action2 = WhereAction(["[and]", "[0]", "[user.email]", "igor@email.com"])
        self.grouped_action.add(where_action1)
        self.grouped_action.add(where_action2)

        self.assertEqual({"where": ["user.name = 'Igor' AND user.email = 'igor@email.com'"], "order": []}, self._translate())

    def test_where_action_logical_operator_or(self):
        where_action1 = WhereAction(["[or]", "[0]", "[user.name]", "Igor"])
        where_action2 = WhereAction(["[or]", "[0]", "[user.name]", "Fernando"])
        self.grouped_action.add(where_action1)
        self.grouped_action.add(where_action2)

        self.assertEqual({"where": ["user.name = 'Igor' OR user.name = 'Fernando'"], "order": []}, self._translate())

    def test_where_action_logical_operator_or(self):
        where_action1 = WhereAction(["[or]", "[0]", "[user.name]", "Igor"])
        where_action2 = WhereAction(["[or]", "[0]", "[user.name]", "Fernando"])
        self.grouped_action.add(where_action1)
        self.grouped_action.add(where_action2)

        self.assertEqual({"where": ["user.name = 'Igor' OR user.name = 'Fernando'"], "order": []}, self._translate())

    def test_sort_where_action(self):
        where_action1 = WhereAction(["[and]", "[1]", "[user.name]", "Igor"])
        where_action2 = WhereAction(["[and]", "[1]", "[user.email]", "igor@email.com"])
        where_action3 = WhereAction(["[and]", "[0]", "[user.name]", "Fernando"])
        where_action4 = WhereAction(["[and]", "[0]", "[user.email]", "fernando@email.com"])
        self.grouped_action.add(where_action1)
        self.grouped_action.add(where_action2)
        self.grouped_action.add(where_action3)
        self.grouped_action.add(where_action4)

        self.assertEqual({
            "where": [
                "user.name = 'Fernando' AND user.email = 'fernando@email.com'", 
                "user.name = 'Igor' AND user.email = 'igor@email.com'"
            ], 
            "order": []
        }, self._translate())

    def test_sort_order_action(self):
        order_action1 = OrderAction(["[3]", "user.name asc"])
        order_action2 = OrderAction(["[0]", "user.email desc"])
        order_action3 = OrderAction(["[1]", "user.id asc"])
        self.grouped_action.add(order_action1)
        self.grouped_action.add(order_action2)
        self.grouped_action.add(order_action3)

        self.assertEqual({"where": [], "order": ["user.email DESC", "user.id ASC", "user.name ASC"]}, self._translate())

    def _translate(self):
        sql_expressions = self.dialect.translate(self.grouped_action.actions)

        return {
            "where": [self._render_expression(expression) for expression in sql_expressions["where"]],
            "order": [self._render_expression(expression) for expression in sql_expressions["order"]]
        }

    def _render_expression(self, expression):
        return str(
            expression.compile(
                dialect=mysql.dialect(),
                compile_kwargs={"literal_binds": True}
            )
        )
