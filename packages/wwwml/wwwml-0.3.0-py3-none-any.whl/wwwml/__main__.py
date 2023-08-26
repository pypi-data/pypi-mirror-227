import argparse
import logging
import sys
from os import environ

import openai
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from loguru import logger

from wwwml.__about__ import __version__
from wwwml.tools import load_tools

INIT_PROMPT = "My Linux server is slow. Use providered function to check the server, then give a short (2-3) sentence description of the problem."


def main():
    parser = argparse.ArgumentParser(
        description="What's wrong with my linux? v" + __version__
    )
    parser.add_argument(
        "-p",
        default=INIT_PROMPT,
        type=str,
        help="Initial prompt to start the conversation.",
    )
    parser.add_argument("-v", action="count", default=0, help="verbose mode")
    args = parser.parse_args()

    logger.remove()
    log_format = "{message}"
    if args.v > 2:
        logger.add(sys.stderr, level="DEBUG", format=log_format)
    elif args.v > 0:
        logger.add(sys.stderr, level="INFO", format=log_format)
    else:
        logger.add(sys.stderr, level="WARNING", format=log_format)

    # avoid "WARNING! deployment_id is not default parameter."
    langchain_logger = logging.getLogger("langchain.chat_models.openai")
    langchain_logger.disabled = True

    if "WWWML_DEPLOYMENT" in environ:
        llm = ChatOpenAI(temperature=0, deployment_id=environ["WWWML_DEPLOYMENT"])
    else:
        llm = ChatOpenAI(
            temperature=0, model=environ.get("WWWML_MODEL", "gpt-3.5-turbo")
        )
    agent = initialize_agent(
        load_tools(llm), llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=args.v > 1
    )
    response = agent.run(args.p)

    logger.info("=" * 24)
    print(response)


if __name__ == "__main__":
    main()
