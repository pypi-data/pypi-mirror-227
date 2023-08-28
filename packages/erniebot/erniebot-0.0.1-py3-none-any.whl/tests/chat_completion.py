import erniebot
from erniebot.utils import logger
logger.set_level("WARNING")


def test_chat_completion(model="ernie-bot-3.5"):
    chat_completion = erniebot.ChatCompletion.create(
        model=model,
        messages=[{
            "role": "user",
            "content": "请问你是谁？"
        }, {
            "role": "assistant",
            "content":
            "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
        }, {
            "role": "user",
            "content": "我在深圳，周末可以去哪里玩？"
        }],
        stream=False)
    print(chat_completion)


def test_chat_completion_stream_mode(model="ernie-bot-3.5"):
    chat_completion = erniebot.ChatCompletion.create(
        model=model,
        messages=[{
            "role": "user",
            "content": "请问你是谁？"
        }, {
            "role": "assistant",
            "content":
            "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
        }, {
            "role": "user",
            "content": "我在深圳，周末可以去哪里玩？"
        }],
        stream=True)

    for item in chat_completion:
        print(item)


if __name__ == "__main__":

    erniebot.api_type = "qianfan"
    # 批量返回
    test_chat_completion(model="ernie-bot-turbo")

    # 流式逐句返回
    test_chat_completion_stream_mode(model="ernie-bot-turbo")

    erniebot.api_type = "aistudio"
    # AIStudio 模式暂不支持流式返回与模型切换，目前只支持EB旗舰版
    test_chat_completion(model="ernie-bot-3.5")
