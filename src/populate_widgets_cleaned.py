import sys
from awsglue.transforms import *
from awsglue import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Data Catalog table
DataCatalogtable_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="gluedatabase-fps8tgqr4qfm",
    table_name="widgets",
    transformation_ctx="DataCatalogtable_node1",
)

# Script generated for node ApplyMapping
mapped_to_target = ApplyMapping.apply(
    frame=DataCatalogtable_node1,
    mappings=[
        ("id", "int", "widget_id", "int"),
        ("name", "string", "widget_name", "string"),
        ("__tx_timestamp", "string", "__tx_timestamp", "string"),
        ("op", "string", "op", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)


most_recent_window_spec = Window.partitionBy("widget_id").orderBy(col("__tx_timestamp").desc())
de_duplicated = DynamicFrame.fromDF(
    mapped_to_target.toDF().withColumn("rn", row_number().over(most_recent_window_spec)).where("rn = 1 and op != 'D'").drop("rn"),
    glueContext
)

glueContext.purge_table(
    database="gluedatabase-fps8tgqr4qfm",
    table_name="widgets_cleaned",
    options={
        "retentionPeriod": 0
    }
)

# Script generated for node Data Catalog table
DataCatalogtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=de_duplicated,
    database="gluedatabase-fps8tgqr4qfm",
    table_name="widgets_cleaned",
    transformation_ctx="DataCatalogtable_node3",
)

job.commit()