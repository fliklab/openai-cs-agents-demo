export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  agent?: string;
  timestamp: Date;
}

export interface Agent {
  name: string;
  description: string;
  handoffs: string[];
  tools: string[];
  /** List of input guardrail identifiers for this agent */
  input_guardrails: string[];
  // 개발자 소개용 확장 필드
  icon?: string; // lucide-react 아이콘 이름 등
  link?: string; // 상세 페이지, 외부 링크 등
  category?: string; // 자기소개, 경력, 프로젝트 등 카테고리
}

export type EventType =
  | "message"
  | "handoff"
  | "tool_call"
  | "tool_output"
  | "context_update";

export interface AgentEvent {
  id: string;
  type: EventType;
  agent: string;
  content: string;
  timestamp: Date;
  metadata?: {
    source_agent?: string;
    target_agent?: string;
    tool_name?: string;
    tool_args?: Record<string, any>;
    tool_result?: any;
    context_key?: string;
    context_value?: any;
    changes?: Record<string, any>;
  };
}

export interface GuardrailCheck {
  id: string;
  name: string;
  input: string;
  reasoning: string;
  passed: boolean;
  timestamp: Date;
}
