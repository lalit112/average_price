"""
Module for getting raw sql queries
"""


class SqlQuery:
    """
    Class for handling raw sql queries
    """
    def __init__(self, origin, destination, from_date, to_date):
        """
        Instance variable initializer for clss
        :param origin: origin code or slug name
        :param destination: destination code or slug name
        :param from_date: beginning date range
        :param to_date: ending date range
        """
        self.origin = origin
        self.destination = destination
        self.from_date = from_date
        self.to_date = to_date

    def query_source_destination_format_ok(self):
        """
        Function for generating query when both source and destination are in code format
        :return: tuple of query and parameters
        """
        query = """
        "SELECT day,ROUND (AVG(price)::numeric, 2) as average_price from prices where orig_code=%(origin)s and 
        dest_code=%(destination)s and day between %(from_date)s and %(to_date)s group by day,orig_code, dest_code
        HAVING COUNT(price) >=3"
        """
        params = {'origin': self.origin, 'destination': self.destination,
                  'from_date': self.from_date, 'to_date': self.to_date}
        return query, params

    def query_origin_or_destination_as_slug_not_in_port(self, flag=False):
        """
        Function for generating sql query where slug name is not available in port class
        :param flag: for checking options for two queries
        :return: tuple of query and parameters
        """
        if flag:
            query = """
                    SELECT prices.day as day, AVG(prices.price) as average_price from prices where prices.orig_code in 
                        (
                          SELECT code from ports where parent_slug in 
                              (
                              SELECT slug from regions where parent_slug = %(origin)s
                              )
                        ) 
                        AND prices.dest_code = %(destination)s AND prices.day BETWEEN %(from_date)s AND %(to_date)s 
                        GROUP BY prices.day, prices.orig_code, prices.dest_code;
    
                    """
            params = {'origin': self.origin,
                      'destination': self.destination,
                      'from_date': self.from_date, 'to_date': self.to_date}
        else:
            query = """
                    SELECT prices.day as day, AVG(prices.price) as average_price from prices where prices.dest_code in 
                        (
                          SELECT code from ports where parent_slug in 
                              (
                              SELECT slug from regions where parent_slug = %(destination)s
                              )
                        ) 
                        AND prices.orig_code = %(origin)s AND prices.day BETWEEN %(from_date)s AND %(to_date)s 
                        GROUP BY prices.day, prices.orig_code, prices.dest_code;

                    """
            params = {'destination': self.destination,
                      'origin': self.origin,
                      'from_date': self.from_date, 'to_date': self.to_date}
        return query, params

    def query_origin_or_destination_as_slug_in_port(self, flag=False):
        """
        Function for generating queries where slug name is present in port name
        :param flag: for checking options for two queries
        :return: tuple of query and parameters
        """
        if flag:
            query = """
                            SELECT prices.day as day, AVG(prices.price) as average_price from prices where prices.orig_code in 
                                (
                                    SELECT code from ports where parent_slug = %(origin)s
                                ) 
                                AND prices.dest_code = %(destination)s AND prices.day between %(from_date)s AND %(to_date)s 
                                GROUP BY prices.day, prices.orig_code, prices.dest_code;
                            """
            params = {'origin': self.origin,
                      'destination': self.destination,
                      'from_date': self.from_date, 'to_date': self.to_date}
        else:
            query = """
                            SELECT prices.day as day, AVG(prices.price) as average_price from prices where prices.dest_code in 
                                (
                                    SELECT code from ports where parent_slug = %(destination)s
                                ) 
                                AND prices.orig_code = %(origin)s AND prices.day between %(from_date)s AND %(to_date)s 
                                GROUP BY prices.day, prices.orig_code, prices.dest_code;
                            """
            params = {'destination': self.destination,
                      'origin': self.origin,
                      'from_date': self.from_date, 'to_date': self.to_date}
        return query, params

    def query_not_origin_not_destination(self):
        """
        Function for generating query where both origin and destination are in slug form name
        :return: tuple of query and parameters
        """
        query = """
                SELECT orig_code ,dest_code, prices.day as day, AVG(prices.price) as average_price from prices 
                where prices.orig_code in 
                    (
                        SELECT code from ports where parent_slug = %(origin)s
                    ) 
                    AND prices.dest_code in 
                    (
                        SELECT code from ports where parent_slug = %(destination)s
                    ) 
                    AND prices.day BETWEEN %(from_date)s and %(to_date)s
                    GROUP BY prices.day, prices.orig_code, prices.dest_code;
                        """
        params = {'origin': self.origin, 'destination': self.destination,
                  'from_date': self.from_date, 'to_date': self.to_date}
        return query, params

    def query_not_origin_not_destination_origin_slug(self):
        """
        Function for generating query where there is slug name in both source
        and destination and origin found in port
        :return: tuple of query and parameters
        """
        query = """
                SELECT orig_code ,dest_code, prices.day as day, AVG(prices.price) as average_price from prices
                where prices.orig_code in 
                    (
                        SELECT code from ports where parent_slug = %(origin)s
                    ) 
                    AND prices.dest_code in 
                    (
                        SELECT code from ports where parent_slug in
                         (
                            SELECT slug from regions where parent_slug = %(destination)s
                         )
                    ) 
                    AND prices.day BETWEEN %(from_date)s and %(to_date)s
                    GROUP BY prices.day, prices.orig_code, prices.dest_code;
                """
        params = {'origin': self.origin, 'destination': self.destination,
                  'from_date': self.from_date, 'to_date': self.to_date}
        return query, params

    def query_not_origin_not_destination_slug(self):
        """
        Function for generating query where there is slug name in both source
         and destination and destination found
        in port
        :return: tuple of query and parameters
        """
        query = """
                SELECT orig_code ,dest_code, prices.day as day, AVG(prices.price) as average_price from prices 
                where prices.orig_code in 
                    (
                         SELECT code from ports where parent_slug in 
                            (
                                SELECT slug from regions where parent_slug = %(origin)s
                            )
                    ) 
                AND prices.dest_code in 
                    (
                        SELECT code from ports where parent_slug = %(destination)s
                    ) 
                AND prices.day BETWEEN %(from_date)s and %(to_date)s
                GROUP BY prices.day, prices.orig_code, prices.dest_code;
                """
        params = {'origin': self.origin, 'destination': self.destination,
                  'from_date': self.from_date, 'to_date': self.to_date}
        return query, params
