import os
import pandas as pd

def task(INPUT_LENS:str, OUTPUT_LENS:str, user:int=10, rate:int=10, time:str="10s", tags="base", remark=""):
    os.system(f"INPUT_LENS={INPUT_LENS} OUTPUT_LENS={OUTPUT_LENS} locust -f job.py --tags {tags} --headless -u {user} -r {rate} --run-time {time} --only-summary --csv csv")
    csv_data = pd.read_csv(f"csv_stats.csv")
    text  = csv_data.to_markdown()
    # 添加标题
    if OUTPUT_LENS == "1":
        title = "首响应测试"
    else:
        title = "常规响应测试"

    text = f"# {remark}-{title}：输入长度: {INPUT_LENS} 输出长度: {OUTPUT_LENS} 并发数: {user} 运行时间: {time} 标签: {tags}\n\n" + text + "\n\n"
    os.system(f"rm csv_*.csv")
    return text

text = """
# 当前测试单个实例情况
- 例如单卡2个并发，对应8卡16个并发
- 例如单卡5个并发，对应8卡40个并发
- 例如单卡25个并发，对应8卡200个并发

## CodeGeeX 案例数据参考指标（显卡3090）
- 输入长度都是93
### 响应时间测试
- 响应时间：8卡-输出⻓度64tokens情况；60并发，平均时长1.3s,P95时长1.5s；200并发，平均时长3.4s,P95时长4.1s
- 响应时间：1卡-输出⻓度64tokens情况；7并发，平均时长1.3s,P95时长1.5s；25并发，平均时长3.4s,P95时长4.1s
### 响应时间测试
- 响应时间：8卡-输出⻓度173tokens情况；30并发，平均时长3.9s,P95时长4.9s
- 响应时间：1卡-输出⻓度173tokens情况；8并发，平均时长3.9s,P95时长4.9s
### qps测试
- 8卡-输出⻓度1024tokens情况；60并发，qps 7
- 1卡-输出⻓度1024tokens情况；7并发，qps 1
- 8卡-输出⻓度200tokens情况；60并发，qps 20
- 1卡-输出⻓度200tokens情况；7并发，qps 2.5
- 8卡-输出⻓度100tokens情况；60并发，qps 26
- 1卡-输出⻓度100tokens情况；7并发，qps 3
- 8卡-输出⻓度173tokens情况；30并发，qps 7.3
- 1卡-输出⻓度173tokens情况；4并发，qps 0.9
### 首响应时间测试
- 8卡-输出⻓度1tokens情况；40并发，首响应时间3.4s
- 1卡-输出⻓度1tokens情况；5并发，首响应时间3.4s
- 8卡-输出⻓度1tokens情况；30并发，首响应时间3.3s
- 1卡-输出⻓度1tokens情况；4并发，首响应时间3.3s
- 8卡-输出⻓度1tokens情况；20并发，首响应时间1.0s
- 1卡-输出⻓度1tokens情况；2并发，首响应时间1.0s
### Chat生成速度
- 8卡-输出⻓度64tokens情况: 876token/s
- 1卡-输出⻓度64tokens情况: 110token/s
"""

def run():
    global text
    # 首响应时间测试
    text += task(INPUT_LENS="93", OUTPUT_LENS="1", user=5, rate=1, time="20s", tags="chat", remark="首响应时间测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="1", user=4, rate=1, time="20s", tags="chat", remark="首响应时间测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="1", user=2, rate=1, time="20s", tags="chat", remark="首响应时间测试")
    # 响应时间测试
    text += task(INPUT_LENS="93", OUTPUT_LENS="64", user=7, rate=4, time="20s", tags="chat", remark="响应时间测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="64", user=25, rate=20, time="20s", tags="chat", remark="响应时间测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=8, rate=4, time="20s", tags="chat", remark="响应时间测试")
    # qps测试
    text += task(INPUT_LENS="93", OUTPUT_LENS="1024", user=7, rate=4, time="20s", tags="chat", remark="qps测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="200", user=7, rate=4, time="20s", tags="chat", remark="qps测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="100", user=7, rate=4, time="20s", tags="chat", remark="qps测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=4, rate=4, time="20s", tags="chat", remark="qps测试")
    # 极限测试
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=50, rate=4, time="40s", tags="chat", remark="极限测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=100, rate=50, time="40s", tags="chat", remark="极限测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=200, rate=100, time="40s", tags="chat", remark="极限测试")
    text += task(INPUT_LENS="93", OUTPUT_LENS="173", user=300, rate=100, time="40s", tags="chat", remark="极限测试")
    # 写markdown
    with open("result.md", "w") as f:
        f.write(text)

if __name__ == "__main__":
    run()