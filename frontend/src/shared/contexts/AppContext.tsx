import { createContext, type ReactNode, useContext, useMemo } from "react";
import { useRootState } from "../hooks/useRootState";

type AppContextValue = ReturnType<typeof useRootState>;

export const AppContext = createContext<AppContextValue | undefined>(undefined);

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const rootState = useRootState();
  const value = useMemo(() => rootState, [rootState]);
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = (): AppContextValue => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within AppProvider");
  }
  return context;
};