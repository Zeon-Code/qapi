from sqlalchemy import and_, or_

from qapi.dialect import Dialect


class NotRegisteredTable(Exception):
    pass


class SQLAlchemyDialect(Dialect):
    def __init__(self):
        self._tables = {}

    def register_table(self, table):
        self._tables[table.name] = table
    
    def translate(self, grouped_action):
        sorted_grouped_where = sorted(grouped_action.get("where", {}).values(), key=lambda actions: actions[0].index)
        sorted_grouped_order = sorted(grouped_action.get("order", {}).values(), key=lambda actions: actions[0].index)

        return {
            "where": self._translate_where(sorted_grouped_where),
            "order": self._translate_order(sorted_grouped_order)
        }

    def _translate_where(self, sorted_where):
        where_clause = []

        for actions in sorted_where:
            logical_operator = self._translate_where_logical_operator(actions)
            conditions = [self._translate_where_action(action) for action in actions]
            if logical_operator is None:
                where_clause += conditions
            else:
                where_clause.append(logical_operator(*conditions))

        return where_clause

    def _translate_order(self, sorted_order):
        return [
            self._translate_order_action(action)
            for actions in sorted_order 
            for action in actions
        ]

    def _translate_order_action(self, action):
        column = self._get_column(action)
        if action.value == "asc":
            return column.asc()
        elif action.value == "desc":
            return column.desc()

    def _translate_where_logical_operator(self, actions):
        if actions[0].logical_operator == "and":
            return and_
        elif actions[0].logical_operator == "or":
            return or_

    def _translate_where_action(self, action):
        column = self._get_column(action)
        if action.relational_operator == "eq":
            return column.__eq__(action.value)
        elif action.relational_operator == "lt":
            return column.__lt__(action.value)
        elif action.relational_operator == "lte":
            return column.__le__(action.value)
        elif action.relational_operator == "gt":
            return column.__gt__(action.value)
        elif action.relational_operator == "gte":
            return column.__ge__(action.value)
        elif action.relational_operator == "like":
            return column.like(action.value)
        elif action.relational_operator == "nlike":
            return column.notlike(action.value)
        elif action.relational_operator == "inq":
            return column.in_(action.value)

    def _get_column(self, action):
        table = self._tables.get(action.model)
        if table is None:
            raise NotRegisteredTable(action.model)
        
        column = getattr(table.c, action.property, None)
        if column is None:
            raise AttributeError(f"{action.model}.{action.property}")

        return column
