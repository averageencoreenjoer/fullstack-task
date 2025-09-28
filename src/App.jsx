import { useState, useEffect } from 'react';
import axios from 'axios'; // Импортируем axios
import AddTaskForm from './components/AddTaskForm/AddTaskForm';
import TaskList from './components/TaskList/TaskList';
import Filter from './components/Filter/Filter';

const API_URL = 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState('all');
  const [error, setError] = useState(null); 

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setError(null);
        const endpoint = filter === 'all' ? '/tasks/' : `/tasks/?status=${filter}`;
        const response = await axios.get(`${API_URL}${endpoint}`);
        setTasks(response.data);
      } catch (err) {
        console.error('Failed to fetch tasks:', err);
        setError('Could not connect to the server. Please make sure it is running.');
      }
    };

    fetchTasks();
  }, [filter]); 

  const addTask = async (title, description) => {
    try {
      const newTask = { title, description, status: 'pending' };
      const response = await axios.post(`${API_URL}/tasks/`, newTask);
      setTasks([...tasks, response.data]);
    } catch (err) {
      console.error('Failed to add task:', err);
      setError('Failed to add the task.');
    }
  };

  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/tasks/${id}`);
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete the task.');
    }
  };

  const updateTaskStatus = async (id, status) => {
    try {
      const response = await axios.put(`${API_URL}/tasks/${id}`, { status });
      setTasks(
        tasks.map((task) => (task.id === id ? response.data : task))
      );
    } catch (err) {
      console.error('Failed to update task status:', err);
      setError('Failed to update the task status.');
    }
  };

  return (
    <div className="container">
      <h1>Task Manager</h1>
      <AddTaskForm onAddTask={addTask} />
      <Filter currentFilter={filter} onFilterChange={setFilter} />
      {error && <p className="error-message">{error}</p>}
      <TaskList
        tasks={tasks}
        onDeleteTask={deleteTask}
        onUpdateTaskStatus={updateTaskStatus}
      />
    </div>
  );
}

export default App;