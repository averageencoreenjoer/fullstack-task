import TaskItem from '../TaskItem/TaskItem';
import './TaskList.css';

function TaskList({ tasks, onDeleteTask, onUpdateTaskStatus }) {
  if (tasks.length === 0) {
    return <p className="no-tasks">No tasks yet. Add one!</p>;
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onDelete={onDeleteTask}
          onStatusChange={onUpdateTaskStatus}
        />
      ))}
    </div>
  );
}

export default TaskList;