"use client";
import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

const ChevronDownIcon = ChevronDown as unknown as React.FC<
  React.SVGProps<SVGSVGElement>
>;
const ChevronRightIcon = ChevronRight as unknown as React.FC<
  React.SVGProps<SVGSVGElement>
>;

interface PanelSectionProps {
  title: string;
  icon: React.ReactElement;
  children: React.ReactNode;
}

export function PanelSection({ title, icon, children }: PanelSectionProps) {
  const [show, setShow] = useState(true);

  return (
    <div className="mb-5">
      <h2
        className="text-lg font-semibold mb-3 text-zinc-900 flex items-center justify-between cursor-pointer"
        onClick={() => setShow(!show)}
      >
        <div className="flex items-center">
          <span className="bg-blue-600 bg-opacity-10 p-1.5 rounded-md mr-2 shadow-sm">
            {icon}
          </span>
          <span>{title}</span>
        </div>
        {show ? (
          <ChevronDownIcon className="h-4 w-4 text-zinc-900" />
        ) : (
          <ChevronRightIcon className="h-4 w-4 text-zinc-900" />
        )}
      </h2>
      {show && children}
    </div>
  );
}
