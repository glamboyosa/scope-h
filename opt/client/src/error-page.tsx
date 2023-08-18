import { useRouteError, isRouteErrorResponse } from "react-router-dom";

const ErrorBoundary = () => {
  const error = useRouteError();
  console.error(error);

  if (isRouteErrorResponse(error)) {
    return (
      <div className="flex items-center justify-center flex-col min-h-screen">
        <h1 className="mb-4">Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
        <p className="text-gray-300">
          <i>{error.statusText}</i>
        </p>
      </div>
    );
  } else {
    return (
      <div className="flex justify-center items-center flex-col min-h-screen">
        <h1 className="mb-4">Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
      </div>
    );
  }
};

export default ErrorBoundary;
