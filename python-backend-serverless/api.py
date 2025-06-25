from conversation_store import create_conversation_store
from agents import (
    Runner,
    ItemHelpers,
    MessageOutputItem,
    HandoffOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
    InputGuardrailTripwireTriggered,
    Handoff,
)
from main import (
    triage_agent,
    faq_agent,
    intro_agent,
    career_agent,
    project_agent,
    tech_agent,
    create_initial_context,
)
import logging
import time
from uuid import uuid4
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration (서버리스 환경을 위한 설정)
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Models
# =========================


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class MessageResponse(BaseModel):
    content: str
    agent: Optional[str] = None


class AgentEvent(BaseModel):
    id: str
    type: str
    agent: str
    content: str
    metadata: Optional[dict] = None
    timestamp: Optional[float] = None


class GuardrailCheck(BaseModel):
    id: str
    name: str
    input: str
    reasoning: str
    passed: bool
    timestamp: float


class ChatResponse(BaseModel):
    conversation_id: str
    current_agent: str
    messages: List[MessageResponse]
    events: List[AgentEvent]
    context: dict
    agents: List[dict]
    guardrails: List[GuardrailCheck]

# =========================
# 서버리스 환경을 위한 Redis 기반 conversation store
# =========================


# 환경에 따라 자동으로 적절한 스토어 선택 (Redis 또는 InMemory 폴백)
conversation_store = create_conversation_store()


# =========================
# 헬스체크 및 유틸리티 엔드포인트
# =========================

@app.get("/health")
async def health_check():
    """서버리스 환경에서 헬스체크 및 웜업용 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "store_type": type(conversation_store).__name__
    }


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "OpenAI Developer Profile Agents API",
        "version": "2.0.0-serverless",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

# =========================
# Helpers
# =========================


def safe_context_to_dict(ctx):
    if isinstance(ctx, dict):
        return ctx
    elif hasattr(ctx, "model_dump"):
        return ctx.model_dump()
    elif hasattr(ctx, "dict"):
        return ctx.dict()
    else:
        return {}


def _get_agent_by_name(name: str):
    """Return the agent object by name."""
    agents = {
        triage_agent.name: triage_agent,
        faq_agent.name: faq_agent,
        intro_agent.name: intro_agent,
        career_agent.name: career_agent,
        project_agent.name: project_agent,
        tech_agent.name: tech_agent,
    }
    return agents.get(name, triage_agent)


def _get_guardrail_name(g) -> str:
    """Extract a friendly guardrail name."""
    name_attr = getattr(g, "name", None)
    if isinstance(name_attr, str) and name_attr:
        return name_attr
    guard_fn = getattr(g, "guardrail_function", None)
    if guard_fn is not None and hasattr(guard_fn, "__name__"):
        return guard_fn.__name__.replace("_", " ").title()
    fn_name = getattr(g, "__name__", None)
    if isinstance(fn_name, str) and fn_name:
        return fn_name.replace("_", " ").title()
    return str(g)


def _build_agents_list() -> List[Dict[str, Any]]:
    """Build a list of all available agents and their metadata."""
    def make_agent_dict(agent):
        return {
            "name": agent.name,
            "description": getattr(agent, "handoff_description", ""),
            "handoffs": [getattr(h, "agent_name", getattr(h, "name", "")) for h in getattr(agent, "handoffs", [])],
            "tools": [getattr(t, "name", getattr(t, "__name__", "")) for t in getattr(agent, "tools", [])],
            "input_guardrails": [],
        }
    return [
        make_agent_dict(triage_agent),
        make_agent_dict(faq_agent),
        make_agent_dict(intro_agent),
        make_agent_dict(career_agent),
        make_agent_dict(project_agent),
        make_agent_dict(tech_agent),
    ]


def get_agent_name(agent):
    if isinstance(agent, str):
        return agent
    if hasattr(agent, "name"):
        return agent.name
    return None

# =========================
# Main Chat Endpoint
# =========================


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """개발자 자기소개서/포트폴리오 대화 API"""
    conversation_id = req.conversation_id or uuid4().hex
    state = conversation_store.get(conversation_id) or {
        "input_items": [],
        "context": create_initial_context(),
        "current_agent": triage_agent.name,
    }
    old_context = safe_context_to_dict(state["context"])
    guardrail_checks: List[GuardrailCheck] = []

    # 메시지 추가
    state["input_items"].append({"role": "user", "content": req.message})
    current_agent = _get_agent_by_name(state["current_agent"])

    try:
        result = await Runner.run(current_agent, state["input_items"], context=state["context"])
    except InputGuardrailTripwireTriggered as e:
        failed = e.guardrail_result.guardrail
        gr_output = e.guardrail_result.output.output_info
        gr_reasoning = getattr(gr_output, "reasoning", "")
        gr_input = req.message
        gr_timestamp = time.time() * 1000
        for g in getattr(current_agent, "input_guardrails", []):
            guardrail_checks.append(GuardrailCheck(
                id=uuid4().hex,
                name=g,
                input=gr_input,
                reasoning=(gr_reasoning if g == failed else ""),
                passed=(g != failed),
                timestamp=gr_timestamp,
            ))
        refusal = "Sorry, I can only answer questions related to developer profiles."
        state["input_items"].append({"role": "assistant", "content": refusal})
        return ChatResponse(
            conversation_id=conversation_id,
            current_agent=current_agent.name,
            messages=[MessageResponse(
                content=refusal, agent=current_agent.name)],
            events=[],
            context=safe_context_to_dict(state["context"]),
            agents=_build_agents_list(),
            guardrails=guardrail_checks,
        )

    messages: List[MessageResponse] = []
    events: List[AgentEvent] = []

    # 꼭 필요한 핵심 프린트만 유지
    print("=== RUNNER RESULT ===")
    print(result)
    items = next(
        (v for v in [
            getattr(result, "new_items", None),
            getattr(result, "items", None),
            getattr(result, "messages", None)
        ] if v), []
    )
    print(f"=== items (len={len(items)}) ===")
    for idx, item in enumerate(items):
        print(
            f"Item {idx}: type={type(item)}, agent={getattr(item, 'agent', None)}")

    for item in items:
        # role이 'assistant'이거나, role이 없으면 모두 추가
        role = getattr(item, "role", None)
        content = getattr(item, "content", None)
        # MessageOutputItem의 경우 content가 None이고, raw_item.content에 텍스트가 있음
        if content is None and hasattr(item, "raw_item"):
            raw_item = getattr(item, "raw_item")
            if hasattr(raw_item, "content"):
                raw_content = getattr(raw_item, "content")
                if isinstance(raw_content, list):
                    content_text = "".join(
                        [c.text for c in raw_content if hasattr(c, "text")]
                    )
                else:
                    content_text = str(raw_content)
            else:
                content_text = ""
        elif isinstance(content, list):
            content_text = "".join(
                [c.text for c in content if hasattr(c, "text")]
            )
        else:
            content_text = content

        agent_name = get_agent_name(getattr(item, "agent", None))
        if (role is None or role == "assistant") and content_text:
            messages.append(MessageResponse(
                content=content_text, agent=agent_name))
        # 기타 이벤트 등은 필요시 확장

    new_context = safe_context_to_dict(state["context"])
    changes = {k: new_context[k]
               for k in new_context if old_context.get(k) != new_context[k]}
    if changes:
        events.append(
            AgentEvent(
                id=uuid4().hex,
                type="context_update",
                agent=current_agent.name,
                content="",
                metadata={"changes": changes},
            )
        )

    state["input_items"] = result.to_input_list(
    ) if hasattr(result, "to_input_list") else []
    state["current_agent"] = current_agent.name

    # 상태 저장 및 Redis TTL 연장 (활성 대화 세션 유지)
    conversation_store.save(conversation_id, state)
    if hasattr(conversation_store, 'extend_ttl'):
        conversation_store.extend_ttl(conversation_id)

    # Build guardrail results: mark failures (if any), and any others as passed
    final_guardrails: List[GuardrailCheck] = []
    for g in getattr(current_agent, "input_guardrails", []):
        name = g
        failed = next((gc for gc in guardrail_checks if gc.name == name), None)
        if failed:
            final_guardrails.append(failed)
        else:
            final_guardrails.append(GuardrailCheck(
                id=uuid4().hex,
                name=name,
                input=req.message,
                reasoning="",
                passed=True,
                timestamp=time.time() * 1000,
            ))

    return ChatResponse(
        conversation_id=conversation_id,
        current_agent=current_agent.name,
        messages=messages,
        events=events,
        context=new_context,
        agents=_build_agents_list(),
        guardrails=final_guardrails,
    )
