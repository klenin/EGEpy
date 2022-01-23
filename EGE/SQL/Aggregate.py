class Aggregate:
    @staticmethod
    def call(self):  # abstract
        pass

class Count(Aggregate):
    @staticmethod
    def call(self):
        raise NotImplemented()

class Sum(Aggregate):
    @staticmethod
    def call(self):
        raise NotImplemented()

class Avg(Aggregate):
    @staticmethod
    def call(self):
        raise NotImplemented()

class Min(Aggregate):
    @staticmethod
    def call(self):
        raise NotImplemented()

class Max(Aggregate):
    @staticmethod
    def call(self):
        raise NotImplemented()