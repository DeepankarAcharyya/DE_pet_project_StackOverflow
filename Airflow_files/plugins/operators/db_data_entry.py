from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PostgresqlDataEntryOperator(BaseOperator):
    """ Operator to load data from the csv files into the database table."""

    ui_color = '#358140'

    COPY_SQL = """
        COPY {}({})
        FROM '{}'
        DELIMITER ','
        CSV HEADER;
    """

    @apply_defaults
    def __init__(self,
                 table_name,
                 col_list,
                 ptask_id,
                 *args, **kwargs):
        
        """
        Operator to load data from the csv files into the database table.

        Args:
            table_name : name of the table
            col_list : colum list for the table
            task_id : task_id of the prev task to retrieve the csv file path
        """
        super(PostgresqlDataEntryOperator, self).__init__(*args, **kwargs)
        
        # Mapping the params here
        self.table_name = table_name
        self.col_list = ','.join(col_list)
        self.ptask_id = ptask_id
       

    def execute(self,**kwargs):
        self.log.info("Copying data from S3 to Redshift: STARTING")
        postgresql_hook = PostgresHook(self.postgresql_conn_id)
        
        ti = kwargs['ti']
        csv = ti.xcom_pull(task_ids=self.ptask_id)[0]

        sql_statement = self.COPY_SQL.format(
            self.table_name, 
            self.col_list, 
            csv
            )

        postgresql_hook.run(sql_statement)
        self.log.info("Copying data from CSV to PostgreSQL DB: DONE")

