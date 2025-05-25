import type { Meta, StoryObj } from "@storybook/react";
import { CapsuleBadge } from "@/components/ui/capsule-badge";
const meta: Meta<typeof CapsuleBadge> = { component: CapsuleBadge };
export default meta;
export const Primary: StoryObj = { args: { children: "Primary" } };
export const Success: StoryObj = { args: { intent: "success", children: "Success" } }; 