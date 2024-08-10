from datetime import timedelta, datetime


from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src.newsapi.top_headlines import TopHeadline
from src.common.aws.s3_uploader import S3Uploader


DAG_ID = 'bronze_travel_newsapi'
TARGET_PLATFORM = "headline"
COUNTRY = "kr"
CATEGORY = "general"


# aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# task setting
def fetch_and_store():
    data = request_news_api()
    upload_to_s3(data)


def request_news_api():
    client = TopHeadline(COUNTRY, CATEGORY)
    return client.request_with_country_category()


def upload_to_s3(data):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    s3_uploader = S3Uploader()
    s3_uploader.write_s3(
        file_key=f"{DAG_ID.replace('_', '/')}/{timestamp}/{TARGET_PLATFORM}",
        data_type='json',
        data=data
    )


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description='sample dag for fetching data from kr headline from newsapi',
    schedule_interval='@daily',
):
    extract_task = PythonOperator(
        task_id="request_news_api",
        python_callable=fetch_and_store
    )

    extract_task