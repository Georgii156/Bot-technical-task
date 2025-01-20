from bot.config import GigaChatKey
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage

LLM = GigaChat(
    credentials=GigaChatKey,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False, 
    streaming=False,
)

messages = [
    SystemMessage(
        content="Вы — эксперт по нейропластичности мозга и тренер по развитию когнитивных способностей. Ваша задача — рекомендовать физические и когнитивные упражнения, которые помогают пользователю стимулировать нейропластичность. Вы объясняете, как упражнения способствуют улучшению работы мозга, создают новые кровеносные сосуды, способствуют ветвлению дендритов и формированию новых синапсов."
    )
]

def get_response(user_message: str) -> str:
    messages.append(HumanMessage(content=user_message))
    
    res = LLM.invoke(messages)
    
    return res.content

