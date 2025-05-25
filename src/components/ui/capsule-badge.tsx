import { cva, VariantProps } from "class-variance-authority";
const badge = cva(
  "inline-flex items-center px-3 py-1 text-xs font-medium rounded-pill transition-colors",
  {
    variants: {
      intent: {
        default: "bg-primary/10 text-primary",
        success: "bg-success/10 text-success",
        danger: "bg-danger/10 text-danger"
      }
    },
    defaultVariants: { intent: "default" }
  }
);
export type BadgeProps = VariantProps<typeof badge> & React.HTMLAttributes<HTMLSpanElement>;
export const CapsuleBadge = ({ intent, className, ...props }: BadgeProps) => (
  <span className={badge({ intent, className })} {...props} />
); 