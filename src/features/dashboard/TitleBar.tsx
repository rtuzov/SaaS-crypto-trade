export const TitleBar = (props: {
  title: React.ReactNode;
  description?: React.ReactNode;
}) => (
  <div className="mb-8">
    <div className="text-2xl font-semibold text-gray-900">{props.title}</div>

    {props.description && (
      <div className="text-sm font-medium text-gray-600">
        {props.description}
      </div>
    )}
  </div>
);
