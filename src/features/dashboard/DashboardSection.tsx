export const DashboardSection = (props: {
  title: string;
  description: string;
  children: React.ReactNode;
}) => (
  <div className="rounded-md bg-white p-5 shadow-sm">
    <div className="max-w-3xl">
      <div className="text-lg font-semibold text-gray-900">{props.title}</div>

      <div className="mb-4 text-sm font-medium text-gray-600">
        {props.description}
      </div>

      {props.children}
    </div>
  </div>
);
