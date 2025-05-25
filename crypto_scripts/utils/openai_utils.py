from openai import OpenAI
import sys
from config import CHATGPT_TOKEN, DEBUG

client = OpenAI(api_key=CHATGPT_TOKEN)
async def chat_gpt(text: str):
    sample = '''I am a trader, I trade in the cryptocurrency market, and everything written below pertains only to cryptocurrency. Sometimes I receive external signals and need assistance in determining a trading strategy.\n
\n
Revise the text below the heading "Beginning of text for processing:" according to the following template:\n
\n
Криптовалюта: Specify the coin, pair, token, or currency. If you come across "ID" or "HFT," it indicates a coin with the token "ID" or "HFT." Examples of cryptocurrency coins and tokens include ape, arb, gmt, op, hook, dydx, perp, ID, hft, band, bnx, mask, woo. Conditions apply only to the line "cryptocurrency" - If you cannot determine, write - not determined.\n
\n
Направление сделки: Determine the direction and insert long or short, without adding leverage. Conditions apply only to the line "trade direction" - If you cannot determine, write - not determined. If there is leverage (e.g., 20x), do not include it in this line.\n
\n
Точка входа: Highlight and insert the entry point from the text below in one line, without bullet points. Conditions apply only to the line "entry point" - If the entry point is at the market or currently, insert "at market." If you cannot determine a range or numerical value for the entry point, insert "not determined." Remove the dollar sign from the values.\n
\n
Тейк-профит: Highlight and insert the take profit value(s) from the text below. List specific values in one line without adding extra words. Conditions apply only to the line "take profit" - If you cannot determine, write - not determined.\n
\n
Стоп-лосс: Highlight the value from the text below. Conditions apply only to the line "stop loss" - If you cannot determine, write - not determined. If no value is present in the text below, insert "at discretion."\n
\n
Плечо: Determine the leverage from the signal and insert it here, e.g., 20x or a range like 5x-100x. If no leverage is mentioned in the text below, use the value "20x."\n
\n
Лимитные заявки: Highlight only the entry values of all limit orders from the text below. If absent, insert "absent."\n
\n
Усреднения: Highlight all suggested averaging from the text. If absent, insert "absent."\n
\n
Сигнал: Is there a trading signal in the message? If yes, write "yes"; if no, write "no."\n
\n
Remove any additional information in the response, do not add any notes, and delete all combinations of characters from the words usdt, usd, /usdt, /usd in the message. Remove all # and $ symbols from the response, and delete any emoji characters. Do not include periods at the end of lines.\n
Названия строк напиши на русском языке.\n
\n
Beginning of text for processing:\n'''

    response_text = f'{sample}\n{text}'
#    if DEBUG:
#        print(f'text: {response_text}, type: {type(response_text)}')

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for crypto trading. Act as honest assistant."},
        {"role": "user", "content": response_text}
    ],
    max_tokens=500,
    n=1,
    temperature=0.7)
    return response.choices[0].message.content.strip()