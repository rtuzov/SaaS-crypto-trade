import React from 'react';

export const MessageState = (props: {
  icon: React.ReactNode;
  title: React.ReactNode;
  description: React.ReactNode;
  button: React.ReactNode;
}) => (
  <div className="flex h-[600px] flex-col items-center justify-center rounded-md bg-white p-5 shadow-sm">
    <div className="size-16 rounded-full bg-gray-100 p-3 [&_svg]:stroke-gray-600 [&_svg]:stroke-2">
      {props.icon}
    </div>

    <div className="mt-3 text-center">
      <div className="text-xl font-semibold text-gray-900">{props.title}</div>
      <div className="mt-1 text-sm font-medium text-gray-600">
        {props.description}
      </div>

      <div className="mt-5">{props.button}</div>
    </div>
  </div>
);
