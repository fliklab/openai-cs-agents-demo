from agents import function_tool, RunContextWrapper
from context import DeveloperProfileContext


@function_tool(
    name_override="list_projects",
    description_override="주요 프로젝트 목록과 설명을 제공합니다."
)
async def list_projects(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    projects = context.context.projects
    return "\n\n".join([
        f"- {p.name}: {p.description} (기술스택: {', '.join(p.tech_stack)})" +
        (f" [링크]({p.link})" if p.link else "")
        for p in projects
    ])


@function_tool(
    name_override="list_experiences",
    description_override="경력 및 근무한 회사 정보를 제공합니다."
)
async def list_experiences(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    exps = context.context.experiences
    return "\n\n".join([
        f"- {e.company} ({e.period}): {e.position}" +
        (f" - {e.description}" if e.description else "")
        for e in exps
    ])


@function_tool(
    name_override="describe_strengths",
    description_override="성격적 강점과 협업 스타일을 설명합니다."
)
async def describe_strengths(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    strengths = ", ".join(context.context.strengths)
    personality = context.context.personality
    return f"강점: {strengths}\n성격/협업 스타일: {personality}"


@function_tool(
    name_override="show_tech_stack",
    description_override="주요 기술스택을 보여줍니다."
)
async def show_tech_stack(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    return ", ".join(context.context.tech_stack)


@function_tool(
    name_override="show_portfolio",
    description_override="포트폴리오 및 깃허브 링크를 제공합니다."
)
async def show_portfolio(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    return f"포트폴리오: {context.context.portfolio_url}\nGitHub: {context.context.github}"


@function_tool(
    name_override="faq_lookup_tool",
    description_override="개발자 본인에 대해 자주 묻는 질문에 답변합니다."
)
async def faq_lookup_tool(question: str) -> str:
    q = question.lower()
    if "취미" in q:
        return "독서와 오픈소스 기여를 즐깁니다. (예시)"
    if "협업" in q:
        return "다양한 팀과의 협업 경험이 많으며, 소통을 중시합니다. (예시)"
    if "장점" in q:
        return "문제 해결력과 책임감이 강점입니다. (예시)"
    return "죄송합니다. 해당 질문에 대한 답변이 준비되어 있지 않습니다. (예시)"


@function_tool(
    name_override="about_me",
    description_override="개발자 본인의 자기소개를 제공합니다."
)
async def about_me(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    return context.context.about_me


@function_tool(
    name_override="list_awards",
    description_override="수상경력 목록을 제공합니다."
)
async def list_awards(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    awards = context.context.awards
    if not awards:
        return "수상경력이 없습니다."
    return "\n\n".join([
        f"- {a.title} ({a.issuer}, {a.year})" +
                       (f" - {a.description}" if a.description else "")
                       for a in awards
                       ])


@function_tool(
    name_override="list_certifications",
    description_override="자격증 목록을 제공합니다."
)
async def list_certifications(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    certs = context.context.certifications
    if not certs:
        return "자격증이 없습니다."
    return "\n\n".join([
        f"- {c.name} ({c.issuer}, {c.year})" +
                      (f" - {c.description}" if c.description else "")
        for c in certs
    ])


@function_tool(
    name_override="summarize_portfolio",
    description_override="포트폴리오 전체를 간단히 요약합니다."
)
async def summarize_portfolio(context: RunContextWrapper[DeveloperProfileContext]) -> str:
    # 실제 구현에서는 포트폴리오 내용을 분석해 요약할 수 있음
    return f"포트폴리오 요약: 다양한 AI/웹 프로젝트와 실무 경험을 보유하고 있습니다. 상세 내용은 {context.context.portfolio_url} 참고 바랍니다."
