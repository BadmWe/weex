import requests
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage

model = ChatOpenAI(model="gpt-5.1")


@tool
def get_mexc_futures_ADA():
    """Get Futures MEXC Data for ADA and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/ADA_USDT').json()
    return r


@tool
def get_mexc_futures_BNB():
    """Get Futures MEXC Data for BNB and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/BNB_USDT').json()
    return r


@tool
def get_mexc_futures_BTC():
    """Get Futures MEXC Data for BTC and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/BTC_USDT').json()
    return r


@tool
def get_mexc_futures_DOGE():
    """Get Futures MEXC Data for DOGE and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/DOGE_USDT').json()
    return r


@tool
def get_mexc_futures_ETH():
    """Get Futures MEXC Data for ETH and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/ETH_USDT').json()
    return r


@tool
def get_mexc_futures_LTC():
    """Get Futures MEXC Data for LTC and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/LTC_USDT').json()
    return r


@tool
def get_mexc_futures_SOL():
    """Get Futures MEXC Data for SOL and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/SOL_USDT').json()
    return r


@tool
def get_mexc_futures_XRP():
    """Get Futures MEXC Data for XRP and usdt"""
    r = requests.get(
        f'https://contract.mexc.com/api/v1/contract/depth/XRP_USDT').json()
    return r


@tool
def get_mexc_ticker():
    """Get Futures MEXC Data for 832 trading pairs includes data for last price and 24 hour window detailed data"""
    r = requests.get('https://contract.mexc.com/api/v1/contract/ticker').json()
    return r


agent = create_agent(model, tools=[get_mexc_futures_ADA, get_mexc_futures_BTC, get_mexc_futures_DOGE, get_mexc_futures_BNB, get_mexc_futures_ETH, get_mexc_futures_LTC, get_mexc_futures_SOL, get_mexc_futures_XRP],
                     system_prompt="You are a helpful Senior Research Analyst. Analyze the major trading pairs involving ADA, SOL, LTC, DOGE, BTC, ETH, XRP, BNB on CEX Weex. Be concise and accurate.")

result = agent.invoke(
    {"messages": [HumanMessage(
        "Conduct a comprehensive analysis of the tickers including spot and futures. Identify key trends and document your analysis. Suggest trading actions: stop limits, leverage, time window and a ticker to trade. Provide 3 detailed trades. The opportunity exit should be in under 2-3 hours.")]}
)

# print(result)
print(result['messages'][-1].content)
