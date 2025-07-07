// src/context/AuthContext.tsx
import React, { createContext, useState, useEffect } from "react";


interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState(null);

  // 로그인
  const login = async (username:string, password :string) => {
    try {
      const res = await fetch("http://localhost:8000/auth/jwt/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error("Login failed");

      const data = await res.json();
      localStorage.setItem("token", data.access);

      // 유저 정보 가져오기
      const userRes = await fetch("http://localhost:8000/auth/users/me/", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${data.access}`,
        },
      });

      if (!userRes.ok) throw new Error("User fetch failed");

      const userData = await userRes.json();
      setUser(userData);
      return true;
    } catch (err) {
      console.error("로그인 실패:", err);
      return false;
    }
  };

  // 로그아웃
  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  // 초기화 (새로고침 시 유저 상태 유지)
  const initialize = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await fetch("http://localhost:8000/auth/users/me/", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error();

      const userData = await res.json();
      setUser(userData);
    } catch {
      localStorage.removeItem("token");
    }
  };

  useEffect(() => {
    initialize();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};


interface AuthContextType {
  user: any;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);
