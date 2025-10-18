import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SignIn from './features/Landing/SignIn';
import Chat from './features/Chat/page/Chat';
import ProtectedRoute from './utils/ProtectedRoute';
import { AppProvider } from './shared/contexts/AppContext';

function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/auth" element={<SignIn />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Chat />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}

export default App;
