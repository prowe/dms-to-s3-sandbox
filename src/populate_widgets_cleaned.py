import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

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
ApplyMapping_node2 = ApplyMapping.apply(
    frame=DataCatalogtable_node1,
    mappings=[
        ("id", "int", "widget_id", "int"),
        ("name", "string", "widget_name", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

collapsed_df = ApplyMapping_node2.repartition(1)

collapsed_df.show()

glueContext.purge_table(
    database="gluedatabase-fps8tgqr4qfm",
    table_name="widgets_cleaned",
    options={
        "retentionPeriod": 0
    }
)

# Script generated for node Data Catalog table
DataCatalogtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=collapsed_df,
    database="gluedatabase-fps8tgqr4qfm",
    table_name="widgets_cleaned",
    transformation_ctx="DataCatalogtable_node3",
)

job.commit()