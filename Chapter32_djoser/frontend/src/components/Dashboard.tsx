import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export  const Dashboard: React.FC =()=> {
  const authContext = useContext(AuthContext);

  if (!authContext || !authContext.user) return <Navigate to="/login" replace />;

  const { user, logout } = authContext;

  return (
    <div>
      <h2>Welcome, {user.username}</h2>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
