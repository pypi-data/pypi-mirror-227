"""Utilities for sending events to Imaginary Dev."""
import asyncio
import logging
import os
import time
import uuid
import warnings
from contextlib import asynccontextmanager
from typing import Any, Dict, List, TypedDict

import aiohttp

logger = logging.getLogger(__name__)


class SendEventResponse(TypedDict):
    id: str
    """The id of the event that was added on the server."""
    api_name: str
    """The name of the API that was used or created, in case null api name was used."""


async def send_event(
    session: aiohttp.ClientSession,
    api_key: str | None,
    *,
    project_key: str | None = None,
    prompt_template_name: str | None,
    prompt_event_id: str | None = None,
    prompt_template_text: str | None = None,
    prompt_template_chat: List | None = None,
    prompt_params: Dict | None = None,
    chat_id: str | None = None,
    response: str | None = None,
    response_time: float | None = None,
    prompt: Any | None = None,
    parent_event_id: str | None = None,
    model_params: Dict | None = None,
) -> SendEventResponse | None:
    """Send an event to Imaginary Dev. Returns the id of the event that was added on the server."""
    PROMPT_REPORTING_URL = os.environ.get(
        "PROMPT_REPORTING_URL", "https://app.imaginary.dev/api/event"
    )
    event = {
        "apiName": prompt_template_name,
        "params": {},
        "prompt": prompt or {},
        "promptEventId": prompt_event_id,
        "modelParameters": model_params or {},
    }

    logger.debug(f"Sending event to {PROMPT_REPORTING_URL} {prompt_template_name}")
    if project_key is not None:
        event["projectKey"] = project_key
    if api_key is not None:
        event["apiKey"] = api_key

    if not api_key and not project_key:
        logger.warning("No project key or api key set, not sending event")
        return

    if prompt_template_text is not None:
        if isinstance(prompt_template_text, str):
            # first default template to just the raw text
            event["promptTemplateText"] = prompt_template_text
            if prompt_params is None and getattr(prompt_template_text, "params", None):
                # Can be TemplateString or any other
                prompt_params = prompt_template_text.params  # type: ignore

            # If the original template is available, send it too
            if getattr(prompt_template_text, "template", None):
                event["promptTemplateText"] = prompt_template_text.template  # type: ignore

    elif prompt_template_chat is not None:
        # We're going to assume that if a non-string was passed in, then it
        # was probably a chat template, aka a chat message history

        # Do any langchain conversion, in case there are langchain objects inside
        try:
            # import will fail if langchain is not installed
            from .langchain import format_chat_template

            prompt_template_chat = format_chat_template(prompt_template_chat)
        except ImportError:
            pass
        # TODO: figure out template extraction for chat templates
        event["promptTemplateChat"] = prompt_template_chat

    if prompt_params is not None:
        event["params"] = prompt_params
    if response is not None:
        event["response"] = response
    if response_time is not None:
        event["responseTime"] = response_time
    if chat_id is not None:
        event["chatId"] = chat_id
    if parent_event_id is not None:
        event["parentEventId"] = str(parent_event_id)

    result = await session.post(PROMPT_REPORTING_URL, json=event)
    json: SendEventResponse = await result.json()

    return json


@asynccontextmanager
async def event_session(
    project_key: str | None,
    api_key: str | None,
    prompt_template_name: str | None,
    prompt_template_text: str | None,
    prompt_template_chat: List | None,
    model_params: Dict | None = None,
    chat_id: str | None = None,
    prompt_template_params: dict | None = None,
    prompt_event_id: str | None = None,
    parent_event_id: str | None = None,
):
    """Context manager for sending an event to Imaginary Dev.

    Usage::

        with event_session(project_key, prompt_template_name, prompt_text, prompt_event_id) as complete_event:
            # do something
            complete_event(response)

    """
    start = time.time()
    if prompt_event_id is None:
        prompt_event_id = str(uuid.uuid4())

    async with aiohttp.ClientSession() as session:
        pending_events_sent = []
        first_event_sent = send_event(
            session=session,
            project_key=project_key,
            api_key=api_key,
            prompt_template_name=prompt_template_name,
            prompt_event_id=prompt_event_id,
            prompt_template_text=prompt_template_text,
            prompt_template_chat=prompt_template_chat,
            prompt_params=prompt_template_params,
            chat_id=chat_id,
            parent_event_id=parent_event_id,
            model_params=model_params,
        )
        pending_events_sent.append(first_event_sent)
        event_prompt_template_name = prompt_template_name

        async def complete_event(response):
            local_prompt_template_name = prompt_template_name
            if not event_prompt_template_name:
                first_event = await first_event_sent
                if first_event:
                    local_prompt_template_name = first_event["api_name"]
            response_time = (time.time() - start) * 1000
            second_event_sent = send_event(
                session=session,
                project_key=project_key,
                api_key=api_key,
                prompt_template_name=local_prompt_template_name,
                prompt_event_id=prompt_event_id,
                prompt_template_text=prompt_template_text,
                prompt_template_chat=prompt_template_chat,
                prompt_params=prompt_template_params,
                chat_id=chat_id,
                parent_event_id=parent_event_id,
                model_params=model_params,
                response=response,
                response_time=response_time,
            )
            pending_events_sent.append(second_event_sent)

        yield complete_event
        w = time.time()
        pending_events_results = await asyncio.gather(*pending_events_sent, return_exceptions=True)
        failed_events = [e for e in pending_events_results if isinstance(e, Exception)]
        if failed_events:
            warnings.warn(
                f"Failed to report calls. {len(failed_events)} failure(s). First failure: {failed_events[0]}",
                stacklevel=3,
            )
