import Todos from "./components/Todos";
import * as jose from "jose";
import { ReactQueryDevtools } from "react-query/devtools";

import { useState } from "react";
import {
  QueryClient,
  QueryClientProvider,
  useMutation,
  useQueryClient,
} from "react-query";
// import { queryClient } from "./main"

// Create a client
// const queryClient = new QueryClient();

function App() {
  const [token, setToken] = useState("");
  const [hide, setHide] = useState(false);
  const queryClient = useQueryClient();

  const newAddTodo = async () => {
    const body = JSON.stringify({
      subject: "React",
      details: "New todo",
    });

    const request = await fetch("http://localhost:8080/todos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body,
    });
    const data = await request.json();
    return data;
  };
  const { mutate } = useMutation(newAddTodo, {
    onSuccess: () => {
      queryClient.invalidateQueries("todos");
    },
  });

  const login = async (username: string, password: string) => {
    const response = await fetch("http://localhost:8080/api/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const data = await response.json();
    setToken(data.access);
    // jose.jwtDecrypt(data.access,)
  };

  const addTodo = async () => {
    const body = JSON.stringify({
      subject: "React",
      details: "New todo",
    });

    const response = await fetch("http://localhost:8080/todos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body,
    });
  };

  return (
    <>
      <h1>Todos</h1>
      <button onClick={() => setHide(!hide)}>Toggle</button>
      <button onClick={() => login("admin", "admin")}>Login</button>
      <button onClick={() => mutate()}>Add</button>
      {hide ? null : <Todos />}
      <ReactQueryDevtools initialIsOpen={true} />
    </>
  );
}

export default App;
