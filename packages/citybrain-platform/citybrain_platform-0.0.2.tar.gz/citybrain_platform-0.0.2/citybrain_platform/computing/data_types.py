from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class ColumnType(str, Enum):
    STRING: str = "STRING"
    INT: str = "INT"
    BIGINT: str = "BIGINT"
    FLOAT: str = "FLOAT"
    DOUBLE: str = "DOUBLE"
    TIMESTAMP: str = "TIMESTAMP"

@dataclass
class Column:
    name: str
    type: ColumnType
    comment: str = ""

@dataclass
class Schema:
    name: str
    comment: str
    columns: List[dict]
    partition_columns: List[dict]
    cluster_columns: List[dict]
    create_table_sql: str

@dataclass
class TableListItem:
    name: str
    description: str

@dataclass
class AvaliableTableList:
    public: List[TableListItem]
    own: List[TableListItem]

@dataclass
class JobProgress:
    task_name: str
    total_instances: int
    running_instances: int
    terminated_instances: int
    # finished_percent: float

@dataclass
class JobSummary:
    start_time: str
    end_time: str
    job_run_time: int
    cpu_cost: int
    mem_cost: int

@dataclass
class JobStatus:
    status: str
    progress: List[JobProgress]
    summary: Optional[JobSummary] = None

