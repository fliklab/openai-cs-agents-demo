"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot } from "lucide-react";
import { PanelSection } from "./panel-section";
import type { Agent } from "@/lib/types";

interface AgentsListProps {
  agents: Agent[];
  currentAgent: string;
}

export function AgentsList({ agents, currentAgent }: AgentsListProps) {
  const activeAgent = agents.find((a) => a.name === currentAgent);
  return (
    <PanelSection
      title="에이전트 목록"
      icon={<Bot className="h-4 w-4 text-blue-600" />}
    >
      <div className="grid grid-cols-3 gap-3">
        {agents.map((agent) => (
          <Card
            key={agent.name}
            className={`bg-white border-gray-200 transition-all ${
              agent.name === currentAgent ||
              activeAgent?.handoffs.includes(agent.name)
                ? ""
                : "opacity-50 filter grayscale cursor-not-allowed pointer-events-none"
            } ${
              agent.name === currentAgent
                ? "ring-1 ring-blue-500 shadow-md"
                : ""
            }`}
          >
            <CardHeader className="p-3 pb-1 flex items-center gap-2">
              {agent.icon && (
                <span className="mr-2">
                  <Bot className="h-4 w-4 text-blue-600" />
                </span>
              )}
              <CardTitle className="text-sm flex items-center text-zinc-900">
                {agent.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-1">
              <p className="text-xs font-light text-zinc-500">
                {agent.description}
              </p>
              {agent.category && (
                <div className="text-[11px] text-blue-500 mt-1">
                  {agent.category}
                </div>
              )}
              {agent.link && (
                <a
                  href={agent.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-xs text-blue-700 underline mt-1"
                >
                  상세보기
                </a>
              )}
              {agent.name === currentAgent && (
                <Badge className="mt-2 bg-blue-600 hover:bg-blue-700 text-white">
                  활성화됨
                </Badge>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </PanelSection>
  );
}
