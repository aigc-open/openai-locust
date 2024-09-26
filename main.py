from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from enum import Enum
import os
import pandas as pd
from loguru import logger
import time
import uvicorn

app = FastAPI()

# 加载静态文件
# app.mount("/static", StaticFiles(directory="static"), name="static")


class TagEnum(str, Enum):
    chat_completions = "chat_completions"
    completions = "completions"


class TaskRequest(BaseModel):
    input_lens: str = "1,2"
    output_lens: str = "1,2"
    user: int = 10
    rate: int = 10
    time_: str = "10s"
    tags: TagEnum = TagEnum.chat_completions  # 使用 Enum 限制 tags 的值
    remark: str = ""
    host: str = "https://easycoder.puhuacloud.com"  # 添加 host 字段
    RANDOM_STRING: bool = False


def task(INPUT_LENS: str, OUTPUT_LENS: str, user: int = 10, rate: int = 10, time_: str = "10s", tags: TagEnum = TagEnum.chat_completions, remark: str = "", host: str = "", RANDOM_STRING: bool = False):
    logger.info(f"是否随机输入字符串: {RANDOM_STRING}")
    if RANDOM_STRING:
        RANDOM_STRING = "true"
    else:
        RANDOM_STRING = ""

    # 在命令中添加 --host 参数
    os.system(f"RANDOM_STRING={RANDOM_STRING} INPUT_LENS={INPUT_LENS} OUTPUT_LENS={OUTPUT_LENS} locust -f src/job.py --host {host} --tags {tags} --headless -u {user} -r {rate} --run-time {time_} --only-summary --csv csv")

    # 读取 CSV 文件
    data = pd.read_csv(f"csv_stats.csv")
    # 处理无效值
    data = data.replace([float('inf'), float('-inf')],
                        pd.NA)  # 替换 inf 和 -inf 为 NaN
    data = data.fillna(0)  # 将 NaN 替换为 0，或使用其他合适的值
    result = data.to_dict()

    # 删除生成的 CSV 文件
    os.system(f"rm csv_*.csv")
    time.sleep(4)

    return result


@app.post("/run-task/")
async def run_task(task_request: TaskRequest):
    try:
        result = task(
            INPUT_LENS=task_request.input_lens,
            OUTPUT_LENS=task_request.output_lens,
            user=task_request.user,
            rate=task_request.rate,
            time_=task_request.time_,
            tags=task_request.tags,  # 传递 tags 参数
            remark=task_request.remark,
            host=task_request.host,  # 传递 host 参数
            RANDOM_STRING=task_request.RANDOM_STRING
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        raise HTTPException(status_code=500, detail="任务执行失败")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("templates/index.html") as f:
        return f.read()

# 运行 FastAPI 应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50000)
