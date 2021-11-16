type Todo = {
  id: number;
  subject: string;
  description: string;
};

import { useState, useEffect } from "react";
import { useQuery, useQueryClient } from "react-query";

const fetchTodo = async () => {
  const response = await fetch("http://localhost:8080/todos/");
  const todos: Todo[] = await response.json();
  return todos;
};

function Todos() {
  // const [todos, setTodos] = useState<Todo[]>([]);

  const queryClient = useQueryClient();
  const { status, data } = useQuery("todos", fetchTodo);

  // useEffect(() => {
  //   const fetchTodo = async () => {
  //     const response = await fetch("http://localhost:8080/todos/");
  //     const todos: Todo[] = await response.json();
  //     setTodos(todos)
  //   };

  //   fetchTodo();
  // }, [])

  if (status === "loading") {
    return <span>Loading...</span>;
  }

  if (status === "error") {
    return <span>Error</span>;
  }

  return (
    <ul>
      {data?.map((todo) => (
        <li key={todo.id}>{todo.subject}</li>
      ))}
    </ul>
  );
}

export default Todos;
