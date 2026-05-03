FROM quay.io/astronomer/astro-runtime:9.1.0

USER root

RUN python -m venv /opt/dbt_venv && \
    /opt/dbt_venv/bin/pip install --upgrade pip && \
    /opt/dbt_venv/bin/pip install dbt-core==1.7.9 dbt-snowflake==1.7.1 protobuf==4.25.3


COPY requirements.txt .
RUN /opt/dbt_venv/bin/pip install -r requirements.txt

USER astro
































# FROM apache/airflow:2.9.0-python3.12

# USER root

# # Create dbt virtual environment
# RUN python -m venv /opt/dbt_venv

# # Install everything in ONE layer (important)
# RUN /opt/dbt_venv/bin/pip install --upgrade pip \
#  && /opt/dbt_venv/bin/pip install \
#     dbt-core==1.7.9 \
#     dbt-snowflake==1.7.1 \
#     protobuf==4.25.3

# # Fix permissions so astro user can use it
# RUN chown -R airflow:root /opt/dbt_venv

# USER airflow



# # FROM quay.io/astronomer/astro-runtime:12.0.0

# # USER root

# # # install dbt
# # RUN python -m venv /opt/dbt_venv \
# #  && /opt/dbt_venv/bin/pip install --upgrade pip \
# #  && /opt/dbt_venv/bin/pip install dbt-core==1.7.9 \
# #  && /opt/dbt_venv/bin/pip install protobuf==4.25.3 \
# #  && /opt/dbt_venv/bin/pip install "dbt-snowflake==1.7.1"

# # # RUN python -m venv /opt/dbt_venv && \
# # #     /opt/dbt_venv/bin/pip install \
# # #         "dbt-core==1.7.9" \
# # #         "dbt-snowflake==1.7.1"

# # RUN pip install protobuf==4.25.3

# # RUN mkdir -p /usr/local/airflow/dbt/country_dbt_project/logs && \
# #     chown -R astro:astro /usr/local/airflow/dbt

# # # copy FULL dbt project (this is what you're missing)
# # COPY dbt /usr/local/airflow/dbt

# # USER astro