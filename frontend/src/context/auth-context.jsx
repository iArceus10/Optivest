import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { getCurrentUser, loginUser, registerUser } from "../services/auth-service";
import {
  clearStoredAccessToken,
  getStoredAccessToken,
  storeAccessToken,
} from "../utils/auth-storage";

const AuthContext = createContext(null);

function buildInitialState() {
  const token = getStoredAccessToken();

  return {
    accessToken: token,
    currentUser: null,
    isAuthenticated: Boolean(token),
    isBootstrapping: Boolean(token),
  };
}

export function AuthProvider({ children }) {
  const [authState, setAuthState] = useState(buildInitialState);

  useEffect(() => {
    async function bootstrapCurrentUser() {
      if (!authState.accessToken) {
        return;
      }

      try {
        const user = await getCurrentUser();

        setAuthState((previousState) => ({
          ...previousState,
          currentUser: user,
          isAuthenticated: true,
          isBootstrapping: false,
        }));
      } catch (error) {
        clearStoredAccessToken();
        setAuthState({
          accessToken: null,
          currentUser: null,
          isAuthenticated: false,
          isBootstrapping: false,
        });
      }
    }

    bootstrapCurrentUser();
  }, [authState.accessToken]);

  async function login(credentials) {
    const tokenResponse = await loginUser(credentials);

    storeAccessToken(tokenResponse.access_token);

    setAuthState((previousState) => ({
      ...previousState,
      accessToken: tokenResponse.access_token,
      isAuthenticated: true,
      isBootstrapping: true,
    }));

    const user = await getCurrentUser();

    setAuthState({
      accessToken: tokenResponse.access_token,
      currentUser: user,
      isAuthenticated: true,
      isBootstrapping: false,
    });

    return user;
  }

  async function register(payload) {
    return registerUser(payload);
  }

  function logout() {
    clearStoredAccessToken();
    setAuthState({
      accessToken: null,
      currentUser: null,
      isAuthenticated: false,
      isBootstrapping: false,
    });
  }

  const value = useMemo(
    () => ({
      currentUser: authState.currentUser,
      accessToken: authState.accessToken,
      isAuthenticated: authState.isAuthenticated,
      isBootstrapping: authState.isBootstrapping,
      login,
      register,
      logout,
    }),
    [authState]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider.");
  }

  return context;
}