import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './features/Landing/Landing';
import SignIn from './features/Landing/SignIn';
import ProtectedRoute from './utils/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth" element={<SignIn />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Landing />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
