import * as React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { tokenStore } from '../api/tokenStore';

const ProtectedRoute = () => {
  const location = useLocation();
  const hasAccessToken = Boolean(tokenStore.getAccessToken());

  if (!hasAccessToken) {
    return <Navigate to="/auth" replace state={{ from: location }} />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
