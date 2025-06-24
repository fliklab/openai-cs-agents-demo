"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Shield as LucideShield,
  CheckCircle as LucideCheckCircle,
  XCircle as LucideXCircle,
} from "lucide-react";
import { PanelSection } from "./panel-section";
import type { GuardrailCheck } from "@/lib/types";

interface GuardrailsProps {
  guardrails: GuardrailCheck[];
  inputGuardrails: string[];
}

const ShieldIcon = LucideShield as unknown as React.FC<
  React.SVGProps<SVGSVGElement>
>;
const CheckCircleIcon = LucideCheckCircle as unknown as React.FC<
  React.SVGProps<SVGSVGElement>
>;
const XCircleIcon = LucideXCircle as unknown as React.FC<
  React.SVGProps<SVGSVGElement>
>;

export function Guardrails({ guardrails, inputGuardrails }: GuardrailsProps) {
  const guardrailNameMap: Record<string, string> = {
    relevance_guardrail: "경력 검증",
    jailbreak_guardrail: "프로젝트 검증",
  };

  const guardrailDescriptionMap: Record<string, string> = {
    "경력 검증": "입력된 경력이 실제와 일치하는지 검증합니다.",
    "프로젝트 검증": "프로젝트 경험의 진위 여부를 검증합니다.",
  };

  const extractGuardrailName = (rawName: string): string =>
    guardrailNameMap[rawName] ?? rawName;

  const guardrailsToShow: GuardrailCheck[] = inputGuardrails.map((rawName) => {
    const existing = guardrails.find((gr) => gr.name === rawName);
    if (existing) {
      return existing;
    }
    return {
      id: rawName,
      name: rawName,
      input: "",
      reasoning: "",
      passed: false,
      timestamp: new Date(),
    };
  });

  return (
    <PanelSection
      title="검증 항목"
      icon={<ShieldIcon className="h-4 w-4 text-blue-600" />}
    >
      <div className="grid grid-cols-3 gap-3">
        {guardrailsToShow.map((gr) => (
          <Card
            key={gr.id}
            className={`bg-white border-gray-200 transition-all ${
              !gr.input ? "opacity-60" : ""
            }`}
          >
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-sm flex items-center text-zinc-900">
                {extractGuardrailName(gr.name)}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-1">
              <p className="text-xs font-light text-zinc-500 mb-1">
                {(() => {
                  const title = extractGuardrailName(gr.name);
                  return guardrailDescriptionMap[title] ?? gr.input;
                })()}
              </p>
              <div className="flex text-xs">
                {!gr.input || gr.passed ? (
                  <Badge className="mt-2 px-2 py-1 bg-emerald-500 hover:bg-emerald-600 flex items-center text-white">
                    <CheckCircleIcon className="h-4 w-4 mr-1 text-white" />
                    Passed
                  </Badge>
                ) : (
                  <Badge className="mt-2 px-2 py-1 bg-red-500 hover:bg-red-600 flex items-center text-white">
                    <XCircleIcon className="h-4 w-4 mr-1 text-white" />
                    Failed
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </PanelSection>
  );
}
